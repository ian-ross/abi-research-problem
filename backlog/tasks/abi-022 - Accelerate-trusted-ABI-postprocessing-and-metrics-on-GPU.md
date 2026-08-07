---
id: ABI-022
title: Accelerate trusted ABI postprocessing and metrics on GPU
status: To Do
assignee: []
created_date: '2026-08-07 11:56'
labels:
  - evaluation
  - performance
  - gpu
  - filters
dependencies: []
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
