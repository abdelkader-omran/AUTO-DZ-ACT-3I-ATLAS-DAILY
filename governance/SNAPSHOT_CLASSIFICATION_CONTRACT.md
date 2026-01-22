# Snapshot Classification Contract

**Version:** 1.0  
**Effective Date:** 2026-01-22  
**Status:** CANONICAL — DO NOT MODIFY WITHOUT GOVERNANCE APPROVAL

---

## Purpose

This document formalizes the **exact snapshot classification logic** as implemented in `scripts/trizel_monitor.py`. It serves as a permanent, immutable contract preventing future semantic drift, memory loss, or misinterpretation of system behavior.

**Critical Constraint:** This contract describes existing behavior. It does NOT introduce new logic, optimization, or interpretation.

---

## Snapshot State Machine

### State Definitions

The system recognizes the following snapshot states, as evidenced in the code:

#### 1. WRITTEN

**Trigger Condition:**
```
IF snapshot does NOT exist
OR (snapshot exists AND content hash differs AND overwrite policy permits)
THEN create/update snapshot file
```

**Required Inputs:**
- `registry/sources.json` with at least one source entry
- Valid observation date (YYYY-MM-DD format)
- Network connectivity for source fetching

**Side Effects:**
- Snapshot file created at: `data/snapshots/snapshot_YYYY-MM-DD.json`
- Manifest file created at: `data/manifests/manifest_YYYY-MM-DD.json`
- Raw evidence files stored at: `data/raw/YYYY-MM-DD/SOURCE_ID.*`
- Console output: `[OK] YYYY-MM-DD -> <path>`

**What is NOT Done:**
- No scientific interpretation
- No analysis of content
- No validation of astronomical correctness
- No theory testing

#### 2. NOOP_UNCHANGED

**Trigger Condition:**
```
IF snapshot exists
AND SHA-256(new_content) == SHA-256(existing_content)
THEN skip write operation
```

**Required Inputs:**
- Existing snapshot file
- Ability to compute current snapshot (requires source fetching)

**Side Effects:**
- No file writes
- Console output: `[NO-OP] YYYY-MM-DD unchanged (sha256 identical)`

**Interpretation:**
- Raw source material has NOT changed since last collection
- No archive update needed (immutable record preserved)

#### 3. SKIPPED_EXISTS

**Trigger Condition:**
```
IF snapshot exists
AND content hash differs
AND skip_existing policy is TRUE
AND NOT (force_overwrite_all_days is TRUE)
AND NOT (is_today AND allow_overwrite_today is TRUE)
THEN protect existing file from modification
```

**Required Inputs:**
- Existing snapshot file
- Policy flags from CLI or workflow

**Side Effects:**
- No file writes
- Console output: `[SKIP] YYYY-MM-DD exists and is protected by policy`

**Rationale:**
- Historical immutability protection
- Prevents accidental data loss
- Requires explicit override for modification

---

## Source Fetch States

Each source within a snapshot has one of two states:

#### SOURCE_OK

**Trigger Condition:**
```
IF HTTP fetch succeeds (status 2xx)
AND response body received
THEN mark source as successful
```

**Recorded Fields:**
- `"ok": true`
- `"status_code": <int>` (e.g., 200)
- `"content_type": <string>` (MIME type)
- `"bytes_len": <int>` (response size)
- `"sha256": <string>` (64-char hex)
- `"raw_path": <string>` (filesystem path)
- `"error": null`

**Side Effects:**
- Raw content written to: `data/raw/YYYY-MM-DD/SOURCE_ID.<ext>`
- File extension inferred from Content-Type header

#### SOURCE_FAILED

**Trigger Condition:**
```
IF HTTP fetch fails
OR timeout occurs (>25 seconds)
OR network error
OR server error (4xx, 5xx)
THEN mark source as failed
```

**Recorded Fields:**
- `"ok": false`
- `"status_code": <int|null>` (null if network error)
- `"content_type": null`
- `"bytes_len": 0`
- `"sha256": null`
- `"raw_path": null`
- `"error": <string>` (error description)

**Side Effects:**
- No raw file written
- Failure logged in snapshot for auditing

**Interpretation:**
- Source was unreachable or unresponsive
- NOT a statement about astronomical reality
- Temporal network/infrastructure issue

---

## Snapshot Write Policy

### Policy Rules (as implemented)

```pseudocode
FUNCTION safe_write_day(
    day: DATE,
    registry: REGISTRY,
    skip_existing: BOOL,
    allow_overwrite_today: BOOL,
    force_overwrite_all_days: BOOL
) -> (snapshot_path, manifest_path, status_code)

    # Always build fresh snapshot (triggers source fetching + raw evidence storage)
    new_snapshot = build_snapshot(registry, day)
    new_hash = SHA256(new_snapshot)
    
    # Decision tree
    IF snapshot file exists:
        existing_hash = SHA256(existing_snapshot)
        
        IF new_hash == existing_hash:
            RETURN (null, null, "noop_unchanged")
        END
        
        # Content differs
        IF skip_existing AND NOT force_overwrite_all_days:
            IF day == today AND allow_overwrite_today:
                # Permitted: today's snapshot can be refreshed
                PASS
            ELSE:
                # Protected: historical snapshot preserved
                RETURN (null, null, "skipped_exists")
            END
        END
    END
    
    # Write snapshot + manifest
    WRITE snapshot_path <- new_snapshot
    WRITE manifest_path <- build_manifest(new_hash, day)
    
    RETURN (snapshot_path, manifest_path, "written")
END
```

### Policy Invariants

1. **Immutability by Default**
   - Historical snapshots CANNOT be modified without explicit override
   - Protects archival integrity

2. **Content-Addressed**
   - Write decisions based on SHA-256 comparison
   - Identical content = no-op (saves storage/commits)

3. **Today Exception**
   - Today's snapshot MAY be refreshed if content changes
   - Allows correction of in-progress daily collections

4. **Emergency Override**
   - `--overwrite` flag bypasses all protections
   - Use ONLY for registry updates or corruption recovery

---

## Classification Prohibitions

The following are **EXPLICITLY NOT** part of snapshot classification:

### Prohibited Interpretations

❌ **Scientific Analysis**
- Snapshots do NOT interpret astronomical phenomena
- No physics, no trajectory calculations, no predictions

❌ **Eligibility Assessment**
- System does NOT decide if data is "worthy" of analysis
- All official sources treated equally

❌ **Content Validation**
- System does NOT verify astronomical correctness
- Only verifies: fetch success, hash integrity, timestamp

❌ **Filtering by Quality**
- Failed fetches are recorded, not hidden
- Empty responses preserved as evidence

### What Snapshots Are

✅ **Timestamped Archive**
- Immutable record of "what was available at YYYY-MM-DD HH:MM:SS UTC"

✅ **Source Evidence**
- Byte-for-byte preservation of official source responses

✅ **Integrity Proofs**
- SHA-256 checksums for tamper detection

✅ **Audit Trail**
- Success/failure logs for operational transparency

---

## Snapshot Naming and Storage

### File Naming Convention

```
Snapshot: data/snapshots/snapshot_YYYY-MM-DD.json
Manifest: data/manifests/manifest_YYYY-MM-DD.json
Raw Data: data/raw/YYYY-MM-DD/SOURCE_ID.{html|json|txt|bin}
```

**Invariant:** Date is the observation/request date, NOT the processing date.

### Directory Structure (as implemented)

```
data/
├── snapshots/          # Daily snapshot archives
│   └── snapshot_YYYY-MM-DD.json
├── manifests/          # Integrity metadata
│   └── manifest_YYYY-MM-DD.json
├── raw/                # Preserved source responses
│   └── YYYY-MM-DD/
│       ├── IAU_MPC.html
│       ├── NASA_JPL_SBDB.html
│       ├── NASA_JPL_HORIZONS.html
│       ├── ESA_NEOCC.html
│       ├── NASA_CNEOS.html
│       └── NASA_PDS_SMALL_BODIES.html
└── metadata/           # Reserved (future use)
```

---

## Schema Version

Current snapshot schema: **`auto-dz-act.snapshot.v1`**

**Contract:** This identifier MUST remain unchanged unless schema fields are modified. Schema evolution requires:
1. New version identifier (e.g., `v2`)
2. Backward compatibility preservation
3. Governance approval
4. Documentation update to this contract

---

## Integrity Guarantees

### Snapshot-Level Integrity

```
manifest.snapshot_sha256 == SHA256(snapshot_file_bytes)
```

**Enforcement:** Automated verification possible via manifest cross-check

### Source-Level Integrity

```
snapshot.sources[i].sha256 == SHA256(raw_file_bytes)
```

**Enforcement:** Raw files can be re-verified against snapshot records

### Temporal Integrity

```
snapshot.requested_day_utc <= source[i].retrieved_utc <= snapshot.retrieved_utc
```

**Enforcement:** All timestamps in ISO 8601 UTC format with monotonic ordering

---

## Operational Constraints

### Mandatory Fields (Snapshot)

```json
{
  "schema": "string (required)",
  "object": "string (required)",
  "requested_day_utc": "YYYY-MM-DD (required)",
  "retrieved_utc": "ISO8601_UTC (required)",
  "sources": "array (required, may be empty)"
}
```

### Mandatory Fields (Source Entry)

**On Success:**
```json
{
  "id": "string",
  "url": "string",
  "retrieved_utc": "ISO8601_UTC",
  "ok": true,
  "status_code": "int",
  "content_type": "string",
  "bytes_len": "int",
  "sha256": "string (64 hex)",
  "raw_path": "string"
}
```

**On Failure:**
```json
{
  "id": "string",
  "url": "string",
  "retrieved_utc": "ISO8601_UTC",
  "ok": false,
  "status_code": "int|null",
  "content_type": "null",
  "error": "string"
}
```

---

## Enforcement

This contract is enforced by:

1. **Code Behavior** (`scripts/trizel_monitor.py`)
   - Implementation IS the specification
   - Code changes require contract update

2. **Automated Workflow** (`.github/workflows/trizel-monitor.yml`)
   - Daily execution enforces write policy
   - Commits preserve historical snapshots

3. **Git Version Control**
   - Modification history immutable
   - Rollback capability for errors

4. **Governance Review** (Layer-0: `trizel-core`)
   - Changes require explicit approval
   - Prevents unauthorized reinterpretation

---

## Relationship to Other Layers

### Layer-0 (Governance)

Repository: `trizel-core`

**Defines:**
- Authorization for snapshot collection
- Cross-repository governance rules
- Modification approval process

**Does NOT Define:**
- Snapshot content structure (defined here)
- Source selection (defined in registry)

### Layer-1 (This Repository)

Repository: `AUTO-DZ-ACT-3I-ATLAS-DAILY`

**Defines:**
- Snapshot classification (this contract)
- Source registry (`registry/sources.json`)
- Collection automation

**Does NOT Define:**
- Scientific interpretation
- Analysis frameworks
- Publication standards

### Layer-2 (Public Display - hypothetical)

**Uses:**
- Snapshot files as read-only input
- Integrity checksums for validation

**Does NOT:**
- Modify historical snapshots
- Reinterpret classification states
- Generate new raw data

---

## Compliance Statement

This contract ensures:

✅ **Deterministic Behavior**
- Same inputs produce same outputs
- No hidden state or randomness

✅ **Auditability**
- All decisions logged
- State transitions traceable

✅ **Immutability Protection**
- Historical data preserved by default
- Overrides require explicit flags

✅ **Non-Interpretation**
- System observes, does NOT analyze
- Archive function only

---

## Future Modifications

Any modification to snapshot classification logic requires:

1. **Pre-Approval**
   - Governance review and sign-off
   - Impact analysis on historical data

2. **Contract Update**
   - This document updated BEFORE code
   - Version increment

3. **Validation**
   - Prove no unintended behavioral changes
   - Test against historical snapshots

4. **Documentation**
   - Update all cross-references
   - Notify downstream consumers

---

## References

- **Implementation:** `scripts/trizel_monitor.py` (lines 243-300, 306-382)
- **Schema Specification:** `docs/SNAPSHOT_SCHEMA.md`
- **Data Formats:** `docs/DATA_FORMATS.md`
- **Governance Authority:** `trizel-core/docs/governance/CROSS_REPO_GOVERNANCE.md`

---

**Document Maintained By:** TRIZEL Governance Team  
**Last Updated:** 2026-01-22  
**Next Review:** On any code modification to `trizel_monitor.py`
