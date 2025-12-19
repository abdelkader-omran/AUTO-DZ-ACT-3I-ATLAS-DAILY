#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "registry" / "sources.json"
DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
MANIFEST_DIR = DATA_DIR / "manifests"


# Safety limits (to avoid huge downloads in Actions)
DEFAULT_TIMEOUT_SEC = 25
MAX_BYTES = 5 * 1024 * 1024         # 5 MB hard cap per source
MAX_TEXT_CHARS = 20000             # store at most 20k chars of non-JSON text
USER_AGENT = "AUTO-DZ-ACT-TRIZEL-Monitor/1.0 (+https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY)"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_yyyy_mm_dd(s: str) -> date:
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        raise ValueError(f"Invalid date '{s}'. Expected YYYY-MM-DD.")


def iter_days(start: date, end: date) -> List[date]:
    if end < start:
        raise ValueError("end_date must be >= start_date")
    days = []
    cur = start
    while cur <= end:
        days.append(cur)
        cur += timedelta(days=1)
    return days


@dataclass
class FetchResult:
    ok: bool
    url: str
    status: Optional[int]
    content_type: Optional[str]
    retrieved_utc: str
    sha256: Optional[str]
    bytes_len: int
    parsed_json: Optional[Any]
    text_preview: Optional[str]
    truncated: bool
    error: Optional[str]


def fetch_url(url: str, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> FetchResult:
    retrieved = iso_utc_now()
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    raw = b""
    status = None
    ctype = None

    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            status = getattr(resp, "status", None)
            ctype = resp.headers.get("Content-Type")
            # Read at most MAX_BYTES + 1 to detect overflow
            chunk = resp.read(MAX_BYTES + 1)
            if len(chunk) > MAX_BYTES:
                raw = chunk[:MAX_BYTES]
                h = sha256_bytes(raw)
                return FetchResult(
                    ok=False,
                    url=url,
                    status=status,
                    content_type=ctype,
                    retrieved_utc=retrieved,
                    sha256=h,
                    bytes_len=len(raw),
                    parsed_json=None,
                    text_preview=None,
                    truncated=True,
                    error=f"Response exceeded MAX_BYTES={MAX_BYTES} (stored first {MAX_BYTES} bytes).",
                )
            raw = chunk

        h = sha256_bytes(raw)

        # Try JSON parse if content-type suggests JSON OR looks like JSON
        parsed_json = None
        text_preview = None
        truncated = False

        looks_json = False
        if ctype and ("application/json" in ctype.lower() or "text/json" in ctype.lower()):
            looks_json = True
        else:
            # heuristic: starts with { or [
            s = raw.lstrip()[:1]
            looks_json = (s == b"{" or s == b"[")

        if looks_json:
            try:
                parsed_json = json.loads(raw.decode("utf-8"))
            except Exception:
                # fallback to text preview
                txt = raw.decode("utf-8", errors="replace")
                if len(txt) > MAX_TEXT_CHARS:
                    text_preview = txt[:MAX_TEXT_CHARS]
                    truncated = True
                else:
                    text_preview = txt
        else:
            txt = raw.decode("utf-8", errors="replace")
            if len(txt) > MAX_TEXT_CHARS:
                text_preview = txt[:MAX_TEXT_CHARS]
                truncated = True
            else:
                text_preview = txt

        return FetchResult(
            ok=True,
            url=url,
            status=status,
            content_type=ctype,
            retrieved_utc=retrieved,
            sha256=h,
            bytes_len=len(raw),
            parsed_json=parsed_json,
            text_preview=text_preview,
            truncated=truncated,
            error=None,
        )

    except HTTPError as e:
        # HTTPError is also a file-like response; still try to read body safely
        try:
            ctype = e.headers.get("Content-Type")
            body = e.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                body = body[:MAX_BYTES]
            raw = body
            h = sha256_bytes(raw)
        except Exception:
            h = None
            raw = b""
        return FetchResult(
            ok=False,
            url=url,
            status=getattr(e, "code", None),
            content_type=ctype,
            retrieved_utc=retrieved,
            sha256=h,
            bytes_len=len(raw),
            parsed_json=None,
            text_preview=None,
            truncated=False,
            error=f"HTTPError: {e}",
        )
    except URLError as e:
        return FetchResult(
            ok=False,
            url=url,
            status=None,
            content_type=None,
            retrieved_utc=retrieved,
            sha256=None,
            bytes_len=0,
            parsed_json=None,
            text_preview=None,
            truncated=False,
            error=f"URLError: {e}",
        )
    except Exception as e:
        return FetchResult(
            ok=False,
            url=url,
            status=None,
            content_type=None,
            retrieved_utc=retrieved,
            sha256=None,
            bytes_len=0,
            parsed_json=None,
            text_preview=None,
            truncated=False,
            error=f"Exception: {e}",
        )


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry file not found: {REGISTRY_FILE}")
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)


def build_snapshot_for_day(registry: Dict[str, Any], requested_day: date) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Returns:
      snapshot_dict, sources_records
    """
    retrieved_utc = iso_utc_now()
    day_str = requested_day.strftime("%Y-%m-%d")

    sources = registry.get("sources", [])
    source_records: List[Dict[str, Any]] = []

    # Fetch each source as of *now*; requested_day is a labeling key for backfill.
    # This preserves reproducibility of what was retrieved, and records a clear distinction.
    for src in sources:
        name = src.get("name") or src.get("id") or "unnamed-source"
        url = src.get("url")
        kind = src.get("kind") or src.get("type") or None

        if not url:
            source_records.append({
                "name": name,
                "kind": kind,
                "url": None,
                "ok": False,
                "error": "Missing 'url' in registry entry.",
            })
            continue

        r = fetch_url(url)

        rec: Dict[str, Any] = {
            "name": name,
            "kind": kind,
            "url": r.url,
            "ok": r.ok,
            "status": r.status,
            "content_type": r.content_type,
            "retrieved_utc": r.retrieved_utc,
            "sha256": r.sha256,
            "bytes_len": r.bytes_len,
            "truncated": r.truncated,
        }

        # Store JSON payload if parsed, otherwise store text preview.
        # (We keep it "raw-friendly" while avoiding binary blobs in JSON.)
        if r.parsed_json is not None:
            rec["payload_json"] = r.parsed_json
        elif r.text_preview is not None:
            rec["payload_text_preview"] = r.text_preview

        if r.error:
            rec["error"] = r.error

        source_records.append(rec)

    snapshot: Dict[str, Any] = {
        "schema": "auto-dz-act.snapshot.v1",
        "object": registry.get("object", "3I/ATLAS"),
        "requested_day_utc": day_str,
        "retrieved_utc": retrieved_utc,
        "generated_at_utc": retrieved_utc,
        "run_context": {
            "github_repository": os.environ.get("GITHUB_REPOSITORY"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_number": os.environ.get("GITHUB_RUN_NUMBER"),
            "github_workflow": os.environ.get("GITHUB_WORKFLOW"),
            "github_sha": os.environ.get("GITHUB_SHA"),
        },
        "sources": source_records,
    }

    return snapshot, source_records


def write_snapshot_and_manifest(
    snapshot: Dict[str, Any],
    source_records: List[Dict[str, Any]],
    day_str: str,
    overwrite: bool = False
) -> Tuple[Path, Path]:
    snapshot_path = SNAPSHOT_DIR / f"snapshot_{day_str}.json"
    manifest_path = MANIFEST_DIR / f"manifest_{day_str}.json"

    if (not overwrite) and (snapshot_path.exists() or manifest_path.exists()):
        raise FileExistsError(f"Files already exist for {day_str}. Use --overwrite to replace.")

    snapshot_bytes = json.dumps(snapshot, ensure_ascii=False, indent=2).encode("utf-8")
    snapshot_sha = sha256_bytes(snapshot_bytes)
    snapshot_path.write_bytes(snapshot_bytes)

    # Build manifest with per-source hashes already included in snapshot
    retrieved_utc = snapshot.get("retrieved_utc") or iso_utc_now()
    manifest: Dict[str, Any] = {
        "schema": "auto-dz-act.manifest.v1",
        "generated_at_utc": retrieved_utc,
        "requested_day_utc": day_str,
        "snapshot_file": snapshot_path.name,
        "snapshot_sha256": snapshot_sha,
        "sources_index": [
            {
                "name": r.get("name"),
                "url": r.get("url"),
                "ok": r.get("ok"),
                "status": r.get("status"),
                "sha256": r.get("sha256"),
                "bytes_len": r.get("bytes_len"),
                "retrieved_utc": r.get("retrieved_utc"),
            }
            for r in source_records
        ],
        "integrity": {
            "generated_automatically": True,
            "no_interpretation_applied": True,
            "raw_payloads_may_be_truncated": True,
        },
    }

    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)

    return snapshot_path, manifest_path


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="trizel_monitor.py",
        description="AUTO-DZ-ACT TRIZEL Monitor: daily snapshot + backfill mode."
    )
    parser.add_argument(
        "--mode",
        choices=["daily", "backfill"],
        default="daily",
        help="Run mode: daily (default) or backfill."
    )
    parser.add_argument("--start", dest="start_date", help="Backfill start date YYYY-MM-DD (required for backfill).")
    parser.add_argument("--end", dest="end_date", help="Backfill end date YYYY-MM-DD (required for backfill).")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing snapshot/manifest files.")
    parser.add_argument(
        "--limit-per-run",
        type=int,
        default=0,
        help="Optional cap on number of days processed in backfill (0 = no limit)."
    )
    args = parser.parse_args(argv)

    ensure_dirs()
    registry = load_registry()

    if args.mode == "daily":
        today = datetime.now(timezone.utc).date()
        day_str = today.strftime("%Y-%m-%d")

        snapshot, source_records = build_snapshot_for_day(registry, today)
        snapshot_path, manifest_path = write_snapshot_and_manifest(
            snapshot, source_records, day_str, overwrite=args.overwrite
        )

        print(f"OK daily: {day_str}")
        print(f"Snapshot written: {snapshot_path}")
        print(f"Manifest written: {manifest_path}")
        return 0

    # backfill
    if not args.start_date or not args.end_date:
        print("ERROR: backfill requires --start YYYY-MM-DD and --end YYYY-MM-DD", file=sys.stderr)
        return 2

    start = parse_yyyy_mm_dd(args.start_date)
    end = parse_yyyy_mm_dd(args.end_date)
    days = iter_days(start, end)

    if args.limit_per_run and args.limit_per_run > 0:
        days = days[:args.limit_per_run]

    ok_days = 0
    skipped_days = 0
    failed_days: List[str] = []

    for d in days:
        day_str = d.strftime("%Y-%m-%d")
        try:
            snapshot, source_records = build_snapshot_for_day(registry, d)
            write_snapshot_and_manifest(snapshot, source_records, day_str, overwrite=args.overwrite)
            ok_days += 1
            print(f"OK backfill: {day_str}")
        except FileExistsError as e:
            skipped_days += 1
            print(f"SKIP backfill: {day_str} ({e})")
        except Exception as e:
            failed_days.append(day_str)
            print(f"FAIL backfill: {day_str} ({e})", file=sys.stderr)

    print("----- Backfill summary -----")
    print(f"Processed days: {len(days)}")
    print(f"OK: {ok_days}")
    print(f"Skipped(existing): {skipped_days}")
    print(f"Failed: {len(failed_days)}")
    if failed_days:
        print("Failed days:", ", ".join(failed_days))

    # Exit non-zero if any failures occurred
    return 1 if failed_days else 0


if __name__ == "__main__":
    raise SystemExit(main())