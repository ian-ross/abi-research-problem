---
id: ABI-001
title: Scaffold ABI contrail research problem provider
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:35'
labels:
  - provider
  - vertical-slice
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the package and workspace structure for the GOES ABI Contrail Segmentation research problem, following the GVCCS provider pattern while using this repository as the workspace root.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Provider package exposes a build_spec entry point loadable by ml-autoresearch
- [ ] #2 pyproject/package metadata supports installing the provider package
- [ ] #3 Research problem spec declares v0 ids, abi_16ch input, mask_logits output, bce_dice loss, and val/dice temporary metric
- [ ] #4 README or brief documents how to register/run the provider in the workspace
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect current repo structure and compare with ../gvccs-research-problem and ../ml-autoresearch provider interfaces.
2. Identify the package/build_spec entry point and metadata needed for installation.
3. Add the minimal provider scaffold and v0 ResearchProblemSpec fields required by the ACs.
4. Add README/brief registration instructions.
5. Validate with uv-based import/smoke checks and any available ml-autoresearch validation.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added abi_contrail provider package exposing abi_contrail.research_problem:build_spec.
- Declared v0 ResearchProblemSpec with abi_16ch input, mask_logits output, bce_dice loss, adamw optimizer, deterministic sampling policies, and val/dice primary metric.
- Added README registration instructions and provider smoke tests.
- Validated with uv run pytest tests -q and uv build.
<!-- SECTION:NOTES:END -->
