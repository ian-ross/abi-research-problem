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
1. Inspect ABI-007 outputs and current spec/checkpoint metric wiring.
2. Update ResearchProblemSpec and reporting to use val/filtered_dice as primary while keeping raw metrics visible.
3. Ensure filtered Dice, IoU, precision, and recall are emitted consistently.
4. Add/adjust tests for best-epoch selection on filtered Dice and run targeted uv pytest.
<!-- SECTION:PLAN:END -->
