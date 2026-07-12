---
id: ABI-013
title: Integrate MCAST Baseline Segmenters
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:54'
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
1. Implement a provider-owned Baseline Segmenter loader for MCAST detection-1.1.pt and detection-2.1 directories.
2. Avoid invoking full MCAST operational run_detection; extract class-1 probabilities and thresholded masks from model output before MCAST postprocessing.
3. Recreate required MCAST input features only inside the baseline adapter: C11, C14, and C13-C15.
4. Ensure offline loading works without network downloads, especially for SMP encoder initialization.
5. Evaluate baselines through the same raw/filtered metric path as candidates.
6. Store baseline metrics/artifacts so acceptance reports can compare candidates to the best available Baseline Segmenter.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- MCAST source code path: /home/iross/work/mit/code/mcast. The planning-inputs/mcast symlink was removed because it interfered with editor/tooling traversal; use the absolute path when implementing this task.
<!-- SECTION:NOTES:END -->
