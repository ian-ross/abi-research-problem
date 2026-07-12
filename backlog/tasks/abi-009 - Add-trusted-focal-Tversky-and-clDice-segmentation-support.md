---
id: ABI-009
title: Add trusted focal-Tversky and clDice segmentation support
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:46'
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
- [x] #1 focal_tversky loss is implemented in trusted harness/problem-support code
- [x] #2 clDice or equivalent Contrail Connectivity Metric is implemented and tested
- [x] #3 bce_dice_cldice loss is implemented as a trusted allowlisted loss
- [x] #4 ABI provider spec allowlists bce_dice, focal_tversky, and bce_dice_cldice
- [x] #5 Capability-request path is documented for any future loss functions
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing ml_autoresearch.problem_support.segmentation helpers in ../ml-autoresearch and current ABI provider integration points.
2. Implement focal_tversky, clDice/Contrail Connectivity Metric, and bce_dice_cldice in trusted harness/problem-support code in ../ml-autoresearch, not candidate code.
3. Add/adjust tests in ../ml-autoresearch for focal Tversky, clDice connectivity behavior, composed loss, and empty-mask edge cases.
4. Update this repository only where the ABI provider spec/allowlist or documentation must reference the trusted losses exposed by ml-autoresearch.
5. Run targeted uv-managed tests and update ABI-009 acceptance criteria/final notes.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented trusted focal_tversky_loss, clDice/Contrail Connectivity Metric, cldice_loss, and bce_dice_cldice_loss in ../ml-autoresearch/src/ml_autoresearch/problem_support/segmentation.py.
- Added ml-autoresearch tests for thin-line loss behavior, clDice connected/broken line behavior, and empty-mask handling.
- Updated ABI provider to allowlist and dispatch bce_dice, focal_tversky, and bce_dice_cldice; added raw/filtered connectivity metrics to training/evaluation outputs.
- Documented future loss additions via Capability Request in ../ml-autoresearch/docs/candidate-experiment-contract.md and abi_contrail/brief/goes-abi-contrail-segmentation.md.
- Validation: uv run pytest tests/test_problem_support_library.py tests/test_research_problem_training_dispatch.py -q in ../ml-autoresearch; uv run pytest -q in abi-research-problem; ruff checks passed for touched files.
<!-- SECTION:NOTES:END -->
