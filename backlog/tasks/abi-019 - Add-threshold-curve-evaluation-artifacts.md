---
id: ABI-019
title: Add threshold-curve evaluation artifacts
status: To Do
assignee: []
created_date: '2026-07-13 11:38'
labels:
  - evaluation
  - metrics
  - artifacts
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add provider-owned validation/evaluation artifacts that summarize segmentation performance across prediction thresholds, drawing on the earlier training code's precision/recall and Dice threshold sweep utilities. These artifacts should complement existing raw/filtered aggregate metrics without changing the v0 primary checkpoint metric.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Evaluation computes precision/recall and Dice over an explicit threshold grid from candidate or baseline probability maps
- [ ] #2 Artifacts include raw and filtered threshold curves where Artifact Filter context is available
- [ ] #3 Artifacts report best threshold by filtered Dice and the threshold where precision and recall are approximately equal, when computable
- [ ] #4 Aggregate metrics and acceptance-gate behavior remain backward compatible; val/filtered_dice remains the primary metric
- [ ] #5 Unit tests cover empty-mask/no-positive edge cases, NaN handling, and artifact serialization on tiny fixtures
<!-- AC:END -->
