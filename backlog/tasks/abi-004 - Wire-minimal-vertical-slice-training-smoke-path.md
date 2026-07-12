---
id: ABI-004
title: Wire minimal vertical-slice training smoke path
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:05'
labels:
  - training
  - vertical-slice
dependencies:
  - ABI-001
  - ABI-002
  - ABI-003
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Connect the ABI provider adapter to ml-autoresearch training on tiny fixtures so a simple candidate can pass smoke and a minimal training run before advanced metrics are added.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Training adapter validates data root and builds train/validation datasets
- [ ] #2 A minimal candidate using abi_16ch and mask_logits passes harness smoke
- [ ] #3 A tiny fixture training run produces metrics and model artifacts
- [ ] #4 Temporary primary metric val/dice is reported until filtered metrics are available
<!-- AC:END -->
