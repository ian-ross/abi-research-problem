---
id: ABI-010
title: 'Add line, boundary, and centerline auxiliary targets'
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 17:12'
labels:
  - auxiliary-targets
  - harness
  - provider
dependencies:
  - ABI-009
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expose trusted auxiliary targets and optional auxiliary output heads for thin contrail supervision.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 line auxiliary target is available in the ABI spec
- [x] #2 boundary auxiliary target is available in the ABI spec
- [x] #3 centerline auxiliary target and centerline_logits output are available in the ABI spec
- [x] #4 Auxiliary target losses are trusted and manifest-declared
- [x] #5 Tests verify auxiliary target shapes match mask_logits shape
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reuse existing line and boundary target helpers where possible.
2. Add trusted centerline target derivation consistent with the clDice/centerline metric implementation.
3. Declare ABI auxiliary targets line, boundary, and centerline in the provider spec with matching auxiliary outputs.
4. Wire trusted auxiliary losses and manifest-declared weights through the training adapter.
5. Add tests for derived target shapes, values on simple masks, and output/target name validation.
6. Update agent-facing docs with allowed auxiliary heads and discourage arbitrary auxiliary objectives.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented ABI auxiliary targets line, boundary, and centerline with line_logits/boundary_logits/centerline_logits output mappings and [1, 256, 256] shapes.
- Added trusted auxiliary target derivation: line/boundary use ml-autoresearch segmentation helpers; centerline uses the same trusted skeletonization support used by clDice.
- Added compute_auxiliary_losses validation for target name, output name, loss name, output presence, shape matching, and trusted weighted_bce loss with manifest-declared weights.
- Updated provider brief with optional auxiliary head contract and no arbitrary auxiliary objectives guidance.
- Validation: uv run ruff check abi_contrail/adapters.py tests/test_provider_spec.py tests/test_abi_training_adapter.py; uv run pytest -q.
- Independent reviewer found no blockers.
<!-- SECTION:NOTES:END -->
