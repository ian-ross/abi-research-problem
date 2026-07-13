---
id: ABI-020
title: Add balanced SMP guidance to candidate brief
status: To Do
assignee: []
created_date: '2026-07-13 11:40'
labels:
  - documentation
  - candidates
  - brief
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add light, non-prescriptive guidance to the ABI research brief that positions SMP-style encoder-decoder models as acceptable baseline-compatible reference paths without steering agents exclusively toward SMP. The guidance should encourage broader exploration of contrail-specific approaches such as thin-structure continuity, ABI spectral-channel interactions, source transfer robustness, and artifact-aware false-positive suppression.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Provider brief mentions SMP-style architectures only as optional quick baselines/comparators, not preferred solutions
- [ ] #2 Guidance explicitly states existing UNet/MANet baselines should not constrain candidate search space
- [ ] #3 Guidance highlights contrail-specific opportunities beyond generic SMP segmentation models
- [ ] #4 No runnable SMP template is added unless clearly labeled as a minimal wrapper example rather than recommended architecture
<!-- AC:END -->
