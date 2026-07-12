---
id: ABI-003
title: Add leakage-safe split and ABI Patch indexing
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:05'
labels:
  - data
  - splits
dependencies:
  - ABI-002
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create deterministic sample indexing for MIT and Google ABI Patches while enforcing Leakage-Safe Split rules.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Google train/validation provenance in scene names is respected
- [ ] #2 MIT patches are split by whole scene, never random patch
- [ ] #3 MIT full scenes are indexed as 256x256 windows without loading whole scenes per sample
- [ ] #4 Split metadata records Dataset Source, scene/time provenance, patch coordinates, and positivity
- [ ] #5 Tests prove no scene crosses train/validation for MIT
<!-- AC:END -->
