---
id: ABI-026
title: Add curated Agent-visible ABI dataset and MCAST campaign context artifact
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 11:34'
updated_date: '2026-08-10 11:49'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define a versioned, whitelist-based Agent Campaign Context schema and safety contract. The single generated JSON artifact will contain dataset_profile, canonical_mcast, and abi_025_manual_canary sections; it will record generation/input provenance while excluding raw samples, coordinate arrays/statistics, model assets, host-only paths, and unrestricted artifact references.
2. Extend the trusted ABI Dataset Profile generator to emit exact MIT/Google split, positivity, and Contrail Mask area summaries plus bounded deterministic statistics for provider-approved ABI channels 1-16 only. Record channel semantics/units, selection and pixel-subsampling bounds, sample digests, snapshot shapes, and projection/split caveats; explicitly exclude longitude/latitude source indices 16/17.
3. Add a trusted operator-side campaign-context generator/CLI that loads Workspace Configuration, verifies the canonical MCAST registry and referenced checksums, extracts only approved MCAST 1.1/2.1 aggregate/source metrics, threshold summaries, Artifact Filter configuration/effects, and provenance, and validates explicit ABI-025 Run/Evaluation/acceptance-report inputs without importing or executing candidate code.
4. Generate the durable canonical artifact under abi_contrail/profile/ from the configured local dataset, canonical registry, run_20260810_110532_b465cf, and eval_20260810_110644_c0d61d. Review the serialized output against a denylist/allowlist, ensure all numeric scopes and bounds are explicit, and checksum the source artifacts used.
5. Declare the generated campaign context as a required Dataset Profile Artifact in the ResearchProblemSpec while retaining concise generation/refresh instructions. Ensure the progressive-disclosure Research Problem Brief/Profile index names the artifact and explains that it is summary context, not raw data or authoritative new Run output.
6. Add tiny-fixture unit tests for deterministic dataset/channel summaries, per-split mask distributions, channel-unit metadata, coordinate exclusion, MCAST metric/threshold/filter extraction, provenance and tamper failures, canary linkage, schema validation, and forbidden path/asset leakage. Add provider/snapshot tests proving the declared artifact resolves and copies read-only.
7. Run focused and full uv-managed validation, regenerate the real artifact with the trusted command, verify canonical registry parity, run prepare-agent-boundary, and inspect the prepared snapshot/index/fort configuration to prove the context is visible while training, ancillary, and baselines roots remain unmounted. Do not train models or invoke autonomy-step.
8. Document the reproducible refresh command, input identities, review checklist, and residual limitations; complete ABI-026 only after all acceptance criteria pass, then return ABI-025 to the pre-Gate-4 boundary review for explicit human approval.
<!-- SECTION:PLAN:END -->
