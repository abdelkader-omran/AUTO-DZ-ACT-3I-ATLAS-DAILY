# Governance Reference

This repository operates under the TRIZEL Cross-Repository Governance framework.

Governance is defined, versioned, and maintained exclusively in the canonical source below.
No local governance interpretation or modification is permitted.

## Canonical Source

**Layer-0 Governance Repository:** [trizel-core](https://github.com/abdelkader-omran/trizel-core)  
**Governance Documentation:** `trizel-core/docs/governance/CROSS_REPO_GOVERNANCE.md`

## Governance Linkage Status

**✅ Layer-2 → Layer-0 Linkage: COMPLETED**

- Date Achieved: 2026-01-17
- PR #13: Merged
- Validation Check: `Layer-0 Gate / Verify Layer-0 reference` - Passing
- Proof Document: `docs/GOVERNANCE_PROOF_LAYER2_TO_LAYER0.md`

This repository now correctly references its Layer-0 governance root of truth without enforcing Layer-0 validation on Layer-2 execution logic.

## Validation

The Layer-0 governance reference is automatically validated on every pull request via the `layer0-gate.yml` workflow. This ensures the governance linkage remains intact and properly documented.
