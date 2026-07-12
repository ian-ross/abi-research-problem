---
id: ABI-002
title: Implement minimal ABI Patch dataset loading
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:50'
labels:
  - data
  - vertical-slice
dependencies:
  - ABI-001
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement trusted dataset code for ABI Patch samples from zarr/parquet inputs, enough for the first vertical slice using abi_16ch and binary Contrail Mask targets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 MIT zarr arrays and Google zarr groups are opened through the correct layouts
- [x] #2 Labels are collapsed to Contrail Mask with label != 0
- [x] #3 Returned tensors are float32 channel-first inputs and [1,H,W] targets
- [x] #4 Unit tests cover label values 0, 1, 2, 4, and 255 collapsing to binary masks
- [x] #5 Dataset code can run against tiny local fixtures without full training data
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect real zarr layouts and create tiny fixture datasets for both MIT-style top-level arrays and Google-style grouped arrays.
2. Implement dataset opening functions that hide the MIT/Google zarr layout difference.
3. Implement Contrail Mask collapse as label != 0 and enforce float32 [1,H,W] targets.
4. Implement ABI Patch tensor conversion from channel-last arrays to channel-first torch tensors.
5. Add unit tests for shape, dtype, and bit-plane collapse values 0,1,2,4,255.
6. Keep fixture tests independent of the large linked data directory.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented trusted ABI Patch dataset loading with explicit MIT top-level array and Google grouped-array zarr openers.
- Added binary Contrail Mask collapse via labels != 0 and float32 channel-first abi_16ch conversion.
- Added tiny local zarr fixture tests independent of the data symlink.
- Validation: uv run pytest -q
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented minimal trusted ABI Patch dataset loading in abi_contrail/datasets.py. Added explicit MIT zarr top-level array and Google grouped-array openers, provider-owned abi_16ch channel selection, channel-first float32 inputs, and binary float32 [1,H,W] Contrail Mask collapse with labels != 0. Added unit tests with tiny generated zarr fixtures for both layouts and label values 0,1,2,4,255.

Tests:
- uv run pytest -q
<!-- SECTION:FINAL_SUMMARY:END -->
