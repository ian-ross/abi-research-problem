---
id: ABI-034
title: Prepare and run the first bounded autonomy boundary trial
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-12 10:31'
updated_date: '2026-08-12 10:32'
labels:
  - harness
  - autonomy
  - boundary
  - reliability
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reconcile the approved Gate 5 campaign state, add trusted test-run execution ceilings, validate notification setup, refresh the Agent Control Boundary, and run one handoff-only Autonomy Step without executing any Candidate or evaluation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Agent-visible campaign records consistently state that Gate 5 approved resuming autonomy planning, without authorizing promotion or automatic execution
- [ ] #2 Trusted Workspace Configuration supports and enforces test-run ceilings of 128 samples per Dataset Source, 3 epochs, one parallel Run, and a 30-minute Candidate training wall-clock budget
- [ ] #3 Mailjet configuration is validated and a notification test to iross@mit.edu succeeds without exposing credentials
- [ ] #4 The Agent Control Boundary is refreshed from the exact validated clean revisions while retaining the approved egress and read-only Runs policy
- [ ] #5 One Autonomy Step completes without --execute-next-action; no Candidate training, evaluation, or other Harness-owned next action executes
- [ ] #6 Focused and full validation pass, and the trial handoff/result artifacts and residual risks are recorded durably
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reconcile Gate 5 and current campaign status in durable Agent-visible records.
2. Add Harness-owned max_epochs and Candidate training wall-clock configuration, tests, and boundary guidance; configure ABI test limits at 128 samples/source, 3 epochs, concurrency 1, and 1800 seconds.
3. Validate the Mailjet fields and send one notification test to iross@mit.edu without logging credentials.
4. Run Harness and ABI validation, rebuild/revalidate runtime identities if required, and refresh the unchanged-policy Agent Control Boundary.
5. Run exactly one autonomy-step without --execute-next-action, inspect the handoff and prove that no Candidate/evaluation action executed.
6. Record evidence, obtain independent review, complete acceptance criteria, and summarize residual risks.
<!-- SECTION:PLAN:END -->
