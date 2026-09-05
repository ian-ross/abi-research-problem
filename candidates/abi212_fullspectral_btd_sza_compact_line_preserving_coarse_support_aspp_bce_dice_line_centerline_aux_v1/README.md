# ABI-212 compact full-spectral BTD+SZA line-preserving coarse-support ASPP

ABI-212 is a resource-safe family-development continuation after ABI-211 (`run_20260904_162059_678c48`) exhausted the 3,600-second exploratory wall-clock budget late in epoch 12. It keeps the ABI-211 hypothesis but compacts the architecture so the Harness can obtain a complete 12-epoch capped Result.

## Hypothesis

ABI-211 produced finite, source-informative partial validation through epoch 11 and reached 0.3778 filtered Dice at epoch 9, but its line-preserving coarse-support bridge was too slow. ABI-212 tests whether the same bounded feature-space support idea remains useful when made smaller and cheaper: broad decoder/stem/full-scale support is only an additive residual cue, while signed-detail and line-refinement streams remain present.

## Candidate boundary

- Uses provider-approved `abi_16ch_plus_sza` input only; longitude and latitude are excluded and not reconstructed.
- Derives normalized ABI, thermal BTD, SZA, and cos-SZA features only from approved input channels.
- Returns `mask_logits`, `line_logits`, and `centerline_logits` only.
- Selects trusted `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, constant LR, batch size 4, and Line/Centerline auxiliary weighted BCE via `manifest.yaml`.
- Does not implement data loading, target derivation, augmentation, sampling, losses, metrics, thresholding, Artifact Filters, postprocessing, coordinate features, runtime downloads, persistence writes, training loops, or resource scheduling.

## Architecture sketch

Relative to ABI-211, ABI-212 makes resource-oriented architecture-only changes:

1. Reduces the learned front-end projection from 16 to 12 channels.
2. Reduces the base width from 34 to 28.
3. Reduces full-scale fusion branch width from 16 to 12.
4. Replaces high-resolution directional convolutions in the final refiner and bridge with depthwise directional convolutions.
5. Simplifies the coarse-support bridge from six fused feature groups to five while keeping zero-initialized bounded residual addition.

## Budget

Request one sequential exploratory capped Run under the active Harness limits: 12 epochs, batch size 4, 1,024 records per Dataset Source/split cap, constant scheduler, disabled early stopping, 25M parameter ceiling, 3,600-second Docker timeout, and fixed first_n prediction retention. No late-improving budget is requested.
