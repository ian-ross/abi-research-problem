---
id: ABI-014
title: Create ABI research brief and dataset profile
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
- [ ] #1 Brief defines the task as binary GOES ABI Contrail Segmentation on ABI Patches
- [ ] #2 Brief explains input modes, no-lon-lat rule, Learned Channel Mixer guidance, and BTD motivation
- [ ] #3 Brief documents loss/auxiliary-target allowlists and capability-request rules
- [ ] #4 Dataset profile summarizes MIT and Google counts, split policy, positivity, and projection caveats
- [ ] #5 Profile generation can tolerate missing full data when explicitly requested
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
