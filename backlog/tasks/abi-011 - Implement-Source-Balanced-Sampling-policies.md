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
1. Define provider-owned training data policies: mit_only, google_only, and combined_source_balanced.
2. Implement source-aware sample pools using Dataset Source metadata from ABI-003.
3. Add configurable positive-patch preference without allowing candidate-owned samplers.
4. Ensure combined_source_balanced uses explicit source mixture weights rather than raw sample counts.
5. Record sampling policy, source mixture, and positive bias in data_policy_metadata and run artifacts.
6. Add deterministic tests for source proportions and positive-bias behavior on fixture sample indexes.
<!-- SECTION:PLAN:END -->
