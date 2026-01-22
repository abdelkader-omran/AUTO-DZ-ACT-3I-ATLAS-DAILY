# Data Formats Specification

## Overview

This document specifies the data formats used throughout the AUTO-DZ-ACT-3I-ATLAS-DAILY system. All data is stored in JSON format with strict schemas for interoperability and integrity verification.

## Directory Structure

```
data/
├── snapshots/          # Daily snapshot files
│   └── snapshot_YYYY-MM-DD.json
├── manifests/          # Manifest metadata files
│   └── manifest_YYYY-MM-DD.json
├── raw/                # Raw fetched content
│   └── YYYY-MM-DD/     # Date directory
│       └── SOURCE_ID/  # Source subdirectory
│           └── *.*     # Fetched files
└── metadata/           # Additional metadata (future use)
```

## Registry Format

**File:** `registry/sources.json`

**Purpose:** Defines the authoritative data sources for monitoring

### Schema

```json
{
  "object": "string",              // Target object (e.g., "3I/ATLAS")
  "activation_level": "string",    // Classification level
  "authority_basis": "string",     // Governing authorities
  "sources": [                     // Array of source configurations
    {
      "id": "string",              // Unique identifier (required)
      "name": "string",            // Human-readable name
      "institution": "string",     // Operating institution
      "authority": "string",       // Authoritative body
      "funding": "string",         // Funding source (optional)
      "role": "string",            // Source's role/purpose
      "official": boolean,         // Official status flag
      "url": "string",             // Primary URL
      "data_access": [             // Data access URLs (optional)
        "string"
      ]
    }
  ]
}
```

### Field Specifications

#### Root Level

- **object** (string, required): The astronomical object being monitored
  - Example: `"3I/ATLAS"`

- **activation_level** (string, required): Classification of monitoring intensity
  - Example: `"international_official"`

- **authority_basis** (string, required): Comma-separated list of governing authorities
  - Example: `"IAU / NASA / ESA"`

- **sources** (array, required): List of data source configurations

#### Source Object

- **id** (string, required): Unique identifier for the source
  - Must be filesystem-safe (no special characters)
  - Used in raw data directory names
  - Example: `"IAU_MPC"`, `"NASA_JPL_SBDB"`

- **name** (string, required): Full human-readable name
  - Example: `"IAU Minor Planet Center"`

- **institution** (string, required): Operating institution or organization
  - Example: `"Smithsonian Astrophysical Observatory"`

- **authority** (string, required): Authoritative governing body
  - Example: `"International Astronomical Union (IAU)"`

- **funding** (string, optional): Primary funding source
  - Example: `"NASA"`

- **role** (string, required): Description of the source's purpose
  - Example: `"Global clearinghouse for observations and orbits"`

- **official** (boolean, required): Whether this is an official authority source
  - Must be `true` for primary sources

- **url** (string, required): Primary URL for the source
  - Must be a valid HTTPS URL
  - This URL is fetched during monitoring

- **data_access** (array of strings, optional): Additional data access URLs
  - For documentation purposes
  - Not directly fetched by the system

### Example

```json
{
  "object": "3I/ATLAS",
  "activation_level": "international_official",
  "authority_basis": "IAU / NASA / ESA",
  "sources": [
    {
      "id": "IAU_MPC",
      "name": "IAU Minor Planet Center",
      "institution": "Smithsonian Astrophysical Observatory",
      "authority": "International Astronomical Union (IAU)",
      "funding": "NASA",
      "role": "Global clearinghouse for observations and orbits",
      "official": true,
      "url": "https://www.minorplanetcenter.net/",
      "data_access": [
        "https://www.minorplanetcenter.net/db_search"
      ]
    }
  ]
}
```

## Snapshot Format

**File:** `data/snapshots/snapshot_YYYY-MM-DD.json`

**Purpose:** Daily record of all data fetches with integrity verification

### Schema

```json
{
  "snapshot_date": "YYYY-MM-DD",      // ISO 8601 date
  "generated_at": "ISO8601_UTC",      // Generation timestamp
  "source_count": number,             // Total sources processed
  "fetch_results": [                  // Array of fetch results
    {
      "source_id": "string",          // Matches registry ID
      "url": "string",                // URL fetched
      "retrieved_utc": "ISO8601_UTC", // Fetch timestamp
      "ok": boolean,                  // Success flag
      "status_code": number|null,     // HTTP status code
      "content_type": "string"|null,  // Content-Type header
      "sha256": "string"|null,        // SHA-256 checksum
      "bytes_len": number,            // Content length
      "raw_path": "string"|null,      // Path to raw file
      "error": "string"|null          // Error message if failed
    }
  ]
}
```

### Field Specifications

#### Root Level

- **snapshot_date** (string, required): Date of the snapshot in ISO 8601 format
  - Format: `YYYY-MM-DD`
  - Example: `"2026-01-22"`

- **generated_at** (string, required): Timestamp when snapshot was generated
  - Format: ISO 8601 UTC with 'Z' suffix
  - Example: `"2026-01-22T03:15:42.123Z"`

- **source_count** (number, required): Total number of sources processed
  - Example: `6`

- **fetch_results** (array, required): List of fetch results, one per source

#### Fetch Result Object

- **source_id** (string, required): Source identifier from registry
  - Example: `"IAU_MPC"`

- **url** (string, required): The URL that was fetched
  - Example: `"https://www.minorplanetcenter.net/"`

- **retrieved_utc** (string, required): Timestamp when fetch occurred
  - Format: ISO 8601 UTC with 'Z' suffix
  - Example: `"2026-01-22T03:15:38.456Z"`

- **ok** (boolean, required): Whether fetch was successful
  - `true`: Successful HTTP 2xx response
  - `false`: Any error (network, HTTP error, timeout)

- **status_code** (number or null, required): HTTP response status code
  - Example: `200`, `404`, `500`
  - `null` if network error prevented response

- **content_type** (string or null, required): Content-Type response header
  - Example: `"text/html; charset=UTF-8"`
  - `null` if not provided or error occurred

- **sha256** (string or null, required): SHA-256 checksum of response body
  - 64 hexadecimal characters
  - Example: `"a3f5d9e8b2c1f0..."`
  - `null` if fetch failed

- **bytes_len** (number, required): Length of response body in bytes
  - Example: `12345`
  - `0` if fetch failed

- **raw_path** (string or null, required): Relative path to saved raw file
  - Example: `"data/raw/2026-01-22/IAU_MPC/index.html"`
  - `null` if fetch failed or file not saved

- **error** (string or null, required): Error message if fetch failed
  - Example: `"Connection timeout after 25s"`
  - `null` if successful

### Example

```json
{
  "snapshot_date": "2026-01-22",
  "generated_at": "2026-01-22T03:15:42.789Z",
  "source_count": 2,
  "fetch_results": [
    {
      "source_id": "IAU_MPC",
      "url": "https://www.minorplanetcenter.net/",
      "retrieved_utc": "2026-01-22T03:15:38.123Z",
      "ok": true,
      "status_code": 200,
      "content_type": "text/html; charset=UTF-8",
      "sha256": "a3f5d9e8b2c1f0e4d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5",
      "bytes_len": 45678,
      "raw_path": "data/raw/2026-01-22/IAU_MPC/index.html",
      "error": null
    },
    {
      "source_id": "NASA_JPL_SBDB",
      "url": "https://ssd.jpl.nasa.gov/sb/",
      "retrieved_utc": "2026-01-22T03:15:41.456Z",
      "ok": false,
      "status_code": null,
      "content_type": null,
      "sha256": null,
      "bytes_len": 0,
      "raw_path": null,
      "error": "Connection timeout after 25s"
    }
  ]
}
```

## Manifest Format

**File:** `data/manifests/manifest_YYYY-MM-DD.json`

**Purpose:** Metadata and integrity verification for snapshot files

### Schema

```json
{
  "manifest_version": "string",  // Manifest schema version
  "date": "YYYY-MM-DD",          // Snapshot date
  "generated_at": "ISO8601_UTC", // Generation timestamp
  "snapshot": {
    "path": "string",            // Relative path to snapshot
    "sha256": "string",          // SHA-256 of snapshot file
    "size_bytes": number         // File size in bytes
  }
}
```

### Field Specifications

#### Root Level

- **manifest_version** (string, required): Schema version for this manifest
  - Current version: `"1.0"`

- **date** (string, required): Date of the associated snapshot
  - Format: `YYYY-MM-DD`
  - Example: `"2026-01-22"`

- **generated_at** (string, required): Timestamp when manifest was created
  - Format: ISO 8601 UTC with 'Z' suffix
  - Example: `"2026-01-22T03:15:43.000Z"`

#### Snapshot Object

- **path** (string, required): Relative path to the snapshot file
  - Example: `"data/snapshots/snapshot_2026-01-22.json"`

- **sha256** (string, required): SHA-256 checksum of the snapshot file
  - 64 hexadecimal characters
  - Example: `"b4e6f8d2a1c3e5..."`

- **size_bytes** (number, required): Size of snapshot file in bytes
  - Example: `8192`

### Example

```json
{
  "manifest_version": "1.0",
  "date": "2026-01-22",
  "generated_at": "2026-01-22T03:15:43.123Z",
  "snapshot": {
    "path": "data/snapshots/snapshot_2026-01-22.json",
    "sha256": "b4e6f8d2a1c3e5d7f9a0b2c4e6f8d0a1b3c5e7f9a1b3c5e7f9a1b3c5e7f9a1b3",
    "size_bytes": 8192
  }
}
```

## Raw Data Files

**Location:** `data/raw/YYYY-MM-DD/SOURCE_ID/`

**Purpose:** Preserve original fetched content for archival and verification

### Naming Convention

Files are named based on URL structure:
- `index.html` - For root URLs
- `page.html` - For HTML pages
- `data.json` - For JSON endpoints
- Custom names based on URL path

### Structure

```
data/raw/
└── 2026-01-22/                    # Date directory
    ├── IAU_MPC/                   # Source ID directory
    │   └── index.html             # Raw fetched content
    ├── NASA_JPL_SBDB/
    │   └── index.html
    └── NASA_JPL_HORIZONS/
        └── index.html
```

### Content

- Exact byte-for-byte copy of HTTP response body
- No processing or transformation
- Binary or text content preserved as-is

## Checksum Verification

### Computing Checksums

All checksums use SHA-256:

```python
import hashlib

def compute_checksum(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()
```

### Verifying Snapshot Integrity

```bash
# Compare manifest checksum with actual snapshot
MANIFEST_SHA=$(cat data/manifests/manifest_2026-01-22.json | jq -r '.snapshot.sha256')
ACTUAL_SHA=$(sha256sum data/snapshots/snapshot_2026-01-22.json | awk '{print $1}')

if [ "$MANIFEST_SHA" = "$ACTUAL_SHA" ]; then
  echo "Integrity verified ✓"
else
  echo "Integrity check failed ✗"
fi
```

### Verifying Raw Content

```bash
# Compare snapshot checksum with actual raw file
SNAPSHOT_SHA=$(cat data/snapshots/snapshot_2026-01-22.json | jq -r '.fetch_results[0].sha256')
ACTUAL_SHA=$(sha256sum data/raw/2026-01-22/IAU_MPC/index.html | awk '{print $1}')

if [ "$SNAPSHOT_SHA" = "$ACTUAL_SHA" ]; then
  echo "Raw content verified ✓"
else
  echo "Raw content check failed ✗"
fi
```

## Timestamp Format

All timestamps follow ISO 8601 format in UTC timezone:

**Format:** `YYYY-MM-DDTHH:MM:SS.sssZ`

**Components:**
- `YYYY` - 4-digit year
- `MM` - 2-digit month (01-12)
- `DD` - 2-digit day (01-31)
- `T` - Time separator
- `HH` - 2-digit hour (00-23)
- `MM` - 2-digit minute (00-59)
- `SS` - 2-digit second (00-59)
- `sss` - Milliseconds (000-999)
- `Z` - UTC timezone indicator

**Example:** `2026-01-22T03:15:42.789Z`

## Encoding

All JSON files use UTF-8 encoding:
- **File encoding:** UTF-8 without BOM
- **JSON strings:** Unicode escaping for special characters
- **Line endings:** LF (Unix-style)
- **Indentation:** 2 spaces

## Compatibility

### JSON Schema Versions

Current schema versions:
- **Registry:** No explicit version (schema is stable)
- **Snapshot:** Implicit v1.0 (field set defines version)
- **Manifest:** Explicit `manifest_version: "1.0"`

### Forward Compatibility

New fields may be added in future versions without breaking existing parsers:
- Parsers should ignore unknown fields
- Required fields will never be removed
- Field types will never change

### Backward Compatibility

Older snapshots remain valid:
- Historical data maintains its original format
- New fields are additive only
- Checksums ensure data hasn't been modified

## Data Size Estimates

Typical file sizes:

| File Type | Size Range | Example |
|-----------|------------|---------|
| Registry | 1-5 KB | 2.5 KB |
| Snapshot | 5-50 KB | 15 KB |
| Manifest | 200-500 bytes | 350 bytes |
| Raw HTML | 10-500 KB | 45 KB |
| Raw JSON | 1-100 KB | 25 KB |

Daily storage accumulation: ~1-30 MB per day (all files combined)

## Related Documentation

- [User Guide](USER_GUIDE.md) - How to use the system
- [Script Reference](SCRIPT_REFERENCE.md) - Script documentation
- [Development Guide](DEVELOPMENT.md) - Contributing and development
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues
