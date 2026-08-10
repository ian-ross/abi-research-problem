---
id: ABI-026
title: Add curated Agent-visible ABI dataset and MCAST campaign context artifact
status: Done
assignee:
  - '@agent'
created_date: '2026-08-10 11:34'
updated_date: '2026-08-10 12:19'
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
- [x] #1 A trusted artifact summarizes the mounted ABI snapshot at a useful aggregate level, including MIT/Google train and validation counts, Contrail Mask positivity and mask-area distributions, ABI channel semantics/units and available safe range statistics, split policy, projection caveats, generation scope, timestamp, and reproducible provenance.
- [x] #2 The artifact summarizes canonical MCAST 1.1 and 2.1 raw and Artifact-Filtered aggregate and Dataset Source-stratified metrics, precision, recall, Contrail Connectivity Metric, threshold behavior, Artifact Filter effects, registry identity, checksums/provenance, and the ABI-025 manual canary context.
- [x] #3 The artifact contains no raw training samples beyond separately approved bounded qualitative examples, no longitude or latitude arrays or candidate features, no baseline model weights, and no candidate-owned data loading, metric, filter, or sampling logic.
- [x] #4 prepare-agent-boundary exposes the artifact read-only and makes it discoverable from the Research Problem Brief/Profile index or equally explicit Agent Control Boundary instructions while leaving full training, ancillary, and baselines roots unmounted.
- [x] #5 Trusted generation or refresh commands are documented and tests or bounded validation prove the artifact matches its source summaries, carries sufficient provenance, and is visible inside the prepared Agent Control Boundary.
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Implemented dataset-profile.v1 with exact MIT/Google split/positivity/mask-area summaries, safe ABI 1-16 channel metadata and bounded deterministic range statistics, and snapshot digests.
- Added abi-campaign-context trusted CLI/schema/safety validation, generated agent-campaign-context.v1.json from the canonical registry and ABI-025 Run/Evaluation, and documented refresh/review procedures.
- Declared the JSON as a required Dataset Profile Artifact and verified prepare-agent-boundary copies/indexes it under the read-only /research-problem mount with no training, ancillary, or baselines mounts.
- Validation: uv run pytest -q (100 passed); uv build; generated artifact source/checksum/path denylist checks; prepared-boundary snapshot/index/mount assertions. No training or autonomy step was invoked.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented a versioned trusted Agent Campaign Context pipeline and durable generated artifact containing curated ABI snapshot, canonical MCAST 1.1/2.1, threshold/Artifact Filter, and ABI-025 manual-canary summaries. Added strict path/content safety validation, reproducible checksums and generator provenance, required ResearchProblemSpec/index exposure, operator documentation, and campaign validation notes.

Tests and validation:
- uv run pytest -q (100 passed)
- uv build
- uv run abi-campaign-context ... (generated and validated)
- uv run ml-autoresearch prepare-agent-boundary --workspace-root . --skip-runtime-image-validation
- bounded assertions verified package inclusion, snapshot parity, read-only /research-problem exposure, index discoverability, and absence of training/ancillary/baselines mounts

No model training or autonomy step was run.
<!-- SECTION:FINAL_SUMMARY:END -->
