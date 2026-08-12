---
id: ABI-036
title: Record durable authorization for bounded autonomous continuation
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-12 15:04'
updated_date: '2026-08-12 15:06'
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
Record the operator's post-onboarding decision in Agent-visible durable campaign state so routine autonomy may continue under existing trusted ABI-034 ceilings without per-step chat approval, while retaining human gates for policy changes, promotion, pauses, failures, and exceptional actions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A durable campaign report records the exact authorization scope, existing ceilings, and retained human stop gates
- [x] #2 EXPERIMENT_INDEX.md exposes the authorization to the Agent Control Boundary
- [x] #3 A validated campaign_resumed Research Ledger event links the authorization report
- [ ] #4 The authorization artifacts are committed locally but not pushed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Record the operator authorization and guardrails in a durable campaign report
2. Update the Agent-visible Experiment Index
3. Append a validated campaign_resumed ledger event linked to the report
4. Validate, commit locally without pushing, and close the task
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added campaign-reports/abi-036-bounded-autonomy-authorization.md with the routine-operation scope, unchanged ABI-034 ceilings, exactly-once rules, and retained human stop gates
- Updated EXPERIMENT_INDEX.md with an active authorization summary suitable for /reference
- Recorded campaign_report_written and validated campaign_resumed(reason=bounded_autonomy_authorized_after_abi035_onboarding) ledger events
- prepare-agent-boundary verification exposed the authorization in agent-reference/EXPERIMENT_INDEX.md and agent-history/research-ledger.jsonl
- No Candidate, evaluation, batch, or Autonomy Step was launched
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Recorded the post-onboarding human decision that routine bounded autonomy may continue without per-step chat approval while the current trusted ABI-034 policy remains unchanged. Added a durable authorization report, surfaced a concise authorization and stop boundary in the Experiment Index, and appended linked campaign_report_written and campaign_resumed events through validated Harness CLI controls. Refreshed the local Agent Control Boundary only to verify visibility: /reference exposes the authorization and /history contains the resume event. No research action executed.

Authorization retains human review for policy/contract/coordinate changes, limit increases, unbounded actions, promotion or deployment, explicit stops, capability blockers, and numerical, timeout, lifecycle, artifact, or Harness failures.

Validation:
- git diff --check
- validated campaign_resumed event parse/assertions
- uv run ml-autoresearch prepare-agent-boundary --workspace-root .
- Agent-visible snapshot grep
- secret-pattern scan

Delivery:
- Commit locally only; operator will push before the next boundary refresh/Autonomy Step.
<!-- SECTION:FINAL_SUMMARY:END -->
