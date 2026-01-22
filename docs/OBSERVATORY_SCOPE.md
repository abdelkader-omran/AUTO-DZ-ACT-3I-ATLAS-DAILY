# Observatory Scope Definition

**Version:** 1.0  
**Effective Date:** 2026-01-22  
**Status:** CAPABILITY STATEMENT — NOT A RESEARCH CLAIM

---

## Purpose

This document defines the scientific scope and operational capabilities of the AUTO-DZ-ACT-3I-ATLAS-DAILY data collection system **without introducing new execution logic or behavioral changes**.

**Critical Constraint:** This is a scope expansion statement, NOT an implementation change. The system's code remains unchanged; only the documented capability envelope is clarified.

---

## Current Focus

### Primary Target: 3I/ATLAS

**Status:** Active observation target since inception

**Characteristics:**
- Interstellar object designation: 3I/ATLAS
- Discovery: International Astronomical Union (IAU) designation
- Data sources: Official observatories (IAU MPC, NASA JPL, ESA NEOCC, etc.)
- Collection frequency: Daily automated snapshots

**Scope:**
- Archival collection of publicly available official data
- Timestamped preservation of source material
- Integrity verification via cryptographic hashing
- NO interpretation, NO analysis, NO scientific claims

---

## Extended Capability: Cosmic Observatory Model

### Generalizable Architecture

**Recognition:** The system architecture is **source-driven and object-agnostic**.

The implementation in `scripts/trizel_monitor.py` does NOT hardcode 3I/ATLAS-specific logic. Instead:

```python
# Line 218: object is read from registry, not hardcoded
"object": registry.get("object", "3I/ATLAS"),
```

**Implication:** The system can collect data for ANY astronomical phenomenon with:
1. Official/authoritative data sources
2. Public HTTP/HTTPS endpoints
3. ISO 8601 date-indexable observations

### Potential Target Classes

The following are **capability statements**, NOT active targets:

#### 1. Interstellar Objects
- 1I/'Oumuamua
- 2I/Borisov
- 3I/ATLAS (current)
- Future interstellar designations

#### 2. Near-Earth Objects (NEOs)
- Asteroids with close approaches
- Potentially Hazardous Asteroids (PHAs)
- Comets with Earth-crossing orbits

#### 3. Transient Phenomena
- Supernovae
- Gamma-ray bursts
- Fast radio bursts (FRBs)
- Gravitational wave events (electromagnetic counterparts)

#### 4. Solar System Bodies
- Comets (periodic and non-periodic)
- Asteroids (main belt, Trojans, etc.)
- Trans-Neptunian Objects (TNOs)
- Centaurs

#### 5. Exoplanetary Events
- Transit observations
- Radial velocity data releases
- Direct imaging campaigns

**Constraint:** All targets must have:
- ✅ Official, institutional data sources
- ✅ Publicly accessible endpoints
- ✅ Temporal/observational indexing
- ❌ NO social media, blogs, or speculative sources

---

## What This System IS

### Data Archive (Layer-1)

**Function:** Observatory-grade timestamped collection

**Characteristics:**
- **Passive observation:** Fetches publicly available data
- **Immutable records:** Snapshots are write-once, SHA-256 verified
- **Source attribution:** Every byte traceable to authoritative origin
- **Temporal indexing:** Organized by observation date (UTC)
- **No interpretation:** Raw material only, no analysis

**Operational Model:**
```
Official Sources → HTTP Fetch → Raw Storage → Snapshot Archive
         ↓
   SHA-256 Hash → Manifest → Integrity Verification
```

### Capabilities

✅ **Multi-Target Collection**
- Registry-driven source configuration
- Object identifier stored in snapshot metadata
- Same architecture for any astronomical phenomenon

✅ **Authoritative Sources**
- IAU Minor Planet Center
- NASA/JPL (SBDB, Horizons, CNEOS)
- ESA Near-Earth Object Coordination Centre
- NASA Planetary Data System
- Any official observatory with public API

✅ **Integrity Guarantee**
- Cryptographic hashing (SHA-256)
- Manifest cross-references
- Tamper-evident archives

✅ **Temporal Resolution**
- Daily automated collection (03:15 UTC)
- Backfill capability for historical dates
- Sub-second timestamp precision

---

## What This System is NOT

### Prohibited Functions

❌ **Scientific Analysis Engine**
- Does NOT compute orbits
- Does NOT predict trajectories
- Does NOT validate theories
- Does NOT interpret observations

❌ **Publication Platform (Layer-2)**
- Does NOT generate DOIs
- Does NOT create visualizations
- Does NOT write research papers
- Does NOT claim discoveries

❌ **Governance Authority (Layer-0)**
- Does NOT authorize observations
- Does NOT define scientific standards
- Does NOT approve methodologies
- Governed BY `trizel-core`, does NOT govern

❌ **Real-Time Alert System**
- Does NOT detect anomalies
- Does NOT trigger notifications
- Does NOT prioritize phenomena
- Archive function only

❌ **Data Quality Filter**
- Does NOT exclude "low quality" sources
- Does NOT weight sources by reputation
- Does NOT hide failed fetches
- Preserves everything as-is

---

## Scope Boundaries

### Geographic/Institutional
- **Global:** No geographic restrictions on source access
- **Institutional:** Official observatories, space agencies, research institutions
- **Public:** Only publicly accessible data (no authentication)

### Temporal
- **Historical:** Can backfill to any past date (limited by source availability)
- **Current:** Daily automated collection
- **Future:** No predictive capability; observation-only

### Phenomenological
- **Observable:** Requires electromagnetic or gravitational wave signature
- **Documented:** Requires official institutional source
- **Non-Speculative:** No hypothetical or theoretical-only targets

---

## Configuration for New Targets

### Registry-Based Target Selection

To observe a new astronomical phenomenon, modify ONLY `registry/sources.json`:

```json
{
  "object": "NEW_TARGET_NAME",          // ← Change this
  "activation_level": "international_official",
  "authority_basis": "IAU / NASA / ESA",
  "sources": [                          // ← Configure sources
    {
      "id": "SOURCE_ID",
      "name": "Source Name",
      "institution": "Operating Institution",
      "authority": "Authoritative Body",
      "role": "Data role description",
      "official": true,
      "url": "https://official.source.endpoint/"
    }
  ]
}
```

**No code changes required.** The system automatically:
1. Reads new `object` field
2. Fetches from configured sources
3. Stores snapshots with new object identifier
4. Maintains same integrity guarantees

---

## Layer Separation

### Layer-0: Governance (trizel-core)

**Defines:**
- Authorization for new target classes
- Cross-repository governance rules
- Ethical/legal constraints on data collection

**Repository:** `trizel-core`

**This layer does NOT:**
- Collect data
- Store snapshots
- Execute workflows

### Layer-1: Data Collection (THIS REPOSITORY)

**Defines:**
- Snapshot collection logic
- Source fetching mechanism
- Integrity verification

**Repository:** `AUTO-DZ-ACT-3I-ATLAS-DAILY`

**This layer does NOT:**
- Interpret data scientifically
- Publish findings
- Govern other layers

### Layer-2: Public Display (hypothetical/future)

**Defines:**
- Visualization
- Public-facing interfaces
- DOI generation and publication

**Repository:** TBD (e.g., `GOI` - Graphical Observatory Interface)

**This layer does NOT:**
- Generate raw data
- Modify historical snapshots
- Execute data collection

---

## Capability vs. Intent

**Critical Distinction:**

| Capability | Intent | Status |
|------------|--------|--------|
| Can collect any astronomical target | Currently collecting 3I/ATLAS only | ✅ |
| Can add NEO sources to registry | No active NEO collection | ⏸️ |
| Can archive transient phenomena | No active transient monitoring | ⏸️ |
| Can support multiple concurrent targets | Single target mode currently | ⏸️ |

**Implication:** The system is **architected** for generalization but **configured** for specificity.

---

## Scientific Restraint

### No Physics Claims

This system does NOT:
- Validate Newtonian mechanics
- Test General Relativity
- Compute orbital elements
- Predict close approaches
- Assess impact probabilities

### No Astronomical Interpretation

This system does NOT:
- Classify object types (asteroid vs. comet)
- Determine composition
- Estimate sizes or masses
- Infer origins (Solar System vs. interstellar)

### Archive-Only Function

**What we do:**
```
"On 2026-01-21 at 04:15:03 UTC, IAU MPC homepage returned 18,240 bytes 
with SHA-256 hash f1ca56b4..."
```

**What we do NOT do:**
```
"Analysis of IAU MPC data suggests 3I/ATLAS is..."
```

---

## Governance Approval for Scope Changes

### Adding New Target Classes

Requires approval from Layer-0 (`trizel-core`) if:
1. Target type represents new scientific domain
2. Source institutions are non-standard
3. Legal/ethical considerations exist

Does NOT require approval if:
- Target is within existing class (e.g., another interstellar object)
- Sources are already-approved institutions (IAU, NASA, ESA)
- Collection is passive observation of public data

### Modifying Existing Targets

Requires contract update if:
- Changing snapshot schema
- Adding new classification states
- Altering integrity guarantees

Does NOT require contract update if:
- Adding/removing sources in registry
- Adjusting fetch timeout
- Changing collection schedule

---

## Future Evolution

### Potential Enhancements (NOT IMPLEMENTED)

Ideas for future development (documentation only):

1. **Multi-Target Concurrent Collection**
   - Separate snapshot series per object
   - Shared raw data directory structure
   - Registry supports multiple object definitions

2. **Real-Time Source Change Detection**
   - Alert on unexpected hash changes
   - Detect source URL modifications
   - NOT an interpretation system

3. **Extended Source Types**
   - API endpoints with JSON responses
   - FITS file archives
   - Catalog databases (VizieR, SIMBAD)

4. **Integrity Proof Chain**
   - Blockchain-style linking of manifests
   - Historical verification without full archive
   - Tamper-evidence reinforcement

**Constraint:** All enhancements must preserve non-interpretation principle.

---

## Compliance

This observatory model complies with:

✅ **Layer-0 Governance**
- Operates within authorized scope
- Follows cross-repository rules
- Maintains traceability

✅ **Scientific Restraint**
- No interpretation or analysis
- Source attribution mandatory
- Transparency in methodology

✅ **Data Integrity**
- Immutable archives
- Cryptographic verification
- Audit trail preservation

✅ **Public Trust**
- Official sources only
- No speculation or prediction
- Institutional-grade rigor

---

## Summary

**This repository is:**
- A generic cosmic/astronomical data collection infrastructure
- Currently configured for 3I/ATLAS monitoring
- Capable of observing any official-source astronomical phenomenon
- Strictly limited to archival function (no interpretation)

**This repository is NOT:**
- A 3I/ATLAS-specific system (architecture is generalizable)
- A scientific analysis platform (observation only)
- A publication engine (Layer-2 function)
- A governance authority (governed BY Layer-0)

---

## References

- **Snapshot Classification:** `governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md`
- **Data Sources Policy:** `docs/DATA_SOURCES_POLICY.md`
- **Layer-0 Governance:** `trizel-core/docs/governance/CROSS_REPO_GOVERNANCE.md`
- **Registry Configuration:** `registry/sources.json`

---

**Document Maintained By:** TRIZEL Architecture Team  
**Last Updated:** 2026-01-22  
**Status:** Approved for publication
