# ABI-134 full-spectral BTD+SZA frequency-gated line U-Net BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate reuses ABI-076's provider-approved Solar Geometry Input frequency-gated line U-Net architecture and changes the trusted primary loss from `focal_tversky` to `bce_dice`.

The hypothesis is that BCE-Dice can temper ABI-076's SZA-driven recall/positive-area expansion while preserving more recall than the non-SZA BCE-Dice ABI-078 branch. The intended diagnostic is a cleaner default-threshold precision/connectivity profile than ABI-076 without reverting to ABI-078's lower-recall behavior.

## Contract boundaries

- Receives only `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input.
- Does not receive longitude, latitude, reconstructed coordinates, Dataset Source identity, or external data.
- Emits `mask_logits` and trusted auxiliary `centerline_logits`.
- Uses manifest-selected trusted `bce_dice` primary loss and `weighted_bce` centerline auxiliary loss.
- Leaves data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and lifecycle execution to provider/Harness code.

## Manifest choices

- Input mode: `abi_16ch_plus_sza`
- Primary loss: `bce_dice`
- Auxiliary target: `centerline`, output `centerline_logits`, trusted `weighted_bce`, weight 0.02
- Sampling policy: `combined_source_balanced`
- Augmentation policy: `random_mirroring`
- Optimizer: AdamW
- Learning rate: 0.0003
- Batch size: 4
- Max epochs: 12
- Scheduler: `constant_lr`

## Comparison targets

Primary controlled targets are ABI-076 (`run_20260828_080008_ce4819`) for the same SZA-aware architecture with focal-Tversky and ABI-078 (`run_20260828_094949_ad2af0`) for the same frequency-gated backbone with BCE-Dice but no SZA. Secondary references are ABI-068, ABI-066, and ABI-130 for aggregate Dice/source balance, precision/connectivity, and SZA-aware calibration context.
