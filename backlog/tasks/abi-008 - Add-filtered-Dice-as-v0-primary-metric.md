---
id: ABI-008
title: Add filtered Dice as v0 primary metric
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:39'
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
- [x] #1 ResearchProblemSpec primary_metric is val/filtered_dice
- [x] #2 Best checkpoint selection uses val/filtered_dice
- [x] #3 Filtered Dice, IoU, precision, and recall are reported
- [x] #4 Raw metrics remain visible alongside filtered metrics
- [x] #5 Tests cover best-epoch selection on filtered Dice
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect ABI-007 outputs and current spec/checkpoint metric wiring.
2. Update ResearchProblemSpec and reporting to use val/filtered_dice as primary while keeping raw metrics visible.
3. Ensure filtered Dice, IoU, precision, and recall are emitted consistently.
4. Add/adjust tests for best-epoch selection on filtered Dice and run targeted uv pytest.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Set ResearchProblemSpec.primary_metric and ABITrainingAdapter.selection_policy to val/filtered_dice.
- Validation now emits val/raw_* and val/filtered_* Dice, IoU, precision, and recall while preserving val/dice aliases for raw metrics.
- Added filtered-Dice best-epoch selection coverage and smoke assertions for filtered/raw metric visibility.
- Validation: uv run pytest -q (28 passed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Promoted ABI v0 checkpoint selection to val/filtered_dice. Training validation now reports raw and filtered Dice/IoU/precision/recall, with raw val/dice aliases kept visible for compatibility, and the provider brief reflects ADR-0003. Added tests proving best-epoch selection follows filtered Dice and smoke training/evaluation artifacts expose raw and filtered metrics.

Tests:
- uv run pytest -q (28 passed)
<!-- SECTION:FINAL_SUMMARY:END -->
