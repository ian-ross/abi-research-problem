---
id: ABI-038
title: Add representative provider-owned sample limiting for bounded ABI research
status: To Do
assignee: []
created_date: '2026-08-12 15:59'
labels:
  - provider
  - data
  - sampling
  - tests
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace deterministic prefix truncation for capped ABI training and validation datasets with a reproducible trusted-provider sampling policy suitable for scientifically meaningful reduced-budget architecture comparisons. Preserve Leakage-Safe Split and Dataset Source boundaries, keep sampling outside Candidate ownership, and make the selected subset auditable. This task performs no real model training.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Capped MIT and Google train/validation records are selected reproducibly without relying on raw record-prefix order
- [ ] #2 The trusted selection policy preserves Dataset Source and Leakage-Safe Split boundaries and defines representative scene/provenance and Contrail Mask-positive coverage
- [ ] #3 Candidate code and manifests cannot implement, override, seed, or inspect the trusted record-selection mechanism beyond approved aggregate metadata
- [ ] #4 Run metadata records the requested and effective caps, policy identity/version, seed, source/split counts, positive counts, and a stable selected-record identity digest
- [ ] #5 Unit tests cover determinism, order-bias resistance, source/split isolation, positivity edge cases, cap behavior, and full-dataset behavior using tiny fixtures
- [ ] #6 Durable provider and Agent-visible documentation explains the capped-sampling semantics and limitations without depending on planning-inputs or external training data
- [ ] #7 No real model training is performed as part of implementation or validation
<!-- AC:END -->
