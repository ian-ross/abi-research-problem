---
id: ABI-017
title: Run MCAST baseline evaluations on GPU server
status: Done
assignee:
  - '@agent'
created_date: '2026-07-12 21:02'
updated_date: '2026-08-07 14:16'
labels:
  - baselines
  - evaluation
  - cluster
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Run the provider-owned MCAST detection 1.1 and 2.1 Baseline Segmenter evaluations on the GPU-enabled training server after ABI-013 implementation is merged. Record aggregate and per-sample baseline metrics as acceptance-gate comparison artifacts.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 MCAST 1.1 baseline evaluation is run with local detection-1.1.pt assets on the GPU server
- [x] #2 MCAST 2.1 baseline evaluation is run with local detection-2.1 directory assets on the GPU server
- [x] #3 Aggregate and per-sample raw/filtered metrics are stored for acceptance-gate comparison
- [x] #4 Run configuration, asset paths or asset provenance, commit SHA, and validation split configuration are documented
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Validate configured MIT/Google data paths and local MCAST 1.1/2.1 assets
2. Smoke-load both checkpoints and run one GPU inference patch
3. Run both provider-owned baseline validation evaluations on the combined Working Validation Split
4. Verify aggregate, per-sample, threshold-sweep, diagnostics, and provenance artifacts
5. Record metrics, commands, paths, validation split configuration, and commit SHA
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Smoke-loaded MCAST 1.1 and 2.1 and ran one 256x256 patch through each on the A100 with CUDA 12.1/PyTorch 2.5.1.
- The first combined full evaluation was aborted at operator request after it saturated all CPU cores; it produced no metric artifacts.
- Added timestamped CLI/file progress logging and documented commands that hard-cap CPU affinity and numerical thread pools to 75% while exposing only the A100.
- Awaiting operator-run full evaluations; keep this task In Progress until both artifact sets are verified.

- Verified completed artifacts under /data/iross/abi-ml-autoresearch/baselines/initial-20260807 for both MCAST versions.
- Both runs evaluated 3,088 samples (MIT 1,232; Google 1,856) on NVIDIA A100-PCIE-40GB with CPU affinity capped at 18/24 logical cores.
- MCAST 1.1 at threshold 0.42: Dice 0.3979016, precision 0.4519188, recall 0.3554189, clDice 0.5429516.
- MCAST 2.1 at threshold 0.314: Dice 0.3995654, precision 0.3448613, recall 0.4748965, clDice 0.1963650.
- Aggregate confusion totals match sums of all per-sample records; records are unique and finite; threshold sweeps, manifests, provenance hashes, and all diagnostic GeoTIFF references validate.
- Geographic ancillary data were not configured and the scanline filter removed zero pixels, so raw and filtered metrics are identical. These are intentionally the initial scanline-only targets; ABI-023 tracks geographic provisioning and replacement runs.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed trusted MCAST 1.1 and 2.1 GPU baseline evaluations over the combined 3,088-sample Working Validation Split (MIT 1,232; Google 1,856). Stored aggregate and per-sample raw/filtered metrics, 19-point threshold sweeps, bounded diagnostic GeoTIFFs, logs, split configuration, Git state, and checkpoint provenance under /data/iross/abi-ml-autoresearch/baselines/initial-20260807.

Primary results:
- MCAST 1.1: Dice 0.3979016, recall 0.3554189, clDice 0.5429516 at threshold 0.42
- MCAST 2.1: Dice 0.3995654, recall 0.4748965, clDice 0.1963650 at threshold 0.314

Validation:
- Parsed all 6,176 per-sample JSONL records; sample IDs unique and values finite
- Aggregate raw/filtered confusion counts equal summed per-sample counts
- Verified threshold sweep structure, artifact manifests, asset hashes, and all 32 diagnostic GeoTIFF references

Limitation:
- Natural Earth ancillary data were not configured and no scanline runs met removal criteria, so filtered metrics equal raw metrics. ABI-023 tracks geographic provisioning and replacement runs; ABI-022 uses these initial artifacts as acceleration parity targets.
<!-- SECTION:FINAL_SUMMARY:END -->
