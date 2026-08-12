---
id: ABI-037
title: Run the first post-onboarding bounded Autonomy Step
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-12 15:11'
updated_date: '2026-08-12 15:22'
labels:
  - harness
  - autonomy
  - boundary
  - candidates
  - gpu
  - reliability
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After the operator pushes ABI-036 durable authorization, verify the preserved boundary state, refresh the Agent Control Boundary, run exactly one bounded Autonomy Step with next-action execution enabled, and inspect/reconcile its handoff and any Harness-owned action under the approved ceilings.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The pushed ABI-036 campaign_resumed authorization is present and Agent-visible before execution
- [x] #2 The boundary refresh preserves the approved 128-sample, 3-epoch, concurrency-one, 1,800-second, pinned-A100 policy
- [x] #3 Exactly one autonomy-step is invoked with next-action execution enabled and its handoff/result identifiers are captured
- [x] #4 Any executed action is inspected and reconciled by stable identifier without duplicate submission, or a no-action stop is recorded
- [x] #5 The result, validation, residual risks, and commands are recorded durably
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Verify clean pushed ABI/Harness revisions, durable authorization, idle execution state, and configured ceilings
2. Revalidate runtime identity and refresh the Agent Control Boundary
3. Invoke exactly one autonomy-step with next-action execution enabled
4. Inspect and, if needed, observe/reconcile the single resulting action by stable identifier
5. Record evidence, validate, review, and close the task
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Verified pushed ABI-036 campaign_resumed authorization in Agent-visible /reference and /history before execution
- Refreshed boundary with unchanged 128-sample/source, 3-epoch, concurrency-one, 1,800-second, two-prediction, 25M-parameter, pinned-A100 policy
- Invoked exactly one autonomy-step --execute-next-action; ingested Candidate abi037_mcast11_bce_dice_cldice_v1 and launched stable Run run_20260812_151543_5b9508
- One Docker/A100-0 container completed and was removed; two same-Run reconciliations were idempotent; no retry, timeout, duplicate, evaluation, batch, or second step
- Operational evidence was finite and contract-compliant, but both bounded masks were all-negative, Google Dice was at the numerical floor, and aggregate filtered recall collapsed to 0.0000618; stop this exact loss branch
- Validation: ABI 114 passed; focused Harness 123 passed; static Candidate/AST/artifact/ledger checks passed
- Independent read-only review found no blocker/high issue and assessed AC1-5 as passed
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Refreshed the Agent Control Boundary after confirming the pushed ABI-036 durable authorization was visible, then ran exactly one post-onboarding Autonomy Step with next-action execution enabled. The Agent submitted one controlled MCAST 1.1 BCE-Dice-clDice Candidate, and the Harness executed one managed Docker Run, run_20260812_151543_5b9508, on pinned A100 GPU 0 under the approved 128-samples-per-source, 3-epoch, batch-4, concurrency-one, two-prediction, and 1,800-second ceilings. The sole container exited 0 and was removed; no retry, timeout, duplicate, evaluation, batch, or second Autonomy Step occurred. Two reconciliations were idempotent.

The Run was operationally reliable: all 1,202 audited structured numeric values and 14,339,829 checkpoint values were finite, required artifacts/mount/input exclusions were present, and exactly one submission/start/completion lineage was recorded. Scientifically, the Result failed its hypothesis: aggregate filtered Dice was 0.000123, filtered recall 0.0000618, Google Dice was at the all-negative floor, and both bounded masks were all-negative. The reported connectivity near 0.5 is not meaningful in this degenerate regime. Stop this exact loss branch; retain the Run as bounded negative evidence.

Evidence:
- campaign-reports/abi-037-post-onboarding-autonomy-step.md
- candidates/abi037_mcast11_bce_dice_cldice_v1
- agent-work/autonomy-step-result.json
- Run run_20260812_151543_5b9508

Validation:
- uv run pytest -q: 114 passed
- focused Harness autonomy/boundary/handoff/config/reconciliation suite: 123 passed
- static Candidate validation and normalized architecture comparison passed
- independent read-only review: no blocker/high issue

Residual risks:
- initial autonomy result records running rather than terminal reconciliation
- provider metadata is dirty after expected handoff/ledger mutation
- retry support remained enabled although retry_count=0
- no separate immutable Autonomy Step ID exists beyond singleton result/ledger/Run evidence
<!-- SECTION:FINAL_SUMMARY:END -->
