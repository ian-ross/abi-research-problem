---
id: ABI-009
title: Add trusted focal-Tversky and clDice segmentation support
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
labels:
  - loss
  - harness
  - metrics
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend trusted segmentation support with losses and metrics needed for rare thin contrail structures, without allowing arbitrary candidate-defined losses.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 focal_tversky loss is implemented in trusted harness/problem-support code
- [ ] #2 clDice or equivalent Contrail Connectivity Metric is implemented and tested
- [ ] #3 bce_dice_cldice loss is implemented as a trusted allowlisted loss
- [ ] #4 ABI provider spec allowlists bce_dice, focal_tversky, and bce_dice_cldice
- [ ] #5 Capability-request path is documented for any future loss functions
<!-- AC:END -->
