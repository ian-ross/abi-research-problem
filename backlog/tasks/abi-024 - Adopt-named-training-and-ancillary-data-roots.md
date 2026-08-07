---
id: ABI-024
title: Adopt named training and ancillary data roots
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-07 20:04'
updated_date: '2026-08-07 20:27'
labels:
  - provider
  - configuration
  - containers
  - data
  - tests
dependencies:
  - ABI-023
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Integrate the Harness named Research Problem Data Root contract into the ABI provider so the primary training dataset and separately provisioned Natural Earth bundle are available through distinct trusted host directories and deterministic read-only container mounts. Remove the production need for dataset-root symlinks or the ABI-023 smoke wrapper while preserving legacy single-dataset-root compatibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Workspace configuration and the committed template declare logical training and ancillary Research Problem data roots, with root-relative provider paths that resolve to host directories natively and /data/training plus /data/ancillary in Docker
- [x] #2 The ABI provider consumes the Harness-supplied data_roots mapping for dataset loading and ancillary resolution while preserving the legacy dataset_root/data_root path for existing native callers and tests
- [x] #3 Natural Earth provisioning and verification can target the standalone ancillary root directly, and geographic_ancillary_manifest, coastline, and river paths resolve beneath that root without depending on a writable training dataset directory
- [x] #4 Tests cover native and simulated-container named-root resolution, invalid or missing logical roots, legacy single-root compatibility, and the invariant that longitude/latitude remain unavailable to Candidate Experiment inputs
- [x] #5 A bounded host and network-disabled container smoke validates the existing /data/iross/abi-ml-autoresearch/ancillary bundle without training, runtime downloads, or symlink-union data wrappers
- [x] #6 Setup and operator documentation describes the named-root layout and ABI-022 baseline handoff; the disposable abi-023-smoke-data wrapper is removed once validation no longer depends on it
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the committed ml-autoresearch named-root provider contract and trace every ABI dataset, baseline, ancillary, CLI, and evaluation path that currently assumes dataset_root.
2. Add one trusted ABI data-config normalization seam that resolves logical training and ancillary roots for native and container execution, preserves legacy dataset_root/data_root callers, and keeps candidate input specifications free of longitude/latitude.
3. Update ancillary provisioning and geographic bundle resolution so the installed manifest and GeoJSON files are relative to the standalone ancillary root; update workspace configuration/template to use training and ancillary named roots without a symlink union.
4. Add focused tests for host and /data mappings, missing/invalid roots, legacy compatibility, standalone provisioning, evaluation provenance, and candidate-boundary invariants.
5. Validate the existing provisioned ancillary bundle on the host and in a network-disabled runner container with a bounded geographic-filter smoke; do not run full baselines or model training in this task.
6. Update operator documentation and the ABI-022 handoff, remove the disposable abi-023-smoke-data wrapper after validation, run the full uv-managed test suite, and record validation/provenance in the task.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added a central ABI named-root normalization seam for Harness data_roots, with training/ancillary resolution, contained root-relative paths, and legacy dataset_root/data_root compatibility.
- Updated training, profile, ancillary, baseline, smoke, and post-run evaluation paths; standalone ancillary provisioning now supports --ancillary-root and preserves the legacy CLI alias.
- Updated local/template configuration for training and ancillary roots, added SciPy to runner requirements, rebuilt and validated runtime images, and retired the ABI-023 wrapper report.
- Host and --network none runner-container smokes both passed on one ABI validation Patch with 588 geographic pixels removed, no training/downloads, and no longitude/latitude Candidate inputs.
- Full validation: uv run --group torch pytest -q (83 passed); uv build --wheel; uv run ml-autoresearch validate-runtime-images --workspace-root .
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented Harness named Research Problem data roots for ABI training and ancillary data. Added trusted root normalization and path containment, migrated dataset/evaluation/baseline/profile/smoke flows to Harness-supplied data_roots, preserved legacy single-root callers, enabled direct Natural Earth provisioning under the ancillary root, and documented the ABI-022 handoff. Added SciPy to the runner runtime and replaced the disposable ABI-023 wrapper smoke with host and network-disabled named-mount validation.

Validation:
- uv run --group torch pytest -q (83 passed)
- uv build --wheel
- uv run ml-autoresearch build-runtime-images --workspace-root . --update-config
- uv run ml-autoresearch validate-runtime-images --workspace-root .
- uv run abi-provision-natural-earth --ancillary-root /data/iross/abi-ml-autoresearch/ancillary --verify-only
- uv run abi-geographic-filter-smoke --workspace-root . --max-samples 64 (1 Patch, 588 pixels removed)
- Docker runner smoke with --network none and read-only /data/training plus /data/ancillary mounts (1 Patch, 588 pixels removed, no training/downloads)
<!-- SECTION:FINAL_SUMMARY:END -->
