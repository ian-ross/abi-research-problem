---
id: ABI-002
title: Implement minimal ABI Patch dataset loading
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - data
  - vertical-slice
dependencies: []
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
