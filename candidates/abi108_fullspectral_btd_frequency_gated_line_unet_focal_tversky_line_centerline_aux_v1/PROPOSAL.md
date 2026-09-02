# ABI-108 full-spectral BTD frequency-gated line U-Net with line and centerline auxiliaries

## Hypothesis

A low-weight provider-derived Line Target auxiliary head can complement the existing Centerline Target auxiliary supervision in the ABI-068 full-spectral BTD frequency-gated line U-Net. The expected effect is to reinforce contiguous thin-line extent and reduce fragmented focal-Tversky masks without moving target derivation, loss computation, metrics, thresholding, or Artifact Filters into candidate code.

This is a family-development continuation of ABI-068. It broadens the recent same-family frontier from small gates, sampling swaps, and regularizers to a trusted auxiliary-target/loss-shaping mechanism that has not yet been tested on the frequency-gated focal-Tversky reference.

## Comparison Target

Primary comparison is ABI-068 (`run_20260828_010836_4ccc77`), the local aggregate filtered-Dice reference for the frequency-gated line U-Net family. Secondary comparison is ABI-066 (`run_20260827_230540_bf4ce3`), the same family BCE-Dice-clDice precision/connectivity reference.

## Expected Effect

Relative to ABI-068, ABI-108 should preserve recall and source balance while improving at least one of filtered Contrail Connectivity Metric, filtered precision, or filtered predicted-positive area discipline. Relative to ABI-066, it should test whether trusted Line Target supervision can recover some connectivity/precision without switching the focal-Tversky branch into ABI-066 lower-recall operating point.

## Implementation Sketch

Start from the ABI-068 architecture over provider-approved `abi_16ch` input. Preserve the normalized raw-channel, deterministic thermal-BTD, learned-mixer front end; frequency-split stem; residual encoder/decoder; frequency-pyramid fusion; and final mask head. Add one additional `line_logits` 1x1 auxiliary head beside the existing `centerline_logits` head. The model returns exactly `mask_logits`, `centerline_logits`, and `line_logits` as requested by the manifest.

No custom target construction, loss function, sampler, augmentation, threshold, postprocessing, Artifact Filter, training loop, filesystem write, network call, pretrained weight, longitude input, or latitude input is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch` only; longitude/latitude are not inputs
- Output form: `mask_logits`
- Primary loss: trusted `focal_tversky`
- Auxiliary targets: provider-derived `centerline` -> `centerline_logits` with trusted `weighted_bce` weight 0.02; provider-derived `line` -> `line_logits` with trusted `weighted_bce` weight 0.02
- Sampling policy: provider/Harness-owned `combined_source_balanced`
- Augmentation policy: trusted `random_mirroring`
- Optimizer/scheduler: `adamw`, constant learning rate

## Budget Requested

Use the current trusted representative cap and execution ceilings: 1,024 train and validation records per Dataset Source/split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, fixed first-four prediction retention, 25M-parameter smoke ceiling, A100 Docker execution, and sequential Harness scheduling.

## Success Criteria

Useful continuation evidence is any of:

- Aggregate `val/filtered_dice` within 0.01 of ABI-068 while improving filtered connectivity by at least 0.03 or filtered precision by at least 0.02.
- Aggregate `val/filtered_dice` exceeding ABI-068 by at least 0.005 without either Dataset Source dropping below 0.37 filtered Dice.
- Filtered Dice at least 0.382 with filtered connectivity at least 0.42, indicating movement toward ABI-066 connectivity regime while retaining stronger recall/source balance than typical clDice branches.

Hard-stop evidence for this exact branch is non-finite state, contract failure, persistent all-negative/all-positive predictions, aggregate filtered Dice below 0.34, either Dataset Source below 0.30 filtered Dice, or lower aggregate filtered Dice than ABI-107 without a compensating connectivity/precision gain.

## Fallback/Next Decision

If ABI-108 is useful but not promotion-grade, consider one bounded follow-up that adjusts only auxiliary weights or primary loss within existing allowlists. If it is finite but misses the success criteria, stop this line+centerline auxiliary branch and broaden away from local ABI-068 modifications toward a materially different calibration, architecture, or preprocessing hypothesis. Promotion decisions remain human-reviewed against canonical MCAST context and any later full-data evidence.
