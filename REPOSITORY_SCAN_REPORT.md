# AUTO-DZ-ACT-3I-ATLAS Repository Scan Report

**Repository:** AUTO-DZ-ACT-3I-ATLAS-DAILY  
**Branch:** main  
**Report Generated:** 2026-01-29  
**Purpose:** Zenodo archival classification and data inventory

---

## Executive Summary

This repository contains **NO FILES LARGER THAN 5 MB**. The entire repository (excluding .git) is approximately **0.84 MB** with the largest individual file being only **15.68 KB**. All content consists of:
- Daily observational snapshots (JSON, avg 2.93 KB each)
- Integrity manifests (JSON)
- Documentation (Markdown)
- Scripts (Python)
- Configuration files (YAML, JSON)

---

## 1. Files Larger Than 5 MB

**Result: NONE**

All files in the repository are significantly smaller than 5 MB. The 20 largest files are:

| File Path | Size (bytes) | Size (KB) | Type |
|-----------|--------------|-----------|------|
| ./docs/SNAPSHOT_SCHEMA.md | 15,681 | 15.31 | Documentation |
| ./docs/DATA_FORMATS.md | 14,120 | 13.79 | Documentation |
| ./docs/DATA_SOURCES_POLICY.md | 13,785 | 13.46 | Documentation |
| ./VALIDATION_REPORT.md | 13,667 | 13.35 | Documentation |
| ./docs/TROUBLESHOOTING.md | 13,650 | 13.33 | Documentation |
| ./scripts/trizel_monitor.py | 11,978 | 11.70 | Python Script |
| ./governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md | 11,957 | 11.68 | Documentation |
| ./docs/OBSERVATORY_SCOPE.md | 11,521 | 11.25 | Documentation |
| ./docs/SCRIPT_REFERENCE.md | 8,986 | 8.78 | Documentation |
| ./analysis/3I-ATLAS-0001/reports/ARCHIVAL_SYNTHESIS.md | 8,072 | 7.88 | Analysis Report |
| ./docs/USER_GUIDE.md | 5,857 | 5.72 | Documentation |
| ./data/snapshots/official_snapshot_3I_ATLAS_20251219_123807.json | 5,256 | 5.13 | JSON Data |
| ./.gitignore | 4,688 | 4.58 | Configuration |
| ./README.md | 4,007 | 3.91 | Documentation |
| ./.github/workflows/trizel-monitor.yml | 3,680 | 3.59 | Workflow Config |
| ./docs/GOVERNANCE_PROOF_LAYER2_TO_LAYER0.md | 3,460 | 3.38 | Documentation |
| ./analysis/3I-ATLAS-0001/README.md | 3,114 | 3.04 | Documentation |
| ./data/snapshots/snapshot_2026-01-29.json | 2,997 | 2.93 | JSON Data |
| ./data/snapshots/snapshot_2026-01-28.json | 2,997 | 2.93 | JSON Data |
| ./data/snapshots/snapshot_2026-01-27.json | 2,997 | 2.93 | JSON Data |

**Repository Statistics:**
- Total size (excluding .git): 0.84 MB
- Total files: ~450+ files
- Largest file: 15.68 KB

---

## 2. Directories Containing Raw, Observational, or External Research Materials

### 2.1 Primary Data Directories

#### **`/data/snapshots/`** (RAW OBSERVATIONAL DATA)
- **Classification:** RAW DATA - External Observatory Snapshots
- **Content:** 214 daily observational snapshot files in JSON format
- **Time Coverage:** July 1, 2025 to January 29, 2026 (~7 months)
- **Size:** ~627.93 KB total (avg 2.93 KB per file)
- **Source Type:** External official astronomical data sources
- **Data Origin:**
  - IAU Minor Planet Center (https://www.minorplanetcenter.net/)
  - NASA/JPL Small-Body Database (https://ssd.jpl.nasa.gov/sb/)
  - NASA/JPL Horizons (https://ssd.jpl.nasa.gov/horizons/)
  - ESA NEO Coordination Centre (https://neo.ssa.esa.int/)
- **Format:** Immutable, timestamped JSON snapshots
- **Schema:** `auto-dz-act.snapshot.v1`
- **Integrity:** Each snapshot includes SHA-256 hash verification

**Example snapshot structure:**
```json
{
  "schema": "auto-dz-act.snapshot.v1",
  "object": "3I/ATLAS",
  "requested_day_utc": "2026-01-29",
  "retrieved_utc": "2026-01-29T04:49:21.764919Z",
  "sources": [
    {
      "id": "IAU_MPC",
      "url": "https://www.minorplanetcenter.net/",
      "retrieved_utc": "2026-01-29T04:49:18.501175Z",
      "ok": true,
      "status_code": 200,
      "sha256": "d51e9c92a0070bafe7bb2dbcd09de5a7ba42ee2d77fe02a297045eda5d3d20f1",
      "raw_path": "/data/raw/2026-01-29/IAU_MPC.html"
    }
  ]
}
```

**Key Files:**
- Standard daily snapshots: `snapshot_YYYY-MM-DD.json` (213 files)
- Official reference snapshot: `official_snapshot_3I_ATLAS_20251219_123807.json`

#### **`/data/manifests/`** (RAW DATA INTEGRITY RECORDS)
- **Classification:** RAW DATA - Integrity Verification Manifests
- **Content:** 214 manifest files (one per snapshot)
- **Purpose:** Cryptographic verification of snapshot integrity
- **Format:** JSON
- **Schema:** `auto-dz-act.manifest.v1`
- **Key Fields:**
  - `snapshot_sha256`: SHA-256 hash of corresponding snapshot
  - `generated_at_utc`: Timestamp of manifest generation
  - `integrity.generated_automatically`: Boolean flag confirming automation
  - `integrity.no_interpretation_applied`: Boolean flag confirming no analysis

**Example manifest:**
```json
{
  "schema": "auto-dz-act.manifest.v1",
  "requested_day_utc": "2026-01-29",
  "generated_at_utc": "2026-01-29T04:49:21.765140Z",
  "snapshot_file": "snapshot_2026-01-29.json",
  "snapshot_sha256": "7d2323ec6a1e5c9e98c63650e9acb033ea1ae29884ec53b8c0f28a842c3acb0e",
  "integrity": {
    "generated_automatically": true,
    "no_interpretation_applied": true
  }
}
```

#### **`/data/raw/`** (RAW HTML FETCH DATA)
- **Classification:** RAW DATA - Unprocessed External Downloads
- **Content:** Currently empty (contains only `.keep` file)
- **Purpose:** Storage location for raw HTML/data fetched from external sources
- **Status:** Data not committed to repository (transient storage)
- **Note:** Paths referenced in snapshots (e.g., `/data/raw/2026-01-29/IAU_MPC.html`)

#### **`/data/metadata/`** (METADATA STORAGE)
- **Classification:** METADATA
- **Content:** Empty (contains only `.keep` file)
- **Purpose:** Reserved for future metadata storage

### 2.2 External Source Registry

#### **`/registry/sources.json`**
- **Classification:** RAW DATA - Source Registry
- **Content:** Registry of official astronomical data sources
- **Purpose:** Enumeration of authoritative platforms for data collection

---

## 3. Analysis Artifacts Derived from External Datasets

### 3.1 Analysis Directory Structure

#### **`/analysis/3I-ATLAS-0001/`** (DERIVED ANALYSIS)
- **Classification:** DERIVED ANALYSIS - Descriptive Synthesis
- **Purpose:** Gate 4B analysis artifact for 3I/ATLAS data collection
- **Status:** Read-only descriptive inventory (no scientific conclusions)

**Subdirectories:**

##### `/analysis/3I-ATLAS-0001/reports/`
- **File:** `ARCHIVAL_SYNTHESIS.md` (8.07 KB)
- **Type:** Descriptive archival synthesis document
- **Classification:** DERIVED ANALYSIS
- **Content Summary:**
  - Inventory of 214 archived snapshots (213 daily + 1 official reference)
  - Temporal coverage description (July 2025 - January 2026)
  - Data source enumeration
  - Collection methodology description
  - Snapshot schema documentation
  - Data preservation policy
- **Important Constraints:**
  - ✅ No scientific analysis or interpretation
  - ✅ No conclusions or findings
  - ✅ No metrics claims or assessments
  - ✅ Descriptive inventory only

##### `/analysis/3I-ATLAS-0001/notebooks/`
- **Content:** Empty (contains only `.gitkeep`)
- **Purpose:** Reserved for Jupyter notebooks (if any future analysis)

##### `/analysis/3I-ATLAS-0001/README.md`
- **Size:** 3.11 KB
- **Type:** Analysis directory documentation
- **Classification:** DERIVED ANALYSIS - Metadata

---

## 4. Zenodo Archival Classification

### 4.1 RAW DATA Category (Suitable for Zenodo RAW DATA Archive)

The following directories and files should be classified as **RAW DATA** for Zenodo archival:

#### **Primary Raw Data:**

**1. `/data/snapshots/` - Daily Observational Snapshots**
- **Zenodo Upload Type:** `dataset`
- **Qualification:** Immutable, timestamped snapshots from official astronomical sources
- **Coverage:** 214 files, 627.93 KB total
- **Time Range:** 2025-07-01 to 2026-01-29
- **Format:** JSON (schema: `auto-dz-act.snapshot.v1`)
- **Integrity:** SHA-256 verified
- **Sources:** IAU MPC, NASA/JPL SBDB, NASA/JPL Horizons, ESA NEOCC
- **Archival Value:** HIGH - Primary observational record
- **Recommended Zenodo Keywords:**
  - `3I/ATLAS`
  - `observational astronomy`
  - `raw data`
  - `daily snapshots`
  - `astronomical databases`
  - `interstellar object`

**2. `/data/manifests/` - Integrity Verification Manifests**
- **Zenodo Upload Type:** `dataset`
- **Qualification:** Cryptographic integrity records for raw snapshots
- **Coverage:** 214 files
- **Format:** JSON (schema: `auto-dz-act.manifest.v1`)
- **Purpose:** Ensures data provenance and integrity
- **Archival Value:** HIGH - Essential for data verification
- **Recommended Zenodo Keywords:**
  - `data integrity`
  - `cryptographic verification`
  - `SHA-256`
  - `data provenance`

**3. `/registry/sources.json` - Source Registry**
- **Zenodo Upload Type:** `dataset`
- **Qualification:** Registry of authoritative data sources
- **Purpose:** Documents official platforms queried
- **Archival Value:** MEDIUM - Context for data collection

#### **Supporting Raw Data Documentation:**

**4. Schema and Format Documentation**
- `/docs/SNAPSHOT_SCHEMA.md` (15.68 KB)
- `/docs/DATA_FORMATS.md` (13.79 KB)
- `/docs/DATA_SOURCES_POLICY.md` (13.46 KB)
- **Zenodo Upload Type:** `publication` (subtype: `technicaldocumentation`)
- **Purpose:** Technical specifications for raw data formats
- **Archival Value:** HIGH - Essential for data interpretation

### 4.2 DERIVED ANALYSIS Category (Suitable for Zenodo DERIVED ANALYSIS Archive)

The following files represent **DERIVED ANALYSIS** products:

**1. `/analysis/3I-ATLAS-0001/reports/ARCHIVAL_SYNTHESIS.md`**
- **Zenodo Upload Type:** `publication` (subtype: `report`)
- **Qualification:** Descriptive synthesis of collected data
- **Size:** 8.07 KB
- **Content Type:** Inventory and methodology description
- **Analysis Level:** Minimal (descriptive only, no scientific conclusions)
- **Archival Value:** MEDIUM - Provides context and summary
- **Recommended Zenodo Keywords:**
  - `data synthesis`
  - `archival inventory`
  - `collection methodology`
  - `3I/ATLAS`

**2. `/analysis/3I-ATLAS-0001/README.md`**
- **Zenodo Upload Type:** `publication` (subtype: `technicaldocumentation`)
- **Size:** 3.11 KB
- **Purpose:** Analysis directory documentation
- **Archival Value:** LOW - Repository-specific metadata

### 4.3 Code and Infrastructure (Suitable for Software Archive)

**1. `/scripts/trizel_monitor.py`**
- **Zenodo Upload Type:** `software`
- **Size:** 11.70 KB
- **Purpose:** Automated data collection script
- **Language:** Python
- **Function:** Queries external astronomical APIs and generates snapshots
- **Archival Value:** HIGH - Reproducibility and methodology transparency
- **Recommended Zenodo Keywords:**
  - `data collection`
  - `automation`
  - `Python`
  - `astronomical databases`

**2. `/.github/workflows/trizel-monitor.yml`**
- **Zenodo Upload Type:** `software`
- **Size:** 3.59 KB
- **Purpose:** GitHub Actions workflow for daily automation
- **Archival Value:** MEDIUM - Documents execution infrastructure

### 4.4 Governance and Documentation

**Repository Governance Documentation:**
- `/governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md` (11.68 KB)
- `/docs/OBSERVATORY_SCOPE.md` (11.25 KB)
- `/docs/GOVERNANCE_PROOF_LAYER2_TO_LAYER0.md` (3.38 KB)
- `/docs/USER_GUIDE.md` (5.72 KB)
- `/docs/SCRIPT_REFERENCE.md` (8.78 KB)
- `/docs/TROUBLESHOOTING.md` (13.33 KB)
- **Zenodo Upload Type:** `publication` (subtype: `technicaldocumentation`)
- **Archival Value:** MEDIUM - Provides governance and operational context

**Repository Metadata:**
- `/.zenodo.json` - Zenodo metadata configuration
- `/CITATION.cff` - Citation metadata
- `/README.md` (3.91 KB) - Repository overview
- `/VALIDATION_REPORT.md` (13.35 KB) - Validation documentation
- **Archival Value:** MEDIUM - Repository context and citation

---

## 5. Recommended Zenodo Archival Strategy

### 5.1 Primary Archive: RAW OBSERVATIONAL DATA

**Zenodo Record #1: "AUTO-DZ-ACT 3I/ATLAS Daily Snapshots (Raw Data)"**

**Upload Type:** `dataset`  
**Files to Include:**
- Entire `/data/snapshots/` directory (214 files, 627.93 KB)
- Entire `/data/manifests/` directory (214 files)
- `/registry/sources.json`
- `/docs/SNAPSHOT_SCHEMA.md`
- `/docs/DATA_FORMATS.md`
- `/docs/DATA_SOURCES_POLICY.md`

**Metadata:**
- **Title:** AUTO-DZ-ACT — 3I/ATLAS Daily Observational Snapshots (July 2025 - January 2026)
- **Description:** Immutable, timestamped daily snapshots of official astronomical data sources for 3I/ATLAS (Interstellar Object). Data collected from IAU Minor Planet Center, NASA/JPL SBDB, NASA/JPL Horizons, and ESA NEOCC. Each snapshot includes cryptographic integrity verification (SHA-256). Schema version: auto-dz-act.snapshot.v1. Part of the TRIZEL observatory framework (Layer-1 data collection).
- **Upload Type:** dataset
- **Keywords:** 3I/ATLAS, observational astronomy, raw data, daily snapshots, astronomical databases, interstellar object, data integrity, TRIZEL
- **License:** CC-BY-4.0 (as specified in .zenodo.json)
- **Related Identifiers:** (as specified in .zenodo.json)
  - 10.5281/zenodo.18204071 (isSupplementTo)
  - 10.5281/zenodo.18134257 (isSupplementTo)
  - 10.5281/zenodo.18117231 (isSupplementTo)
  - 10.5281/zenodo.18012859 (isSupplementTo)
  - 10.5281/zenodo.17968772 (isSupplementTo)

**Total Size:** ~1.3 MB (compressed)

### 5.2 Secondary Archive: COLLECTION SOFTWARE

**Zenodo Record #2: "AUTO-DZ-ACT 3I/ATLAS Data Collection Software"**

**Upload Type:** `software`  
**Files to Include:**
- `/scripts/trizel_monitor.py`
- `/.github/workflows/trizel-monitor.yml`
- `/docs/SCRIPT_REFERENCE.md`
- `/docs/USER_GUIDE.md`
- `/docs/TROUBLESHOOTING.md`
- `/README.md`

**Metadata:**
- **Title:** AUTO-DZ-ACT — 3I/ATLAS Automated Data Collection Software
- **Description:** Python-based automated data collection system for astronomical observations. Queries official astronomical databases (IAU MPC, NASA/JPL, ESA) and generates timestamped, integrity-verified snapshots. Includes GitHub Actions workflow for daily automation at 03:15 UTC.
- **Upload Type:** software
- **Keywords:** data collection automation, Python, astronomical databases, GitHub Actions, observatory automation
- **License:** CC-BY-4.0

**Total Size:** ~50 KB

### 5.3 Tertiary Archive: DERIVED ANALYSIS

**Zenodo Record #3: "AUTO-DZ-ACT 3I/ATLAS Archival Synthesis Report"**

**Upload Type:** `publication` (subtype: `report`)  
**Files to Include:**
- `/analysis/3I-ATLAS-0001/reports/ARCHIVAL_SYNTHESIS.md`
- `/analysis/3I-ATLAS-0001/README.md`

**Metadata:**
- **Title:** AUTO-DZ-ACT — 3I/ATLAS Data Collection Archival Synthesis (Gate 4B Analysis Artifact)
- **Description:** Descriptive synthesis and inventory of 214 daily observational snapshots (213 standard daily + 1 official reference) collected for 3I/ATLAS from July 2025 to January 2026. Documents data sources, collection methodology, temporal coverage, and archival policy. No scientific analysis or conclusions. Read-only descriptive inventory conforming to TRIZEL Gate 4B constraints.
- **Upload Type:** publication
- **Publication Type:** report
- **Keywords:** archival synthesis, data inventory, collection methodology, 3I/ATLAS, TRIZEL Gate 4B
- **License:** CC-BY-4.0

**Total Size:** ~12 KB

### 5.4 Optional: Complete Repository Archive

**Zenodo Record #4: "AUTO-DZ-ACT 3I/ATLAS Complete Repository Snapshot"**

**Upload Type:** `software`  
**Files to Include:**
- Complete repository export (excluding `.git/`)

**Metadata:**
- **Title:** AUTO-DZ-ACT-3I-ATLAS-DAILY — Complete Repository Archive
- **Description:** Complete snapshot of the AUTO-DZ-ACT-3I-ATLAS-DAILY repository including raw data, manifests, documentation, scripts, and governance contracts. Layer-1 data collection archive for the TRIZEL observatory framework.
- **Upload Type:** software
- **Keywords:** complete archive, TRIZEL, AUTO-DZ-ACT, 3I/ATLAS, repository snapshot
- **License:** CC-BY-4.0

**Total Size:** ~0.84 MB

---

## 6. Data Integrity and Provenance

### 6.1 Cryptographic Verification
- **Method:** SHA-256 hashing
- **Coverage:** All 214 snapshot files have corresponding manifest with SHA-256 hash
- **Verification:** Each manifest includes `integrity.generated_automatically: true` flag
- **Assurance:** No human interpretation applied (`integrity.no_interpretation_applied: true`)

### 6.2 Temporal Integrity
- **Timestamp Format:** ISO 8601 UTC
- **Timestamp Fields:**
  - `retrieved_utc`: When data was fetched from external sources
  - `requested_day_utc`: The observational day being archived
  - `generated_at_utc`: When manifest was generated
- **Collection Schedule:** Daily at 03:15 UTC (automated via GitHub Actions)

### 6.3 Source Traceability
All snapshots include complete source documentation:
- Source URL
- HTTP status code
- Retrieved timestamp
- Content type
- Byte length
- SHA-256 hash of retrieved content
- Raw file path (for transient storage)

---

## 7. Repository Architecture and TRIZEL Framework

### 7.1 Layer Classification
This repository is **Layer-1** in the TRIZEL architecture:
- **Layer-0:** Governance (trizel-core) — Defines cross-repository governance
- **Layer-1:** Data Collection (THIS REPOSITORY) — Raw, immutable snapshots
- **Layer-2:** Public Display (Future) — Visualization and publication

### 7.2 Repository Constraints
**What this repository DOES:**
- ✅ Collects raw data from authoritative astronomical sources
- ✅ Archives immutable snapshots indexed by observation date
- ✅ Verifies integrity using SHA-256 cryptographic hashing
- ✅ Timestamps all operations in ISO 8601 UTC format
- ✅ Preserves byte-for-byte evidence of source material

**What this repository does NOT do:**
- ❌ NO Scientific Analysis — No interpretation of astronomical data
- ❌ NO Publication — No DOI issuance, no research papers
- ❌ NO Theory Validation — No physics calculations or predictions
- ❌ NO Public Display — Raw archive only
- ❌ NO Governance — Governed BY Layer-0, does not govern others

### 7.3 Gate 4B Compliance
The analysis artifact (`ARCHIVAL_SYNTHESIS.md`) complies with Gate 4B constraints:
- ✅ No scientific analysis performed
- ✅ No conclusions drawn
- ✅ No metrics claimed
- ✅ Descriptive inventory only

---

## 8. Conclusions and Recommendations

### 8.1 File Size Assessment
**Finding:** Repository contains **NO FILES > 5 MB**
- Largest file: 15.68 KB (docs/SNAPSHOT_SCHEMA.md)
- Total repository size: 0.84 MB (excluding .git)
- All data files are small JSON snapshots (~3 KB average)

**Implication:** Repository is highly suitable for Zenodo archival with no file size concerns.

### 8.2 Data Classification Summary

**RAW DATA (High Archival Priority):**
- 214 daily observational snapshots (~628 KB)
- 214 integrity manifests
- Schema documentation
- Source registry

**DERIVED ANALYSIS (Medium Archival Priority):**
- 1 archival synthesis report (8 KB)
- Analysis directory metadata

**SOFTWARE (Medium Archival Priority):**
- Data collection script (Python, 12 KB)
- Automation workflow (YAML, 4 KB)

**DOCUMENTATION (Medium Archival Priority):**
- Governance contracts
- User guides
- Technical specifications

### 8.3 Zenodo Archival Recommendations

**Priority 1: Archive RAW DATA**
- Upload `/data/snapshots/` + `/data/manifests/` as primary dataset
- Include schema documentation for interpretability
- Use existing .zenodo.json metadata as template
- Estimated size: ~1.3 MB (highly manageable)

**Priority 2: Archive SOFTWARE**
- Upload collection scripts and workflows separately
- Ensures reproducibility and methodology transparency
- Estimated size: ~50 KB

**Priority 3: Archive DERIVED ANALYSIS**
- Upload archival synthesis report as technical report
- Provides context and inventory summary
- Estimated size: ~12 KB

**Optional: Complete Repository Archive**
- Upload entire repository as snapshot
- Preserves all governance and documentation
- Estimated size: ~0.84 MB

### 8.4 Data Suitability for Research

**Strengths:**
- ✅ Daily temporal coverage (7 months)
- ✅ Cryptographic integrity verification
- ✅ Immutable, timestamped snapshots
- ✅ Traceable to official astronomical sources
- ✅ Well-documented schema and formats
- ✅ Automated, reproducible collection

**Limitations:**
- ⚠️ Data from external sources currently returns HTTP errors (see official_snapshot)
- ⚠️ No processed scientific analysis (by design - Layer-1 archive only)
- ⚠️ Raw HTML data not committed to repository

---

## 9. Appendices

### Appendix A: Directory Tree Structure
```
/
├── data/
│   ├── snapshots/          [214 JSON files, RAW DATA]
│   ├── manifests/          [214 JSON files, RAW DATA]
│   ├── raw/                [Empty, transient storage]
│   └── metadata/           [Empty]
├── analysis/
│   └── 3I-ATLAS-0001/
│       ├── reports/        [ARCHIVAL_SYNTHESIS.md, DERIVED ANALYSIS]
│       └── notebooks/      [Empty]
├── docs/                   [Documentation, 8 files]
├── governance/             [Governance contracts]
├── scripts/                [trizel_monitor.py, SOFTWARE]
├── registry/               [sources.json, RAW DATA]
└── .github/workflows/      [Automation, SOFTWARE]
```

### Appendix B: Data Source Registry
Official astronomical platforms queried:
1. IAU Minor Planet Center (https://www.minorplanetcenter.net/)
2. NASA/JPL Small-Body Database (https://ssd.jpl.nasa.gov/sb/)
3. NASA/JPL Horizons (https://ssd.jpl.nasa.gov/horizons/)
4. ESA NEO Coordination Centre (https://neo.ssa.esa.int/)

Additional platforms tracked (not all machine-fetchable):
- ESA, ESO, JAXA, CNSA, NASA (mission archives)
- MAST (HST/JWST archive)
- ESO Science Archive
- HEASARC (high-energy missions)
- XMM-Newton Science Archive

### Appendix C: File Counts by Type
- JSON data files: 428+ files (snapshots + manifests)
- Markdown documentation: 15+ files
- Python scripts: 1 file
- YAML workflows: 2 files
- Configuration files: 5 files
- Empty placeholders: 3 files (.keep, .gitkeep)

---

**Report End**

**Generated by:** Repository Scan Analysis  
**Date:** 2026-01-29  
**Purpose:** Zenodo archival classification and inventory  
**Status:** Complete - No modifications made to repository
