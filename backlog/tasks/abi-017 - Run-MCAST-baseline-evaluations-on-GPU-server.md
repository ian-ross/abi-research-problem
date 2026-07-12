---
id: ABI-017
title: Run MCAST baseline evaluations on GPU server
status: To Do
assignee: []
created_date: '2026-07-12 21:02'
labels:
  - baselines
  - evaluation
  - cluster
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Run the provider-owned MCAST detection 1.1 and 2.1 Baseline Segmenter evaluations on the GPU-enabled training server after ABI-013 implementation is merged. Record aggregate and per-sample baseline metrics as acceptance-gate comparison artifacts.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 MCAST 1.1 baseline evaluation is run with local detection-1.1.pt assets on the GPU server
- [ ] #2 MCAST 2.1 baseline evaluation is run with local detection-2.1 directory assets on the GPU server
- [ ] #3 Aggregate and per-sample raw/filtered metrics are stored for acceptance-gate comparison
- [ ] #4 Run configuration, asset paths or asset provenance, commit SHA, and validation split configuration are documented
<!-- AC:END -->
