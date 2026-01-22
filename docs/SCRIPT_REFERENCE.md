# Script Reference: trizel_monitor.py

## Overview

`trizel_monitor.py` is the core execution script for the AUTO-DZ-ACT-3I-ATLAS-DAILY monitoring system. It fetches data from configured sources, generates snapshots, and maintains integrity verification.

## Location

```
scripts/trizel_monitor.py
```

## Usage

### Basic Syntax

```bash
python scripts/trizel_monitor.py [OPTIONS]
```

### Command-Line Options

#### `--start DATE`

Specify the start date for data collection (YYYY-MM-DD format).

**Default:** Today's date (UTC)

**Examples:**
```bash
# Collect data for a specific date
python scripts/trizel_monitor.py --start 2026-01-15

# Collect data starting from a date (up to today)
python scripts/trizel_monitor.py --start 2026-01-10
```

#### `--end DATE`

Specify the end date for data collection (YYYY-MM-DD format).

**Default:** Same as start date

**Examples:**
```bash
# Collect data for a date range
python scripts/trizel_monitor.py --start 2026-01-15 --end 2026-01-20

# Single day (redundant but valid)
python scripts/trizel_monitor.py --start 2026-01-15 --end 2026-01-15
```

#### `--overwrite`

Force regeneration of snapshots even if they already exist.

**Default:** False (skip existing snapshots)

**Use Cases:**
- Registry source configuration changed
- Need to refresh historical data
- One-time rebuild of all snapshots

**Warning:** This modifies historical data. Use with caution.

**Examples:**
```bash
# Regenerate today's snapshot
python scripts/trizel_monitor.py --overwrite

# Regenerate a date range
python scripts/trizel_monitor.py --start 2026-01-01 --end 2026-01-10 --overwrite
```

#### `--allow-empty-sources`

Allow snapshot generation even if the registry sources list is empty.

**Default:** False (fail if no sources configured)

**Use Cases:**
- Testing the system without real sources
- Emergency scenarios

**Warning:** NOT recommended for production use. Snapshots without sources are not scientifically valid.

**Examples:**
```bash
# Generate empty snapshot (testing only)
python scripts/trizel_monitor.py --allow-empty-sources
```

## Examples

### Standard Daily Collection

```bash
# Collect data for today
python scripts/trizel_monitor.py
```

This is what the automated GitHub Actions workflow runs daily.

### Backfill Historical Data

```bash
# Collect 10 days of historical data
python scripts/trizel_monitor.py --start 2026-01-10 --end 2026-01-20
```

### Rebuild Existing Snapshots

```bash
# Regenerate all of January 2026
python scripts/trizel_monitor.py --start 2026-01-01 --end 2026-01-31 --overwrite
```

### Single Past Date

```bash
# Collect data for a specific past date only
python scripts/trizel_monitor.py --start 2026-01-15 --end 2026-01-15
```

## How It Works

### 1. Initialization

- Loads the registry configuration from `registry/sources.json`
- Validates that sources are configured (unless `--allow-empty-sources` is set)
- Determines the date range to process
- Creates necessary directories

### 2. Date Range Processing

For each date in the specified range:

1. **Check for existing snapshot**
   - If exists and `--overwrite` not set: skip
   - If exists and `--overwrite` set: regenerate

2. **Fetch from sources**
   - For each source in the registry:
     - Construct request with User-Agent
     - Fetch URL with 25-second timeout
     - Calculate SHA-256 checksum
     - Save raw content to `data/raw/YYYY-MM-DD/SOURCE_ID/`
     - Record fetch result (success/failure)

3. **Generate snapshot**
   - Compile all fetch results
   - Add metadata (timestamp, date, source count)
   - Calculate snapshot checksum
   - Write to `data/snapshots/snapshot_YYYY-MM-DD.json`

4. **Generate manifest**
   - Reference the snapshot file
   - Include file size and checksum
   - Add generation metadata
   - Write to `data/manifests/manifest_YYYY-MM-DD.json`

### 3. Output

The script outputs:
- Console logs (fetch status, errors, progress)
- Snapshot files (JSON)
- Manifest files (JSON)
- Raw data files (original content)

## Data Structures

### Registry Format (`registry/sources.json`)

```json
{
  "object": "3I/ATLAS",
  "activation_level": "international_official",
  "authority_basis": "IAU / NASA / ESA",
  "sources": [
    {
      "id": "SOURCE_ID",
      "name": "Source Name",
      "institution": "Institution Name",
      "authority": "Authority Body",
      "role": "Description of role",
      "official": true,
      "url": "https://example.com/",
      "data_access": ["https://example.com/data"]
    }
  ]
}
```

### Snapshot Format

```json
{
  "snapshot_date": "YYYY-MM-DD",
  "generated_at": "2026-01-22T00:00:00.000Z",
  "source_count": 6,
  "fetch_results": [
    {
      "source_id": "SOURCE_ID",
      "url": "https://example.com/",
      "retrieved_utc": "2026-01-22T00:00:00.000Z",
      "ok": true,
      "status_code": 200,
      "content_type": "text/html",
      "sha256": "abc123...",
      "bytes_len": 12345,
      "raw_path": "data/raw/2026-01-22/SOURCE_ID/index.html",
      "error": null
    }
  ]
}
```

### Manifest Format

```json
{
  "manifest_version": "1.0",
  "date": "YYYY-MM-DD",
  "generated_at": "2026-01-22T00:00:00.000Z",
  "snapshot": {
    "path": "data/snapshots/snapshot_YYYY-MM-DD.json",
    "sha256": "def456...",
    "size_bytes": 54321
  }
}
```

## Error Handling

### HTTP Errors

- **Connection failures:** Recorded in snapshot with `ok: false` and error message
- **Timeouts:** 25-second timeout per source
- **4xx/5xx errors:** Status code recorded, content may be partial

### File System Errors

- **Permission errors:** Script will fail (requires write access to `data/`)
- **Disk full:** Script will fail during write operations

### Configuration Errors

- **Missing registry:** Script will fail at startup
- **Empty sources:** Fails unless `--allow-empty-sources` is set
- **Invalid JSON:** Script will fail during registry load

## Exit Codes

- `0` - Success
- `1` - General error (see console output)

## Environment Requirements

### Python Version

- Python 3.7 or higher
- No external dependencies (uses standard library only)

### System Requirements

- Internet connection for data fetching
- Write access to repository directory
- Sufficient disk space for raw data storage

## Security Considerations

### User-Agent Header

All HTTP requests include a custom User-Agent:

```
TRIZEL-Monitor/1.0 (+https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY)
```

This identifies the bot to remote servers and provides contact information.

### Timeout Protection

25-second timeout prevents hanging on unresponsive servers.

### Content Verification

SHA-256 checksums ensure data integrity and detect tampering.

## Performance

### Execution Time

Typical execution time for a single day:
- 6 sources × ~3 seconds per fetch = ~18 seconds
- Plus overhead for file I/O and processing
- **Total: ~20-30 seconds per day**

### Bandwidth Usage

- Variable depending on source page sizes
- Typical: 100KB - 5MB per source
- **Total per day: ~1-30MB**

### Storage Usage

- Snapshots: ~10-50KB per day
- Manifests: ~1KB per day
- Raw data: ~1-30MB per day
- **Total: ~1-30MB per day**, accumulates over time

## Debugging

### Verbose Output

The script outputs detailed logs to console:
- Fetch attempts and results
- File write operations
- Error messages with stack traces

### Checking Results

```bash
# View snapshot for a specific date
cat data/snapshots/snapshot_2026-01-22.json | python -m json.tool

# View manifest
cat data/manifests/manifest_2026-01-22.json | python -m json.tool

# Check raw data
ls -lah data/raw/2026-01-22/
```

### Common Issues

See [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed debugging steps.

## Integration

### GitHub Actions

The script is designed to run in GitHub Actions. See `.github/workflows/trizel-monitor.yml` for the workflow configuration.

### Local Development

```bash
# Clone the repository
git clone https://github.com/abdelkader-omran/AUTO-DZ-ACT-3I-ATLAS-DAILY.git
cd AUTO-DZ-ACT-3I-ATLAS-DAILY

# Run the script
python scripts/trizel_monitor.py
```

See [Development Guide](DEVELOPMENT.md) for setup instructions.

## Extending the Script

### Adding New Sources

1. Edit `registry/sources.json`
2. Add a new source object with required fields
3. Run with `--overwrite` to regenerate existing snapshots

### Modifying Fetch Behavior

The `fetch_url()` function can be customized:
- Adjust timeout
- Add custom headers
- Implement retry logic
- Add authentication

### Custom Output Formats

Modify the data structure classes to change output format:
- `FetchResult` dataclass
- JSON serialization in snapshot generation

## Related Documentation

- [User Guide](USER_GUIDE.md) - How to use the system
- [Data Formats](DATA_FORMATS.md) - Detailed data specifications
- [Development Guide](DEVELOPMENT.md) - Contributing and development
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
