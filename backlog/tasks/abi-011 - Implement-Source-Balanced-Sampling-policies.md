---
id: ABI-011
title: Implement Source-Balanced Sampling policies
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - sampling
  - data
dependencies: []
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
