---
id: ABI-008
title: Add filtered Dice as v0 primary metric
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - evaluation
  - harness
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Promote val/filtered_dice to the ABI v0 primary checkpoint metric once filtered assessment is available.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 ResearchProblemSpec primary_metric is val/filtered_dice
- [ ] #2 Best checkpoint selection uses val/filtered_dice
- [ ] #3 Filtered Dice, IoU, precision, and recall are reported
- [ ] #4 Raw metrics remain visible alongside filtered metrics
- [ ] #5 Tests cover best-epoch selection on filtered Dice
<!-- AC:END -->
