---
id: ABI-044
title: Run the first representative architecture-scout Autonomy Step
status: To Do
assignee: []
created_date: '2026-08-13 13:36'
labels:
  - autonomy
  - candidates
  - gpu
  - scout
  - reliability
dependencies:
  - ABI-043
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Authorize, prepare, and execute exactly one genuine post-ABI-043 representative-scout Autonomy Step under the promoted ABI-039 envelope. Restore trusted Workspace execution from the 32-record/source/split, one-epoch pilot cap to at most 1,024 representative records per Dataset Source and Leakage-Safe Split and 12 epochs, then allow the Agent to choose one bounded research handoff and at most one Harness-owned sequential Candidate Run on pinned A100 GPU 0. Agent-selected learning rate, trusted loss, augmentation, and other allowlisted Candidate parameters are legitimate autonomous choices when preregistered before execution and enforced by trusted policy. Interpret the scout asymmetrically as feasibility/failure-screen evidence, stop after the single step, and do not authorize extension, full-data training, promotion, concurrency, or automatic follow-up.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A durable authorization defines exactly one representative-scout Autonomy Step, restores trusted ceilings of at most 1,024 representative records per Dataset Source and Leakage-Safe Split and 12 epochs, and retains batch size 4, 3,600-second timeout, four first_n predictions, 25M parameters, constant LR policy, disabled early stopping, concurrency one, and pinned A100 GPU 0
- [ ] #2 The authorization explicitly permits the Agent to preregister and choose Candidate learning rate, trusted loss, augmentation, and other allowlisted parameters within Harness/provider policy; these choices are not treated as protocol deviations merely because they differ from prior Candidates
- [ ] #3 Trusted Workspace/Harness enforcement prevents Candidate source or manifests from raising or bypassing sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, concurrency, GPU, coordinate, sampling, data, loss-definition, metric, Artifact Filter, or lifecycle boundaries
- [ ] #4 Preflight verifies clean pushed ABI and Harness identities, validated runtime images, synchronized Agent Control Boundary authorization, available named roots, no open action, no managed container, and idle pinned A100 GPU 0
- [ ] #5 Exactly one Autonomy Step is invoked with next-action execution enabled and produces at most one primary handoff and one Harness-owned Candidate Run; no duplicate, replacement, retry-driven second Run, Experiment Batch, Post-Run Evaluation, or second Autonomy Step is launched
- [ ] #6 Any stable Run is observed and reconciled idempotently with exactly-once lifecycle evidence, no unresolved action, and complete trusted finite, resource, source-stratified, predicted-positive/non-degeneracy, selected-record-policy, trajectory, and timeout-headroom evidence
- [ ] #7 Scout interpretation follows ABI-039 asymmetric decisions: hard failure, persistent collapse, clear optimization failure, or convincing plateau/divergence may support elimination, while low score alone does not; improving, source-balanced, novel, noisy, or ambiguous trajectories remain extension-eligible without being automatically extended
- [ ] #8 A durable report, Experiment Index and Research Ledger updates, validation results, independent review, and residual risks are recorded before closeout
- [ ] #9 The task stops after the single representative-scout step; a roughly 36-epoch extension, full-data training, promotion, concurrency, policy-limit changes, and any subsequent Autonomy Step require their applicable separate authorization
<!-- AC:END -->
