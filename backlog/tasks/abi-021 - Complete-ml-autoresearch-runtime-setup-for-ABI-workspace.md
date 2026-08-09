---
id: ABI-021
title: Complete ml-autoresearch runtime setup for ABI workspace
status: Done
assignee:
  - '@agent'
created_date: '2026-08-07 10:23'
updated_date: '2026-08-09 20:19'
labels:
  - harness
  - containers
  - baselines
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make the ABI research workspace runnable through the sibling ml-autoresearch harness. Complete and validate workspace configuration, build/reference the required runtime images, and document trusted data and baseline-weight provisioning so ABI-017 can run reproducibly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ml-autoresearch.toml contains valid, non-secret workspace, provider, candidate execution, and agent-boundary settings
- [x] #2 The required runner and agent images can be built and their resulting identities are documented in the workspace configuration or setup documentation
- [x] #3 Dataset and MCAST 1.1/2.1 weight paths are provisioned through explicit trusted host paths or links and are available at the paths expected by the provider and container runtime
- [x] #4 Harness setup/config validation and a bounded provider or candidate smoke run succeed without real model training
- [x] #5 A reproducible handoff documents commands and prerequisites for ABI-017 baseline evaluation on the GPU server
- [x] #6 Canonical MCAST 1.1/2.1 comparison targets are available for unfiltered evaluation and the approved Geographic Feature plus Scanline Artifact Filter pipeline, with validated machine-readable artifact locations consumable by candidate acceptance comparisons
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Treat the existing validated geographic-enabled MCAST 1.1/2.1 run as the source evaluation: its raw metric namespace is the unfiltered target and its filtered namespace is the approved Geographic Feature + Scanline Artifact Filter target.
2. Add a trusted generator/validator for a machine-readable canonical baseline-target registry that records immutable artifact roots, metric namespaces, split/sample identity, model hashes, workspace/Harness provenance, and both filter settings.
3. Configure the registry location in the local workspace config and document the portable template/operator refresh command without making tests depend on external data.
4. Add provider-side loading and acceptance-report integration so candidate raw metrics are compared to canonical unfiltered baselines and candidate filtered metrics to canonical filtered baselines, with target IDs and source paths in the report.
5. Generate and validate the canonical registry from the existing artifacts; verify raw parity and the recorded geographic/scanline filter state.
6. Add fixture-based tests, run focused/full uv-managed validation, document results, and complete ABI-021 only if all original setup criteria and the new canonical-target criterion are satisfied.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Investigation found the current docker_image is a copied GVCCS tag; `uv run ml-autoresearch build-runtime-images --workspace-root . --update-config` generates the ABI-specific tag and Agent image path.
- Current config cannot load the provider because research_problem.id is `abi_contrail_detection` while the provider returns `goes_abi_contrail_segmentation`.
- The ABI data config is incomplete: training requires layout/inputs_zarr/labels_zarr and Google metadata; the real MIT stores are zarr groups although the adapter currently opens MIT roots as arrays, and TOML cannot practically inline all Google metadata rows.
- The generic runner and agent images do not install zarr; a mounted ABI provider import currently fails in the runner. Agent-side static import can be made lightweight, but Candidate Execution still needs an explicit provider-runtime dependency solution.
- MCAST 1.1 is available through the production detection-1.1.pt symlink; MCAST 2.1 is available through /data/iross/mcast/assets/models/detection-2.1. The provider has an evaluation method but no operator CLI or Harness baseline operation yet.
- Workspace bootstrap state is incomplete (no research-ledger.jsonl, EXPERIMENT_INDEX.md, candidates/research-notes handoff directories), so prepare-agent-boundary cannot yet complete.
- ml-autoresearch.toml currently contains live notification credentials and is not ignored; remove/rotate credentials as appropriate and prevent accidental version-control inclusion before setup is committed.
- The harness validate-docker-gpu implementation currently takes --docker-image, despite docs showing --workspace-root; use the configured generated tag explicitly unless the harness CLI is fixed.

- Added baseline evaluation progress logging for dataset/model setup, inference rate and ETA, filtering, threshold sweeps, artifact writes, and completion.
- Pinned the optional baseline environment to PyTorch/torchvision CUDA 12.1 versions compatible with the GPU server driver.
- Full ABI test suite passes: uv run pytest -q (63 passed before the final logger-specific test; targeted logger tests also pass).
- Full baseline evaluations are intentionally deferred to the operator with a 75% CPU cap.

- Added canonical baseline-target registry generation/verification with atomic writes, artifact checksums, common sample/split checks, MCAST asset provenance, and effective Geographic Feature plus Scanline Artifact Filter settings.
- Generated and verified registry /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json (id abi-mcast-working-validation-v1; SHA-256 2239879ef352182aa3769e6ea1142bb641d297032efcc57923d5afcc69756489).
- Candidate acceptance reports now compare raw/dice against the unfiltered target and filtered/dice against the full Artifact Filter target, recording registry/run-manifest/aggregate paths.
- Working Validation Split identity: 3,088 samples (MIT 1,232; Google 1,856), sample-id SHA-256 42982774c168d6b9f24205de66972035e6eaa3a892c4752bc83230ad95a9c290.
- Canonical Dice targets: MCAST 1.1 raw 0.397901603 / filtered 0.384248340; MCAST 2.1 raw 0.399565414 / filtered 0.387284867. Scanline filtering was active but removed zero MCAST pixels.
- Validation passed: 93 tests, wheel build, runtime-image validation, prepare-agent-boundary, canonical-registry verification, configured acceptance-report smoke, and bounded Docker candidate smoke (accepted; no training).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the ABI ml-autoresearch runtime setup and canonical baseline handoff. The workspace now has validated ABI-specific runner/Agent image identities, trusted named training/ancillary/baselines roots, provisioned MCAST assets and Natural Earth data, bounded Docker smoke coverage, and reproducible baseline-evaluation documentation.

Added a trusted abi-baseline-targets generator/validator and produced /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json. The registry exposes unfiltered raw/* and full Geographic Feature + Scanline Artifact Filter filtered/* MCAST 1.1/2.1 targets, with sample identity, source split, model/filter/Git provenance, artifact locations, and checksums. Candidate acceptance reports load the configured registry automatically and record both comparisons and exact source paths.

Validation:
- uv run --group torch pytest -q (93 passed)
- uv build --wheel
- uv run ml-autoresearch validate-runtime-images --workspace-root .
- uv run ml-autoresearch prepare-agent-boundary --workspace-root .
- uv run abi-baseline-targets verify --registry /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json
- uv run python scripts/smoke_workspace.py --workspace-root . (accepted; trained=false)
- Configured canonical acceptance-report smoke (raw and filtered deltas 0.0 for MCAST 2.1)
- git diff --check
<!-- SECTION:FINAL_SUMMARY:END -->
