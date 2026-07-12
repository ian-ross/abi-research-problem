---
id: ABI-011
title: Implement Source-Balanced Sampling policies
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 20:45'
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
- [x] #1 mit_only training policy samples only MIT ABI Patches
- [x] #2 google_only training policy samples only Google ABI Patches
- [x] #3 combined_source_balanced policy uses explicit Dataset Source mixture rather than raw counts
- [x] #4 Positive-patch bias is configurable and logged in data policy metadata
- [x] #5 Sampling policy is harness/provider-owned, not candidate-owned
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect existing provider/harness data modules, task dependencies ABI-003/ABI-004 outputs, and tests/fixtures for sampling hooks.
2. Identify the provider-owned interface where training sampling policies and data policy metadata should live.
3. Implement mit_only, google_only, and combined_source_balanced policies with configurable positive-patch bias and explicit source mixture weights.
4. Add deterministic fixture-based tests covering source filtering/balancing, positive-bias behavior, metadata logging, and candidate isolation.
5. Run targeted uv pytest checks and update task notes/acceptance criteria with results.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added ABI source-aware sampling policies: mit_only, google_only, combined_source_balanced.
- Added provider/harness-owned DataLoader hook in ml-autoresearch so ABI adapter can install weighted samplers.
- Added configurable positive_patch_preference and explicit source_mixture data policy metadata.
- Added tests for source-only filtering, explicit source mixture balancing, positive bias, provider-owned sampler, and candidate rejection of sampling-parameter overrides.
- Validation: uv run pytest -q (36 passed); uv run ruff check targeted files.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented provider/harness-owned Source-Balanced Sampling policies for ABI training. The ABI spec now declares mit_only, google_only, and combined_source_balanced; the ABI adapter computes source-normalized sampling weights with configurable positive_patch_preference and explicit source_mixture metadata; and ml-autoresearch delegates supported sampling policies to trusted Research Problem adapters before falling back to generic samplers. Candidate manifests can select allowlisted policies but cannot set sampling parameters such as source_mixture or positive_patch_preference.

Tests:
- uv run pytest -q
- uv run ruff check abi_contrail/adapters.py tests/test_abi_training_adapter.py tests/test_provider_spec.py tests/test_candidate_filter_boundary.py ../ml-autoresearch/src/ml_autoresearch/training.py
<!-- SECTION:FINAL_SUMMARY:END -->
