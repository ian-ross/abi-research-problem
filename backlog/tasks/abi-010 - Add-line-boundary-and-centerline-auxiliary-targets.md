---
id: ABI-010
title: 'Add line, boundary, and centerline auxiliary targets'
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
- [ ] #1 line auxiliary target is available in the ABI spec
- [ ] #2 boundary auxiliary target is available in the ABI spec
- [ ] #3 centerline auxiliary target and centerline_logits output are available in the ABI spec
- [ ] #4 Auxiliary target losses are trusted and manifest-declared
- [ ] #5 Tests verify auxiliary target shapes match mask_logits shape
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
