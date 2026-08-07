---
id: ABI-024
title: Adopt named training and ancillary data roots
status: To Do
assignee: []
created_date: '2026-08-07 20:04'
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
- [ ] #1 Workspace configuration and the committed template declare logical training and ancillary Research Problem data roots, with root-relative provider paths that resolve to host directories natively and /data/training plus /data/ancillary in Docker
- [ ] #2 The ABI provider consumes the Harness-supplied data_roots mapping for dataset loading and ancillary resolution while preserving the legacy dataset_root/data_root path for existing native callers and tests
- [ ] #3 Natural Earth provisioning and verification can target the standalone ancillary root directly, and geographic_ancillary_manifest, coastline, and river paths resolve beneath that root without depending on a writable training dataset directory
- [ ] #4 Tests cover native and simulated-container named-root resolution, invalid or missing logical roots, legacy single-root compatibility, and the invariant that longitude/latitude remain unavailable to Candidate Experiment inputs
- [ ] #5 A bounded host and network-disabled container smoke validates the existing /data/iross/abi-ml-autoresearch/ancillary bundle without training, runtime downloads, or symlink-union data wrappers
- [ ] #6 Setup and operator documentation describes the named-root layout and ABI-022 baseline handoff; the disposable abi-023-smoke-data wrapper is removed once validation no longer depends on it
<!-- AC:END -->
