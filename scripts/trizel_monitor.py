#!/usr/bin/env python3
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "registry" / "sources.json"
DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
MANIFEST_DIR = DATA_DIR / "manifests"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat().replace("+00:00", "Z")

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    snapshot = {
        "schema": "auto-dz-act.snapshot.v1",
        "object": registry.get("object", "3I/ATLAS"),
        "generated_at_utc": timestamp,
        "sources": registry.get("sources", [])
    }

    snapshot_bytes = json.dumps(snapshot, indent=2).encode("utf-8")
    snapshot_hash = sha256_bytes(snapshot_bytes)

    snapshot_path = SNAPSHOT_DIR / f"snapshot_{day}.json"
    snapshot_path.write_bytes(snapshot_bytes)

    manifest = {
        "schema": "auto-dz-act.manifest.v1",
        "generated_at_utc": timestamp,
        "snapshot_file": snapshot_path.name,
        "snapshot_sha256": snapshot_hash,
        "integrity": {
            "generated_automatically": True,
            "no_interpretation_applied": True
        }
    }

    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    manifest_path = MANIFEST_DIR / f"manifest_{day}.json"
    manifest_path.write_bytes(manifest_bytes)

    print(f"Snapshot written: {snapshot_path}")
    print(f"Manifest written: {manifest_path}")


if __name__ == "__main__":
    main()
