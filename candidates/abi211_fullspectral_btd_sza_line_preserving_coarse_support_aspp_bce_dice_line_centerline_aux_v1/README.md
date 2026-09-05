# ABI-211 full-spectral BTD+SZA line-preserving coarse-support ASPP

ABI-211 is an exploratory family-development continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch for GOES ABI Contrail Segmentation.

## Hypothesis

Use broad decoder/stem/full-scale context as a bounded feature-space support cue while preserving the signed-detail thin-line stream. This should test whether representation-level clutter control can improve precision, positive-area discipline, or connectivity without repeating the recall/connectivity penalties from recent boundary, foreground-head, orientation-consensus, and spectral-support probes.

## Candidate boundary

- Uses provider-approved `abi_16ch_plus_sza` input only.
- Derives normalized ABI, BTD, and SZA/cos-SZA features inside the model from approved channels.
- Returns `mask_logits`, `line_logits`, and `centerline_logits` only.
- Selects trusted `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, constant LR, batch size 4, and Line/Centerline auxiliary weighted BCE via `manifest.yaml`.
- Does not implement data loading, target derivation, augmentation, sampling, losses, metrics, thresholding, Artifact Filters, postprocessing, coordinate features, runtime downloads, persistence writes, training loops, or resource scheduling.

## Architecture sketch

The model starts from the signed-detail ASPP/full-scale skip decoder lineage and replaces the parent cross-scale directional consensus bridge with `LinePreservingCoarseSupportBridge`:

1. Signed-detail residual features preserve local/mid-scale thin-line evidence.
2. Smoothed decoder, stem, and full-scale features form a coarse support cue.
3. A learned support gate modulates only an additive support branch.
4. The decoder/detail stream remains present, and the bridge residual is zero-initialized and bounded.
5. Base width is reduced to 34 to reduce exploratory wall-clock risk.

## Budget

Request one sequential exploratory capped Run under the active Harness limits: 12 epochs, batch size 4, 1,024 records per Dataset Source/split cap, constant scheduler, disabled early stopping, 25M parameter ceiling, 3,600-second Docker timeout, and fixed first_n prediction retention.
