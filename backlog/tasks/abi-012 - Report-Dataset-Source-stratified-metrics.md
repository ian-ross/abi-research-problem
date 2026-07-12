---
id: ABI-012
title: Report Dataset Source-stratified metrics
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:46'
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
- [ ] #1 Validation reports aggregate metrics plus MIT-specific metrics
- [ ] #2 Validation reports Google-specific metrics
- [ ] #3 Filtered and raw metrics are both source-stratified
- [ ] #4 Per-sample records include Dataset Source and scene/time provenance
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
