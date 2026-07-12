---
id: ABI-001
title: Scaffold ABI contrail research problem provider
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
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
