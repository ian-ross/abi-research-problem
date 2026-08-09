---
id: ABI-022
title: Accelerate trusted ABI postprocessing and metrics on GPU
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-07 11:56'
updated_date: '2026-08-09 13:37'
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
- [x] #1 A bounded-batch accelerated path uses CUDA when available for scanline filtering, clDice/connectivity, ordinary segmentation metrics, and threshold-sweep work without loading the full validation split into GPU memory
- [x] #2 CPU fallback remains available and produces equivalent raw/filtered masks, metrics, diagnostics, and threshold artifacts within explicitly tested numerical tolerances
- [x] #3 Parity is validated against tiny exact fixtures and the initial MCAST 1.1/2.1 baseline artifacts, including scanline standard-deviation boundary cases
- [x] #4 Target skeleton work is not redundantly recomputed for raw and filtered clDice, and unavailable geographic filtering does not reread longitude/latitude source data
- [x] #5 Configured geographic feature masks are cached or pre-rasterized outside the per-threshold hot loop while remaining provider-owned
- [x] #6 Progress logs distinguish Artifact Filter, connectivity metric, ordinary metric, and threshold-sweep phases and report benchmark timings
- [x] #7 Accelerated evaluation retains aggregate/per-sample raw and filtered metrics, diagnostics, provenance, and candidate boundary guarantees
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

- Implemented bounded torch CPU/CUDA postprocessing with batch size 8 and threshold tiles of 4; operational Artifact Filters, ordinary metrics, clDice/connectivity, and the 19-threshold sweep now use bounded device batches.
- Added one-time geographic context preparation, parsed Natural Earth geometry/bbox caching, per-phase timings/provenance, and target-skeleton reuse. Diagnosed an initial geographic preparation rate near 1 Patch/s as repeated parsing/scanning of 18.8 MB of GeoJSON per Patch; caching improved the completed runs to 31-35 Patches/s.
- Full validation: uv run --group torch pytest -q (88 passed); uv build --wheel; git diff --check.
- Completed geographic-enabled MCAST 1.1/2.1 artifacts at /data/iross/abi-ml-autoresearch/baselines/geographic-enabled-20260807-abi022-r2. Both have 3,088 samples, torch_cuda provenance, max device batch 8, active Natural Earth filtering, and selected filter-hit diagnostics.
- MCAST 1.1: inference 98.9s; context preparation 87.2s; GPU Artifact Filter 1.48s; ordinary metrics 0.73s; connectivity 4.88s; threshold sweep 4.54s; 35,586 geographic pixels removed across 545 Patches.
- MCAST 2.1: inference 119.5s; context preparation 98.3s; GPU Artifact Filter 1.39s; ordinary metrics 0.88s; connectivity 4.82s; threshold sweep 4.55s; 58,315 geographic pixels removed across 1,033 Patches.
- Accelerated raw parity against initial-20260807 is exact for both baselines: aggregate raw metrics, all per-sample raw counts/ordinary/connectivity metrics, and raw counts/metrics at all 19 thresholds have maximum absolute delta 0.0.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented bounded-batch trusted ABI postprocessing on torch CPU/CUDA. Added accelerated ordered Geographic and Scanline Artifact Filters, ordinary metrics, clDice/connectivity with target-skeleton reuse, and a tiled 19-threshold sweep while keeping full validation tensors off GPU. Geographic contexts and Natural Earth vectors are prepared/cached outside hot loops; phase timings, backend/batch bounds, and provenance are persisted without exposing longitude/latitude to candidates.

Generated and validated immutable geographic-enabled MCAST 1.1/2.1 artifacts at /data/iross/abi-ml-autoresearch/baselines/geographic-enabled-20260807-abi022-r2. Raw aggregate, per-sample, connectivity, and all 19 threshold outputs match initial-20260807 exactly (maximum delta 0.0); active filtering removed 35,586 and 58,315 geographic pixels. End-to-end runs fell from about 57-58 minutes to about 3m35s and 3m57s.

Validation:
- uv run --group torch pytest -q (88 passed)
- uv build --wheel
- git diff --check
- Full A100 MCAST 1.1/2.1 geographic-enabled evaluation and artifact inspection
- Exact parity comparison against /data/iross/abi-ml-autoresearch/baselines/initial-20260807
<!-- SECTION:FINAL_SUMMARY:END -->
