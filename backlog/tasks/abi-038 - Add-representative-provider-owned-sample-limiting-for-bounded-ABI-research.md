---
id: ABI-038
title: Add representative provider-owned sample limiting for bounded ABI research
status: Done
assignee:
  - '@agent'
created_date: '2026-08-12 15:59'
updated_date: '2026-08-12 16:29'
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
- [x] #1 Capped MIT and Google train/validation records are selected reproducibly without relying on raw record-prefix order
- [x] #2 The trusted selection policy preserves Dataset Source and Leakage-Safe Split boundaries and defines representative scene/provenance and Contrail Mask-positive coverage
- [x] #3 Candidate code and manifests cannot implement, override, seed, or inspect the trusted record-selection mechanism beyond approved aggregate metadata
- [x] #4 Run metadata records the requested and effective caps, policy identity/version, seed, source/split counts, positive counts, and a stable selected-record identity digest
- [x] #5 Unit tests cover determinism, order-bias resistance, source/split isolation, positivity edge cases, cap behavior, and full-dataset behavior using tiny fixtures
- [x] #6 Durable provider and Agent-visible documentation explains the capped-sampling semantics and limitations without depending on planning-inputs or external training data
- [x] #7 No real model training is performed as part of implementation or validation
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented provider-owned hash-ranked, positivity-aware scene/provenance-spread record selection with fixed v1 policy/seed and order-independent identity digests.
- Replaced prefix truncation in ABITrainingAdapter and added per-source/per-split audit metadata propagated through final_metrics.json and run_metadata.json.
- Added tiny fixture coverage for determinism, order resistance, source/split isolation, positivity/cap edge cases, combined-source metadata, candidate boundary rejection, and full-data behavior.
- Updated provider brief, dataset-profile guidance, profile generator caveats, and provider policy metadata.
- Validation so far: uv run pytest -q (123 passed); focused ABI-038 tests (43 passed); relevant Harness metadata dispatch test passed. Full Harness dispatch file had 1 unrelated environment-sensitive failure because CUDA was selected where its test asserted CPU.

- Fixed explicit-empty ABIPatchIndex handling so an empty selected split cannot fall back to all backing-array records.
- Final ABI validation: uv run pytest -q -> 126 passed, 16 existing multiprocessing deprecation warnings.
- Relevant Harness validation: test_run_candidate_trains_through_generic_research_problem_provider passed; full dispatch file was 5 passed/1 unrelated CUDA-vs-CPU environment assertion failure.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented fixed provider-owned representative record selection for bounded ABI Runs. Capped membership is deterministic and raw-order independent, preserves Dataset Source and Leakage-Safe Split boundaries, allocates positive/negative coverage, and spreads over MIT scenes or Google provenance scene names. The adapter now records bounded aggregate audit metadata and stable selected-record identity digests through final_metrics.json and run_metadata.json without exposing record lists or coordinates. Added candidate-boundary, combined-source, empty-split, cap/full-data, determinism, and documentation/profile tests.

Tests:
- uv run pytest -q (126 passed)
- uv run pytest -q ../ml-autoresearch/tests/test_research_problem_training_dispatch.py::test_run_candidate_trains_through_generic_research_problem_provider (passed)
- uv run python -m compileall -q abi_contrail tests
- git diff --check

Validation note:
- The full Harness dispatch file produced 5 passes and one unrelated environment-sensitive failure because CUDA was available while that test asserts CPU. No real dataset training was performed; validation used tiny fixtures/smoke tests only.
<!-- SECTION:FINAL_SUMMARY:END -->
