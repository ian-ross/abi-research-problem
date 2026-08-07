---
id: ABI-017
title: Run MCAST baseline evaluations on GPU server
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 21:02'
updated_date: '2026-08-07 11:29'
labels:
  - baselines
  - evaluation
  - cluster
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Run the provider-owned MCAST detection 1.1 and 2.1 Baseline Segmenter evaluations on the GPU-enabled training server after ABI-013 implementation is merged. Record aggregate and per-sample baseline metrics as acceptance-gate comparison artifacts.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 MCAST 1.1 baseline evaluation is run with local detection-1.1.pt assets on the GPU server
- [ ] #2 MCAST 2.1 baseline evaluation is run with local detection-2.1 directory assets on the GPU server
- [ ] #3 Aggregate and per-sample raw/filtered metrics are stored for acceptance-gate comparison
- [ ] #4 Run configuration, asset paths or asset provenance, commit SHA, and validation split configuration are documented
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Validate configured MIT/Google data paths and local MCAST 1.1/2.1 assets
2. Smoke-load both checkpoints and run one GPU inference patch
3. Run both provider-owned baseline validation evaluations on the combined Working Validation Split
4. Verify aggregate, per-sample, threshold-sweep, diagnostics, and provenance artifacts
5. Record metrics, commands, paths, validation split configuration, and commit SHA
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Smoke-loaded MCAST 1.1 and 2.1 and ran one 256x256 patch through each on the A100 with CUDA 12.1/PyTorch 2.5.1.
- The first combined full evaluation was aborted at operator request after it saturated all CPU cores; it produced no metric artifacts.
- Added timestamped CLI/file progress logging and documented commands that hard-cap CPU affinity and numerical thread pools to 75% while exposing only the A100.
- Awaiting operator-run full evaluations; keep this task In Progress until both artifact sets are verified.
<!-- SECTION:NOTES:END -->
