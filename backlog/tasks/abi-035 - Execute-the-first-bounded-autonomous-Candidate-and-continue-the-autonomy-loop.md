---
id: ABI-035
title: Execute the first bounded autonomous Candidate and continue the autonomy loop
status: To Do
assignee: []
created_date: '2026-08-12 11:39'
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
- [ ] #1 The exact validated ABI and Harness revisions, including ABI-034 and Harness a38ad74, are pushed or otherwise durably preserved before Candidate execution
- [ ] #2 A preregistered execution protocol records the exact open abi032_mcast11_focal_tversky_v1 action, 128-samples-per-source/3-epoch/sequential-A100/1,800-second bounds, expected artifacts, finite and non-degeneracy checks, and explicit stop conditions before execution
- [ ] #3 Human review authorizes exactly one execution of the existing open run_candidate action; no second Candidate, automatic retry, or duplicate Run is launched after caller disconnect, timeout, or failure
- [ ] #4 The Candidate executes through the trusted managed Docker lifecycle on pinned A100 GPU 0, and the stable Run ID is observed and reconciled idempotently without resubmission
- [ ] #5 Terminal evidence is reviewed for finite losses, metrics, gradients/checkpoint parameters, prediction non-degeneracy, MIT/Google source-stratified behavior, sample/epoch bounds, resource profile, timeout state, artifacts, read-only mounts, coordinate exclusion, and exactly-once ledger finalization
- [ ] #6 The bounded Run result is recorded durably as directional autonomy/reliability evidence and is not represented as promotion-grade or directly comparable to ABI-031's larger training Run
- [ ] #7 Only if the Candidate Run passes the preregistered continuation gate, the Agent Control Boundary is refreshed with the new Run and exactly one subsequent bounded Autonomy Step is run with next-action execution enabled; otherwise the campaign stops for human review
- [ ] #8 Any handoff and Harness-owned action from the subsequent Autonomy Step are inspected, linked durably, and shown to obey the configured 128-sample, 3-epoch, concurrency-one, and 1,800-second ceilings
- [ ] #9 Focused/full validation, final independent review, residual risks, commands, Run and handoff identifiers, and a PR-style final summary are recorded before the task is marked Done
<!-- AC:END -->
