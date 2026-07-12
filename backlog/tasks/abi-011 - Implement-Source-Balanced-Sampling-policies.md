---
id: ABI-011
title: Implement Source-Balanced Sampling policies
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:39'
labels:
  - sampling
  - data
dependencies:
  - ABI-003
  - ABI-004
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add provider/harness sampling support for MIT-only, Google-only, and combined Source-Balanced Sampling with explicit positive-patch preference.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 mit_only training policy samples only MIT ABI Patches
- [ ] #2 google_only training policy samples only Google ABI Patches
- [ ] #3 combined_source_balanced policy uses explicit Dataset Source mixture rather than raw counts
- [ ] #4 Positive-patch bias is configurable and logged in data policy metadata
- [ ] #5 Sampling policy is harness/provider-owned, not candidate-owned
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing provider/harness data modules, task dependencies ABI-003/ABI-004 outputs, and tests/fixtures for sampling hooks.
2. Identify the provider-owned interface where training sampling policies and data policy metadata should live.
3. Implement mit_only, google_only, and combined_source_balanced policies with configurable positive-patch bias and explicit source mixture weights.
4. Add deterministic fixture-based tests covering source filtering/balancing, positive-bias behavior, metadata logging, and candidate isolation.
5. Run targeted uv pytest checks and update task notes/acceptance criteria with results.
<!-- SECTION:PLAN:END -->
