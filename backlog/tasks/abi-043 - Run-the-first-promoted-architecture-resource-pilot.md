---
id: ABI-043
title: Run the first promoted architecture resource pilot
status: To Do
assignee: []
created_date: '2026-08-13 09:33'
labels:
  - autonomy
  - candidates
  - gpu
  - scout
  - reliability
dependencies:
  - ABI-039
  - ABI-042
priority: high
type: task
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Prepare, authorize, and execute the first post-ABI-039 real architecture-research Autonomy Step: exactly one new or materially different Candidate family followed by at most one trusted 32-record-per-Dataset-Source-and-Leakage-Safe-Split, one-epoch sequential resource pilot on pinned A100 GPU 0. Establish an explicit trusted mechanism for the reduced pilot budget, collect finite/resource/non-degeneracy evidence, and stop before any 12-epoch representative scout or promotion decision.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 One new or materially different Candidate architecture family and its resource-pilot hypothesis, controlled factors, success evidence, and stop conditions are preregistered
- [ ] #2 A trusted Harness or Workspace mechanism applies exactly 32 representative records per Dataset Source and Leakage-Safe Split and one epoch for this pilot; Candidate source and manifest cannot select, raise, or bypass the budget
- [ ] #3 Preflight verifies clean pushed ABI and Harness identities, validated runtime images, synchronized Agent Control Boundary authorization, available named data roots, no open action, no managed container, and idle pinned A100 GPU 0
- [ ] #4 Exactly one Autonomy Step is invoked with next-action execution enabled and it produces at most one Candidate Submission and one Harness-owned Candidate Run; no duplicate, replacement, retry-driven second Run, Experiment Batch, or Post-Run Evaluation is launched
- [ ] #5 The stable Run is observed and reconciled idempotently, with exactly-once lifecycle evidence and no unresolved action remaining
- [ ] #6 Trusted evidence records finite state, parameter count, throughput, wall-clock duration, peak GPU allocation/reservation, batch compatibility, source-stratified metrics, predicted-positive/non-degeneracy state, selected-record policy identity, and timeout headroom
- [ ] #7 The pilot is interpreted only as contract, resource, and finite/non-degeneracy evidence; it is not used to rank, promote, eliminate for low score alone, or authorize concurrency
- [ ] #8 A durable report, Experiment Index and Research Ledger updates, validation results, independent review, and residual risks are recorded before closeout
- [ ] #9 The task stops before a 12-epoch representative scout; continuation, 36-epoch extension, full-data training, promotion, and policy-limit changes require their applicable separate authorization
<!-- AC:END -->
