---
id: ABI-022
title: Accelerate trusted ABI postprocessing and metrics on GPU
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-07 11:56'
updated_date: '2026-08-07 21:15'
labels:
  - evaluation
  - performance
  - gpu
  - filters
dependencies:
  - ABI-023
  - ABI-024
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the current per-sample CPU/NumPy postprocessing hot path with a bounded-batch accelerated provider implementation after the initial MCAST 1.1/2.1 baseline artifacts are available as parity targets. Preserve trusted Artifact Filter and metric semantics, artifact schemas, and the candidate/provider boundary.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A bounded-batch accelerated path uses CUDA when available for scanline filtering, clDice/connectivity, ordinary segmentation metrics, and threshold-sweep work without loading the full validation split into GPU memory
- [ ] #2 CPU fallback remains available and produces equivalent raw/filtered masks, metrics, diagnostics, and threshold artifacts within explicitly tested numerical tolerances
- [ ] #3 Parity is validated against tiny exact fixtures and the initial MCAST 1.1/2.1 baseline artifacts, including scanline standard-deviation boundary cases
- [ ] #4 Target skeleton work is not redundantly recomputed for raw and filtered clDice, and unavailable geographic filtering does not reread longitude/latitude source data
- [ ] #5 Configured geographic feature masks are cached or pre-rasterized outside the per-threshold hot loop while remaining provider-owned
- [ ] #6 Progress logs distinguish Artifact Filter, connectivity metric, ordinary metric, and threshold-sweep phases and report benchmark timings
- [ ] #7 Accelerated evaluation retains aggregate/per-sample raw and filtered metrics, diagnostics, provenance, and candidate boundary guarantees
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Capture the current CPU evaluator as the parity oracle: inventory aggregate/per-sample/threshold/diagnostic schemas, initial MCAST 1.1/2.1 outputs and timings, and add focused fixtures for filter hits, empty masks, NaN probabilities, source strata, and scanline stddev values below/at/above the configured boundary.
2. Introduce a trusted provider-owned bounded-batch postprocessing engine with explicit CPU and CUDA backends, configurable batch size/device selection, and no full-validation GPU residency; preserve the existing Artifact Filter pipeline and candidate/provider boundary.
3. Add a preparation/cache phase that obtains each sample filter context once, pre-rasterizes or caches provider-owned geographic feature masks outside operational and threshold loops, and discards longitude/latitude from the hot-loop representation so unavailable filtering never rereads source coordinates.
4. Implement batched geographic and contiguous-scanline filtering on torch tensors while preserving ordered filter semantics, diagnostics, removed-pixel/area accounting, and NumPy population-standard-deviation boundary behavior within documented tolerances.
5. Implement batched ordinary metric/confusion reducers and clDice/connectivity evaluation on CPU/CUDA, reusing each target skeleton for raw and filtered scores and retaining per-sample, aggregate, and Dataset Source-stratified metric keys.
6. Rework the 19-threshold diagnostic sweep to process bounded sample batches (and bounded threshold tiles if needed), reuse prepared geographic masks, accumulate raw/filtered counts without retaining full sweep tensors on GPU, and preserve the threshold_sweep.json schema and threshold-selection semantics.
7. Integrate the engine into candidate and MCAST baseline evaluation, add phase-specific progress/timing logs and persisted benchmark/backend provenance, and expose only trusted operator configuration such as postprocessing batch size while keeping CPU fallback automatic and available.
8. Add exact/tolerance parity tests for CPU versus CUDA (skipping CUDA only where unavailable), regression tests for context-read counts, geographic cache reuse, target-skeleton reuse, bounded transfers, progress phases, artifact schemas, and candidate exclusion of longitude/latitude; run focused and full uv-managed test suites.
9. Run bounded A100 benchmarks and accelerated MCAST 1.1/2.1 evaluations: compare scanline-only outputs against /data/iross/abi-ml-autoresearch/baselines/initial-20260807, then generate immutable geographic-enabled replacement artifacts per the ABI-023 handoff, record timings/provenance/parity results, and inspect filter-hit diagnostics before completing the task.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Initial parity targets are complete at /data/iross/abi-ml-autoresearch/baselines/initial-20260807. Each run has 3,088 samples (MIT 1,232; Google 1,856).
- MCAST 1.1 timing: inference 104.5s, per-sample metrics/filtering 1,653.5s, threshold sweep 1,177.1s, total about 57m22s.
- MCAST 2.1 timing: inference 113.4s, per-sample metrics/filtering 1,670.5s, threshold sweep 1,201.4s, total about 58m03s.
- Raw and filtered outputs are identical at the operational thresholds and all 19 sweep thresholds; no filter removed a pixel. GPU/CPU parity must therefore also use filter-hit fixtures and later ABI-023 geographic-enabled artifacts.
<!-- SECTION:NOTES:END -->
