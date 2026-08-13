---
id: ABI-042
title: Restore pi-subagents TypeBox runtime dependency
status: Done
assignee:
  - '@agent'
created_date: '2026-08-13 09:33'
updated_date: '2026-08-13 09:49'
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
- [x] #1 The root cause of the unresolved typebox/compile import is identified and recorded, including the responsible package/version or installation state
- [x] #2 The durable pi-subagents installation or dependency declaration is fixed so a new Pi session can launch subagents without MODULE_NOT_FOUND
- [x] #3 A fresh-context reviewer subagent completes a read-only repository review and returns a persisted result
- [x] #4 Structured-output and ordinary non-structured subagent paths both pass focused smoke validation
- [x] #5 The fix does not modify ABI scientific policy, launch a Candidate Run, or depend on an unrecorded manual NODE_PATH or shell workaround
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reproduce the pi-subagents launch failure and inspect the installed package/dependency graph to identify the exact TypeBox resolution root cause.
2. Implement a durable dependency or installation fix without shell-path workarounds or changes to ABI scientific policy.
3. Add or run focused smoke validation for ordinary and structured-output subagent paths.
4. Launch a fresh-context read-only reviewer, persist its repository review, and record the diagnosis, validation, and task completion metadata.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Reproduced detached-runner failure with pi-subagents@0.35.1 missing optional peer typebox/compile (run cf76106e-e28d-4da1-8d02-a85ebb0d13e9).
- Updated the unpinned user package through `pi update npm:pi-subagents` to 0.48.0, which installs typebox@1.1.38 as a production dependency.
- Passed managed-resolution, separate new-parent-session ordinary launch, schema-bound structured-output, and fresh-context reviewer smoke checks.
- Persisted diagnosis and independent review in campaign-reports/abi-042-pi-subagents-runtime-repair.md and campaign-reports/abi-042-fresh-context-review.md.
- No scientific policy or candidate/training paths changed; no Candidate Run was launched and no NODE_PATH workaround was used.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Restored delegated-agent startup by updating the managed user-scoped pi-subagents installation from affected 0.35.1 to 0.48.0, where typebox@1.1.38 is a production dependency. Recorded the root cause, pre-fix reproduction, durable repair, and independent fresh-context review.

Validation:
- npm ls --prefix /home/iross/.pi/agent/npm pi-subagents typebox --all
- require.resolve("typebox/compile") from the installed pi-subagents root
- Separate `pi --no-session --mode json` parent launched a fresh delegate and returned ABI_042_NEW_SESSION_CHILD_OK
- Structured-output run feae7b2d-5175-4229-9029-2c0def79d988 returned ABI_042_STRUCTURED_OUTPUT_OK
- Fresh reviewer run ed50ee52-4b7c-4305-b9c4-90de9a783154 completed with no blocker and persisted its report
- git diff --cached --check
<!-- SECTION:FINAL_SUMMARY:END -->
