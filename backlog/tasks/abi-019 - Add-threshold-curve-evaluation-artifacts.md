---
id: ABI-019
title: Add threshold-curve evaluation artifacts
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-13 11:38'
updated_date: '2026-07-13 11:53'
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
- [x] #1 Evaluation computes precision/recall and Dice over an explicit threshold grid from candidate or baseline probability maps
- [x] #2 Artifacts include raw and filtered threshold curves where Artifact Filter context is available
- [x] #3 Artifacts report best threshold by filtered Dice and the threshold where precision and recall are approximately equal, when computable
- [x] #4 Aggregate metrics and acceptance-gate behavior remain backward compatible; val/filtered_dice remains the primary metric
- [x] #5 Unit tests cover empty-mask/no-positive edge cases, NaN handling, and artifact serialization on tiny fixtures
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing ABI evaluation flow, baseline evaluation artifact writing, raw/filtered metric aggregation, and acceptance-gate inputs.
2. Define a provider-owned threshold grid and small threshold-curve data structure that accumulates TP/FP/FN/intersection/union from probability maps without altering primary aggregate metrics.
3. Implement raw threshold curves for candidate and baseline probability outputs; add filtered curves where Artifact Filter context is available by applying the same provider-owned filtering path before metric accumulation.
4. Compute serialized summaries including per-threshold precision, recall, Dice, best threshold by filtered Dice when present, raw fallback best threshold if needed, and approximate equal precision-recall threshold when computable.
5. Persist artifacts in the evaluation output directory alongside existing aggregate/per-sample metrics without changing val/filtered_dice selection or acceptance-gate behavior.
6. Add unit tests with tiny masks/probability maps covering normal positives, empty/no-positive masks, all-background predictions, NaN-safe precision/recall behavior, filtered-vs-raw serialization, and backward-compatible aggregate metrics.
7. Run targeted uv pytest for evaluation, baseline segmenter, acceptance-gate, and any artifact tests touched.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented provider-owned threshold curve artifact in ABI evaluation with explicit 0.05..0.95 threshold grid.
- Added raw and Artifact Filtered curve records with precision/recall/Dice and confusion counts.
- Added best-threshold and approximate equal precision-recall summaries; NaN probabilities are treated as non-positive predictions.
- Added tiny-fixture unit tests for filtering, empty/no-positive masks, NaN handling, JSON serialization, and aggregate metric compatibility.
- Validation: uv run pytest; uv run ruff check abi_contrail/evaluation.py tests/test_threshold_curve_artifacts.py
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented threshold-curve evaluation artifacts for ABI candidate and baseline evaluation paths. The returned/written threshold_sweep artifact now includes raw and filtered curves over an explicit 0.05..0.95 grid, confusion counts, precision/recall/Dice metrics, best thresholds, and approximate precision-recall balance thresholds while leaving aggregate metrics and filtered/dice acceptance behavior unchanged.

Tests:
- uv run pytest
- uv run ruff check abi_contrail/evaluation.py tests/test_threshold_curve_artifacts.py
<!-- SECTION:FINAL_SUMMARY:END -->
