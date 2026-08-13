---
id: ABI-045
title: Align ABI autonomy policy with commissioned GVCCS operations
status: Done
assignee:
  - '@agent'
created_date: '2026-08-13 15:54'
updated_date: '2026-08-13 16:27'
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
- [x] #1 Repository instructions no longer require a backlog task or separate plan approval for each autonomous research operation
- [x] #2 Operator invocation of autonomy-step or run-autonomous-iteration is documented as sufficient authorization for bounded research
- [x] #3 Commissioning-only one-step and task-specific authorization language is superseded without weakening trusted resource, data, coordinate, lifecycle, or pause safeguards
- [x] #4 Agent-visible policy and operational documentation are internally consistent with the commissioned GVCCS model
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Compare commissioned GVCCS operator/autonomy policy with ABI commissioning-era gates
2. Replace ABI per-operation backlog and authorization requirements with operator-invocation authority while retaining trusted safety boundaries
3. Update active campaign/index/readme guidance and tests that encode the old policy
4. Regenerate/validate Agent-visible policy and run focused/full tests
5. Record final evidence and close the transition task
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Compared commissioned GVCCS policy: no Backlog directory or per-operation approval workflow; operator commands drive bounded research.
- Replaced ABI commissioning gates with operator-invocation authority in AGENTS.md, README.md, Experiment Index, provider brief, template, and durable ABI-045 report. Historical ABI-034 through ABI-044 records remain unchanged and are prospectively superseded.
- Updated Harness generated-boundary guidance to defer current scientific policy to mounted Experiment Index/Brief and removed generic staged-authorization prose; neutralized campaign resume wording. Harness commit e0032df is pushed.
- ABI full suite: 135 passed. Harness focused: 49 passed. Harness full configured: 582 passed, 2 skipped, 1 known unrelated stale GVCCS fake-allowlist failure.
- Rebuilt and validated clean-Harness runtime images at fingerprint cd7fa06690041d26; regenerated Agent boundary and verified current index/report/ledger visibility. No autonomy, Candidate, Evaluation, Batch, or GPU research operation launched.
- Independent ABI and Harness reviews approved with no remaining blocker/high/medium findings.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aligned ABI autonomous research governance with the commissioned GVCCS operating model. Direct operator invocation of autonomy-step or run-autonomous-iteration is now sufficient authority for bounded work; ordinary operations no longer require Backlog tasks, plans, per-step approval, campaign authorization events, or manual commissioning preflight. Trusted Workspace/provider limits, coordinate exclusion, ownership boundaries, exactly-once lifecycle, pause, and failure stops remain. Historical commissioning artifacts are preserved and prospectively superseded. Updated provider-neutral Harness boundary guidance and pushed Harness e0032df.

Validation:
- ABI: uv run --group torch pytest -q (135 passed)
- Harness focused: 49 passed
- Harness full configured: 582 passed, 2 skipped, 1 known unrelated GVCCS fake-allowlist failure
- Runtime images rebuilt/validated from clean Harness e0032df; Agent boundary regenerated and inspected
- Independent ABI/Harness review: approved, no blocker/high/medium findings
- No research execution launched
<!-- SECTION:FINAL_SUMMARY:END -->
