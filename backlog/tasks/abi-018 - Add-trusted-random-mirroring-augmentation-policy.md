---
id: ABI-018
title: Add trusted random mirroring augmentation policy
status: To Do
assignee: []
created_date: '2026-07-13 11:38'
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
- [ ] #1 ResearchProblemSpec exposes an allowlisted random_mirroring augmentation policy in addition to none
- [ ] #2 Training adapter applies random mirroring only when selected by the candidate manifest or resolved run configuration
- [ ] #3 Input tensors and Contrail Mask targets are flipped consistently for no-flip, horizontal, vertical, and both-axis cases
- [ ] #4 Unit tests cover deterministic/seeding behavior or injectable randomness so tiny fixtures verify all flip modes
- [ ] #5 Provider brief documents the policy as trusted/harness-owned and not candidate-owned data augmentation
<!-- AC:END -->
