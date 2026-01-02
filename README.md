# AUTO-DZ-ACT-3I-ATLAS-DAILY

Daily automated monitor of officially activated international data sources
(MPC / NASA / JPL / ESA) for the interstellar object **3I/ATLAS**.

This repository produces **verifiable daily snapshots**, **cryptographic manifests**,
and **raw-source archives** in compliance with international scientific standards,
ensuring long-term traceability and reproducibility.

---

## Data Provenance and International Activation

As of **2025-12-19**, this repository operates in a fully **internationally activated**
scientific configuration.

All snapshots are generated exclusively from **authoritative and globally recognized
institutions** operating under the auspices of the **International Astronomical Union (IAU)**,
**NASA**, and the **European Space Agency (ESA)**.

### Official Primary Sources

- **IAU Minor Planet Center (MPC)**  
  Global clearinghouse for observations, designations, and orbits of minor planets and comets.

- **NASA/JPL Small-Body Database (SBDB)**  
  High-precision orbital solutions and physical parameters derived from MPC data.

- **NASA/JPL Horizons System**  
  Authoritative ephemerides (positions and velocities) for Solar System bodies.

- **ESA Near-Earth Object Coordination Centre (NEOCC)**  
  European monitoring, impact assessment, and coordination for small bodies.

- **NASA Center for Near-Earth Object Studies (CNEOS)**  
  Close-approach analysis and impact-risk monitoring (Scout, Sentry).

- **NASA Planetary Data System – Small Bodies Node (PDS)**  
  Archival mission and derived data for asteroids and comets.

The authoritative source registry is defined ---

## Snapshot Integrity and Scientific Policy

For each requested UTC day:

- Raw responses from each official source are retrieved and archived **without modification**
- Retrieval timestamps are recorded in UTC
- HTTP status, content type, byte length, and SHA-256 hashes are stored
- No scientific interpretation, filtering, or model fitting is applied

All historical snapshots were **fully rebuilt after official source activation**
to eliminate pre-activation artifacts and ensure scientific validity.
Raw source responses are collected and stored locally or archived externally.
The GitHub repository publishes normalized snapshots and cryptographic manifests.
---

## Repository Structure
data/
├─ snapshots/   # Daily normalized snapshot JSON files
├─ manifests/   # Cryptographic manifests (SHA-256 integrity)
└─ raw/         # Archived raw source responses (HTML / data)
registry/
└─ sources.json # Official international source registry
scripts/
└─ trizel_monitor.py
---

## Scientific Scope

This repository provides a **traceable, reproducible, and citation-ready**
record of official observational and reference data related to **3I/ATLAS**.

It is designed for:
- International scientific research
- Independent verification
- Long-term archival use
- DOI-based publication workflows

---
This repository constitutes the authoritative data layer for AUTO DZ ACT verification states. The TRIZEL Monitor is used solely as an automation tool and is not required for independent verification.

## License

This project is released under an open scientific data license.
Raw source data remain the property of their respective institutions.
