---
id: ABI-016
title: Add GeoTIFF diagnostics for filtered and unfiltered ABI predictions
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 16:34'
updated_date: '2026-07-13 11:16'
labels:
  - evaluation
  - filters
  - diagnostics
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Evaluation should save georeferenced diagnostic masks for samples where Artifact Filters remove predicted positives and for samples where filters have no hits, so humans can load outputs in GIS and spot-check filter behavior against coastline/river features and scanline artifacts.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Evaluation writes unfiltered prediction mask GeoTIFFs for selected validation samples
- [ ] #2 Evaluation writes filtered prediction mask GeoTIFFs for the same selected validation samples
- [ ] #3 Diagnostic sample selection includes at least one filter-hit case when available and at least one no-filter-hit case when available
- [ ] #4 GeoTIFFs contain georeferencing sufficient for GIS spot-checking against approved ancillary coastline/river data
- [ ] #5 Evaluation manifest records which filters hit, removed pixel counts/area, and relative paths to each GeoTIFF
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect evaluation/artifact filter code and existing tests to identify manifest/output extension points.
2. Add fixture-driven tests for diagnostic sample selection, GeoTIFF path manifest entries, and georeferencing metadata.
3. Implement GeoTIFF diagnostic writing for paired unfiltered/filtered prediction masks without candidate-side data-loading responsibility.
4. Run focused uv pytest tests, then update acceptance criteria and final task notes.
<!-- SECTION:PLAN:END -->
