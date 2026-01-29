# Zenodo Archival Policy

**Version:** 1.0  
**Effective Date:** 2026-01-29  
**Status:** IMMUTABLE POLICY — MANDATORY COMPLIANCE

---

## Policy Statement

This document establishes the **mandatory archival policy** for Zenodo dataset publishing from the AUTO-DZ-ACT-3I-ATLAS-DAILY repository. All personnel, automated systems, and future maintainers MUST comply with these requirements.

---

## Core Principle: APPEND-ONLY ARCHIVE

### Fundamental Constraint

**ALL Zenodo datasets from this repository are APPEND-ONLY.**

Once a snapshot, manifest, or archive version is published to Zenodo:
- ❌ **MUST NOT** be modified
- ❌ **MUST NOT** be replaced
- ❌ **MUST NOT** be deleted
- ❌ **MUST NOT** be updated in-place
- ✅ **MAY** be supplemented with new data in a new version

### Rationale

1. **Scientific Integrity:** Raw observational records must remain immutable for reproducibility
2. **Provenance Preservation:** Historical data provides evidence of temporal evolution
3. **Trust:** Once cited, archived data must remain permanently accessible in original form
4. **Legal Compliance:** CC-BY-4.0 license requires attribution to specific versions

---

## Raw Data Definition

### Classification: RAW OBSERVATIONAL DATA

Snapshot JSON files (`snapshot_YYYY-MM-DD.json`) and integrity manifests (`manifest_YYYY-MM-DD.json`) are classified as:

✅ **RAW OBSERVATIONAL DATA** under provenance-based, non-instrumental scientific archiving standards

### What This Means

**These files ARE:**
- Raw observational records from official astronomical institutions
- Timestamped snapshots of institutional database states
- Provenance-documented aggregations with complete source attribution
- Cryptographically-verified immutable records
- Primary evidence for temporal analysis
- Non-instrumental observational data (no direct telescope operation)

**These files are NOT:**
- ❌ Analysis or interpretation
- ❌ Summaries or derived products
- ❌ Processed or filtered data
- ❌ Scientific conclusions
- ❌ Curated selections
- ❌ Predictions or models
- ❌ Commentary or annotation

### Institutional Basis

This classification is supported by:
1. **Complete provenance chain:** Every data point traceable to authoritative source
2. **Timestamped acquisition:** ISO 8601 UTC timestamps document temporal provenance
3. **Cryptographic verification:** SHA-256 hashes ensure byte-for-byte preservation
4. **Institutional sources:** All data from official observatories (IAU MPC, NASA JPL, ESA)
5. **Immutability protection:** State machine prevents historical modification
6. **No interpretation:** Explicit flags confirm automated generation only

---

## Versioning Policy

### Version Numbering

Zenodo dataset versions MUST follow this scheme:

```
v1 (initial): 2025-07-01 to 2026-01-29 (214 snapshots)
v2 (next):    2025-07-01 to 2026-04-30 (append 90 days)
v3 (future):  2025-07-01 to 2026-07-31 (append 92 days)
...
```

**Rules:**
- Version number increments: `v1`, `v2`, `v3`, etc.
- Temporal coverage ALWAYS starts from earliest snapshot (2025-07-01)
- Temporal coverage end date extends to latest snapshot at publication time
- Historical data (v1) MUST be completely contained in v2, v3, etc.

### Archive Naming

Archive filenames MUST encode temporal range:

```
AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-{START}_to_{END}.tar.gz
```

**Examples:**
- `AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz` (v1)
- `AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-04-30.tar.gz` (v2)

**Prohibition:** NEVER reuse a filename with different content.

---

## Publication Workflow

### Permitted: New Version Publication

**Scenario:** Quarterly dataset update with new snapshots

**Process:**
1. ✅ Collect new daily snapshots (append-only in repository)
2. ✅ Generate NEW archive with extended date range
3. ✅ Create NEW GitHub release with incremented version tag
4. ✅ Upload NEW archive to Zenodo as NEW version
5. ✅ Link to previous version using Zenodo's versioning

**Result:** Both v1 and v2 remain accessible; v2 contains all of v1 plus new data

### PROHIBITED: Modification of Published Version

**Scenario:** Error discovered in snapshot from 2025-07-15

**FORBIDDEN Actions:**
- ❌ Fix the snapshot and republish v1
- ❌ Delete v1 and upload corrected version
- ❌ Edit v1 on Zenodo
- ❌ Replace archive file in GitHub release

**PERMITTED Actions:**
- ✅ Document the error in a separate erratum (if significant)
- ✅ Include corrected data in future versions (v2+) if source updates
- ✅ Note in v2 description that v1 had known limitation
- ✅ Leave v1 as-is for historical integrity

### PROHIBITED: Deletion or Replacement

**Never permitted:**
- ❌ Delete a Zenodo version after publication
- ❌ Mark a version as "deprecated" or "superseded"
- ❌ Hide or unlist a published version
- ❌ Replace archive file after GitHub release

**Rationale:** Citations may exist; data must remain accessible

---

## Technical Safeguards

### GitHub Workflow Protection

The automated workflow (`.github/workflows/zenodo-dataset-preparation.yml`) includes:

```yaml
- name: Check if dataset already exists
  run: |
    if [ -f "$ARCHIVE_NAME" ]; then
      echo "Archive already exists - SKIP"
      exit 0
    fi
```

This prevents accidental re-creation of existing archives.

### Git Tag Protection

GitHub release tags MUST be protected:
- Tag format: `zenodo-raw-v{VERSION}`
- Once created, tags MUST NOT be deleted or moved
- Releases MUST NOT be deleted

### Manual Review Required

Before Zenodo publication:
1. ✅ Verify archive does not replace existing version
2. ✅ Confirm temporal range is strictly append-only
3. ✅ Check .zenodo.json version number is incremented
4. ✅ Review that no historical snapshots were modified

---

## Compliance Verification

### Pre-Publication Checklist

Before uploading to Zenodo, verify:

- [ ] Archive filename includes correct date range
- [ ] Date range starts from original earliest snapshot (2025-07-01)
- [ ] No historical snapshots (before last publication) were modified
- [ ] Version number is incremented from previous publication
- [ ] GitHub release tag is new (not reusing old tag)
- [ ] .zenodo.json metadata is updated for new version
- [ ] Archive contains all previous data plus new data only

### Post-Publication Verification

After Zenodo publication:

- [ ] Verify previous version(s) still accessible on Zenodo
- [ ] Confirm new version DOI is distinct from previous
- [ ] Check that both versions are linked via Zenodo versioning
- [ ] Update repository README with new DOI
- [ ] Do NOT modify or delete previous GitHub releases

---

## Violation Response

### If Published Version Contains Error

1. **Document publicly:** Create GitHub issue describing error
2. **Do NOT modify:** Leave published version as-is
3. **Plan correction:** Include fix in next quarterly version (if applicable)
4. **Notify users:** If error is significant, announce via repository channels
5. **Cite original:** All corrections must cite the original flawed version

### If Accidental Modification Detected

1. **STOP immediately:** Halt any upload or publication
2. **Investigate:** Determine what was modified and why
3. **Restore original:** Use Git history to restore original state
4. **Document incident:** Create incident report in governance/
5. **Prevent recurrence:** Update safeguards and policies

---

## Authority and Enforcement

### Governing Documents

This policy operates under:
- **Layer-0:** TRIZEL-BASELINE-v1.0.0 (https://github.com/abdelkader-omran/trizel-core)
- **Layer-1:** Snapshot Classification Contract (governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md)
- **License:** CC-BY-4.0 (immutable license requirements)

### Policy Hierarchy

1. **IMMUTABLE:** Raw data never modified once published
2. **APPEND-ONLY:** New data extends archive; historical unchanged
3. **PROVENANCE:** Complete documentation required
4. **TRANSPARENCY:** All changes logged and publicly visible

### Modification of This Policy

This policy itself is **append-only**:
- Clarifications MAY be added
- New sections MAY be appended
- Existing constraints MUST NOT be relaxed
- Version history MUST be maintained in Git

---

## Summary

**Three Immutable Rules:**

1. **RAW DATA:** Snapshots and manifests are raw observational data, not analysis
2. **APPEND-ONLY:** Once published, never modify, replace, or delete
3. **PROVENANCE:** Complete documentation chain required for all data

**Violation = Policy Breach**

Any modification, deletion, or replacement of published data is a governance violation requiring formal incident response.

---

**Policy End**

**Effective:** 2026-01-29  
**Authority:** AUTO-DZ-ACT Layer-1 Observatory System  
**Status:** MANDATORY — NO EXCEPTIONS
