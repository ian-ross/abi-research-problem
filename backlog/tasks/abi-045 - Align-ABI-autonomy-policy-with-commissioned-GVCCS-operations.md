---
id: ABI-045
title: >-
  Simplify ABI autonomous research policy and remove issue-oriented campaign
  guidance
status: To Do
assignee: []
created_date: '2026-08-13 15:54'
updated_date: '2026-08-13 19:59'
labels:
  - autonomy
  - policy
  - docs
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Remove per-operation Backlog and authorization gates from ABI autonomous research policy. Direct operator invocation of `autonomy-step --execute-next-action` or `run-autonomous-iteration` is sufficient authority for bounded research under the active trusted Workspace Configuration and Research Problem contract.

Operational guidance must follow the established commissioned workspace structure, adapted only for ABI-specific configuration and scientific constraints. It must not name or refer readers to another Research Problem repository. Current policy must be stated positively, without obsolete-gate lists, historical-issue explanations, or commissioning supersession prose.

Rename every campaign report so its filename is independent of a Backlog issue identifier, remove Backlog-issue framing from report text, and repair every resulting reference while preserving scientific evidence and durable Run/Candidate provenance. No Harness repository changes are allowed.

Implementation must start from local `main` at `6707824`. The commits, diffs, file contents, and implementation changes between local `main` and `origin/main` are not inputs to this task and must not be merged, rebased, cherry-picked, copied, or otherwise used.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Repository instructions do not require a Backlog task, implementation plan, or separate plan approval for an operator-invoked autonomous research operation.
- [ ] #2 Direct operator invocation of `autonomy-step --execute-next-action` or `run-autonomous-iteration` is documented as sufficient authority for bounded in-contract research.
- [ ] #3 Operational guidance follows the established commissioned workspace structure with only ABI-specific path, configuration, provider, and scientific differences, and contains no reference to another Research Problem or its repository.
- [ ] #4 Current policy is expressed positively and contains no negative catalogue of obsolete requirements, no historical/supersession discussion of Backlog issues, and no references to Backlog issues ABI-034 through ABI-044 as policy or operational context.
- [ ] #5 Every campaign report has an issue-independent filename and report title/body text contains no Backlog issue identifiers or issue-oriented framing; scientific evidence, commands, measurements, Run identities, and conclusions are preserved.
- [ ] #6 All renamed-report references are repaired, including report cross-links, Experiment Index links, Candidate documentation, evaluation requests, Backlog metadata, tests, and Research Ledger report paths/reasons; no stale report path remains.
- [ ] #7 Candidate documentation no longer describes experiments through Backlog issues or commissioning authorization gates, while canonical Candidate identities and Run provenance remain intact.
- [ ] #8 Trusted resource, data, sampling, coordinate-exclusion, loss, metric, Artifact Filter, execution, exactly-once lifecycle, pause, and failure safeguards remain enforced and consistently documented.
- [ ] #9 No file in the Harness repository is changed.
- [ ] #10 No commit, diff, file content, or implementation change from the range between local `main` at `6707824` and `origin/main` is used; the work is implemented independently from local `main` and direct inspection of the commissioned workspace pattern.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Establish the local-only baseline at `6707824`, inventory current policy/report references, and inspect the commissioned workspace files directly for the operational structure to reproduce. Do not inspect or use the `local main..origin/main` change range.
2. Replace the broad Backlog prerequisite and task-specific training gates in `AGENTS.md`, `README.md`, `EXPERIMENT_INDEX.md`, the ABI Research Problem Brief, and portable configuration comments. Keep only positive current authority, ABI-specific scientific guidance, and trusted safeguards; include no external-project references or historical-issue/supersession section.
3. Rename all existing campaign reports to descriptive issue-independent filenames, resolving generic-name collisions semantically. Edit every report to remove Backlog issue identifiers, task bookkeeping, and commissioning authorization framing while preserving durable scientific and operational evidence.
4. Repair all references to renamed reports and removed issue framing across report cross-links, the Experiment Index, Research Ledger paths/reasons, Candidate READMEs/proposals, evaluation requests, tests, and Backlog metadata. Use the Backlog CLI for task metadata. Preserve canonical Candidate IDs and Run identities.
5. Update focused policy tests to assert the positive operator-invocation model, issue-independent report corpus, valid links/ledger paths, and retained trusted safeguards. Make no Harness repository changes.
6. Validate from the ABI repository: search for stale issue-oriented guidance and report paths, check Markdown links and Research Ledger parsing, run focused tests and the full ABI suite, and inspect generated Agent-visible policy only if needed without modifying the Harness repository.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Planning revision requested by the operator.
- Local `main` is `6707824`; `origin/main` is ahead, but that change range is explicitly excluded as an implementation source.
- No implementation, merge, rebase, cherry-pick, Harness edit, or research execution is part of this task update.
<!-- SECTION:NOTES:END -->
