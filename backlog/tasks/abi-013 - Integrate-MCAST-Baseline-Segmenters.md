---
id: ABI-013
title: Integrate MCAST Baseline Segmenters
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 21:04'
labels:
  - baselines
  - evaluation
dependencies:
  - ABI-007
  - ABI-008
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Evaluate MCAST detection model versions 1.1 and 2.1 as provider-owned Baseline Segmenters against the same Contrail Mask and filtered assessment protocol.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 MCAST 1.1 checkpoint can be loaded offline without candidate code
- [x] #2 MCAST 2.1 checkpoint directory can be loaded offline without candidate code
- [x] #3 Baseline adapter returns class-1 probabilities and thresholded masks before MCAST operational postprocessing
- [x] #4 Artifact Filters are applied consistently to baseline and candidate predictions
- [x] #5 Baseline metrics are stored for later acceptance-gate comparison
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect current provider/evaluation extension points and MCAST loading semantics.
2. Add provider-owned MCAST baseline segmenter loaders for v1.1 file and v2.1 directory without invoking MCAST operational postprocessing.
3. Route baseline predictions through the existing raw/filtered evaluation metric path and persist baseline metrics artifacts for later comparison.
4. Add lightweight unit tests with fake models/assets; do not run real MCAST evaluations or training.
5. Create a follow-up backlog issue to run baseline evaluations on the GPU server if needed.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- MCAST source code path: /home/iross/work/mit/code/mcast. The planning-inputs/mcast symlink was removed because it interfered with editor/tooling traversal; use the absolute path when implementing this task.

- Started implementation; will not run real MCAST baseline evaluations on this machine.

- Added provider-owned MCAST baseline segmenter module for detection 1.1 file assets and detection 2.1 directory assets.
- Baseline forward path returns class-1 softmax probabilities and thresholded masks before MCAST operational postprocessing.
- Baseline validation evaluation reuses candidate raw/filtered metric aggregation and writes baseline artifacts when an evaluation_dir is supplied.
- Added optional baselines dependency group and fake-asset tests; did not run real baseline evaluations on this machine.
- Created follow-up ABI-017 to run MCAST baseline evaluations on the GPU server.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented provider-owned MCAST Baseline Segmenter support without running real MCAST evaluations locally.

Changes:
- Added MCAST 1.1 and 2.1 local asset loaders with offline SMP initialization, C11/C14/C13-C15 preprocessing, class-1 probability extraction, and thresholded masks before MCAST operational postprocessing.
- Added baseline declarations and a baseline validation evaluation hook that applies the same raw/filtered metric and Artifact Filter path as candidates and can persist aggregate/per-sample artifacts.
- Exposed provider-only raw ABI inputs for trusted baselines while keeping candidate inputs unchanged.
- Added optional baseline dependencies and lightweight fake-asset tests.
- Created ABI-017 to run the real baseline evaluations on the GPU server.

Validation:
- uv run pytest
<!-- SECTION:FINAL_SUMMARY:END -->
