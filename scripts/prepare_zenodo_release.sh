#!/bin/bash
set -e

# Zenodo Release Preparation Script
# This script prepares a GitHub release for Zenodo dataset archival

echo "🚀 Zenodo Release Preparation Script"
echo "======================================"
echo ""

# Check if we're in the repository root
if [ ! -f ".zenodo.json" ]; then
    echo "❌ Error: .zenodo.json not found. Run this script from the repository root."
    exit 1
fi

# Detect snapshot date range
echo "📅 Detecting snapshot date range..."
EARLIEST=$(ls data/snapshots/snapshot_*.json 2>/dev/null | head -1 | grep -oP '\d{4}-\d{2}-\d{2}' || echo "unknown")
LATEST=$(ls data/snapshots/snapshot_*.json 2>/dev/null | tail -1 | grep -oP '\d{4}-\d{2}-\d{2}' || echo "unknown")
SNAPSHOT_COUNT=$(ls data/snapshots/snapshot_*.json 2>/dev/null | wc -l)

if [ "$EARLIEST" = "unknown" ] || [ "$LATEST" = "unknown" ]; then
    echo "❌ Error: Could not detect snapshot date range"
    exit 1
fi

echo "   Range: $EARLIEST to $LATEST"
echo "   Count: $SNAPSHOT_COUNT snapshots"
echo ""

# Define archive name
ARCHIVE_NAME="AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-${EARLIEST}_to_${LATEST}.tar.gz"
TAG_NAME="zenodo-raw-v${LATEST//-/}"

echo "📦 Archive: $ARCHIVE_NAME"
echo "🏷️  Tag: $TAG_NAME"
echo ""

# Check if archive exists
if [ ! -f "$ARCHIVE_NAME" ]; then
    echo "❌ Error: Archive not found: $ARCHIVE_NAME"
    echo "   Run the workflow first: .github/workflows/zenodo-dataset-preparation.yml"
    exit 1
fi

ARCHIVE_SIZE=$(ls -lh "$ARCHIVE_NAME" | awk '{print $5}')
echo "✅ Archive found: $ARCHIVE_SIZE"
echo ""

# Generate release notes
RELEASE_NOTES_FILE="release_notes_${LATEST}.md"

cat > "$RELEASE_NOTES_FILE" << EOF
# Zenodo Dataset Package — Raw Observational Archive

**Dataset Version:** v${LATEST}
**Temporal Coverage:** ${EARLIEST} to ${LATEST}
**Snapshot Count:** ${SNAPSHOT_COUNT} daily snapshots
**Package Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Archive Contents

- **Daily Snapshots:** ${SNAPSHOT_COUNT} files (\`data/snapshots/snapshot_YYYY-MM-DD.json\`)
- **Integrity Manifests:** ${SNAPSHOT_COUNT} files (\`data/manifests/manifest_YYYY-MM-DD.json\`)
- **Official Snapshots:** 1 reference snapshot
- **Documentation:** Schema specifications, data formats, governance contracts

## Data Sources

All snapshots aggregate data from official astronomical institutions:

1. **IAU Minor Planet Center (MPC)**
   - Authority: International Astronomical Union (IAU)
   - URL: https://www.minorplanetcenter.net/

2. **NASA/JPL Small-Body Database (SBDB)**
   - Authority: NASA Jet Propulsion Laboratory
   - URL: https://ssd.jpl.nasa.gov/sb/

3. **NASA/JPL Horizons**
   - Authority: NASA Jet Propulsion Laboratory
   - URL: https://ssd.jpl.nasa.gov/horizons/

4. **ESA Near-Earth Object Coordination Centre (NEOCC)**
   - Authority: European Space Agency
   - URL: https://neo.ssa.esa.int/

5. **NASA Center for Near-Earth Object Studies (CNEOS)**
   - Authority: NASA Jet Propulsion Laboratory
   - URL: https://cneos.jpl.nasa.gov/

6. **NASA Planetary Data System Small Bodies Node**
   - Authority: NASA Planetary Data System
   - URL: https://pds-smallbodies.astro.umd.edu/

## Data Integrity and Provenance

### Cryptographic Verification
- **SHA-256 hashing:** Every snapshot paired with integrity manifest
- **Immutability flags:** All manifests confirm automated generation
- **No interpretation:** \`"no_interpretation_applied": true\` in all manifests

### Provenance Documentation
Each snapshot includes complete provenance:
- Source URLs and institutional attribution
- Retrieval timestamps (ISO 8601 UTC)
- HTTP status codes and content types
- SHA-256 hashes of fetched content

### Archival Standards Compliance
- ✅ **Provenance-based:** Complete documentation of data origin
- ✅ **Immutable:** Historical snapshots protected by policy
- ✅ **Non-instrumental:** Aggregation from institutional databases
- ✅ **Timestamped:** ISO 8601 UTC throughout
- ✅ **Append-only:** New data extends archive; historical data unchanged

## Usage Instructions

### Download and Extract
\`\`\`bash
# Download the archive
wget https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY/releases/download/${TAG_NAME}/${ARCHIVE_NAME}

# Extract
tar -xzf ${ARCHIVE_NAME}

# Navigate to dataset
cd zenodo_dataset/
\`\`\`

### Read Documentation
\`\`\`bash
# Primary documentation
cat README.md

# Schema specification
cat docs/SNAPSHOT_SCHEMA.md

# Data format details
cat docs/DATA_FORMATS.md

# Governance contract
cat governance/SNAPSHOT_CLASSIFICATION_CONTRACT.md
\`\`\`

### Verify Integrity
\`\`\`bash
# Example: Verify a single snapshot
SNAPSHOT="data/snapshots/snapshot_2026-01-29.json"
MANIFEST="data/manifests/manifest_2026-01-29.json"

# Extract expected hash from manifest
EXPECTED_HASH=\$(jq -r '.snapshot_sha256' "\$MANIFEST")

# Compute actual hash
ACTUAL_HASH=\$(sha256sum "\$SNAPSHOT" | awk '{print \$1}')

# Compare
if [ "\$EXPECTED_HASH" = "\$ACTUAL_HASH" ]; then
    echo "✅ Integrity verified"
else
    echo "❌ Hash mismatch!"
fi
\`\`\`

## What This Dataset IS

✅ **Raw observational archive** — Timestamped records from official sources  
✅ **Provenance-verified** — Complete documentation of data origin  
✅ **Integrity-protected** — Cryptographic hashing for verification  
✅ **Non-instrumental** — Aggregation from institutional databases  
✅ **Append-only** — Historical records preserved immutably  

## What This Dataset is NOT

❌ **NOT scientific analysis** — No interpretation or conclusions  
❌ **NOT instrumental data** — No direct telescope observations  
❌ **NOT predictive** — No modeling or forecasting  
❌ **NOT curated** — Source responses preserved as-received  
❌ **NOT validated scientifically** — Content verification is institutional responsibility  

## License

This dataset is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Full license: https://creativecommons.org/licenses/by/4.0/

## Citation

\`\`\`bibtex
@dataset{omran2026_autodz_3iatlas_raw,
  author       = {Omran, Abdelkader},
  title        = {{AUTO-DZ-ACT — 3I/ATLAS Daily Observational 
                   Snapshots (${EARLIEST} → ${LATEST})}},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v${LATEST}},
  license      = {CC-BY-4.0},
  note         = {Raw observational archive from official 
                  astronomical data sources}
}
\`\`\`

## References

**Repository:** https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY  
**Governance:** TRIZEL-BASELINE-v1.0.0 (https://github.com/abdelkader-omran/trizel-core)

**Related Archives:**
- 10.5281/zenodo.18204071
- 10.5281/zenodo.18134257
- 10.5281/zenodo.18117231
- 10.5281/zenodo.18012859
- 10.5281/zenodo.17968772

---

**Prepared by:** AUTO-DZ-ACT Layer-1 Data Collection System  
**Contact:** Abdelkader Omran (Independent Researcher)
EOF

echo "✅ Release notes created: $RELEASE_NOTES_FILE"
echo ""

# Instructions
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Create GitHub Release:"
echo "   - Go to: https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY/releases/new"
echo "   - Tag: $TAG_NAME"
echo "   - Title: Zenodo Dataset v${LATEST} — Raw Observational Archive (${EARLIEST} → ${LATEST})"
echo "   - Description: Copy from $RELEASE_NOTES_FILE"
echo "   - Upload: $ARCHIVE_NAME"
echo ""
echo "2. Or use GitHub CLI:"
echo "   gh release create $TAG_NAME \\"
echo "     --title 'Zenodo Dataset v${LATEST} — Raw Observational Archive (${EARLIEST} → ${LATEST})' \\"
echo "     --notes-file $RELEASE_NOTES_FILE \\"
echo "     $ARCHIVE_NAME"
echo ""
echo "3. After release is published:"
echo "   - Download the release asset from GitHub"
echo "   - Upload to Zenodo (manual process)"
echo "   - Link Zenodo DOI back to GitHub release"
echo ""
echo "⚠️  Note: Archive is prepared but NOT automatically published to Zenodo."
echo "   Manual Zenodo upload is required for formal archival."
echo ""
