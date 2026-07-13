---
id: ABI-015
title: Implement acceptance-gate reporting
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-13 10:45'
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
- [ ] #1 Report compares candidates to best available Baseline Segmenter on aggregate filtered Dice or IoU
- [ ] #2 Report flags filtered recall regressions beyond configured tolerance
- [ ] #3 Report includes Contrail Connectivity Metric comparison
- [ ] #4 Report flags Dataset Source-specific catastrophic failures
- [ ] #5 Report flags excessive dependence on Artifact Filters
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define an acceptance-report schema comparing a candidate run with the best available Baseline Segmenter.
2. Include aggregate filtered Dice/IoU, filtered recall tolerance, Contrail Connectivity Metric, source-stratified metrics, and Artifact Filter dependence.
3. Implement reporting as a harness/provider evaluation artifact rather than a candidate responsibility.
4. Treat numeric thresholds as configurable after baseline evaluation, but preserve the agreed gate shape.
5. Add tests using synthetic metrics for pass, recall-regression, source-failure, and filter-dependence warning cases.
6. Document that final promotion remains a human-reviewed decision informed by the report.
<!-- SECTION:PLAN:END -->
