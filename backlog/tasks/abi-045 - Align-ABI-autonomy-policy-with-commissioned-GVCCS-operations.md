---
id: ABI-045
title: Align ABI autonomy policy with commissioned GVCCS operations
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-13 15:54'
updated_date: '2026-08-13 15:54'
labels:
  - autonomy
  - policy
  - docs
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Remove commissioning-only per-operation backlog and authorization gates from ABI autonomous research policy. Match the commissioned GVCCS workspace model: direct operator invocation of autonomy-step or run-autonomous-iteration is sufficient authority, while trusted Harness/provider bounds and pause/failure safeguards remain enforced.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Repository instructions no longer require a backlog task or separate plan approval for each autonomous research operation
- [ ] #2 Operator invocation of autonomy-step or run-autonomous-iteration is documented as sufficient authorization for bounded research
- [ ] #3 Commissioning-only one-step and task-specific authorization language is superseded without weakening trusted resource, data, coordinate, lifecycle, or pause safeguards
- [ ] #4 Agent-visible policy and operational documentation are internally consistent with the commissioned GVCCS model
<!-- AC:END -->
