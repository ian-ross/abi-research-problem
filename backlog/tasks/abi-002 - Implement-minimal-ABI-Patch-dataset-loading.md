---
id: ABI-002
title: Implement minimal ABI Patch dataset loading
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
- [ ] #1 MIT zarr arrays and Google zarr groups are opened through the correct layouts
- [ ] #2 Labels are collapsed to Contrail Mask with label != 0
- [ ] #3 Returned tensors are float32 channel-first inputs and [1,H,W] targets
- [ ] #4 Unit tests cover label values 0, 1, 2, 4, and 255 collapsing to binary masks
- [ ] #5 Dataset code can run against tiny local fixtures without full training data
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
