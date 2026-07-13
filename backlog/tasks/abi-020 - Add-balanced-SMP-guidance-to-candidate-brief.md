---
id: ABI-020
title: Add balanced SMP guidance to candidate brief
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-13 11:40'
updated_date: '2026-07-13 12:01'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read the current provider brief and README sections that discuss candidate model design, baselines, learned channel mixers, losses, and acceptance gates.
2. Add a concise guidance paragraph that frames SMP-style encoder-decoder models as optional quick baselines/comparators only.
3. Explicitly state that existing UNet/MANet baselines and SMP families should not constrain the candidate search space.
4. Add balanced examples of contrail-specific opportunities beyond generic SMP models: thin-line continuity/connectivity, ABI spectral interactions/BTDs, source-transfer robustness, calibration/threshold behavior, and artifact-aware false-positive suppression.
5. Avoid adding runnable SMP code/templates in this task; if mentioning wrappers, label them as minimal comparator wrappers rather than recommended architectures.
6. Run documentation/provider-spec smoke checks or targeted tests that validate brief paths/metadata if available.
<!-- SECTION:PLAN:END -->
