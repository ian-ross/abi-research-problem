---
id: ABI-001
title: Scaffold ABI contrail research problem provider
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
1. Compare the current repository with ../gvccs-research-problem provider structure and ../ml-autoresearch ResearchProblemSpec requirements.
2. Choose the provider package name and build_spec target for GOES ABI Contrail Segmentation.
3. Add package scaffold: research_problem.py, adapters.py, datasets.py placeholders, profile/brief directories, and package metadata.
4. Declare a minimal v0 spec for the vertical slice: abi_16ch input, mask_logits output, bce_dice loss, adamw optimizer, sequential/deterministic sampling, and temporary val/dice primary metric.
5. Add minimal docs showing how the provider is registered/loaded from this workspace.
6. Validate by importing build_spec and checking ml-autoresearch provider validation if available.
<!-- SECTION:PLAN:END -->
