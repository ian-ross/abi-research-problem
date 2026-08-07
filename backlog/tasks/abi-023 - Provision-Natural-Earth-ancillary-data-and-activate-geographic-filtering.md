---
id: ABI-023
title: Provision Natural Earth ancillary data and activate geographic filtering
status: To Do
assignee: []
created_date: '2026-08-07 11:58'
updated_date: '2026-08-07 14:16'
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
- [ ] #1 An explicit idempotent operator command provisions the approved Natural Earth 1:10m coastline and North America river datasets under the trusted external data root; evaluation remains offline and performs no runtime downloads
- [ ] #2 Ancillary source versions, immutable download URLs, licenses, file sizes, and SHA-256 checksums are pinned and recorded in a provenance manifest
- [ ] #3 Research Problem configuration supports durable dataset-root-relative ancillary paths and resolves them correctly for both host baseline evaluation and Harness-owned container evaluation
- [ ] #4 Evaluation emits a clear error when required geographic ancillary data are missing or invalid, rather than silently applying an empty Geographic Feature Filter
- [ ] #5 Run manifests and filter diagnostics record whether geographic filtering was active plus the ancillary dataset identities and checksums
- [ ] #6 Tests and a bounded integration smoke check demonstrate that coastline/river geometry is rasterized onto ABI geolocation grids and removes overlapping predicted-positive pixels without exposing longitude or latitude to candidate models
- [ ] #7 The initial MCAST artifacts are documented as scanline-only, and replacement MCAST 1.1/2.1 artifacts are generated or handed off with the Geographic Feature Filter active
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- ABI-017 initial runs are complete and verified as scanline-only targets. Geographic availability was false for all 6,176 per-sample records; the scanline filter removed zero pixels at operational thresholds and raw/filtered threshold curves were identical across all 19 thresholds.
- Initial artifacts are under /data/iross/abi-ml-autoresearch/baselines/initial-20260807 and must remain distinguishable from future geographic-enabled replacement artifacts.
<!-- SECTION:NOTES:END -->
