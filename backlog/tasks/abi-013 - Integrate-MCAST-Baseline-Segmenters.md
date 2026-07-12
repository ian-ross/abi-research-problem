---
id: ABI-013
title: Integrate MCAST Baseline Segmenters
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:05'
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
