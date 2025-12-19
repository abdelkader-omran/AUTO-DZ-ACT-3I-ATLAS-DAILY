#!/usr/bin/env python3
import argparse
import json
import hashlib
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, date, timedelta
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "registry" / "sources.json"

DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
MANIFEST_DIR = DATA_DIR / "manifests"
RAW_DIR = DATA_DIR / "raw"


# -------------------------
# Utilities
# -------------------------

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8")


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_day(s: str) -> date:
    return date.fromisoformat(s)


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def today_utc_date() -> date:
    return datetime.now(timezone.utc).date()


def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def is_truthy(s: str) -> bool:
    return str(s).strip().lower() in {"1", "true", "yes", "y", "on"}


# -------------------------
# HTTP fetch (official sources)
# -------------------------

@dataclass
class FetchResult:
    source_id: str
    url: str
    retrieved_utc: str
    ok: bool
    status_code: Optional[int]
    content_type: Optional[str]
    sha256: Optional[str]
    bytes_len: int
    raw_path: Optional[str]
    error: Optional[str]


def fetch_url(url: str, timeout_s: int = 25) -> Tuple[Optional[bytes], Optional[int], Optional[str], Optional[str]]:
    """
    Returns: (content_bytes, http_status, content_type, error_string)
    """
    headers = {
        "User-Agent": "TRIZEL-Monitor/1.0 (+https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY)",
        "Accept": "*/*",
    }
    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=timeout_s) as resp:
            status = getattr(resp, "status", None)
            ctype = resp.headers.get("Content-Type")
            data = resp.read()
            return data, status, ctype, None
    except HTTPError as e:
        try:
            body = e.read()
            _ = body  # not stored here (avoid huge logs)
        except Exception:
            pass
        return None, int(getattr(e, "code", 0) or 0), None, f"HTTPError: {e}"
    except URLError as e:
        return None, None, None, f"URLError: {e}"
    except Exception as e:
        return None, None, None, f"Exception: {e}"


def resolve_url_template(url_tmpl: str, requested_day: date) -> str:
    """
    Supports:
      {YYYY} {MM} {DD} {DATE} (YYYY-MM-DD)
    """
    return (
        url_tmpl
        .replace("{YYYY}", f"{requested_day.year:04d}")
        .replace("{MM}", f"{requested_day.month:02d}")
        .replace("{DD}", f"{requested_day.day:02d}")
        .replace("{DATE}", requested_day.isoformat())
    )


def infer_extension(content_type: Optional[str], fallback: str = "bin") -> str:
    if not content_type:
        return fallback
    ct = content_type.lower()
    if "application/json" in ct or "text/json" in ct:
        return "json"
    if "text/html" in ct:
        return "html"
    if "text/plain" in ct:
        return "txt"
    if "application/pdf" in ct:
        return "pdf"
    return fallback


def collect_sources_for_day(registry: Dict[str, Any], requested_day: date) -> List[Dict[str, Any]]:
    """
    Fetches all sources listed in registry["sources"] (official sources),
    stores raw evidence under data/raw/YYYY-MM-DD/,
    returns a normalized list for snapshot["sources"].
    """
    sources = registry.get("sources", [])
    if not isinstance(sources, list):
        return []

    day_dir = RAW_DIR / requested_day.isoformat()
    safe_mkdir(day_dir)

    out: List[Dict[str, Any]] = []
    for idx, src in enumerate(sources):
        if not isinstance(src, dict):
            continue

        source_id = str(src.get("id") or f"source_{idx+1}").strip()
        url_tmpl = str(src.get("url") or "").strip()
        if not url_tmpl:
            out.append({
                "id": source_id,
                "ok": False,
                "error": "Missing url in registry source entry",
                "retrieved_utc": iso_utc_now(),
            })
            continue

        url = resolve_url_template(url_tmpl, requested_day)
        retrieved = iso_utc_now()

        data, status, ctype, err = fetch_url(url, timeout_s=int(src.get("timeout_s", 25)))

        if data is None:
            out.append({
                "id": source_id,
                "url": url,
                "retrieved_utc": retrieved,
                "ok": False,
                "status_code": status,
                "content_type": ctype,
                "error": err or "Unknown fetch error",
            })
            continue

        h = sha256_bytes(data)
        ext = infer_extension(ctype, fallback=str(src.get("ext") or "bin"))
        raw_filename = f"{source_id}.{ext}"
        raw_path = day_dir / raw_filename
        raw_path.write_bytes(data)

        out.append({
            "id": source_id,
            "url": url,
            "retrieved_utc": retrieved,
            "ok": True,
            "status_code": status,
            "content_type": ctype,
            "bytes_len": len(data),
            "sha256": h,
            "raw_path": str(raw_path.as_posix()),
        })

    return out


# -------------------------
# Snapshot / Manifest builders
# -------------------------

def build_snapshot(registry: Dict[str, Any], requested_day: date) -> Dict[str, Any]:
    # IMPORTANT: sources are fetched per-day (not copied statically)
    sources_evidence = collect_sources_for_day(registry, requested_day)
    return {
        "schema": "auto-dz-act.snapshot.v1",
        "object": registry.get("object", "3I/ATLAS"),
        "requested_day_utc": requested_day.isoformat(),
        "retrieved_utc": iso_utc_now(),
        "sources": sources_evidence,
    }


def build_manifest(snapshot_filename: str, snapshot_sha256: str, requested_day: date) -> Dict[str, Any]:
    return {
        "schema": "auto-dz-act.manifest.v1",
        "requested_day_utc": requested_day.isoformat(),
        "generated_at_utc": iso_utc_now(),
        "snapshot_file": snapshot_filename,
        "snapshot_sha256": snapshot_sha256,
        "integrity": {
            "generated_automatically": True,
            "no_interpretation_applied": True
        }
    }


# -------------------------
# Write policy
# -------------------------

def safe_write_day(
    day: date,
    registry: Dict[str, Any],
    skip_existing: bool,
    allow_overwrite_today: bool,
    force_overwrite_all_days: bool
) -> Tuple[Optional[Path], Optional[Path], str]:
    """
    Status:
      - "written"
      - "skipped_exists"
      - "noop_unchanged"
    Policy:
      - If skip_existing=True and file exists:
          - If force_overwrite_all_days=True => overwrite (any day)
          - Else if day is today and allow_overwrite_today => overwrite if changed
          - Else => skip
      - Always content-hash compare; if unchanged => NO-OP
    """
    safe_mkdir(SNAPSHOT_DIR)
    safe_mkdir(MANIFEST_DIR)
    safe_mkdir(RAW_DIR)

    day_str = day.isoformat()
    snapshot_path = SNAPSHOT_DIR / f"snapshot_{day_str}.json"
    manifest_path = MANIFEST_DIR / f"manifest_{day_str}.json"

    is_today = (day == today_utc_date())

    # Build snapshot bytes and hash (this triggers fetching sources + writing raw evidence)
    snapshot_obj = build_snapshot(registry, day)
    new_snapshot_bytes = dump_json_bytes(snapshot_obj)
    new_hash = sha256_bytes(new_snapshot_bytes)

    if snapshot_path.exists():
        existing_bytes = snapshot_path.read_bytes()
        existing_hash = sha256_bytes(existing_bytes)

        if existing_hash == new_hash:
            return None, None, "noop_unchanged"

        # content differs
        if skip_existing and not force_overwrite_all_days:
            if is_today and allow_overwrite_today:
                pass  # allowed
            else:
                return None, None, "skipped_exists"

    # Write snapshot
    snapshot_path.write_bytes(new_snapshot_bytes)

    # Write manifest
    manifest_obj = build_manifest(snapshot_path.name, new_hash, day)
    manifest_bytes = dump_json_bytes(manifest_obj)
    manifest_path.write_bytes(manifest_bytes)

    return snapshot_path, manifest_path, "written"


# -------------------------
# CLI
# -------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="TRIZEL official daily snapshot + manifest generator (with official source fetching + backfill)"
    )

    # Accept both styles to be compatible with workflows/users
    parser.add_argument("--start", help="Start day (YYYY-MM-DD) for backfill (inclusive)")
    parser.add_argument("--end", help="End day (YYYY-MM-DD) for backfill (inclusive)")
    parser.add_argument("--start-date", dest="start_date", help="Alias for --start (YYYY-MM-DD)")
    parser.add_argument("--end-date", dest="end_date", help="Alias for --end (YYYY-MM-DD)")

    parser.add_argument("--day", help="Single requested day (YYYY-MM-DD). If absent, uses today UTC.")

    parser.add_argument("--overwrite", action="store_true",
                        help="Force overwrite existing snapshot/manifest for ANY day in range (use with care).")
    parser.add_argument("--overwrite-today", action="store_true",
                        help="Allow overwrite only for today UTC if content changed.")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip if snapshot exists (default behavior).")

    args = parser.parse_args()

    if not REGISTRY_FILE.exists():
        print(f"ERROR: Missing registry file: {REGISTRY_FILE}", file=sys.stderr)
        return 2

    registry = load_json(REGISTRY_FILE)

    # Determine mode (normalize start/end aliases)
    start_s = args.start_date or args.start
    end_s = args.end_date or args.end

    if start_s and end_s:
        start = parse_day(start_s)
        end = parse_day(end_s)
        days = list(daterange(start, end))
    elif args.day:
        days = [parse_day(args.day)]
    elif start_s and not end_s:
        # Allow start only => single day backfill
        days = [parse_day(start_s)]
    else:
        days = [today_utc_date()]

    # Default behavior: skip existing ON
    # (GitHub Actions dispatch can still set overwrite true if needed)
    skip_existing = True if args.skip_existing or True else True  # always True by default
    # If user explicitly wants overwrite, they pass --overwrite

    written = 0
    skipped = 0
    noop = 0

    for d in days:
        snapshot_path, manifest_path, status = safe_write_day(
            day=d,
            registry=registry,
            skip_existing=skip_existing,
            allow_overwrite_today=args.overwrite_today,
            force_overwrite_all_days=args.overwrite
        )

        if status == "written":
            written += 1
            print(f"[OK] {d} -> {snapshot_path} ; {manifest_path}")
        elif status == "noop_unchanged":
            noop += 1
            print(f"[NO-OP] {d} unchanged (sha256 identical)")
        elif status == "skipped_exists":
            skipped += 1
            print(f"[SKIP] {d} exists and is protected by policy")
        else:
            raise RuntimeError(f"Unexpected status: {status}")

    print(f"Summary: written={written}, noop_unchanged={noop}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())