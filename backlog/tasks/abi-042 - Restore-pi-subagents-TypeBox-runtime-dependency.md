---
id: ABI-042
title: Restore pi-subagents TypeBox runtime dependency
status: To Do
assignee: []
created_date: '2026-08-13 09:33'
labels:
  - tooling
  - pi-subagents
  - reliability
dependencies: []
priority: high
type: bug
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Diagnose and fix the local pi-subagents runtime failure caused by the unresolved `typebox/compile` module. Restore fresh-context reviewer and other delegated-agent launches needed for independent autonomy-step review without weakening structured-output validation or relying on ad-hoc per-session workarounds.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The root cause of the unresolved typebox/compile import is identified and recorded, including the responsible package/version or installation state
- [ ] #2 The durable pi-subagents installation or dependency declaration is fixed so a new Pi session can launch subagents without MODULE_NOT_FOUND
- [ ] #3 A fresh-context reviewer subagent completes a read-only repository review and returns a persisted result
- [ ] #4 Structured-output and ordinary non-structured subagent paths both pass focused smoke validation
- [ ] #5 The fix does not modify ABI scientific policy, launch a Candidate Run, or depend on an unrecorded manual NODE_PATH or shell workaround
<!-- AC:END -->
