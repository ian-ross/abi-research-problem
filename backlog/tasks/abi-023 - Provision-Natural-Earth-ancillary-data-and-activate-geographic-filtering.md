---
id: ABI-023
title: Provision Natural Earth ancillary data and activate geographic filtering
status: Done
assignee:
  - '@agent'
created_date: '2026-08-07 11:58'
updated_date: '2026-08-07 14:54'
labels:
  - evaluation
  - filters
  - data
  - provisioning
dependencies:
  - ABI-017
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Close the ABI-007 provisioning gap by adding an explicit, reproducible operator setup path for the approved Natural Earth 1:10m coastline and North America river data, configuring trusted host/container evaluation to use it, and making geographic-filter availability and provenance unambiguous. Downloads must occur during explicit workspace setup, never during candidate execution or evaluation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 An explicit idempotent operator command provisions the approved Natural Earth 1:10m coastline and North America river datasets under the trusted external data root; evaluation remains offline and performs no runtime downloads
- [x] #2 Ancillary source versions, immutable download URLs, licenses, file sizes, and SHA-256 checksums are pinned and recorded in a provenance manifest
- [x] #3 Research Problem configuration supports durable dataset-root-relative ancillary paths and resolves them correctly for both host baseline evaluation and Harness-owned container evaluation
- [x] #4 Evaluation emits a clear error when required geographic ancillary data are missing or invalid, rather than silently applying an empty Geographic Feature Filter
- [x] #5 Run manifests and filter diagnostics record whether geographic filtering was active plus the ancillary dataset identities and checksums
- [x] #6 Tests and a bounded integration smoke check demonstrate that coastline/river geometry is rasterized onto ABI geolocation grids and removes overlapping predicted-positive pixels without exposing longitude or latitude to candidate models
- [x] #7 The initial MCAST artifacts are documented as scanline-only, and replacement MCAST 1.1/2.1 artifacts are generated or handed off with the Geographic Feature Filter active
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define the trusted ancillary-data contract: add a committed Natural Earth provenance manifest with pinned dataset/version identities, immutable download URLs, public-domain/license references, expected filenames, byte sizes, and SHA-256 checksums; keep downloaded vectors outside the repository and prohibit evaluation-time network access.
2. Add an explicit uv-run operator provisioning command that installs both approved GeoJSON datasets beneath a dataset-root-relative ancillary directory, verifies hashes and sizes before atomic replacement, is idempotent for already-valid files, and emits the installed manifest/provenance.
3. Centralize trusted ancillary configuration and validation: resolve configured manifest/coastline/river paths relative to dataset_root, support the same relative values after the Harness rewrites dataset_root to /data, and fail before evaluation when geographic filtering is required but files, identities, sizes, or checksums are invalid. Update the committed TOML template and local setup documentation.
4. Activate the provider-owned Geographic Feature Filter with the validated ancillary bundle. Keep longitude/latitude available only through trusted filter_context, distinguish ancillary availability/activation from whether a particular ABI Patch intersects a feature, and preserve a stable raster-mask interface for ABI-022 without moving filtering into candidate code.
5. Propagate geographic-filter state and ancillary provenance into per-sample filter diagnostics, baseline evaluation metadata, and run manifests, including explicit inactive/error reasons where applicable. Document the existing initial-20260807 MCAST artifacts as scanline-only.
6. Add tiny deterministic tests for provisioning/idempotency, checksum and missing-data failures, dataset-root-relative host and simulated /data resolution, LineString/MultiLineString rasterization and buffered filter hits on ABI-style longitude/latitude grids, provenance serialization, and the candidate boundary that excludes longitude/latitude.
7. Add and run a bounded operator integration smoke that uses configured real ancillary files plus a small number of ABI validation patches and an all-positive trusted prediction to prove geographic pixels are rasterized and removed without training or exposing coordinates to a candidate.
8. Run focused and full uv-managed validation, then create the ABI-023 operator handoff for geographic-enabled MCAST 1.1/2.1 replacement artifacts. Defer the expensive full rerun to the ABI-022 accelerated evaluator unless explicitly requested; record exact provisioning, smoke, and later rerun commands and output-root naming so replacement artifacts cannot be confused with initial scanline-only results.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- ABI-017 initial runs are complete and verified as scanline-only targets. Geographic availability was false for all 6,176 per-sample records; the scanline filter removed zero pixels at operational thresholds and raw/filtered threshold curves were identical across all 19 thresholds.
- Initial artifacts are under /data/iross/abi-ml-autoresearch/baselines/initial-20260807 and must remain distinguishable from future geographic-enabled replacement artifacts.

- Added pinned Natural Earth v5.1.2 source manifest and idempotent provision/verify CLI; evaluation-side resolution is offline and checksum-strict.
- Added dataset-root-relative host/container resolution, required-data failures, active/intersection diagnostics, and run/baseline provenance.
- Bounded real-data smoke passed on 1 ABI validation patch: 16 candidate channels, 588 rasterized/removed geographic pixels, no longitude/latitude candidate exposure. A network-disabled runner-container smoke resolved the same bundle at /data.
- The production dataset root is not writable by the current operator. Provisioning and geographic-enabled MCAST replacement runs are handed off in evaluation-requests/abi-023-geographic-enabled-mcast-baselines.md; the initial-20260807 artifacts are documented as scanline-only.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented trusted Natural Earth ancillary provisioning and Geographic Feature Filter activation. Added a pinned v5.1.2 provenance manifest, atomic/idempotent provision and offline verification commands, dataset-root-relative host/container resolution, strict missing/hash failures, filter and run-manifest provenance, bounded real-ABI and container smoke validation, and replacement-baseline handoff documentation.

Validation:
- uv run --group torch pytest -q (70 passed)
- uv build --wheel (passed; pinned manifest included)
- uv run abi-provision-natural-earth --dataset-root /data/iross/abi-ml-autoresearch/abi-023-smoke-data --verify-only
- uv run abi-geographic-filter-smoke --workspace-root . --dataset-root /data/iross/abi-ml-autoresearch/abi-023-smoke-data --max-samples 64 (passed; 588 pixels rasterized/removed)
- Network-disabled runner-container /data manifest resolution smoke (passed)
<!-- SECTION:FINAL_SUMMARY:END -->
