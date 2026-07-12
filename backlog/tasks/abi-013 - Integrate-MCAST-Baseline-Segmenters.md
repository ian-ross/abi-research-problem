---
id: ABI-013
title: Integrate MCAST Baseline Segmenters
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:57'
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
- [ ] #1 MCAST 1.1 checkpoint can be loaded offline without candidate code
- [ ] #2 MCAST 2.1 checkpoint directory can be loaded offline without candidate code
- [ ] #3 Baseline adapter returns class-1 probabilities and thresholded masks before MCAST operational postprocessing
- [ ] #4 Artifact Filters are applied consistently to baseline and candidate predictions
- [ ] #5 Baseline metrics are stored for later acceptance-gate comparison
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
<!-- SECTION:NOTES:END -->
