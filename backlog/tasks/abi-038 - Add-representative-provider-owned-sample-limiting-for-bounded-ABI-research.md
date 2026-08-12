---
id: ABI-038
title: Add representative provider-owned sample limiting for bounded ABI research
status: To Do
assignee: []
created_date: '2026-08-12 15:59'
updated_date: '2026-08-12 16:01'
labels:
  - provider
  - data
  - sampling
  - tests
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace deterministic prefix truncation for capped ABI training and validation datasets with a reproducible trusted-provider sampling policy suitable for scientifically meaningful reduced-budget architecture comparisons. Preserve Leakage-Safe Split and Dataset Source boundaries, keep sampling outside Candidate ownership, and make the selected subset auditable. This task performs no real model training.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Capped MIT and Google train/validation records are selected reproducibly without relying on raw record-prefix order
- [ ] #2 The trusted selection policy preserves Dataset Source and Leakage-Safe Split boundaries and defines representative scene/provenance and Contrail Mask-positive coverage
- [ ] #3 Candidate code and manifests cannot implement, override, seed, or inspect the trusted record-selection mechanism beyond approved aggregate metadata
- [ ] #4 Run metadata records the requested and effective caps, policy identity/version, seed, source/split counts, positive counts, and a stable selected-record identity digest
- [ ] #5 Unit tests cover determinism, order-bias resistance, source/split isolation, positivity edge cases, cap behavior, and full-dataset behavior using tiny fixtures
- [ ] #6 Durable provider and Agent-visible documentation explains the capped-sampling semantics and limitations without depending on planning-inputs or external training data
- [ ] #7 No real model training is performed as part of implementation or validation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Baseline the current provider/Harness seam: trace ABI Patch index construction, `_limit_records`, combined Dataset Source assembly, `data_policy_metadata` persistence, and existing profile digest helpers; add characterization tests proving the current capped path is prefix-order dependent.
2. Define the versioned trusted selection contract before coding: stable record identity fields, fixed provider-owned seed/version, per-source and per-split cap semantics, uncapped/full-dataset behavior, positivity quota rules, MIT scene-spread and Google provenance-spread rules, deterministic tie-breaking, and safe behavior when a stratum is smaller than its quota. Present this design for approval before implementation.
3. Add tiny fixture tests for the approved contract: repeatability, invariance to input record ordering, different stable identities, positive/negative representation when available, scene/provenance spread, MIT/Google and train/validation isolation, cap larger than population, cap of one, empty/minority strata, and unchanged all-record membership when uncapped.
4. Implement a pure provider-owned selector and canonical record-identity/digest helpers in the ABI provider package. Rank/select only from trusted `ABIPatchIndexRecord` metadata; do not expose a Candidate-controlled seed, selector, or record list. Preserve deterministic output ordering separately from deterministic membership selection.
5. Replace `_limit_records` in `ABITrainingAdapter.build_datasets` with the selector after Leakage-Safe Split indexes are built and before Torch dataset wrapping. Apply the requested cap independently to each Dataset Source and split, while retaining existing provider-owned Source-Balanced Sampling for epoch sampling.
6. Emit bounded auditable metadata for every source/split: requested/effective cap, available/selected counts, positive/negative counts, distinct scene/provenance counts, policy name/version, seed identity, and stable selected-record digest. Ensure combined datasets retain per-source metadata rather than flattening it away.
7. Trace the metadata through the generic Harness training path. If current `final_metrics.json` data-policy persistence is insufficient for Run-level auditability, add the smallest backward-compatible trusted Harness artifact/run-metadata integration and focused Harness tests; never include coordinates, raw samples, or an unrestricted selected-record list.
8. Add boundary/contract tests proving Candidate manifests and source cannot set or override selector policy or seed, and verify existing longitude/latitude exclusion, data ownership, sampling ownership, and full-data behavior remain unchanged.
9. Update the Research Problem Brief, dataset-profile guidance, and generated Agent-facing guidance with the capped-selection semantics, reproducibility guarantees, distinctions from epoch sampling, and known limitations. Keep durable context out of `planning-inputs/`.
10. Validate with focused ABI provider/training tests, any affected Harness dispatch/artifact tests, then `uv run pytest -q` in ABI and the relevant `uv run pytest ...` Harness suites. Run only tiny fixtures and static/boundary smoke checks; perform no real model training. Record evidence, residual risks, acceptance checks, and final summary in ABI-038.
<!-- SECTION:PLAN:END -->
