---
id: ABI-005
title: Add ABI input modes and channel selection policies
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 15:56'
labels:
  - inputs
  - provider
dependencies:
  - ABI-004
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expose the agreed candidate input modes through provider-owned channel selection rather than candidate-owned data slicing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 abi_16ch returns GOES ABI channels 1-16 only
- [x] #2 abi_16ch_plus_sza returns GOES ABI channels 1-16 plus Solar Geometry Input
- [x] #3 abi_thermal_10ch returns GOES ABI channels 7-16
- [x] #4 Longitude and latitude are never exposed as candidate inputs
- [x] #5 Tests verify channel counts and channel-index mappings
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Centralize channel selection in the ABI provider/dataset adapter, not in candidate code.
2. Implement abi_16ch as GOES ABI channels 1-16, excluding longitude/latitude/SZA.
3. Implement abi_16ch_plus_sza as channels 1-16 plus Solar Geometry Input.
4. Implement abi_thermal_10ch as GOES ABI channels 7-16.
5. Ensure longitude and latitude are impossible to expose through declared input modes.
6. Add tests for input shapes and exact zero-based channel mappings.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added provider-owned ABI input mode source-index map: abi_16ch, abi_16ch_plus_sza, abi_thermal_10ch.
- Dataset adapter now selects channels by resolved manifest input_mode and rejects longitude/latitude exposure.
- Updated provider spec and brief with mode shapes and source-index mappings.
- Added tests for exact mappings, dataset channel counts, and training adapter manifest-driven channel selection.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented provider-owned ABI input modes and channel selection policies. The dataset boundary now maps declared modes to exact source indices, keeps longitude/latitude out of every mode, and the training adapter uses the resolved manifest input_mode when building datasets. The provider spec and brief now advertise abi_16ch, abi_16ch_plus_sza, and abi_thermal_10ch with shapes and source mappings.

Tests:
- uv run pytest -q (18 passed)
<!-- SECTION:FINAL_SUMMARY:END -->
