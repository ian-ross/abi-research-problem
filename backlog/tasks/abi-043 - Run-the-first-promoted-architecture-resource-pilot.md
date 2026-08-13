---
id: ABI-043
title: Run the first promoted architecture resource pilot
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-13 09:33'
updated_date: '2026-08-13 13:10'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Re-baseline ABI-039/ABI-042 completion, inspect the promoted authorization, candidate families, autonomy-step workflow, Harness sampling controls, current git/Harness identities, and prior run/index/ledger state; do not launch training during preparation.
2. Select exactly one new or materially different Candidate architecture family and draft a preregistration covering the hypothesis, controlled factors, trusted 32-record-per-source-and-split one-epoch budget, success evidence, interpretation limits, and hard stop conditions.
3. Implement or configure the smallest trusted Harness/Workspace-only reduced-pilot mechanism needed to enforce exactly 32 representative records per Dataset Source and Leakage-Safe Split and one epoch, with focused no-bypass tests proving Candidate source/manifest cannot raise, select, or evade the budget.
4. Prepare the durable pilot authorization/report and obtain the required human approval before execution; preserve sequential execution, pinned A100 GPU 0, no retries or replacement Runs, and explicit prohibition on scouts, extensions, promotion, concurrency, or policy-limit changes.
5. Validate focused and relevant full ABI/Harness suites, runtime images, generated Agent Control Boundary, and synchronized authorization. Establish clean pushed ABI and Harness revisions without discarding unrelated work, then run operational preflight for named roots, idle GPU 0, Docker/container state, open actions, and run/evaluation/batch baselines.
6. Invoke exactly one Autonomy Step with next-action execution enabled. Observe without issuing duplicate/retry execution, reconcile the stable Run idempotently, and stop with no unresolved action.
7. Collect trusted lifecycle and resource evidence: finite state, parameter count, throughput, wall time, peak GPU allocation/reservation, batch compatibility, source-stratified metrics, prediction non-degeneracy, selected-record policy identity, and timeout headroom. Interpret it only as contract/resource/finite/non-degeneracy evidence.
8. Update the durable report, Experiment Index, Research Ledger, validation results, residual risks, and task metadata; obtain an independent fresh-context review, address blockers, verify no second Run or downstream evaluation/scout was launched, and close only when every acceptance criterion is evidenced.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Human approved the implementation/execution plan after confirming main was pushed.
- Preregistered full-spectral DeepLabV3+ ResNet-18 as the single materially different family and activated the machine-local trusted 32/source/split, one-epoch Workspace cap.
- Added an exact-32 provider fixture regression; ABI full suite passed (133), focused Harness policy/autonomy/reconciliation suite passed (135).
- Recorded the linked pilot report and campaign resume authorization; no Autonomy Step or Candidate Run has been launched yet.
<!-- SECTION:NOTES:END -->
