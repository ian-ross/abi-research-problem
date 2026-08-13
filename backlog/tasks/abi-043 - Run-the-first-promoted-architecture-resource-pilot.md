---
id: ABI-043
title: Run the first promoted architecture resource pilot
status: Done
assignee:
  - '@agent'
created_date: '2026-08-13 09:33'
updated_date: '2026-08-13 13:25'
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
- [x] #1 One new or materially different Candidate architecture family and its resource-pilot hypothesis, controlled factors, success evidence, and stop conditions are preregistered
- [x] #2 A trusted Harness or Workspace mechanism applies exactly 32 representative records per Dataset Source and Leakage-Safe Split and one epoch for this pilot; Candidate source and manifest cannot select, raise, or bypass the budget
- [x] #3 Preflight verifies clean pushed ABI and Harness identities, validated runtime images, synchronized Agent Control Boundary authorization, available named data roots, no open action, no managed container, and idle pinned A100 GPU 0
- [x] #4 Exactly one Autonomy Step is invoked with next-action execution enabled and it produces at most one Candidate Submission and one Harness-owned Candidate Run; no duplicate, replacement, retry-driven second Run, Experiment Batch, or Post-Run Evaluation is launched
- [x] #5 The stable Run is observed and reconciled idempotently, with exactly-once lifecycle evidence and no unresolved action remaining
- [x] #6 Trusted evidence records finite state, parameter count, throughput, wall-clock duration, peak GPU allocation/reservation, batch compatibility, source-stratified metrics, predicted-positive/non-degeneracy state, selected-record policy identity, and timeout headroom
- [x] #7 The pilot is interpreted only as contract, resource, and finite/non-degeneracy evidence; it is not used to rank, promote, eliminate for low score alone, or authorize concurrency
- [x] #8 A durable report, Experiment Index and Research Ledger updates, validation results, independent review, and residual risks are recorded before closeout
- [x] #9 The task stops before a 12-epoch representative scout; continuation, 36-epoch extension, full-data training, promotion, and policy-limit changes require their applicable separate authorization
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

- Invoked exactly one Autonomy Step with next-action execution. It created Candidate abi043_fullspectral_deeplabv3plus_resource_pilot_v1 and stable Run run_20260813_131515_ff53ab; no launch command was repeated.
- The one-epoch Run selected exactly 32 MIT/Google records in every train/validation split, completed at batch 4 with 12.37M parameters, 38.26 train samples/s, 14.79 validation samples/s, 463.7MB peak allocated, 528.5MB peak reserved, and zero retries.
- Finite audit passed for 516 JSON numeric values and 12,383,918 checkpoint values; source metrics and all four bounded masks were non-degenerate.
- Stable reconciliation, no-open-action, no-container, idle-GPU, exactly-once ledger, final boundary, and independent-review checks passed. No Evaluation, Batch, second Run, or scout was launched.
- The Agent preregistered random mirroring/LR 0.0003 before execution rather than the outer protocol intent of no augmentation/LR 0.001; independent review classified this as a comparison residual, not a resource-pilot blocker. No architecture ranking or continuation decision was made.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Executed and closed the first promoted architecture resource pilot. Preregistered a materially different full-spectral DeepLabV3+ ResNet-18 family, activated trusted Workspace caps of exactly 32 records per Dataset Source and Leakage-Safe Split and one epoch, and invoked exactly one Autonomy Step. Candidate abi043_fullspectral_deeplabv3plus_resource_pilot_v1 completed as stable Run run_20260813_131515_ff53ab on pinned A100 GPU 0 with one container attempt, zero retries, finite state/checkpoint, source-stratified non-degenerate predictions, and substantial resource/timeout headroom. Reconciled the stable Run idempotently, recorded the durable report/index/ledger and independent review, and verified no unresolved action, second Run, Evaluation, Batch, scout, promotion, or concurrency change.

Validation:
- uv run pytest -q: 133 passed
- Focused Harness policy/autonomy/boundary/reconciliation suite: 135 passed
- Static Candidate validation, trusted config/boundary reload, runtime-image and Docker CUDA validation: passed
- Exact-32 selection, finite JSON/checkpoint, bounded-mask, exactly-once ledger, open-action, container, and GPU audits: passed
- Independent fresh-context review: no substantive blocker

Residual risks:
- The Agent pre-run proposal used random mirroring and LR 0.0003 rather than the outer intended no-augmentation/LR 0.001 controls, so this is not a clean architecture-only comparison.
- One epoch and four bounded masks cannot support ranking, promotion, elimination, or broad non-degeneracy claims.
- Retry support remains structurally enabled although retry count was zero; measured batch-4 headroom does not authorize concurrency.
<!-- SECTION:FINAL_SUMMARY:END -->
