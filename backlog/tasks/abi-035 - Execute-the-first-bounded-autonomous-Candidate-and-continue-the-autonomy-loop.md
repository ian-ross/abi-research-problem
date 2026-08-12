---
id: ABI-035
title: Execute the first bounded autonomous Candidate and continue the autonomy loop
status: Done
assignee:
  - '@agent'
created_date: '2026-08-12 11:39'
updated_date: '2026-08-12 13:12'
labels:
  - harness
  - autonomy
  - candidates
  - gpu
  - reliability
dependencies:
  - ABI-034
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Execute the existing open run_candidate action for abi032_mcast11_focal_tversky_v1 as the first bounded automatic Candidate execution, validate its numerical/resource/lifecycle evidence without duplicate execution, refresh the Agent Control Boundary with the result, and then run the next bounded Autonomy Step with execution enabled only if the Candidate Run passes the preregistered continuation gate. This is an autonomy reliability trial under ABI-034 test ceilings, not promotion-grade scientific evidence.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The exact validated ABI and Harness revisions, including ABI-034 and Harness a38ad74, are pushed or otherwise durably preserved before Candidate execution
- [x] #2 A preregistered execution protocol records the exact open abi032_mcast11_focal_tversky_v1 action, 128-samples-per-source/3-epoch/sequential-A100/1,800-second bounds, expected artifacts, finite and non-degeneracy checks, and explicit stop conditions before execution
- [x] #3 Human review authorizes exactly one execution of the existing open run_candidate action; no second Candidate, automatic retry, or duplicate Run is launched after caller disconnect, timeout, or failure
- [x] #4 The Candidate executes through the trusted managed Docker lifecycle on pinned A100 GPU 0, and the stable Run ID is observed and reconciled idempotently without resubmission
- [x] #5 Terminal evidence is reviewed for finite losses, metrics, gradients/checkpoint parameters, prediction non-degeneracy, MIT/Google source-stratified behavior, sample/epoch bounds, resource profile, timeout state, artifacts, read-only mounts, coordinate exclusion, and exactly-once ledger finalization
- [x] #6 The bounded Run result is recorded durably as directional autonomy/reliability evidence and is not represented as promotion-grade or directly comparable to ABI-031's larger training Run
- [x] #7 Only if the Candidate Run passes the preregistered continuation gate, the Agent Control Boundary is refreshed with the new Run and exactly one subsequent bounded Autonomy Step is run with next-action execution enabled; otherwise the campaign stops for human review
- [x] #8 Any handoff and Harness-owned action from the subsequent Autonomy Step are inspected, linked durably, and shown to obey the configured 128-sample, 3-epoch, concurrency-one, and 1,800-second ceilings
- [x] #9 Focused/full validation, final independent review, residual risks, commands, Run and handoff identifiers, and a PR-style final summary are recorded before the task is marked Done
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Phase 0 — preservation, preregistration, and execution authorization
1. **Agent:** Confirm ABI-034 is Done; verify the ABI and Harness worktrees are clean; record exact ABI/Harness commits, runtime-image validation identity, current Workspace ceilings, idle A100 GPU 0, and the single open `run_candidate` action for `abi032_mcast11_focal_tversky_v1`.
2. **Agent:** Push or otherwise durably preserve the exact validated ABI and Harness commits. Re-run runtime-image validation after any revision or configuration change; do not execute from a dirty or identity-mismatched checkout.
3. **Agent:** Audit the canonical Candidate against ABI-031: prove architecture equivalence apart from names/docstrings, confirm the sole intended experimental change is trusted loss `bce_dice` to `focal_tversky`, verify no longitude/latitude, baseline weights, runtime downloads, or Candidate-owned data/loss/metric/filter/sampling/training policy, and record source checksums.
4. **Agent:** Write a durable ABI-035 execution protocol before launching anything. Preregister exactly one existing open action; sequential A100 device 0; at most 128 train and 128 validation samples per Dataset Source; batch 4; three epochs; two bounded prediction samples; 1,800-second trusted Docker training timeout; expected logs/checkpoint/metrics/resource/postprocessing artifacts; and the stable-Run/no-resubmission rule.
5. **Agent:** Preregister the continuation gate: all losses, required metrics, checkpoint tensors, gradients/parameters, and structured validation evidence finite; Run terminalizes exactly once; no timeout or forced termination; no all-negative/all-positive aggregate or bounded predictions; nonzero raw/filtered aggregate, MIT, and Google Dice above the all-negative numerical floor; complete sample/epoch/resource/mount/input/artifact evidence. A scientifically poor but finite/non-degenerate Run may pass reliability, but any contract, lifecycle, timeout, missing-artifact, coordinate, or numerical failure stops before another Autonomy Step.
6. **Human Gate 0:** Review the exact Candidate, checksums, revisions, protocol, thresholds, commands, and open-action identity. Authorize exactly one `execute-next-action` invocation or stop. This approval must explicitly forbid duplicate submission, automatic retry, and a second Candidate Run.

## Phase 1 — exactly-once Candidate execution
7. **Agent:** Immediately before execution, record Run/Evaluation/ledger counts, confirm no GPU workload, revalidate runtime images, and dry-run open-action discovery to prove there is exactly one matching action. Do not clean or replace `agent-work/autonomy-step-result.json`.
8. **Agent:** Invoke `uv run ml-autoresearch execute-next-action --workspace-root .` exactly once. Capture its output and stable Run ID. If the caller disconnects or the command returns while managed execution continues, observe the same Run with `run-status`; never invoke the action again.
9. **Agent:** Monitor only by stable Run ID and durable managed-execution state. If needed, invoke `reconcile-run` idempotently on that same Run after the recorded container exits. Never create a replacement Run because of timeout, caller failure, stale metadata, or incomplete host-side finalization.
10. **Agent:** On any non-finite diagnostic, trusted timeout request, forced termination, Resource Failure, harness failure, contract violation, missing artifact, unexpected GPU placement/concurrency, or lifecycle inconsistency, stop for human review. Do not repair, retry, evaluate, refresh for continuation, or launch another Autonomy Step.

## Phase 2 — terminal evidence and continuation decision
11. **Agent:** Validate the terminal Run: exactly 128 training and 128 validation samples per Dataset Source per epoch; three epochs maximum; batch 4; A100 device 0; one Run/container lineage; timeout not requested; all logged losses/metrics and checkpoint tensors finite; bounded predictions contain both classes; aggregate and MIT/Google raw/filtered Dice exceed the preregistered floor; and no retry occurred.
12. **Agent:** Inspect model summary, resolved manifest, Candidate checksum, execution metadata, read-only named data mounts, coordinate exclusion, resource profile, postprocessing backend/batch/timings/progress reports, final/best metrics, checkpoint, prediction samples, non-finite diagnostics, and Research Ledger. Prove exactly one terminal event and idempotent reconciliation.
13. **Agent:** Write a durable Run report comparing only directional behavior against ABI-031 while stating the 128-versus-1,024 per-source mismatch. Do not claim promotion, baseline parity, or production throughput. Record whether the preregistered reliability continuation gate passed.
14. **Human Gate 1:** Review terminal evidence and the continuation decision. If any criterion failed or evidence is incomplete, stop ABI-035 for follow-up work. If all reliability criteria passed, authorize one boundary refresh and one subsequent bounded Autonomy Step with execution enabled. This gate does not pre-authorize arbitrary later Runs.

## Phase 3 — one conditional autonomous continuation
15. **Agent:** Only after Gate 1 approval, ensure the completed Run/report/index/ledger state is committed and durably preserved, rebuild/revalidate runtime images only if trusted code/config changed, and refresh the Agent Control Boundary. Verify the Agent-visible history includes the new Run and report while egress and full read-only Runs-history policy remain unchanged.
16. **Agent:** Confirm no un-ingested handoff remains and no unresolved executable action exists from the previous step. Record current Run/Evaluation/ledger counts and configured 128-sample, 3-epoch, concurrency-one, and 1,800-second ceilings.
17. **Agent:** Invoke exactly one `uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action`. Capture `autonomy-step-result.json`, handoff identity, next action, execution result, and any new stable Run/Evaluation identifier. Do not begin another Autonomy Step.
18. **Agent:** Inspect the handoff and any Harness-owned action. Prove static/ingestion validation and effective execution policy respected all ceilings. If the action starts a managed Candidate Run, observe/reconcile only its stable Run ID under the same no-duplicate rule; if it requests human review, capability, pause, or a non-executable action, stop normally.
19. **Agent:** Apply the same finite, timeout, lifecycle, artifact, coordinate, mount, and exactly-once checks to any executed action. Do not automatically run a Post-Run Evaluation or additional Candidate beyond the single action owned by this Autonomy Step.

## Phase 4 — closeout
20. **Agent:** Update `EXPERIMENT_INDEX.md`, the Research Ledger-linked campaign report, and ABI-035 notes with exact commands, commits, image identity, Candidate/handoff checksums, Run/Evaluation IDs, gate decisions, metrics, resource/timing evidence, and residual risks. Keep durable reports free of Mailjet secrets and raw data.
21. **Agent:** Run focused Harness autonomy/config/handoff/execution/reconciliation suites, the full ABI suite, and the correctly configured full Harness suite. Record the known unrelated GVCCS stale fake-Spec failure separately if still present; do not hide new failures.
22. **Agent:** Obtain an independent final review of the commits, terminal artifacts, no-duplicate evidence, policy enforcement, and task acceptance criteria. Address blockers within approved scope or create follow-up work.
23. **Agent:** Check each acceptance criterion only when evidenced, add a PR-style final summary, ensure exact validated revisions are pushed/preserved, and mark ABI-035 Done only after all gates, validations, reports, and checklist items are complete.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Phase 0 protocol committed at 51c3f24: campaign-reports/abi-035-first-bounded-autonomous-candidate-protocol.md
- Preserved ABI execution-bearing revision c8adf5c and Harness a38ad74; runtime identity/config SHA revalidated
- Candidate tree fbcf6294e7350286bfa734382d63b45ad0ed466f86d6e359b07253fdf6adf333 is architecture-equivalent to ABI-031 apart from names/docstrings; manifest changes trusted loss bce_dice to focal_tversky
- Dry run found exactly one open run_candidate action at ledger index 73; baseline remains 12 Runs, 3 Evaluations, 74 ledger lines; no Candidate executed
- Pre-execution validation: ABI focused 33 passed; Harness autonomy/config/reconciliation 56 passed
- Gate 0 execution authorization remains pending

- Human Gate 0 authorized exactly one execute-next-action invocation and explicitly forbade duplicate submission, retry, replacement Run, and a second Candidate
- Exactly one invocation created stable Run run_20260812_121722_8d6cd3; one Docker/A100-0 container completed and was removed; two same-Run reconciliations were idempotent
- Reliability gate passed: 3 epochs, 128 train/validation observations per source per epoch, batch 4, no timeout/retry, all structured numerics and 184 checkpoint tensors finite, both bounded masks non-degenerate, source Dice above 0.0001
- Directional report committed/pushed at 6fe98c7 and linked by campaign_report_written: campaign-reports/abi-035-first-bounded-autonomous-candidate-run.md
- Human Gate 1 remains pending; no boundary refresh, subsequent Autonomy Step, evaluation, or second Candidate was launched

- Human Gate 1 approved one boundary refresh and one autonomy-step with execution enabled
- Exactly one continuation step ran and returned no_handoff/stop_for_human with execution=null because interactive approval was not yet Agent-visible; no Run, Evaluation, ledger event, handoff, or Harness action was created and no second step was run
- Full ABI suite: 114 passed; focused Harness suite: 123 passed; configured full Harness suite: 570 passed, 2 skipped, 1 known unrelated GVCCS stale fake-Spec failure
- Independent read-only final review found no blocker in numerical/resource/coordinate/mount/exactly-once evidence; its closeout finding was addressed in d36a226
- Residual risks: retry mechanism remained enabled though retry_count=0; Gate 1 durable visibility sequencing; mutable metadata dirty-state presentation; timeout path unexercised; directional 128-vs-1024 comparison only
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Executed ABI-035 as a bounded autonomy reliability trial. Preregistered and pushed the exact Candidate/revision/runtime protocol, then invoked execute-next-action exactly once. Stable Run run_20260812_121722_8d6cd3 completed three epochs on Docker-pinned A100 GPU 0 with 128 train and validation samples per MIT/Google source per epoch, batch 4, no timeout or retry, one removed container, finite structured evidence/checkpoint, non-degenerate bounded predictions, read-only mounts, and coordinate exclusion. Two reconciliations were idempotent. The reliability continuation gate passed; results remain directional and non-promotion-grade versus ABI-031's 1,024-per-source Run.

After Human Gate 1, refreshed the unchanged Agent boundary and ran exactly one autonomy-step with execution enabled. The Agent conservatively returned no_handoff/stop_for_human because interactive approval was not yet durable in Agent-visible state; no action executed, counts stayed 13 Runs/3 Evaluations, and no second step ran.

Evidence:
- campaign-reports/abi-035-first-bounded-autonomous-candidate-protocol.md
- campaign-reports/abi-035-first-bounded-autonomous-candidate-run.md
- Run run_20260812_121722_8d6cd3
- agent-work/autonomy-step-result.json
- ABI launch commit 51126c4; Harness a38ad74; final review commit d36a226

Validation:
- uv run pytest -q: 114 passed
- focused Harness autonomy/boundary/handoff/config/reconciliation suite: 123 passed
- configured full Harness suite: 570 passed, 2 skipped, 1 known unrelated GVCCS stale fake-Spec failure
- independent read-only final review: no execution blocker; closeout finding addressed

Residual risks:
- Resource Failure retries were structurally enabled although no retry occurred
- Gate 1 approval must be made Agent-visible before future continuation steps
- mutable Run metadata dirty-state presentation is less clear than the clean resolved manifest
- timeout path remains unexercised and scientific comparison is sample-budget mismatched
<!-- SECTION:FINAL_SUMMARY:END -->
