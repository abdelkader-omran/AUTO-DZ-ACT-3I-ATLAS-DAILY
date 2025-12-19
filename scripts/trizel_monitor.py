#!/usr/bin/env python3
"""
TRIZEL Monitor — Daily Official Data Monitor (AUTO-DZ-ACT)
- Produces daily raw snapshot JSON + manifest JSON (checksums, timestamps)
- Fetches official data where possible (current step: NASA/JPL SBDB API)
- Uses a designation resolver (tries multiple official strings) to reduce query failures
- No interpretation, no post-processing of scientific meaning (raw-only)
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error


# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "registry" / "sources.json"

DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
MANIFEST_DIR = DATA_DIR / "manifests"


# -----------------------------
# Constants
# -----------------------------
PROJECT_NAME = "TRIZEL Monitor"
PIPELINE_NAME = "Daily Official Data Monitor"

# Official API used in this acquisition step:
SBDB_ENDPOINT = "https://ssd-api.jpl.nasa.gov/sbdb.api"

# Some services may not accept "3I/ATLAS" directly, so we try multiple known/expected designations.
DESIGNATION_CANDIDATES = [
    "3I/ATLAS",
    "C/2025 N1",
    "ATLAS",
    "C/2025 N1 (ATLAS)"
]


# -----------------------------
# Utilities
# -----------------------------
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now():
    now = datetime.now(timezone.utc)
    return now, now.isoformat().replace("+00:00", "Z")


def http_get_json(url: str, params: dict, timeout: int = 30):
    """
    Minimal JSON GET using urllib (no extra dependencies).
    Returns: (ok: bool, payload: dict, error: dict|None, full_url: str)
    """
    query = urllib.parse.urlencode(params, doseq=True, safe="/()")
    full_url = f"{url}?{query}"

    req = urllib.request.Request(
        full_url,
        headers={
            "User-Agent": "AUTO-DZ-ACT TRIZEL Monitor/1.0 (GitHub Actions; scientific archiving)",
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read() or b""
            payload = json.loads(raw.decode("utf-8", errors="replace")) if raw else {}
            return True, payload, None, full_url

    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read() or b""
        except Exception:
            body = b""

        err = {
            "type": "http_error",
            "http_status": int(getattr(e, "code", 0) or 0),
            "message": str(e),
            "url": full_url,
            "body_preview": body[:500].decode("utf-8", errors="replace"),
        }
        return False, {}, err, full_url

    except urllib.error.URLError as e:
        err = {
            "type": "network_error",
            "message": str(e),
            "url": full_url,
        }
        return False, {}, err, full_url

    except Exception as e:
        err = {
            "type": "request_error",
            "message": str(e),
            "url": full_url,
        }
        return False, {}, err, full_url


def fetch_sbdb_with_resolver():
    """
    Try multiple designation strings until SBDB returns payload.
    Returns:
      {
        "has_payload": bool,
        "query_used": str|None,
        "payload": dict,
        "error": dict|None,
        "attempts": [ {designation, ok, url, error} ... ]
      }
    """
    attempts = []
    last_error = None

    for designation in DESIGNATION_CANDIDATES:
        ok, payload, err, full_url = http_get_json(
            SBDB_ENDPOINT,
            params={"sstr": designation, "orb": 1, "phys-par": 1},
            timeout=30,
        )

        attempts.append(
            {
                "designation": designation,
                "ok": bool(ok and payload),
                "url": full_url,
                "error": err,
            }
        )

        if ok and payload:
            return {
                "has_payload": True,
                "query_used": designation,
                "payload": payload,
                "error": None,
                "attempts": attempts,
            }

        last_error = err

    return {
        "has_payload": False,
        "query_used": None,
        "payload": {},
        "error": last_error
        or {"type": "unknown_error", "message": "All designation candidates failed"},
        "attempts": attempts,
    }


def build_platforms_registry():
    """
    Registry of official / institutional platforms (evidence targets).
    Not all are machine-fetchable in this monitor step; this is a registry for provenance.
    """
    return {
        "intent": "Evidence & archive targets (official platforms). Not all are machine-fetchable via API.",
        "categories": {
            "authoritative_orbit_and_astrometry": [
                {
                    "name": "Minor Planet Center (MPC)",
                    "role": "IAU clearinghouse for astrometry/orbits",
                    "type": "registry",
                },
                {
                    "name": "NASA/JPL SSD SBDB",
                    "role": "public small-body database API",
                    "type": "api",
                },
                {
                    "name": "NASA/JPL Horizons",
                    "role": "ephemerides / vectors / observer geometry",
                    "type": "service",
                },
            ],
            "major_space_agencies_and_missions": [
                {"name": "ESA", "role": "missions + archives", "type": "agency"},
                {"name": "ESO", "role": "ground-based observatory archives", "type": "observatory"},
                {"name": "JAXA", "role": "missions + archives", "type": "agency"},
                {"name": "CNSA", "role": "missions/announcements; data varies", "type": "agency"},
                {"name": "NASA", "role": "missions + archives", "type": "agency"},
            ],
            "space_and_ground_archives": [
                {"name": "MAST (HST/JWST)", "role": "space telescope archive", "type": "archive"},
                {"name": "ESO Science Archive", "role": "ESO observational archive", "type": "archive"},
                {"name": "HEASARC", "role": "high-energy mission archive gateway", "type": "archive"},
                {"name": "XMM-Newton Science Archive (XSA)", "role": "XMM data archive (ESA)", "type": "archive"},
            ],
        },
        "policy": {
            "verification_first": "Every claim should cite a primary dataset record (ObsID/DOI/solution id).",
            "no_unverifiable_claims": "Platforms without public DOI/ObsID/product are tracked as 'media-only' until operationalized.",
        },
    }


# -----------------------------
# Main
# -----------------------------
def main():
    now, timestamp = utc_now()
    day_compact = now.strftime("%Y%m%d")
    time_compact = now.strftime("%H%M%S")

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    # Load registry (sources list + object label)
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    query_designation = registry.get("object", "3I/ATLAS")

    # Fetch official SBDB snapshot (raw)
    sbdb = fetch_sbdb_with_resolver()

    # Build snapshot (raw-only)
    snapshot = {
        "metadata": {
            "project": PROJECT_NAME,
            "pipeline": PIPELINE_NAME,
            "query_designation": query_designation,
            "resolved_designation": sbdb["query_used"],
            "retrieved_utc": timestamp,
            "sources": {
                "sbdb": SBDB_ENDPOINT,
                "note": "SBDB is used as an official orbit/phys snapshot endpoint in this acquisition step.",
            },
            "integrity": {
                "has_sbdb_payload": bool(sbdb["has_payload"]),
                "has_error": bool(not sbdb["has_payload"]),
            },
        },
        "platforms_registry": build_platforms_registry(),
        "sbdb_data": sbdb["payload"] if sbdb["has_payload"] else {},
        "sbdb_attempts": sbdb["attempts"],
        "sbdb_error": sbdb["error"] if (not sbdb["has_payload"]) else None,
    }

    # Write snapshot file (timestamped)
    snapshot_filename = f"official_snapshot_3I_ATLAS_{day_compact}_{time_compact}.json"
    snapshot_path = SNAPSHOT_DIR / snapshot_filename
    snapshot_bytes = json.dumps(snapshot, indent=2, ensure_ascii=False).encode("utf-8")
    snapshot_path.write_bytes(snapshot_bytes)

    # Manifest (checksums + provenance)
    manifest = {
        "schema": "auto-dz-act.manifest.v1",
        "generated_at_utc": timestamp,
        "files": [
            {
                "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256_file(snapshot_path),
                "bytes": snapshot_path.stat().st_size,
            }
        ],
        "integrity": {
            "generated_automatically": True,
            "no_interpretation_applied": True,
            "raw_only": True,
        },
    }

    manifest_filename = f"manifest_{day_compact}_{time_compact}.json"
    manifest_path = MANIFEST_DIR / manifest_filename
    manifest_bytes = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)

    print(f"Snapshot written: {snapshot_path}")
    print(f"Manifest written: {manifest_path}")


if __name__ == "__main__":
    main()