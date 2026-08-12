---
id: ABI-036
title: Record durable authorization for bounded autonomous continuation
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-12 15:04'
updated_date: '2026-08-12 15:05'
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
- [ ] #1 A durable campaign report records the exact authorization scope, existing ceilings, and retained human stop gates
- [ ] #2 EXPERIMENT_INDEX.md exposes the authorization to the Agent Control Boundary
- [ ] #3 A validated campaign_resumed Research Ledger event links the authorization report
- [ ] #4 The authorization artifacts are committed locally but not pushed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Record the operator authorization and guardrails in a durable campaign report
2. Update the Agent-visible Experiment Index
3. Append a validated campaign_resumed ledger event linked to the report
4. Validate, commit locally without pushing, and close the task
<!-- SECTION:PLAN:END -->
