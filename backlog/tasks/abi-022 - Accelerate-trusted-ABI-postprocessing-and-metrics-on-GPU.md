---
id: ABI-022
title: Accelerate trusted ABI postprocessing and metrics on GPU
status: To Do
assignee: []
created_date: '2026-08-07 11:56'
updated_date: '2026-08-07 14:16'
labels:
  - evaluation
  - performance
  - gpu
  - filters
dependencies:
  - ABI-023
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Initial parity targets are complete at /data/iross/abi-ml-autoresearch/baselines/initial-20260807. Each run has 3,088 samples (MIT 1,232; Google 1,856).
- MCAST 1.1 timing: inference 104.5s, per-sample metrics/filtering 1,653.5s, threshold sweep 1,177.1s, total about 57m22s.
- MCAST 2.1 timing: inference 113.4s, per-sample metrics/filtering 1,670.5s, threshold sweep 1,201.4s, total about 58m03s.
- Raw and filtered outputs are identical at the operational thresholds and all 19 sweep thresholds; no filter removed a pixel. GPU/CPU parity must therefore also use filter-hit fixtures and later ABI-023 geographic-enabled artifacts.
<!-- SECTION:NOTES:END -->
