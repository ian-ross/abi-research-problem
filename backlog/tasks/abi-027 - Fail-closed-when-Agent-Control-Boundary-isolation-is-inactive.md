---
id: ABI-027
title: Fail closed when Agent Control Boundary isolation is inactive
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 13:50'
updated_date: '2026-08-10 15:01'
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
1. Apply the repository-local Pi trust fix so the autonomy command launches as `pi --approve --session-dir ../agent-sessions`.
2. Run one minimal no-training boundary smoke to confirm pi-fort loads and `/reference` is visible instead of the host filesystem.
3. Record the result and return to the existing ABI-025 manual review flow without changing Harness or pi-fort code.
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

- Correction: the earlier Harness/pi-fort hardening implementation was over-scoped and has been fully reverted. ABI-027 is reopened. The only retained diagnosis is that Pi print mode ignored project-local pi-fort because the launch omitted `--approve`.
<!-- SECTION:NOTES:END -->
