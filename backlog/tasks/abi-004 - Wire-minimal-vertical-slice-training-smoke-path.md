---
id: ABI-004
title: Wire minimal vertical-slice training smoke path
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 15:35'
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
- [x] #1 Training adapter validates data root and builds train/validation datasets
- [x] #2 A minimal candidate using abi_16ch and mask_logits passes harness smoke
- [x] #3 A tiny fixture training run produces metrics and model artifacts
- [x] #4 Temporary primary metric val/dice is reported until filtered metrics are available
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Wire the ABI training adapter to validate a fixture data root and build train/validation datasets from ABI-002/ABI-003.
2. Add or adapt a minimal candidate model using abi_16ch -> mask_logits for smoke testing.
3. Run harness candidate smoke against the provider spec.
4. Run a tiny fixture training job with bce_dice and temporary val/dice selection.
5. Verify expected artifacts are produced: metrics.jsonl, final/best metrics, and model checkpoint.
6. Document remaining temporary limitations before filtered metrics and advanced losses land.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added ABITrainingAdapter with data root/zarr validation, Google/MIT split-index dataset construction, trusted bce_dice loss and val/dice selection policy.
- Added torch tuple wrapper and ABI RGB diagnostic renderer for prediction sample artifacts.
- Added vertical-slice tests for adapter dataset construction, provider training capability, candidate smoke, and tiny fixture training artifacts.
<!-- SECTION:NOTES:END -->
