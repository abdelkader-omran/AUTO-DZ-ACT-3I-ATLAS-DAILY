# AUTO-DZ-ACT-3I-ATLAS-DAILY

**Layer 2 — Execution-Only Repository**

This repository executes daily data collection and processing workflows for 3I/ATLAS observational data.

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

## Governance & Definitions

This repository operates under external governance and definitions:
- **Layer 0 Governance:** [trizel-core repository](https://github.com/abdelkader-omran/trizel-core)
- **Layer 1 Definitions:** [AUTO-DZ-ACT-FRAMEWORK repository](https://github.com/abdelkader-omran/AUTO-DZ-ACT-FRAMEWORK)
