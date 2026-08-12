---
id: ABI-037
title: Run the first post-onboarding bounded Autonomy Step
status: To Do
assignee: []
created_date: '2026-08-12 15:11'
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
- [ ] #1 The pushed ABI-036 campaign_resumed authorization is present and Agent-visible before execution
- [ ] #2 The boundary refresh preserves the approved 128-sample, 3-epoch, concurrency-one, 1,800-second, pinned-A100 policy
- [ ] #3 Exactly one autonomy-step is invoked with next-action execution enabled and its handoff/result identifiers are captured
- [ ] #4 Any executed action is inspected and reconciled by stable identifier without duplicate submission, or a no-action stop is recorded
- [ ] #5 The result, validation, residual risks, and commands are recorded durably
<!-- AC:END -->
