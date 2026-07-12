---
id: ABI-007
title: Add provider-owned artifact filters and harness-applied filtered assessment
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - evaluation
  - harness
  - filters
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the ADR decision that Geographic Feature Filter and Scanline Artifact Filter are domain-owned but applied consistently by the harness during model assessment.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 ABI provider exposes deterministic Artifact Filters for predicted masks/probabilities
- [ ] #2 Geographic Feature Filter removes coastline/river-like static features using approved ancillary data
- [ ] #3 Scanline Artifact Filter removes long approximately constant ABI-y artifacts
- [ ] #4 Harness evaluation reports raw and filtered metrics for all models
- [ ] #5 Evaluation records number and area of predicted-positive pixels removed by filters
- [ ] #6 Candidate code cannot define or override Artifact Filters
<!-- AC:END -->
