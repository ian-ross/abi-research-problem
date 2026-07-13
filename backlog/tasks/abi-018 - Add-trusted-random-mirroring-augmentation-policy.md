---
id: ABI-018
title: Add trusted random mirroring augmentation policy
status: Done
assignee:
  - '@agent'
created_date: '2026-07-13 11:38'
updated_date: '2026-07-13 11:49'
labels:
  - training
  - augmentation
  - provider
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a provider/harness-owned random mirroring augmentation policy for ABI Patch training, based on the earlier contrail segmentation training practice of randomly applying no flip, horizontal flip, vertical flip, or both-axis flip. The policy should remain outside candidate code and preserve alignment between ABI inputs and Contrail Mask targets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ResearchProblemSpec exposes an allowlisted random_mirroring augmentation policy in addition to none
- [x] #2 Training adapter applies random mirroring only when selected by the candidate manifest or resolved run configuration
- [x] #3 Input tensors and Contrail Mask targets are flipped consistently for no-flip, horizontal, vertical, and both-axis cases
- [x] #4 Unit tests cover deterministic/seeding behavior or injectable randomness so tiny fixtures verify all flip modes
- [x] #5 Provider brief documents the policy as trusted/harness-owned and not candidate-owned data augmentation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect ABITrainingAdapter manifest/config resolution for augmentation policy handling and confirm how ml-autoresearch passes selected augmentation_policies.
2. Add a provider-owned random_mirroring policy constant and expose it through ResearchProblemSpec.augmentation_policies while keeping none available.
3. Implement the trusted flip transform at the training adapter boundary so inputs, mask targets, and any auxiliary targets remain spatially aligned; use injectable RNG or seeded torch/numpy randomness for testability.
4. Wire application so random mirroring runs only when the selected/resolved augmentation policy is random_mirroring; preserve current behavior for none and unsupported policies.
5. Add tiny-fixture/unit tests that force no flip, horizontal, vertical, and both-axis flips and verify channel-first inputs and [1,H,W] masks are transformed consistently.
6. Update the provider brief to document random_mirroring as trusted harness/provider augmentation, not candidate-owned data augmentation.
7. Run targeted uv pytest for adapter/spec/brief-related tests.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added provider-owned random_mirroring augmentation policy and spec allowlist exposure.
- Implemented trusted dataset wrapper that flips inputs and targets together for no/horizontal/vertical/both modes with injectable selector for tests.
- Updated provider brief and targeted tests.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented trusted random_mirroring augmentation for ABI training. ResearchProblemSpec now allowlists none and random_mirroring; ABITrainingAdapter wraps training datasets only when random_mirroring is selected. The wrapper applies a shared no/horizontal/vertical/both-axis flip to channel-first inputs, Contrail Mask targets, and tensor-like auxiliary sample values while preserving metadata passthrough. Updated the provider brief to document augmentation as harness/provider-owned and not candidate-owned.

Tests:
- uv run pytest tests/test_abi_training_adapter.py tests/test_provider_spec.py
- uv run ruff check abi_contrail/adapters.py tests/test_abi_training_adapter.py tests/test_provider_spec.py
<!-- SECTION:FINAL_SUMMARY:END -->
