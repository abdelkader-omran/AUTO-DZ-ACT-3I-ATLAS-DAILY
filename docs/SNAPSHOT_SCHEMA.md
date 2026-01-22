# Snapshot Schema Documentation

**Version:** 1.0  
**Schema Identifier:** `auto-dz-act.snapshot.v1`  
**Effective Date:** 2026-01-22  
**Status:** CANONICAL — REFLECTS ACTUAL IMPLEMENTATION

---

## Purpose

This document describes the **exact JSON schema** for snapshot files as implemented in `scripts/trizel_monitor.py`. It serves as the authoritative reference for snapshot structure, preventing future misinterpretation or schema drift.

**Critical Constraint:** This document describes existing behavior. It does NOT introduce new fields or modify the schema.

---

## Schema Overview

### File Location

```
data/snapshots/snapshot_YYYY-MM-DD.json
```

**Naming Convention:**
- `snapshot_` - Fixed prefix
- `YYYY-MM-DD` - ISO 8601 date (observation date, NOT processing date)
- `.json` - File extension

**Examples:**
- `snapshot_2026-01-21.json`
- `snapshot_2025-12-25.json`

### File Format

- **Encoding:** UTF-8 (no BOM)
- **Line Endings:** LF (Unix-style)
- **Indentation:** 2 spaces
- **Serialization:** Python `json.dumps(obj, indent=2, ensure_ascii=False)`

---

## Root Schema

### Complete Structure

```json
{
  "schema": "auto-dz-act.snapshot.v1",
  "object": "3I/ATLAS",
  "requested_day_utc": "2026-01-21",
  "retrieved_utc": "2026-01-21T04:15:07.502037Z",
  "sources": [
    { /* Source entry 1 */ },
    { /* Source entry 2 */ }
  ]
}
```

### Field Definitions

#### `schema` (string, required)

**Purpose:** Schema version identifier

**Format:** `auto-dz-act.snapshot.v1`

**Source Code:**
```python
# Line 217
"schema": "auto-dz-act.snapshot.v1",
```

**Constraints:**
- Fixed string literal
- MUST NOT change without schema evolution
- Future versions: `v2`, `v3`, etc.

**Usage:**
- Allows parsers to handle multiple schema versions
- Enables backward compatibility detection

---

#### `object` (string, required)

**Purpose:** Astronomical object identifier

**Format:** Free-form string (typically IAU designation)

**Source Code:**
```python
# Line 218
"object": registry.get("object", "3I/ATLAS"),
```

**Examples:**
- `"3I/ATLAS"` (current)
- `"1I/'Oumuamua"` (potential)
- `"C/2020 F3 (NEOWISE)"` (potential)

**Constraints:**
- Read from `registry/sources.json`
- Default fallback: `"3I/ATLAS"`
- String length: Reasonable (< 256 chars recommended)

**Interpretation:**
- Identifier ONLY, not a scientific classification
- Does NOT imply object type, composition, or characteristics

---

#### `requested_day_utc` (string, required)

**Purpose:** Observation date (date being archived)

**Format:** ISO 8601 date (YYYY-MM-DD)

**Source Code:**
```python
# Line 219
"requested_day_utc": requested_day.isoformat(),
```

**Examples:**
- `"2026-01-21"`
- `"2025-12-31"`

**Constraints:**
- MUST be valid ISO 8601 date
- MUST NOT include time component
- Timezone: Implicitly UTC (no offset)

**Relationship:**
- Determines snapshot filename
- Indexes raw data directory
- NOT the date of processing

---

#### `retrieved_utc` (string, required)

**Purpose:** Processing timestamp (when snapshot was generated)

**Format:** ISO 8601 UTC timestamp with milliseconds

**Source Code:**
```python
# Line 220
"retrieved_utc": iso_utc_now(),

# Line 40-41 (utility function)
def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
```

**Examples:**
- `"2026-01-21T04:15:07.502037Z"`
- `"2025-12-31T23:59:59.999999Z"`

**Format Breakdown:**
```
2026-01-21 T 04:15:07.502037 Z
   ↑       ↑      ↑       ↑   ↑
  Date   Sep   Time    Msec UTC
```

**Constraints:**
- MUST end with `Z` (UTC indicator)
- MUST include microsecond precision (6 decimal places)
- MUST be later than or equal to `requested_day_utc 00:00:00Z`

---

#### `sources` (array, required)

**Purpose:** List of source fetch results

**Format:** Array of source entry objects (may be empty)

**Source Code:**
```python
# Line 215
sources_evidence = collect_sources_for_day(registry, requested_day)
# Line 221
"sources": sources_evidence,
```

**Constraints:**
- MUST be an array (even if empty)
- Order: Same as registry order (deterministic)
- Length: Matches `registry.sources[]` length

**Interpretation:**
- Empty array is valid (if registry has no sources)
- Each entry represents ONE source fetch attempt

---

## Source Entry Schema

### Two Variants: Success vs. Failure

#### Successful Fetch

```json
{
  "id": "IAU_MPC",
  "url": "https://www.minorplanetcenter.net/",
  "retrieved_utc": "2026-01-21T04:15:03.928685Z",
  "ok": true,
  "status_code": 200,
  "content_type": "text/html; charset=utf-8",
  "bytes_len": 18240,
  "sha256": "f1ca56b49be4662dd5be8bb032214677aa18e1d39b75199e026a99164153b0f8",
  "raw_path": "/home/runner/work/.../data/raw/2026-01-21/IAU_MPC.html"
}
```

**Source Code:**
```python
# Lines 194-204
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
```

#### Failed Fetch

```json
{
  "id": "SOURCE_ID",
  "url": "https://example.com/",
  "retrieved_utc": "2026-01-21T04:15:05.123456Z",
  "ok": false,
  "status_code": 404,
  "content_type": null,
  "error": "HTTPError: 404 Not Found"
}
```

**Source Code:**
```python
# Lines 177-185
out.append({
    "id": source_id,
    "url": url,
    "retrieved_utc": retrieved,
    "ok": False,
    "status_code": status,
    "content_type": ctype,
    "error": err or "Unknown fetch error",
})
```

### Source Field Definitions

#### `id` (string, required)

**Purpose:** Unique source identifier

**Source Code:**
```python
# Line 160
source_id = str(src.get("id") or f"source_{idx+1}").strip()
```

**Format:**
- Uppercase with underscores (convention)
- Filesystem-safe (no special characters)

**Examples:**
- `"IAU_MPC"`
- `"NASA_JPL_SBDB"`
- `"ESA_NEOCC"`

**Constraints:**
- MUST match registry entry `id`
- Fallback: `source_1`, `source_2`, etc. if registry ID missing

---

#### `url` (string, required)

**Purpose:** Fetched URL (after template resolution)

**Source Code:**
```python
# Line 171
url = resolve_url_template(url_tmpl, requested_day)
```

**Format:**
- Valid HTTP or HTTPS URL
- May include date parameters if templated

**Examples:**
- `"https://www.minorplanetcenter.net/"`
- `"https://ssd.jpl.nasa.gov/sb/"`
- `"https://example.org/data/2026/01/21/summary.json"` (templated)

**Constraints:**
- MUST be publicly accessible
- MUST be the actual fetched URL, not the template

---

#### `retrieved_utc` (string, required)

**Purpose:** Fetch timestamp for THIS source

**Source Code:**
```python
# Line 172
retrieved = iso_utc_now()
```

**Format:** Same as root `retrieved_utc` (ISO 8601 UTC with microseconds)

**Example:**
- `"2026-01-21T04:15:03.928685Z"`

**Constraints:**
- MUST be between snapshot start and end time
- Precision: Microseconds (6 decimal places)

---

#### `ok` (boolean, required)

**Purpose:** Fetch success flag

**Source Code:**
```python
# Line 195 (success)
"ok": True,
# Line 181 (failure)
"ok": False,
```

**Values:**
- `true` - HTTP 2xx response received
- `false` - Any error (network, timeout, HTTP 4xx/5xx)

**Decision Logic:**
```python
# Line 176
if data is None:
    # ok = False
else:
    # ok = True
```

---

#### `status_code` (integer or null, required)

**Purpose:** HTTP response status code

**Source Code:**
```python
# Line 96 (on success)
status = getattr(resp, "status", None)
# Line 106 (on HTTP error)
int(getattr(e, "code", 0) or 0)
# Line 108 (on network error)
None
```

**Values:**
- `200`, `301`, `404`, `500`, etc. (if HTTP response received)
- `null` (if network error, DNS failure, timeout)

**Examples:**
- `200` - Success
- `404` - Not Found
- `null` - Connection timeout

---

#### `content_type` (string or null, required)

**Purpose:** HTTP Content-Type response header

**Source Code:**
```python
# Line 97
ctype = resp.headers.get("Content-Type")
```

**Values:**
- `"text/html"`, `"text/html; charset=utf-8"`, `"application/json"`, etc.
- `null` (if not provided or fetch failed)

**Examples:**
- `"text/html; charset=utf-8"`
- `"application/json"`
- `null`

**Usage:**
- Determines file extension for raw storage (lines 127-139)

---

#### `bytes_len` (integer, required on success)

**Purpose:** Response body length in bytes

**Source Code:**
```python
# Line 199
"bytes_len": len(data),
```

**Values:**
- `0` to `N` (actual byte count)
- NOT present on failure (implicit 0)

**Examples:**
- `18240`
- `176802`

**Constraints:**
- MUST match actual file size if raw_path exists
- Zero is valid (empty response)

---

#### `sha256` (string, required on success)

**Purpose:** SHA-256 checksum of response body

**Source Code:**
```python
# Line 188
h = sha256_bytes(data)
# Line 200
"sha256": h,

# Utility function (line 28-29)
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
```

**Format:**
- 64 hexadecimal characters (lowercase)

**Example:**
- `"f1ca56b49be4662dd5be8bb032214677aa18e1d39b75199e026a99164153b0f8"`

**Constraints:**
- NOT present on failure
- MUST match `SHA256(raw_file_bytes)`

**Verification:**
```bash
sha256sum data/raw/2026-01-21/IAU_MPC.html
# Should match snapshot entry
```

---

#### `raw_path` (string, required on success)

**Purpose:** Absolute filesystem path to saved raw file

**Source Code:**
```python
# Lines 189-192
ext = infer_extension(ctype, fallback=str(src.get("ext") or "bin"))
raw_filename = f"{source_id}.{ext}"
raw_path = day_dir / raw_filename
raw_path.write_bytes(data)
# Line 203
"raw_path": str(raw_path.as_posix()),
```

**Format:**
- Absolute POSIX path
- Includes repository root

**Example:**
- `"/home/runner/work/AUTO-DZ-ACT-3I-ATLAS-DAILY/AUTO-DZ-ACT-3I-ATLAS-DAILY/data/raw/2026-01-21/IAU_MPC.html"`

**Constraints:**
- NOT present on failure
- File MUST exist at this path
- Format: `data/raw/YYYY-MM-DD/SOURCE_ID.{ext}`

**Extension Inference (lines 127-139):**
```python
def infer_extension(content_type: Optional[str], fallback: str = "bin") -> str:
    if "application/json" in ct: return "json"
    if "text/html" in ct: return "html"
    if "text/plain" in ct: return "txt"
    if "application/pdf" in ct: return "pdf"
    return fallback
```

---

#### `error` (string, required on failure)

**Purpose:** Error message describing fetch failure

**Source Code:**
```python
# Line 106 (HTTP error)
f"HTTPError: {e}"
# Line 108 (network error)
f"URLError: {e}"
# Line 110 (general exception)
f"Exception: {e}"
# Line 184 (in snapshot)
"error": err or "Unknown fetch error",
```

**Examples:**
- `"HTTPError: HTTP Error 404: Not Found"`
- `"URLError: <urlopen error timed out>"`
- `"Exception: Connection refused"`
- `"Missing url in registry source entry"`

**Constraints:**
- NOT present on success (or `null` if field included)
- Free-form string (error details from exception)

---

## Schema Invariants

### Mandatory Relationships

1. **If `ok == true`:**
   - `status_code` MUST be integer (typically 200)
   - `bytes_len` MUST be present
   - `sha256` MUST be present (64 hex chars)
   - `raw_path` MUST be present
   - `error` MUST be absent or `null`

2. **If `ok == false`:**
   - `status_code` MAY be integer or `null`
   - `bytes_len` MUST be absent (implicit 0)
   - `sha256` MUST be absent
   - `raw_path` MUST be absent
   - `error` MUST be present (non-empty string)

3. **Timestamp Ordering:**
   ```
   snapshot.requested_day_utc (00:00:00) 
       <= source.retrieved_utc 
       <= snapshot.retrieved_utc
   ```

4. **File Existence:**
   ```
   IF source.raw_path exists THEN file at path must exist
   ```

5. **Hash Integrity:**
   ```
   IF source.sha256 exists THEN SHA256(file at raw_path) == source.sha256
   ```

---

## Schema Evolution

### Schema Version Semantics

Schema version identifiers are declarative and descriptive only.

No runtime rejection, validation failure, or execution branching is performed solely based on schema version.

### Current Version: v1

**Identifier:** `auto-dz-act.snapshot.v1`

**Stability:** STABLE (since inception)

### Future Versioning

If schema must change:

1. **New Version Identifier:**
   - `auto-dz-act.snapshot.v2`
   - Increment version number

2. **Backward Compatibility:**
   - Old snapshots remain valid
   - Parsers must support multiple versions
   - No retroactive modification

3. **Governance Approval:**
   - Layer-0 review required
   - Contract update (this document)
   - Implementation change

4. **Deprecation Policy:**
   - Old versions remain readable
   - New snapshots use new version
   - Cross-version validation tools

---

## Validation

### JSON Schema (JSON Schema Draft 7)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["schema", "object", "requested_day_utc", "retrieved_utc", "sources"],
  "properties": {
    "schema": {
      "type": "string",
      "const": "auto-dz-act.snapshot.v1"
    },
    "object": {
      "type": "string",
      "minLength": 1
    },
    "requested_day_utc": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    },
    "retrieved_utc": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d+Z$"
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "url", "retrieved_utc", "ok"],
        "properties": {
          "id": {"type": "string"},
          "url": {"type": "string"},
          "retrieved_utc": {"type": "string"},
          "ok": {"type": "boolean"},
          "status_code": {"type": ["integer", "null"]},
          "content_type": {"type": ["string", "null"]},
          "bytes_len": {"type": "integer"},
          "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
          "raw_path": {"type": "string"},
          "error": {"type": "string"}
        }
      }
    }
  }
}
```

### Validation Script

```python
import json
from pathlib import Path

def validate_snapshot(snapshot_path: Path) -> bool:
    """Validate snapshot structure against schema."""
    data = json.loads(snapshot_path.read_text())
    
    # Check required root fields
    assert data["schema"] == "auto-dz-act.snapshot.v1"
    assert "object" in data
    assert "requested_day_utc" in data
    assert "retrieved_utc" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    
    # Check each source
    for src in data["sources"]:
        assert "id" in src
        assert "ok" in src
        
        if src["ok"]:
            assert "sha256" in src
            assert "raw_path" in src
            assert len(src["sha256"]) == 64
        else:
            assert "error" in src
    
    return True
```

---

## Related Schemas

### Manifest Schema

**File:** `data/manifests/manifest_YYYY-MM-DD.json`

**Schema:** `auto-dz-act.manifest.v1`

**Relationship:**
- References snapshot file
- Contains snapshot SHA-256
- Cross-validation possible

**See:** Snapshot Classification Contract

### Registry Schema

**File:** `registry/sources.json`

**Schema:** Implicit (no version identifier)

**Relationship:**
- Source of `object` field
- Source of `sources[]` entries
- Template for fetch operations

**See:** Data Sources Policy

---

## References

- **Implementation:** `scripts/trizel_monitor.py` (lines 213-222)
- **Classification Contract:** `governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md`
- **Data Formats:** `docs/DATA_FORMATS.md`
- **Data Sources Policy:** `docs/DATA_SOURCES_POLICY.md`

---

**Document Maintained By:** TRIZEL Schema Working Group  
**Last Updated:** 2026-01-22  
**Next Review:** On schema modification
