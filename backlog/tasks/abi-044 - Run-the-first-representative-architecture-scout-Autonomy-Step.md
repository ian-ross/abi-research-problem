---
id: ABI-044
title: Run the first representative architecture-scout Autonomy Step
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-13 13:36'
updated_date: '2026-08-13 15:30'
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
- [x] #1 A durable authorization defines exactly one representative-scout Autonomy Step, restores trusted ceilings of at most 1,024 representative records per Dataset Source and Leakage-Safe Split and 12 epochs, and retains batch size 4, 3,600-second timeout, four first_n predictions, 25M parameters, constant LR policy, disabled early stopping, concurrency one, and pinned A100 GPU 0
- [x] #2 The authorization explicitly permits the Agent to preregister and choose Candidate learning rate, trusted loss, augmentation, and other allowlisted parameters within Harness/provider policy; these choices are not treated as protocol deviations merely because they differ from prior Candidates
- [x] #3 Trusted Workspace/Harness enforcement prevents Candidate source or manifests from raising or bypassing sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, concurrency, GPU, coordinate, sampling, data, loss-definition, metric, Artifact Filter, or lifecycle boundaries
- [x] #4 Preflight verifies clean pushed ABI and Harness identities, validated runtime images, synchronized Agent Control Boundary authorization, available named roots, no open action, no managed container, and idle pinned A100 GPU 0
- [x] #5 Exactly one Autonomy Step is invoked with next-action execution enabled and produces at most one primary handoff and one Harness-owned Candidate Run; no duplicate, replacement, retry-driven second Run, Experiment Batch, Post-Run Evaluation, or second Autonomy Step is launched
- [x] #6 Any stable Run is observed and reconciled idempotently with exactly-once lifecycle evidence, no unresolved action, and complete trusted finite, resource, source-stratified, predicted-positive/non-degeneracy, selected-record-policy, trajectory, and timeout-headroom evidence
- [x] #7 Scout interpretation follows ABI-039 asymmetric decisions: hard failure, persistent collapse, clear optimization failure, or convincing plateau/divergence may support elimination, while low score alone does not; improving, source-balanced, novel, noisy, or ambiguous trajectories remain extension-eligible without being automatically extended
- [x] #8 A durable report, Experiment Index and Research Ledger updates, validation results, independent review, and residual risks are recorded before closeout
- [x] #9 The task stops after the single representative-scout step; a roughly 36-epoch extension, full-data training, promotion, concurrency, policy-limit changes, and any subsequent Autonomy Step require their applicable separate authorization
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

- Human approved execution; authorization/report/resume events were committed and pushed before launch. Immediate preflight passed at ABI 79016b1 and Harness b2d8345.
- Invoked exactly one Autonomy Step. Candidate abi044_fullspectral_deeplabv3plus_representative_scout_v1 completed stable Run run_20260813_145951_a64a37 for 12 epochs with exactly 1,024 selected records in each MIT/Google train/validation stratum, batch 4, one container attempt, and zero retries.
- Reconciled the same Run twice idempotently. Finite/checkpoint/resource/source/predicted-positive/selection/trajectory/timeout evidence passed; filtered Dice improved to 0.1244 (MIT 0.1125, Google 0.1522). Provider assessment found no elimination evidence and marked the trajectory extension-eligible without authorizing extension.
- Independent fresh-context closeout review found no blocker/high issue. No second Run, Evaluation, Batch, extension, promotion, concurrency change, or follow-up Autonomy Step occurred.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Executed exactly one authorized representative-scout Autonomy Step. The Agent preregistered and submitted the full-spectral DeepLabV3+ ResNet-18 family with trusted bce_dice, random mirroring, AdamW 0.0003, and the 1,024-record/source/split, 12-epoch Workspace envelope. Stable Run run_20260813_145951_a64a37 completed once on pinned A100 GPU 0, remained finite and source-balanced, reconciled idempotently, and showed improving late trajectories with no provider-supported elimination evidence. The campaign stopped without Evaluation, extension, full-data training, promotion, concurrency, or a second step.

Validation:
- ABI full suite: 135 passed
- Focused Harness: 201 passed
- Full Harness: 581 passed, 2 skipped, 1 known unrelated GVCCS fake-allowlist failure
- Runtime image/boundary/config/Docker CUDA validation: passed
- Static Candidate, finite JSON/checkpoint, selection, lifecycle, open-action, container, and postflight audits: passed
- Independent review: no blocker/high finding

Residual risks:
- Capped deterministic subset is feasibility evidence only
- Final predicted-positive fractions are low and two bounded masks are all-negative
- The epoch-12 trajectory was still improving, so convergence is not established
- Retry support remains structurally enabled despite zero retries
<!-- SECTION:FINAL_SUMMARY:END -->
