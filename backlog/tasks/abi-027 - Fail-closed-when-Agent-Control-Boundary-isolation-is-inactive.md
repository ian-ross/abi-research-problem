---
id: ABI-027
title: Enable pi-fort for the repository-local autonomy launch
status: Done
assignee:
  - '@agent'
created_date: '2026-08-10 13:50'
updated_date: '2026-08-10 15:03'
labels:
  - harness
  - agent-boundary
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-025 Gate 4 launched Pi non-interactively without approving project-local resources, so Pi ignored agent-work/.pi/settings.json and did not load pi-fort. Apply only the repository-local launch fix and verify it manually; do not change the shared Harness or pi-fort implementation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The repository-local autonomy command is `pi --approve --session-dir ../agent-sessions` so non-interactive Pi loads project pi-fort.
- [x] #2 A no-training smoke confirms `/reference` is visible inside the guest while host `/net` and the ml-autoresearch repository sibling are unavailable.
- [x] #3 No shared ml-autoresearch or pi-fort source changes are part of the fix.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Apply the repository-local Pi trust fix so the autonomy command launches as `pi --approve --session-dir ../agent-sessions`.
2. Run one minimal no-training boundary smoke to confirm pi-fort loads and `/reference` is visible instead of the host filesystem.
3. Record the result and return to the existing ABI-025 manual review flow without changing Harness or pi-fort code.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Root cause: Pi print mode ignored project-local resources because the ABI-025 launch omitted `--approve`; `pi list` omitted pi-fort while `pi list --approve` loaded it.
- Reverted the over-scoped Harness and pi-fort implementation completely. `../ml-autoresearch` is clean; pi-fort retains only its unrelated pre-existing Dockerfile modification.
- Added repository-local `[autonomy_step] agent_command = "pi --approve --session-dir ../agent-sessions"` to `ml-autoresearch.toml`.
- No-training smoke result: `cwd=/home/iross/code/abi-research-problem/agent-work reference=yes host_net=no harness_sibling=no`.
- No shared Harness or pi-fort source change is part of the final fix.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixed the ABI repository locally by adding `--approve` to its configured non-interactive Pi autonomy command. This makes Pi load the existing project-local pi-fort package/configuration. A minimal no-training smoke confirmed `/reference` is visible inside the guest and host `/net` plus the Harness repository sibling are unavailable. All over-scoped shared Harness/pi-fort changes were reverted.
<!-- SECTION:FINAL_SUMMARY:END -->
