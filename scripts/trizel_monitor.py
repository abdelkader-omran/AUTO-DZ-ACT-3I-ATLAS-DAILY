#!/usr/bin/env python3
import argparse
import json
import hashlib
from datetime import datetime, timezone, date, timedelta
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "registry" / "sources.json"

DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
MANIFEST_DIR = DATA_DIR / "manifests"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8")


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_day(s: str) -> date:
    # YYYY-MM-DD
    return date.fromisoformat(s)


def daterange(start: date, end: date):
    # inclusive
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def build_snapshot(registry: Dict[str, Any], requested_day: date) -> Dict[str, Any]:
    return {
        "schema": "auto-dz-act.snapshot.v1",
        "object": registry.get("object", "3I/ATLAS"),
        "requested_day_utc": requested_day.isoformat(),
        "retrieved_utc": iso_utc_now(),
        "sources": registry.get("sources", []),
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


def safe_write_day(
    day: date,
    registry: Dict[str, Any],
    allow_overwrite_today: bool,
    force_overwrite: bool
) -> Tuple[Optional[Path], Optional[Path], str]:
    """
    Policy (2):
      - Past days: SKIP if files exist.
      - Today (UTC): overwrite allowed (if allow_overwrite_today or force_overwrite).
      - Always compute sha256; if unchanged -> NO-OP.
    Returns (snapshot_path, manifest_path, status)
      status in {"written","skipped_exists","noop_unchanged","error"}
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    day_str = day.isoformat()
    snapshot_path = SNAPSHOT_DIR / f"snapshot_{day_str}.json"
    manifest_path = MANIFEST_DIR / f"manifest_{day_str}.json"

    today_utc = datetime.now(timezone.utc).date()
    is_today = (day == today_utc)

    # Build new snapshot bytes and hash
    snapshot_obj = build_snapshot(registry, day)
    new_snapshot_bytes = dump_json_bytes(snapshot_obj)
    new_hash = sha256_bytes(new_snapshot_bytes)

    # If snapshot exists, decide:
    if snapshot_path.exists():
        # Compare existing hash (content-based)
        try:
            existing_bytes = snapshot_path.read_bytes()
            existing_hash = sha256_bytes(existing_bytes)
        except Exception:
            existing_hash = None

        if existing_hash == new_hash:
            # No change → NO-OP (even for today)
            return None, None, "noop_unchanged"

        # Content changed
        if not is_today:
            # Past day: never overwrite automatically
            return None, None, "skipped_exists"

        # Today: overwrite allowed only if policy allows or forced
        if not (allow_overwrite_today or force_overwrite):
            return None, None, "skipped_exists"

    # If manifest exists but snapshot not exists, we still write both (consistent state)
    # Write snapshot
    snapshot_path.write_bytes(new_snapshot_bytes)

    # Write manifest
    manifest_obj = build_manifest(snapshot_path.name, new_hash, day)
    manifest_bytes = dump_json_bytes(manifest_obj)
    manifest_path.write_bytes(manifest_bytes)

    return snapshot_path, manifest_path, "written"


def main():
    parser = argparse.ArgumentParser(description="TRIZEL official daily snapshot + manifest generator")
    parser.add_argument("--start", help="Start day (YYYY-MM-DD) for backfill (inclusive)")
    parser.add_argument("--end", help="End day (YYYY-MM-DD) for backfill (inclusive)")
    parser.add_argument("--day", help="Single requested day (YYYY-MM-DD). If absent, uses today UTC.")
    parser.add_argument("--overwrite", action="store_true", help="Force overwrite (today only recommended)")
    parser.add_argument("--overwrite-today", action="store_true", help="Allow overwrite for today UTC when content changed")
    args = parser.parse_args()

    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Missing registry file: {REGISTRY_FILE}")

    registry = load_json(REGISTRY_FILE)

    # Determine mode
    if args.start and args.end:
        start = parse_day(args.start)
        end = parse_day(args.end)
        days = list(daterange(start, end))
    elif args.day:
        days = [parse_day(args.day)]
    else:
        days = [datetime.now(timezone.utc).date()]

    # Execute
    written = 0
    skipped = 0
    noop = 0

    for d in days:
        snapshot_path, manifest_path, status = safe_write_day(
            day=d,
            registry=registry,
            allow_overwrite_today=args.overwrite_today,
            force_overwrite=args.overwrite
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
            print(f"[ERR] {d} unexpected status: {status}")
            raise RuntimeError(f"Unexpected status {status}")

    print(f"Summary: written={written}, noop_unchanged={noop}, skipped={skipped}")

    # Exit code behavior:
    # - Always 0: because skip/no-op are not errors (important for scheduled runs).
    # Any unexpected condition already raises exception.


if __name__ == "__main__":
    main()