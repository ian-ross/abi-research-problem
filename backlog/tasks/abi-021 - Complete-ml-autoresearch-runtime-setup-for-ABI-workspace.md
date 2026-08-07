---
id: ABI-021
title: Complete ml-autoresearch runtime setup for ABI workspace
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-07 10:23'
updated_date: '2026-08-07 11:29'
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
- [ ] #1 ml-autoresearch.toml contains valid, non-secret workspace, provider, candidate execution, and agent-boundary settings
- [ ] #2 The required runner and agent images can be built and their resulting identities are documented in the workspace configuration or setup documentation
- [ ] #3 Dataset and MCAST 1.1/2.1 weight paths are provisioned through explicit trusted host paths or links and are available at the paths expected by the provider and container runtime
- [ ] #4 Harness setup/config validation and a bounded provider or candidate smoke run succeed without real model training
- [ ] #5 A reproducible handoff documents commands and prerequisites for ABI-017 baseline evaluation on the GPU server
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the ABI provider, current workspace config, data/weight path assumptions, and existing baseline interfaces
2. Inspect ml-autoresearch configuration, image-build, setup, smoke, candidate-run, and trusted-artifact documentation and code
3. Compare with the sibling gvccs workspace pattern and identify ABI-specific differences
4. Produce an exact setup/run sequence, flag missing code or configuration, and separate this setup task from ABI-017 GPU baseline execution
5. After approval, implement only the agreed setup changes and run bounded validation
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
<!-- SECTION:NOTES:END -->
