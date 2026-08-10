---
id: ABI-027
title: Enable pi-fort for the repository-local autonomy launch
status: Done
assignee:
  - '@agent'
created_date: '2026-08-10 13:50'
updated_date: '2026-08-10 15:38'
labels:
  - harness
  - agent-boundary
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-025 Gate 4 launched Pi non-interactively while the ABI repository lacked a saved Pi trust decision, so Pi ignored agent-work/.pi/settings.json and did not load pi-fort. Match the existing GVCCS setup by trusting the ABI repository in the main Pi trust file; do not change the shared Harness, pi-fort, or repository command configuration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A no-training smoke confirms `/reference` is visible inside the guest while host `/net` and the ml-autoresearch repository sibling are unavailable.
- [x] #2 No shared ml-autoresearch or pi-fort source changes are part of the fix.
- [x] #3 The saved Pi trust configuration includes the ABI repository, so the default non-interactive Pi command loads project-local pi-fort without a repository command override.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Compare ABI and GVCCS Pi package discovery and trust state.
2. Persist trust for the ABI repository in the main Pi trust file.
3. Verify plain Pi discovers project-local pi-fort, with no Harness, pi-fort, or repository command override.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Root cause: GVCCS already had a saved trust entry in `~/.pi/agent/trust.json`; ABI did not. In non-interactive mode, plain Pi therefore loaded GVCCS project packages but ignored ABI project packages.
- The operator added `/home/iross/code/abi-research-problem: true` to the main Pi trust file.
- Removed the temporary repository-local `[autonomy_step]` command override. `load_configured_agent_command(...)` now returns `None`, restoring the Harness default command.
- `cd agent-work && pi list` now discovers project package `../../../pi-fort` without `--approve`.
- `../ml-autoresearch` remains clean and pi-fort retains only its unrelated pre-existing Dockerfile modification.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Resolved the local launch difference by adding the ABI repository to Pi saved trust, matching GVCCS. Removed the repository command override; plain non-interactive Pi now discovers project-local pi-fort through the existing default Harness launch. No Harness or pi-fort source changes were made.
<!-- SECTION:FINAL_SUMMARY:END -->
