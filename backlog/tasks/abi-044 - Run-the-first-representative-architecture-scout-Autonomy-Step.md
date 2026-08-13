---
id: ABI-044
title: Run the first representative architecture-scout Autonomy Step
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-13 13:36'
updated_date: '2026-08-13 14:45'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Re-baseline ABI-039, ABI-040, and ABI-043 artifacts plus the current ABI/../ml-autoresearch identities and operational state; inventory the promoted policy, pilot override, lifecycle baselines, and existing report/index/ledger evidence without launching work.
2. Draft durable one-step representative-scout authorization that restores trusted ceilings to at most 1,024 records per Dataset Source and Leakage-Safe Split and 12 epochs while retaining batch 4, 3,600-second timeout, four first_n predictions, 25M parameters, constant LR, disabled early stopping, concurrency one, and pinned A100 GPU 0. Explicitly authorize preregistered Agent choices for LR, trusted loss, augmentation, and all other allowlisted Candidate parameters, and encode the ABI-039 asymmetric interpretation and hard stop.
3. Implement the smallest trusted Workspace/Harness-only policy/configuration changes needed to replace the ABI-043 32-record/one-epoch pilot cap with the representative ceilings. Add focused no-bypass regressions proving Candidate source/manifests cannot alter trusted sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, concurrency, GPU, coordinate, sampling, data, loss/metric/filter, or lifecycle boundaries.
4. Validate focused and full ABI/Harness suites, generated Agent Control Boundary synchronization, runtime images, and authorization/config reload. Prepare the durable scout report and execution checklist, then obtain explicit human approval before the irreversible Autonomy Step/GPU launch.
5. Establish clean pushed ABI and Harness revisions and run preflight for named roots, validated images, synchronized authorization, no open action, no managed container, baseline Run/Evaluation/Batch counts, and idle pinned A100 GPU 0. Abort rather than weaken policy or retry around a failed preflight.
6. Invoke exactly one Autonomy Step with next-action execution enabled. Permit at most one primary handoff and one Harness-owned sequential Candidate Run; do not repeat the launch or create a replacement/retry-driven second Run, Evaluation, Batch, or second step.
7. Observe any stable Run and reconcile it idempotently. Collect exactly-once lifecycle, finite/resource, source-stratified, predicted-positive/non-degeneracy, selected-record-policy, trajectory, and timeout-headroom evidence, with no unresolved action. Apply only ABI-039 asymmetric scout conclusions and do not automatically extend.
8. Update the durable report, Experiment Index, Research Ledger, validation evidence, residual risks, and task metadata. Obtain independent fresh-context review, resolve blockers, verify the campaign stopped after this one step, and close only when every acceptance criterion is evidenced.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Re-baselined completed ABI-039/040/043 policy and lifecycle evidence; Harness remains clean at c346f07 and the ABI task-plan commit is one commit ahead of origin.
- Began read-only policy/enforcement/operations reconnaissance. No Autonomy Step, Candidate Run, Evaluation, Batch, or GPU work has been launched.

- Prepared and pushed durable ABI-044 authorization/index/brief/test changes at ABI 2483509; restored the ignored machine-local Workspace policy to 1,024 records/source/split and 12 epochs.
- Hardened and pushed Harness b2d8345 so autonomy-step requires the Runtime Image Validation Stamp; added stale-stamp and explicit-bypass regressions.
- Validation: ABI 135 passed; focused Harness 201 passed; full Harness 581 passed/2 skipped with the known unrelated GVCCS fake-allowlist failure. Rebuilt and validated runtime images for Harness fingerprint b8f7a78000a5354f and Workspace SHA cf417a0; generated pending-authorization boundary reload passed.
- No Autonomy Step, Candidate Run, Evaluation, Batch, or GPU training has launched. Explicit human execution approval is still required.
<!-- SECTION:NOTES:END -->
