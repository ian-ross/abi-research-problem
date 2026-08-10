---
id: ABI-027
title: Fail closed when Agent Control Boundary isolation is inactive
status: Done
assignee:
  - '@agent'
created_date: '2026-08-10 13:50'
updated_date: '2026-08-10 14:47'
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
- [x] #1 autonomy-step verifies pi-fort is active and fails before Agent invocation when isolation or expected guest mounts are unavailable
- [x] #2 an isolated smoke test proves the Agent sees the Agent Workspace plus declared read-only guest mounts, but not host /data, /net, repository siblings, training data, ancillary roots, or baselines roots
- [x] #3 the regression test covers the production agent-command launch shape used by ABI-025 and confirms exactly one writable handoff surface
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reproduce and trace the ABI-025 production `autonomy-step --agent-command "pi --session-dir ../agent-sessions"` launch through ml-autoresearch and pi-fort, identifying why Pi ran on the host and defining reliable guest/isolation invariants.
2. Add a fail-closed Harness preflight that verifies pi-fort execution, expected read-only guest mounts, forbidden host-root absence, and the single writable Agent Workspace handoff surface before the Agent is invoked.
3. Add regression coverage for the exact ABI-025 agent-command launch shape, including proof that preflight failure prevents Agent invocation or handoff ingestion and that the isolated path exposes only declared mounts with exactly one writable handoff surface.
4. Run focused uv-managed tests and a lightweight isolated smoke test (no training), update durable task notes/documentation as needed, and report residual risks before completing ABI-027.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Reproduced ABI-025 launch failure: non-interactive `pi --session-dir ../agent-sessions` ignored project `.pi/settings.json` because the workspace was not approved; `pi list` omitted pi-fort while `pi list --approve` loaded it. The prior session therefore used host built-in tools.
- Live read-only probe with `pi --approve` loaded pi-fort and booted Gondolin: `/reference`, `/history`, `/docs`, and `/research-problem` were visible; host repository siblings and `/net` were absent; write attempts to declared read-only mounts failed while Agent Workspace writes succeeded.
- Chosen fix is same-process, pre-model attestation rather than static config checks or a separate preflight VM: production Pi will explicitly load only the resolved pi-fort extension, run a pi-fort guest/VFS preflight before the model sees the prompt, and require a nonce-bound read-only attestation before handoff ingestion.

- Implemented same-process pre-model pi-fort preflight and nonce-bound protected attestation. Harness now permits only literal `pi`, resolves the trusted PATH executable, adds `--approve --no-extensions --extension <pi-fort> --fort-preflight <spec>`, validates exact mount evidence, returns `isolation_failed`, and skips ingestion on failure.
- Hardened pi-fort so enabled/preflighted QEMU, image, config, and VM failures never fall back to host read/write/edit/bash tools. Added required/forbidden guest path checks, read-only write probes, sole writable workspace proof, and protected attestation.
- Live success smoke proved required guest mounts, absent host repository/data roots, and exactly one writable host-backed Agent Workspace. Live negative smoke exited 27 before model invocation; the sentinel remained absent.
- Independent security review found and then confirmed fixes for executable impersonation and incomplete mount-evidence validation; no blockers remain.
- Validation: ABI repository 100 tests passed; ml-autoresearch 72 focused tests passed; pi-fort 123 tests plus build/lint passed. Full ml-autoresearch suite had 521 pass, 2 skip, and 4 unrelated environment/neighbor failures documented in the campaign report.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented fail-closed Agent Control Boundary verification across the Harness and pi-fort. The production ABI-025 Pi command is now explicitly trusted and isolated, pi-fort attests effective guest paths and exact mount/write policy in the same process before model invocation, and the Harness refuses handoff ingestion without valid nonce-bound evidence. Added regression coverage, documentation, and campaign smoke evidence.

Tests:
- uv run pytest (ABI repository): 100 passed
- cd ../ml-autoresearch && uv run pytest tests/test_autonomy_step.py tests/test_autonomous_iteration.py tests/test_agent_boundary.py tests/test_agent_control_boundary_docs.py: 72 passed
- cd ../pi-fort && pnpm test: 123 passed
- cd ../pi-fort && pnpm build
- cd ../pi-fort && pnpm lint
- Live same-process success preflight: exit 0, all checks, one writable host-backed workspace
- Live missing-path failure preflight: exit 27, model sentinel absent

Full Harness suite note: 521 passed, 2 skipped, 4 unrelated environment/neighbor failures (external package env, GVCCS candidate drift, mocked CUDA) recorded in campaign-reports/abi-027-agent-boundary-isolation.md.
<!-- SECTION:FINAL_SUMMARY:END -->
