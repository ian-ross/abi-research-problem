---
id: ABI-012
title: Report Dataset Source-stratified metrics
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:51'
labels:
  - evaluation
  - metrics
dependencies:
  - ABI-007
  - ABI-011
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend validation and evaluation reports so aggregate metrics cannot hide MIT-vs-Google performance differences.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Validation reports aggregate metrics plus MIT-specific metrics
- [x] #2 Validation reports Google-specific metrics
- [x] #3 Filtered and raw metrics are both source-stratified
- [x] #4 Per-sample records include Dataset Source and scene/time provenance
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Ensure evaluation datasets expose Dataset Source and scene/time provenance for each sample.
2. Extend validation aggregation to compute metrics globally and grouped by Dataset Source.
3. Include both raw and filtered metrics in each group once filtered assessment exists.
4. Include source/provenance fields in per-sample evaluation records and diagnostic artifacts.
5. Add tests where aggregate performance hides one-source failure and verify source metrics reveal it.
6. Document source-stratified metrics as acceptance-gate inputs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added validation metrics computed from validation dataset metadata so MIT/Google source-specific raw and filtered metrics are reported when present.
- Extended whole-validation evaluation aggregate metrics with source/{mit,google}/raw/* and source/{mit,google}/filtered/* metrics.
- Added per-sample Dataset Source plus scene/time provenance aliases to evaluation records.
- Updated provider brief to call out Dataset Source-stratified metrics as acceptance-gate inputs.
- Validation: uv run ruff check abi_contrail/adapters.py abi_contrail/evaluation.py tests/test_abi_training_adapter.py ../ml-autoresearch/src/ml_autoresearch/training.py; uv run pytest -q
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented Dataset Source-stratified validation and evaluation reporting. Validation now receives dataset metadata and emits MIT/Google raw and filtered metric groups when sources are present. Whole-validation evaluation aggregate metrics now include source/{mit,google}/raw/* and source/{mit,google}/filtered/*, and per-sample metrics include Dataset Source plus scene/time provenance aliases. Updated the provider brief to make source-stratified metrics explicit acceptance-gate inputs.

Tests:
- uv run ruff check abi_contrail/adapters.py abi_contrail/evaluation.py tests/test_abi_training_adapter.py ../ml-autoresearch/src/ml_autoresearch/training.py
- uv run pytest -q
<!-- SECTION:FINAL_SUMMARY:END -->
