---
id: ABI-007
title: Add provider-owned artifact filters and harness-applied filtered assessment
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:15'
labels:
  - evaluation
  - harness
  - filters
dependencies:
  - ABI-004
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define the provider-side Artifact Filter API for predictions/probabilities and removed-pixel diagnostics.
2. Implement an initial Geographic Feature Filter using approved coastline/river ancillary data or a documented placeholder that fails loudly if data are unavailable.
3. Implement a Scanline Artifact Filter that identifies long approximately constant ABI-y positive structures.
4. Extend harness/provider evaluation integration so filters are applied uniformly to candidate and baseline predictions.
5. Report raw metrics, filtered metrics, and removed predicted-positive counts/area.
6. Add tests proving candidate code cannot provide or override filters.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Started task: assigned to @agent and moved to In Progress.
- Awaiting approval on implementation plan and ancillary data choice before coding.
<!-- SECTION:NOTES:END -->
