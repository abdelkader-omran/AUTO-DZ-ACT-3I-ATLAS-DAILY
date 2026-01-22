# AUTO-DZ-ACT-3I-ATLAS-DAILY

**Layer-1 — Internal Observatory Archive (Data Collection)**

This repository is the **raw data collection and archival layer** for the AUTO-DZ-ACT cosmic observatory system. It produces immutable, timestamped snapshots of official astronomical data sources without interpretation or analysis.

## Current Focus

**Primary Target:** 3I/ATLAS (Interstellar Object)

**Data Sources:** Official observatories only (IAU MPC, NASA JPL, ESA NEOCC, etc.)

**Collection Frequency:** Daily automated snapshots at 03:15 UTC

## What This Repository Does

✅ **Collects** raw data from authoritative astronomical sources  
✅ **Archives** immutable snapshots indexed by observation date  
✅ **Verifies** integrity using SHA-256 cryptographic hashing  
✅ **Timestamps** all operations in ISO 8601 UTC format  
✅ **Preserves** byte-for-byte evidence of source material  

## What This Repository Does NOT Do

❌ **NO Scientific Analysis** — No interpretation of astronomical data  
❌ **NO Publication** — No DOI issuance, no research papers  
❌ **NO Theory Validation** — No physics calculations or predictions  
❌ **NO Public Display** — Raw archive only (Layer-2 function)  
❌ **NO Governance** — Governed BY Layer-0, does not govern others  

## Running the Workflow

Trigger the workflow manually via GitHub Actions:
- Go to Actions → "TRIZEL Monitor – Daily Snapshot" → Run workflow
- For backfill: specify `start_date` and `end_date` parameters (YYYY-MM-DD format)
- Scheduled automatic runs: Daily at 03:15 UTC

## Artifact Storage

Generated artifacts are stored in:
- `data/snapshots/` — Daily snapshot files
- `data/manifests/` — Manifest files with integrity metadata
- `data/raw/` — Raw fetched data by date

## Relationship to TRIZEL Layers

This repository is **Layer-1** in the TRIZEL architecture:

### Layer-0: Governance & Authorization
**Repository:** [trizel-core](https://github.com/abdelkader-omran/trizel-core)  
**Defines:** Cross-repository governance, authorization rules, methodological standards  
**Relationship:** Layer-0 governs this repository; Layer-1 → Layer-0 linkage is established and validated

### Layer-1: Data Collection (THIS REPOSITORY)
**Repository:** AUTO-DZ-ACT-3I-ATLAS-DAILY  
**Defines:** Snapshot classification, source registry, collection automation  
**Function:** Internal observatory archive — raw, immutable, date-indexed snapshots  
**Status:** ✅ Operational — Daily automated collection active

### Layer-2: Public Display (GOI - Graphical Observatory Interface)
**Repository:** Hypothetical/Future  
**Defines:** Visualization, public-facing interfaces, publication standards  
**Relationship:** Layer-2 reads Layer-1 snapshots (read-only access)  
**Status:** Not implemented in this repository

**Tone:** Institutional, scientific, restrained — archive function only.

## Documentation

### Governance Contracts
- [Snapshot Classification Contract](governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md) — Formal state machine for snapshot handling
- [Governance Proof](docs/GOVERNANCE_PROOF_LAYER2_TO_LAYER0.md) — Layer-0 linkage validation
- [Governance Reference](docs/GOVERNANCE_REFERENCE.md) — Canonical source reference

### Data Policies
- [Observatory Scope](docs/OBSERVATORY_SCOPE.md) — Scientific scope and capabilities
- [Data Sources Policy](docs/DATA_SOURCES_POLICY.md) — Source qualification criteria
- [Snapshot Schema](docs/SNAPSHOT_SCHEMA.md) — Complete JSON schema specification
- [Data Formats](docs/DATA_FORMATS.md) — Detailed data structure documentation

### Operational Guides
- [User Guide](docs/USER_GUIDE.md) — How to use the system
- [Script Reference](docs/SCRIPT_REFERENCE.md) — Script documentation and CLI reference
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) — Common issues and solutions
