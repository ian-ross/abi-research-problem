---
id: ABI-027
title: Fail closed when Agent Control Boundary isolation is inactive
status: To Do
assignee: []
created_date: '2026-08-10 13:50'
labels:
  - harness
  - agent-boundary
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-025 Gate 4 showed that the autonomy-step Pi process executed against the host filesystem rather than the configured pi-fort VM/mount namespace: /reference was absent while host /data, /net, and repository source paths were visible. Diagnose the launch/configuration failure and make autonomy-step verify effective isolation before invoking the Agent.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 autonomy-step verifies pi-fort is active and fails before Agent invocation when isolation or expected guest mounts are unavailable
- [ ] #2 an isolated smoke test proves the Agent sees the Agent Workspace plus declared read-only guest mounts, but not host /data, /net, repository siblings, training data, ancillary roots, or baselines roots
- [ ] #3 the regression test covers the production agent-command launch shape used by ABI-025 and confirms exactly one writable handoff surface
<!-- AC:END -->
