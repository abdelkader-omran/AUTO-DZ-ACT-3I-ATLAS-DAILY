# User Guide

## Introduction

AUTO-DZ-ACT-3I-ATLAS-DAILY is an automated execution layer for daily monitoring and data collection of 3I/ATLAS observational data from authoritative international sources. This repository operates as a Layer 2 execution component within the TRIZEL governance framework.

## Overview

This system automatically:
- Fetches data from official astronomical sources (IAU MPC, NASA JPL, ESA)
- Generates daily snapshots with integrity verification
- Creates manifest files with metadata and checksums
- Publishes releases with data artifacts
- Maintains a complete historical record

## Quick Start

### Running the Daily Workflow

The easiest way to run the workflow is through GitHub Actions:

1. Navigate to your repository on GitHub
2. Click on the **Actions** tab
3. Select **TRIZEL Monitor – Daily Snapshot** workflow
4. Click **Run workflow**
5. Leave all fields empty for a standard daily run
6. Click **Run workflow** button

The workflow will:
- Fetch data from all configured sources
- Generate a snapshot file for today
- Create a manifest with integrity metadata
- Commit the files to the repository
- Create a GitHub release with the artifacts

### Backfilling Historical Data

To collect data for past dates:

1. Go to **Actions** → **TRIZEL Monitor – Daily Snapshot**
2. Click **Run workflow**
3. Set **start_date**: `2026-01-15` (or your desired start date in YYYY-MM-DD format)
4. Set **end_date**: `2026-01-20` (or your desired end date)
5. Leave other options as default
6. Click **Run workflow**

The system will process each day in the range sequentially.

### Advanced Options

#### Force Overwrite

Use this when you need to regenerate existing snapshots (e.g., after updating the registry):

- Set **overwrite** to `true`
- This will regenerate snapshots even if they already exist
- Useful for one-time rebuilds after registry source updates

**Warning:** Use sparingly as it rewrites historical data.

#### Allow Empty Sources

This is a safety escape hatch that should **NOT** be used in normal operations:

- Set **allow_empty_sources** to `true`
- Allows snapshot generation even if no sources are configured
- Only use for testing or emergency scenarios

## Understanding the Output

### Snapshot Files

Location: `data/snapshots/snapshot_YYYY-MM-DD.json`

Each snapshot contains:
- Timestamp of collection
- List of fetch results from each source
- Status information (success/failure)
- Content checksums for integrity verification
- URLs and metadata for each source

### Manifest Files

Location: `data/manifests/manifest_YYYY-MM-DD.json`

Each manifest contains:
- Snapshot file metadata
- SHA-256 checksum of the snapshot
- File size and location
- Generation timestamp
- Integrity verification information

### Raw Data Files

Location: `data/raw/YYYY-MM-DD/`

Contains the actual fetched content from each source, organized by:
- Date directory
- Source ID subdirectories
- Raw response files with checksums

## Automated Schedule

The workflow runs automatically:
- **Daily at 03:15 UTC**
- Scheduled via GitHub Actions cron
- No manual intervention required
- Commits are made by `trizel-monitor[bot]`

## Data Integrity

Every piece of data includes:
- **SHA-256 checksums** for content verification
- **Timestamps** in ISO 8601 UTC format
- **Source attribution** with URLs
- **HTTP status codes** and error tracking
- **Manifest files** linking snapshots to raw data

## Viewing Results

### GitHub Releases

Each daily run creates a GitHub release:
- Tag: `snapshot-YYYY-MM-DD`
- Title: "Daily Official Scientific Data Snapshot (YYYY-MM-DD)"
- Assets: Snapshot and manifest JSON files

To view:
1. Go to your repository
2. Click on **Releases**
3. Find the release for your desired date
4. Download the snapshot or manifest files

### Repository Files

All data is also committed to the repository:
- Browse the `data/` directory
- View commit history for changes
- Use `git log` to see collection history

## Data Sources

The system collects data from the following official sources:

1. **IAU Minor Planet Center (MPC)**
   - Global clearinghouse for observations and orbits
   - Authority: International Astronomical Union
   - Funding: NASA

2. **NASA/JPL Small-Body Database (SBDB)**
   - High-precision orbital elements and physical parameters
   - Authority: NASA Jet Propulsion Laboratory

3. **NASA/JPL Horizons System**
   - Authoritative ephemerides for Solar System bodies
   - Authority: NASA Jet Propulsion Laboratory

4. **ESA Near-Earth Object Coordination Centre (NEOCC)**
   - NEO monitoring and impact risk assessment
   - Authority: European Space Agency

5. **NASA Center for Near-Earth Object Studies (CNEOS)**
   - Close-approach analysis and impact monitoring
   - Authority: NASA Jet Propulsion Laboratory

6. **NASA Planetary Data System – Small Bodies Node**
   - Archival mission and derived data
   - Authority: NASA Planetary Data System

See `registry/sources.json` for complete source configuration.

## Governance

This repository operates under the TRIZEL governance framework:

- **Layer 0 (Governance):** [trizel-core](https://github.com/abdelkader-omran/trizel-core)
- **Layer 1 (Definitions):** [AUTO-DZ-ACT-FRAMEWORK](https://github.com/abdelkader-omran/AUTO-DZ-ACT-FRAMEWORK)
- **Layer 2 (Execution):** This repository

See [Governance Reference](GOVERNANCE_REFERENCE.md) for details.

## Support and Issues

For issues or questions:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review existing GitHub Issues
3. Create a new issue with detailed information

## Related Documentation

- [Script Reference](SCRIPT_REFERENCE.md) - Detailed script documentation
- [Data Formats](DATA_FORMATS.md) - Data structure specifications
- [Development Guide](DEVELOPMENT.md) - Setup for contributors
- [Governance Proof](GOVERNANCE_PROOF_LAYER2_TO_LAYER0.md) - Governance validation
