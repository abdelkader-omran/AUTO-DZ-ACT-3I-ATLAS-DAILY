# Data Sources Policy

**Version:** 1.0  
**Effective Date:** 2026-01-22  
**Status:** OPERATIONAL POLICY — ENFORCEMENT ACTIVE

---

## Purpose

This document defines the **mandatory requirements** for data sources included in the observatory registry. It ensures that all collected data meets institutional, scientific, and legal standards for archival preservation.

**Scope:** This policy governs source selection ONLY. It does NOT govern snapshot content interpretation or scientific analysis.

---

## Source Qualification Criteria

### Tier 1: Official Observatories and Space Agencies

**Status:** APPROVED BY DEFAULT

**Institutions:**
- International Astronomical Union (IAU)
- NASA (all divisions: JPL, CNEOS, PDS, etc.)
- European Space Agency (ESA)
- National observatories (NOAO, ESO, etc.)
- Major university observatories (Harvard, Caltech, etc.)
- Government space agencies (JAXA, Roscosmos, CSA, CNSA, ISRO)

**Characteristics:**
- ✅ Peer-reviewed operational standards
- ✅ Institutional accountability
- ✅ Public funding/transparency
- ✅ Long-term data stewardship

**Examples:**
```json
{
  "id": "IAU_MPC",
  "name": "IAU Minor Planet Center",
  "institution": "Smithsonian Astrophysical Observatory",
  "authority": "International Astronomical Union (IAU)",
  "official": true,
  "url": "https://www.minorplanetcenter.net/"
}
```

### Tier 2: Institutional Archives and Databases

**Status:** APPROVED WITH VERIFICATION

**Institutions:**
- Planetary Data System (PDS)
- VizieR catalog service
- SIMBAD astronomical database
- NASA Exoplanet Archive
- Minor Planet Center databases

**Characteristics:**
- ✅ Peer-reviewed data curation
- ✅ Institutional hosting
- ✅ Versioned/timestamped releases
- ⚠️ Requires source authority documentation

**Verification Required:**
- Hosting institution identification
- Data provenance documentation
- Update/versioning policy

### Tier 3: Collaborative Surveys (Pre-Approved)

**Status:** REQUIRES GOVERNANCE APPROVAL

**Examples:**
- Pan-STARRS
- Catalina Sky Survey
- ATLAS (Asteroid Terrestrial-impact Last Alert System)
- ZTF (Zwicky Transient Facility)
- LSST/Vera C. Rubin Observatory

**Characteristics:**
- ✅ Multi-institutional collaboration
- ✅ Standardized data products
- ⚠️ Requires explicit approval per survey
- ⚠️ Must verify public data release policy

**Approval Process:**
1. Document survey governance structure
2. Verify public data release policy
3. Obtain Layer-0 approval
4. Add to pre-approved list

---

## Prohibited Source Types

### Tier X: NEVER APPROVED

The following source types are **permanently prohibited**:

❌ **Social Media**
- Twitter/X, Facebook, Reddit, etc.
- User-generated content
- Non-institutional accounts
- Rationale: No peer review, no accountability, high noise

❌ **Personal Blogs and Websites**
- Individual researcher pages (unless official institutional hosting)
- Amateur astronomer sites
- Speculation/commentary sites
- Rationale: No institutional oversight, no data stewardship

❌ **News and Media Outlets**
- Science journalism sites
- Press releases (unless from approved institutions)
- Popular science magazines
- Rationale: Interpretive layer, not raw data

❌ **Preprint Servers (as raw data)**
- arXiv, bioRxiv, etc.
- Rationale: Papers are INTERPRETATIONS, not raw observational data
- Exception: Papers may be cited in documentation, NOT archived as snapshots

❌ **Commercial Providers**
- Paid data services
- Proprietary databases
- Subscription-only access
- Rationale: Public accessibility requirement, legal restrictions

❌ **Aggregators Without Attribution**
- Data scrapers
- Re-hosted datasets without provenance
- Unverified mirrors
- Rationale: Chain of custody requirement

---

## Required Metadata

### Mandatory Fields (Registry Entry)

Every source MUST include:

```json
{
  "id": "UNIQUE_SOURCE_ID",           // Required: filesystem-safe identifier
  "name": "Full Source Name",         // Required: human-readable
  "institution": "Operating Entity",  // Required: institutional affiliation
  "authority": "Governing Body",      // Required: authoritative oversight
  "role": "Data function",            // Required: purpose description
  "official": true,                   // Required: boolean (must be true)
  "url": "https://..."                // Required: HTTPS endpoint
}
```

### Optional but Recommended Fields

```json
{
  "funding": "Funding Source",        // e.g., "NASA", "ESA"
  "data_access": ["url1", "url2"],    // Additional endpoints
  "timeout_s": 25,                    // Custom timeout (default: 25)
  "ext": "html"                       // File extension override
}
```

### Field Specifications

#### `id` (string, required)
- **Format:** Uppercase with underscores, no spaces
- **Examples:** `"IAU_MPC"`, `"NASA_JPL_SBDB"`, `"ESA_NEOCC"`
- **Constraints:** Must be filesystem-safe (no special chars)
- **Purpose:** Used in raw data directory naming

#### `institution` (string, required)
- **Format:** Official institutional name
- **Examples:** `"Jet Propulsion Laboratory (JPL)"`, `"European Space Agency (ESA)"`
- **Purpose:** Accountability and provenance

#### `authority` (string, required)
- **Format:** Governing/oversight body
- **Examples:** `"NASA"`, `"International Astronomical Union (IAU)"`, `"ESA Planetary Defence Office"`
- **Purpose:** Institutional chain of authority

#### `role` (string, required)
- **Format:** Free text description
- **Examples:** `"Global clearinghouse for observations and orbits"`, `"NEO monitoring and impact risk assessment"`
- **Purpose:** Functional documentation

#### `official` (boolean, required)
- **Format:** Must be `true`
- **Constraint:** Only official sources permitted
- **Purpose:** Enforcement of source quality policy

#### `url` (string, required)
- **Format:** Valid HTTPS URL (HTTP acceptable for legacy institutional sites)
- **Constraint:** Must be publicly accessible (no authentication)
- **Purpose:** Primary fetch endpoint

---

## Observation Date vs. Processing Date

### Critical Distinction

**Observation Date (requested_day_utc):**
- The UTC date for which observational data is being archived
- Indexed by snapshot filename: `snapshot_YYYY-MM-DD.json`
- Represents: "What was publicly available on this date"

**Processing Date (retrieved_utc):**
- The UTC timestamp when data was actually fetched
- Recorded in snapshot metadata
- Represents: "When this archive was created"

**Invariant:**
```
observation_date <= processing_date
```

### Source Timestamp Requirements

Sources MUST provide:
- ✅ Date of observation (explicit or implicit in URL structure)
- ✅ Date of data publication/update (if available)
- ⚠️ Processing date recorded automatically by system

Sources MAY provide:
- Observation timestamp (sub-day precision)
- Update frequency information
- Data version identifiers

---

## Source URL Structure

### Static URLs (Most Common)

**Format:** Fixed endpoint, content changes over time

```json
{
  "url": "https://www.minorplanetcenter.net/"
}
```

**Behavior:**
- Same URL fetched daily
- Content hash compared to detect changes
- Previous versions NOT preserved (snapshot archive serves this function)

### Templated URLs (Date-Parameterized)

**Format:** URL includes date placeholders

**Supported Templates:**
- `{YYYY}` - 4-digit year
- `{MM}` - 2-digit month
- `{DD}` - 2-digit day
- `{DATE}` - ISO 8601 date (YYYY-MM-DD)

**Example:**
```json
{
  "url": "https://example.observatory.org/data/{YYYY}/{MM}/{DD}/summary.json"
}
```

**Behavior:**
- Template resolved before fetch
- Each day fetches unique URL
- Historical backfill supported

### API Endpoints

**Format:** RESTful or query-based APIs

```json
{
  "url": "https://ssd-api.jpl.nasa.gov/cad.api"
}
```

**Constraints:**
- Must be publicly accessible (no API keys)
- Rate limiting must allow daily fetches
- Response must be stable (deterministic for same date)

---

## Source Addition Procedure

### Step 1: Qualification Review

**Checklist:**
- [ ] Source is Tier 1, 2, or pre-approved Tier 3
- [ ] Institutional affiliation documented
- [ ] Public accessibility verified
- [ ] No authentication required
- [ ] HTTPS endpoint available
- [ ] Legal/ethical clearance (if needed)

### Step 2: Registry Entry

**Action:** Edit `registry/sources.json`

**Template:**
```json
{
  "id": "NEW_SOURCE_ID",
  "name": "Official Source Name",
  "institution": "Operating Institution",
  "authority": "Governing Body",
  "role": "Data role description",
  "official": true,
  "url": "https://official.endpoint/"
}
```

### Step 3: Test Fetch

**Command:**
```bash
python scripts/trizel_monitor.py --day YYYY-MM-DD
```

**Verification:**
- [ ] Fetch succeeds (ok: true)
- [ ] Raw file created in `data/raw/YYYY-MM-DD/`
- [ ] SHA-256 hash recorded
- [ ] No errors in console output

### Step 4: Documentation

**Update:**
- Source list in documentation
- Data sources policy (this file, if new tier)
- README.md acknowledgments

### Step 5: Commit

**Commit Message Format:**
```
Add SOURCE_NAME to registry

- Institution: INSTITUTION_NAME
- Authority: AUTHORITY_BODY
- Purpose: BRIEF_DESCRIPTION
```

---

## Source Removal Procedure

### When to Remove

Remove a source if:
- ❌ Source endpoint permanently offline (404, domain expired)
- ❌ Institutional closure or data archival
- ❌ Legal/ethical issue discovered
- ❌ Source no longer meets qualification criteria

Do NOT remove if:
- ⚠️ Temporary outage (network, maintenance)
- ⚠️ Rate limiting (can be addressed with timeout adjustment)
- ⚠️ Content changes (expected behavior)

### Removal Process

**DO NOT:**
- Delete historical snapshots containing removed source
- Modify past snapshot files

**DO:**
1. Remove source entry from `registry/sources.json`
2. Document reason in commit message
3. Preserve all historical snapshots AS-IS
4. Update documentation to note source discontinuation

**Commit Message Format:**
```
Remove SOURCE_NAME from registry

Reason: [REASON]
Last successful fetch: YYYY-MM-DD
Historical data: Preserved in snapshots YYYY-MM-DD through YYYY-MM-DD
```

---

## Source Validation Policy

### Automated Validation (Implemented)

Currently enforced by `scripts/trizel_monitor.py`:

```python
# Line 162: Missing URL check
if not url_tmpl:
    out.append({
        "id": source_id,
        "ok": False,
        "error": "Missing url in registry source entry",
    })
```

**Checks:**
- URL field presence
- HTTP fetch success/failure
- Response integrity (SHA-256)

### Manual Validation (Recommended)

**Quarterly Review:**
- [ ] Verify all sources still operational
- [ ] Check for institutional changes
- [ ] Review fetch success rate (should be >90%)
- [ ] Update contact information if needed

**Annual Review:**
- [ ] Re-verify Tier 2 source qualifications
- [ ] Check for new official sources
- [ ] Review prohibited source list for updates
- [ ] Audit compliance with this policy

---

## Compliance and Enforcement

### Registry Compliance Check

**Automated:** None currently implemented

**Manual Checklist:**
```bash
# 1. Validate JSON syntax
cat registry/sources.json | python -m json.tool

# 2. Check required fields
cat registry/sources.json | jq '.sources[] | select(.official != true)'
# Should return empty (all sources must be official)

# 3. Verify source count
cat registry/sources.json | jq '.sources | length'
# Should be > 0 (no empty registry)
```

### Non-Compliance Actions

**If non-compliant source discovered:**

1. **Immediate:** Comment out source in registry (JSON comment workaround)
2. **Short-term:** Remove source, document in commit
3. **Long-term:** Review policy for gap that allowed non-compliance

**If historical non-compliance discovered:**

1. **DO NOT** modify historical snapshots
2. **DO** document issue in governance records
3. **DO** remove source going forward
4. **DO** note discontinuation in documentation

---

## Legal and Ethical Considerations

### Data Usage Rights

**Requirement:** All sources must permit:
- ✅ Automated access (no robots.txt prohibition)
- ✅ Archival storage
- ✅ Redistribution (for open science)
- ✅ Non-commercial use

**Prohibited:**
- ❌ Copyrighted data without explicit permission
- ❌ Restricted datasets
- ❌ Personal/private information

### Attribution

**Policy:**
- All sources attributed in snapshot metadata
- Institutional credit maintained
- Source URLs preserved for traceability

### Rate Limiting and Ethical Scraping

**Policy:**
- Maximum 1 fetch per source per day (current implementation)
- 25-second timeout prevents server overload
- User-Agent header identifies bot and provides contact

**User-Agent:**
```
TRIZEL-Monitor/1.0 (+https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY)
```

---

## Summary

**Approved Sources:**
- Official observatories (IAU, NASA, ESA, etc.)
- Institutional archives (PDS, VizieR, etc.)
- Pre-approved collaborative surveys

**Prohibited Sources:**
- Social media, blogs, news sites
- Preprint servers (as raw data)
- Commercial/subscription services
- Unattributed aggregators

**Required Metadata:**
- Institutional affiliation
- Authoritative oversight
- Public HTTPS endpoint
- Official status (must be true)

**Enforcement:**
- Manual registry review
- Automated fetch validation
- Quarterly compliance checks

---

## References

- **Snapshot Classification:** `governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md`
- **Observatory Scope:** `docs/OBSERVATORY_SCOPE.md`
- **Registry Configuration:** `registry/sources.json`
- **Layer-0 Governance:** `trizel-core/docs/governance/CROSS_REPO_GOVERNANCE.md`

---

**Document Maintained By:** TRIZEL Data Stewardship Team  
**Last Updated:** 2026-01-22  
**Next Review:** 2026-04-22 (Quarterly)
