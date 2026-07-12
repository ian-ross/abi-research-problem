---
id: ABI-015
title: Implement acceptance-gate reporting
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - evaluation
  - acceptance
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Turn the agreed acceptance shape into explicit reports comparing candidate runs with Baseline Segmenters while retaining human judgment for final promotion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Report compares candidates to best available Baseline Segmenter on aggregate filtered Dice or IoU
- [ ] #2 Report flags filtered recall regressions beyond configured tolerance
- [ ] #3 Report includes Contrail Connectivity Metric comparison
- [ ] #4 Report flags Dataset Source-specific catastrophic failures
- [ ] #5 Report flags excessive dependence on Artifact Filters
<!-- AC:END -->
