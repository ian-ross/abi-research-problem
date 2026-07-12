---
id: ABI-005
title: Add ABI input modes and channel selection policies
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
- [ ] #1 abi_16ch returns GOES ABI channels 1-16 only
- [ ] #2 abi_16ch_plus_sza returns GOES ABI channels 1-16 plus Solar Geometry Input
- [ ] #3 abi_thermal_10ch returns GOES ABI channels 7-16
- [ ] #4 Longitude and latitude are never exposed as candidate inputs
- [ ] #5 Tests verify channel counts and channel-index mappings
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
