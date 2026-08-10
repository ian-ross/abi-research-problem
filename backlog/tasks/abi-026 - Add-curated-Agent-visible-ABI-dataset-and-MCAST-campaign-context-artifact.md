---
id: ABI-026
title: Add curated Agent-visible ABI dataset and MCAST campaign context artifact
status: To Do
assignee: []
created_date: '2026-08-10 11:34'
labels:
  - agent-boundary
  - provider
  - baselines
  - dataset-profile
  - documentation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a trusted, reproducible, read-only context artifact for the Agent Control Boundary so autonomous candidate design can use useful local dataset and canonical MCAST summaries without access to raw training data, longitude/latitude, baseline model weights, or unrestricted baseline artifact roots. This task unblocks ABI-025 before Human Execution Gate 4.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A trusted artifact summarizes the mounted ABI snapshot at a useful aggregate level, including MIT/Google train and validation counts, Contrail Mask positivity and mask-area distributions, ABI channel semantics/units and available safe range statistics, split policy, projection caveats, generation scope, timestamp, and reproducible provenance.
- [ ] #2 The artifact summarizes canonical MCAST 1.1 and 2.1 raw and Artifact-Filtered aggregate and Dataset Source-stratified metrics, precision, recall, Contrail Connectivity Metric, threshold behavior, Artifact Filter effects, registry identity, checksums/provenance, and the ABI-025 manual canary context.
- [ ] #3 The artifact contains no raw training samples beyond separately approved bounded qualitative examples, no longitude or latitude arrays or candidate features, no baseline model weights, and no candidate-owned data loading, metric, filter, or sampling logic.
- [ ] #4 prepare-agent-boundary exposes the artifact read-only and makes it discoverable from the Research Problem Brief/Profile index or equally explicit Agent Control Boundary instructions while leaving full training, ancillary, and baselines roots unmounted.
- [ ] #5 Trusted generation or refresh commands are documented and tests or bounded validation prove the artifact matches its source summaries, carries sufficient provenance, and is visible inside the prepared Agent Control Boundary.
<!-- AC:END -->
