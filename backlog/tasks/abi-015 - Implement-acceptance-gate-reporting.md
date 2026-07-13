---
id: ABI-015
title: Implement acceptance-gate reporting
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-13 10:54'
labels:
  - evaluation
  - acceptance
dependencies:
  - ABI-008
  - ABI-009
  - ABI-012
  - ABI-013
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Turn the agreed acceptance shape into explicit reports comparing candidate runs with Baseline Segmenters while retaining human judgment for final promotion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Report compares candidates to best available Baseline Segmenter on aggregate filtered Dice or IoU
- [x] #2 Report flags filtered recall regressions beyond configured tolerance
- [x] #3 Report includes Contrail Connectivity Metric comparison
- [x] #4 Report flags Dataset Source-specific catastrophic failures
- [x] #5 Report flags excessive dependence on Artifact Filters
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing evaluation, baseline, and provider-spec surfaces to locate the acceptance-report API.
2. Add provider-owned acceptance-gate data structures/functions in abi_contrail.evaluation, consuming candidate and baseline aggregate/per-sample metrics rather than candidate code.
3. Select the best available Baseline Segmenter by configured primary aggregate metric (filtered Dice by default, IoU as supported fallback/config).
4. Emit report fields/flags for aggregate baseline comparison, filtered-recall tolerance regressions, Contrail Connectivity Metric comparison, Dataset Source-specific catastrophic failures, and Artifact Filter dependence.
5. Add synthetic-metric unit tests covering pass, recall regression, source failure, filter-dependence warning, and best-baseline selection.
6. Document/report that final promotion remains a human-reviewed decision; run uv-managed tests for the touched surface.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented provider-owned acceptance-gate report builder and adapter persistence hook.
- Added aggregate raw/filtered confusion counts so Artifact Filter dependence can be computed from normal aggregate metrics.
- Added synthetic report tests covering pass, IoU baseline selection, recall regression, source failure, and Artifact Filter dependence.
- Updated provider brief to state gate shape and human-reviewed promotion.
- Validation: uv run ruff check abi_contrail/evaluation.py tests/test_acceptance_gate_reporting.py tests/test_mcast_baseline_segmenters.py; uv run pytest -q
<!-- SECTION:NOTES:END -->
