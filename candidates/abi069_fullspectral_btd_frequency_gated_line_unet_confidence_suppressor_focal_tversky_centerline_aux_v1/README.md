# ABI-069 confidence-suppressor frequency-gated line U-Net

ABI-069 is a bounded family-development continuation of the full-spectral BTD frequency-gated line U-Net branch.

It starts from ABI-068's focal-Tversky, centerline-auxiliary architecture and replaces the direct mask head with a differentiable confidence-suppressor head. The head uses refined decoder features, local high-frequency detail, and broad smoothed context to learn a small suppressive logit term for low-confidence clutter. It does not implement thresholding, postprocessing, Artifact Filters, data loading, losses, target derivation, metrics, scheduling, or coordinate features.

## Contract summary

- Input: `abi_16ch` only; no longitude or latitude inputs.
- Spectral features: normalized ABI channels plus BTD planes derived only from ABI channels 1-16 and learned 1x1 channel mixing.
- Output: `mask_logits` plus trusted `centerline_logits` auxiliary output.
- Losses: trusted `focal_tversky` primary and trusted `weighted_bce` centerline auxiliary at weight 0.02.
- Data policy: provider/Harness-owned `combined_source_balanced`, `all_target_frames`, and `random_mirroring`.
- Training budget: batch size 4, 12 epochs, constant LR 0.0003, active representative cap and Harness-owned limits.

## Intended comparison

Compare primarily to ABI-068 (`run_20260828_010836_4ccc77`) for aggregate filtered Dice and recall-balanced behavior, and secondarily to ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity and negative-patch clutter control.
