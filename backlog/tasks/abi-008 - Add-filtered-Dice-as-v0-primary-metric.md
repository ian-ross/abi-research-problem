---
id: ABI-008
title: Add filtered Dice as v0 primary metric
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:36'
labels:
  - evaluation
  - harness
dependencies:
  - ABI-007
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Build on ABI-007 filtered assessment outputs to expose val/filtered_dice in validation metrics.
2. Update the ABI ResearchProblemSpec primary_metric from temporary val/dice to val/filtered_dice.
3. Ensure best-epoch selection uses val/filtered_dice and preserves raw metrics in artifacts.
4. Add filtered IoU, precision, and recall to reported metrics.
5. Add tests with synthetic metric sequences proving the chosen best epoch follows filtered Dice.
6. Update brief/profile docs to reflect ADR-0003.
<!-- SECTION:PLAN:END -->
