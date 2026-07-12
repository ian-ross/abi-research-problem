---
id: ABI-009
title: Add trusted focal-Tversky and clDice segmentation support
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:42'
labels:
  - loss
  - harness
  - metrics
dependencies:
  - ABI-004
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing ml_autoresearch.problem_support.segmentation helpers and choose where new trusted losses/metrics belong.
2. Implement focal_tversky loss with bounded, documented alpha/beta/gamma defaults appropriate for rare thin positives.
3. Implement trusted clDice/Contrail Connectivity Metric with tests on simple line masks, broken lines, and empty masks.
4. Implement bce_dice_cldice as a trusted composed loss.
5. Update the ABI provider loss allowlist to include bce_dice, focal_tversky, and bce_dice_cldice.
6. Document that future losses require capability requests and agent-control-boundary updates.
<!-- SECTION:PLAN:END -->
