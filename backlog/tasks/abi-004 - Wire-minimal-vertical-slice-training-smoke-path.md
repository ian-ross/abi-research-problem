---
id: ABI-004
title: Wire minimal vertical-slice training smoke path
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 15:50'
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

- Re-ran full suite with project torch dependency group: uv run --group torch pytest -q (15 passed). Torch version reported as 2.13.0+cu130.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented ABI vertical-slice training through ml-autoresearch. The provider now declares training capability with ABITrainingAdapter, validates fixture zarr roots, builds train/validation datasets, keeps bce_dice and val/dice in trusted adapter code, and supports prediction sample artifact rendering for 16-channel ABI inputs. Added tests covering adapter construction, provider loading, minimal abi_16ch -> mask_logits candidate smoke, and tiny fixture training artifacts.

Tests:
- uv run pytest -q (14 passed, 1 skipped: torch-dependent integration skipped in this project venv)
- PYTHONPATH=.:../ml-autoresearch/src:/home/iross/work/mit/projects/abi-research-problem/.venv/lib/python3.12/site-packages ../ml-autoresearch/.venv/bin/python -m pytest tests/test_abi_training_adapter.py::test_minimal_abi_candidate_smoke_and_tiny_training_run_produce_artifacts -q (1 passed; exercised torch-backed smoke/training via ml-autoresearch dev venv)
<!-- SECTION:FINAL_SUMMARY:END -->
