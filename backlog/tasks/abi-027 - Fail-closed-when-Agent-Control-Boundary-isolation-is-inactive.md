---
id: ABI-027
title: Fail closed when Agent Control Boundary isolation is inactive
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 13:50'
updated_date: '2026-08-10 14:00'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reproduce and trace the ABI-025 production `autonomy-step --agent-command "pi --session-dir ../agent-sessions"` launch through ml-autoresearch and pi-fort, identifying why Pi ran on the host and defining reliable guest/isolation invariants.
2. Add a fail-closed Harness preflight that verifies pi-fort execution, expected read-only guest mounts, forbidden host-root absence, and the single writable Agent Workspace handoff surface before the Agent is invoked.
3. Add regression coverage for the exact ABI-025 agent-command launch shape, including proof that preflight failure prevents Agent invocation or handoff ingestion and that the isolated path exposes only declared mounts with exactly one writable handoff surface.
4. Run focused uv-managed tests and a lightweight isolated smoke test (no training), update durable task notes/documentation as needed, and report residual risks before completing ABI-027.
<!-- SECTION:PLAN:END -->
