# Zenodo Archive Download Instructions

## Direct Download Link Generation

To obtain a direct HTTPS download link for the Zenodo RAW DATA archive, follow these steps:

### Option 1: GitHub Actions Artifact (Recommended)

1. **Trigger the workflow:**
   - Go to: https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY/actions/workflows/upload-zenodo-archive.yml
   - Click the "Run workflow" button
   - Select branch: `copilot/generate-zenodo-raw-data-archive` (or `main` after PR merge)
   - Click "Run workflow" to start

2. **Wait for completion:**
   - The workflow will regenerate the archive (takes ~30 seconds)
   - Monitor progress in the Actions tab

3. **Download the archive:**
   - Once complete, scroll to the bottom of the workflow run page
   - Find the "Artifacts" section
   - Click "zenodo-raw-data-archive" to download
   - The artifact will be retained for 90 days

### Option 2: GitHub Release (Alternative)

If you need a permanent download link, create a GitHub Release:

1. **Create a new release:**
   - Go to: https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY/releases/new
   - Tag version: `zenodo-raw-v2026-01-29`
   - Release title: `Zenodo RAW DATA Archive (2025-07-01 to 2026-01-29)`
   - Description: Copy from the generated release notes

2. **Attach the archive:**
   - First, download the artifact from the workflow run (Option 1)
   - Drag and drop the `.tar.gz` file into the release assets section
   - Check "Set as a pre-release" or "Create a draft release" if not ready to publish

3. **Get the download link:**
   - After creating the release, the download link will be:
   ```
   https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY/releases/download/zenodo-raw-v2026-01-29/AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz
   ```

## Archive Details

**File:** `AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz`  
**Size:** 60 KB  
**SHA-256:** `883e14a675f7a8f3d6dc50a7ceb11e6deb149d2c3898dfd64963abc164f31330`

**Contents:**
- 213 snapshot files (data/snapshots/)
- 214 manifest files (data/manifests/)
- 3 documentation files (docs/, governance/)

## Verification

After downloading, verify the archive integrity:

```bash
# Check SHA-256 checksum
sha256sum AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz
# Expected: 883e14a675f7a8f3d6dc50a7ceb11e6deb149d2c3898dfd64963abc164f31330

# List contents
tar -tzf AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz | head -20

# Extract
tar -xzf AUTO-DZ-ACT-3I-ATLAS-DAILY-RAW-2025-07-01_to_2026-01-29.tar.gz
```

## Notes

- The workflow generates a deterministic archive with stable file ordering
- No timestamps are rewritten; source file checksums remain unchanged
- The archive is NOT committed to the repository (excluded by .gitignore)
- Artifact retention: 90 days (for GitHub Actions artifacts)
- Release assets: permanent (for GitHub Releases)
