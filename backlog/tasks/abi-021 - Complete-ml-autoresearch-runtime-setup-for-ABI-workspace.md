---
id: ABI-021
title: Complete ml-autoresearch runtime setup for ABI workspace
status: Done
assignee:
  - '@agent'
created_date: '2026-08-07 10:23'
updated_date: '2026-08-09 21:01'
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
- [x] #7 The canonical registry is self-contained beneath the canonical directory: all indexed MCAST artifacts are copied there and no registry artifact path depends on geographic-enabled-20260807-abi022-r2
- [x] #8 Canonical MCAST model assets are copied beneath the trusted baselines root; workspace configuration and canonical registry/evaluation metadata use contained relative paths and no canonical model-asset path points outside /data/iross/abi-ml-autoresearch/baselines
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Extend canonical generation to copy and checksum-verify MCAST 1.1/2.1 model assets into canonical/model-assets.
2. Rewrite canonical registry and copied evaluation metadata to use canonical-root-relative asset paths, then recompute artifact checksums and reject external/escaping asset paths during verification.
3. Resolve configured MCAST asset paths relative to the named baselines root and update local/template configuration and documentation.
4. Regenerate the canonical bundle, prove no external model paths remain, smoke-load both copied checkpoints, run full validation, and update ABI-021.
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

- Made the canonical bundle self-contained. Complete MCAST 1.1/2.1 evaluation directories now live under /data/iross/abi-ml-autoresearch/baselines/canonical, and registry artifact paths are canonical-root-relative.
- Removed source_evaluation_root from the registry schema and reject absolute or parent-escaping artifact paths during verification. The canonical bundle contains no geographic-enabled-20260807-abi022-r2 strings or runtime dependencies.
- Canonical generation now copies and checksum-verifies full baseline directories before atomic replacement; tests prove source changes do not affect canonical verification while canonical tampering is detected.
- Regenerated registry SHA-256: cf93781911c214f49e2086206749543163c68b592d23a6677739a9ed4925de16. Final validation: 94 tests passed, wheel build passed, registry verified.

- Copied MCAST 1.1 (57,397,165 bytes; SHA-256 0feba22e59c3922dd2bfc765ffc3acdf7d472aaacd3fae9cb22075014f0d5dff) and MCAST 2.1 (86,864,010 bytes; aggregate SHA-256 4c68c7b0c119618f0b6da1dea32583e5ff4230454aed76c80419479b9981f9ca) into canonical/model-assets.
- Named-root configuration now uses canonical/model-assets/detection-1.1.pt and canonical/model-assets/detection-2.1 relative to data_roots.baselines; absolute or parent-escaping paths are rejected.
- Canonical generation checksum-verifies copied model assets, rewrites canonical run manifests/aggregate metadata/registry paths, recomputes artifact checksums, and registry verification validates contained assets.
- No external model-asset paths remain in the canonical bundle or active repository configuration/documentation. Both copied models loaded successfully on CPU and were visible read-only at /data/baselines/canonical/model-assets in the runner container.
- Regenerated canonical registry SHA-256: dc7de95ce72ffdddbd6a8a58832ed63d3a00737bdebdc29a5fa52c28c97102a1. Final validation: 97 tests passed, wheel build, runtime-image validation, registry verification, and bounded Docker candidate smoke.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the ABI ml-autoresearch runtime setup and fully self-contained canonical baseline handoff. The canonical registry is /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json. Complete MCAST 1.1/2.1 evaluation artifacts and both required model assets now live beneath the same canonical directory.

All active workspace configuration, canonical registry, run-manifest, and evaluation-metadata model paths are contained relative paths beneath data_roots.baselines. Provider asset resolution rejects absolute or escaping paths when named roots are configured. Canonical generation copies and checksum-verifies model assets, rewrites copied metadata, and recomputes artifact checksums; registry verification validates both evaluation artifacts and model assets. Candidate acceptance reports continue to consume raw/* and fully filtered/* targets from canonical paths.

Validation:
- uv run --group torch pytest -q (97 passed)
- uv build --wheel
- uv run abi-baseline-targets verify --registry /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json
- Both copied MCAST models loaded successfully on CPU
- Runner-container /data/baselines model-asset visibility check passed with network disabled
- uv run ml-autoresearch validate-runtime-images --workspace-root .
- uv run python scripts/smoke_workspace.py --workspace-root . (accepted; trained=false)
- No external model paths in canonical bundle or active repository config/docs
- git diff --check
<!-- SECTION:FINAL_SUMMARY:END -->
