---
id: ABI-014
title: Create ABI research brief and dataset profile
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-13 08:31'
labels:
  - docs
  - profile
dependencies:
  - ABI-001
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Write the agent-facing research brief and dataset profile for GOES ABI Contrail Segmentation, capturing the decisions made during planning without putting implementation details in CONTEXT.md.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Brief defines the task as binary GOES ABI Contrail Segmentation on ABI Patches
- [x] #2 Brief explains input modes, no-lon-lat rule, Learned Channel Mixer guidance, and BTD motivation
- [x] #3 Brief documents loss/auxiliary-target allowlists and capability-request rules
- [x] #4 Dataset profile summarizes MIT and Google counts, split policy, positivity, and projection caveats
- [x] #5 Profile generation can tolerate missing full data when explicitly requested
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Draft the research brief from the finalized planning decisions: binary Contrail Mask target, ABI Patch sample, Dataset Source handling, no-lon-lat rule, input modes, losses, aux targets, metrics, artifact filters, and baselines.
2. Include concise BTD/Learned Channel Mixer guidance without over-constraining candidate exploration.
3. Implement or adapt a dataset profile generator that summarizes MIT/Google counts, positivity, split policy, time/projection caveats, and missing-data behavior.
4. Keep CONTEXT.md glossary-only; put operational instructions and implementation guidance in brief/profile docs.
5. Wire brief/profile artifacts into the ResearchProblemSpec.
6. Add validation/tests that the declared brief/profile paths exist or fail clearly.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Expanded the ABI research brief with task definition, input modes/no-lon-lat guardrail, BTD/Learned Channel Mixer guidance, allowlists, and capability-request rules.
- Added abi_contrail.profile JSON generator with MIT/Google count, split, positivity, mask-area, projection-caveat, and --allow-missing placeholder behavior.
- Updated profile artifact docs and ResearchProblemSpec artifact metadata.
- Added profile/provider-spec tests; full test suite passes.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented ABI research brief and dataset profile support.

Changes:
- Rewrote abi_contrail/brief/goes-abi-contrail-segmentation.md as an agent-facing brief for binary GOES ABI Contrail Segmentation on ABI Patches, covering input modes, no-lon-lat guardrails, BTD/Learned Channel Mixer guidance, provider-owned boundaries, allowlists, and Capability Request rules.
- Added abi_contrail/profile.py with a trusted JSON Dataset Profile generator for MIT and Google sources, including split counts, positivity, mask-area summaries, split policy metadata, projection caveats, and explicit --allow-missing placeholder behavior.
- Replaced the placeholder profile markdown with operator guidance for profile generation and missing-data behavior.
- Updated ResearchProblemSpec metadata to require the profile artifact guidance and added tests for declared artifact paths.

Tests:
- uv run pytest
- uv run python -m abi_contrail.profile --allow-missing --output /tmp/abi-profile-placeholder.json
<!-- SECTION:FINAL_SUMMARY:END -->
