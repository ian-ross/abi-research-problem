# ABI-349 temporal-attention pre-decoder line-support U-Net

ABI-349 is an exploratory temporal-attention family-development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-345 showed that final-head center-detail sharpening can raise recall but loses compact connected-line behavior. ABI-348 and related temporal C4 final-head blends likewise separate aggregate Dice from thin-line continuity. ABI-349 moves the line mechanism earlier: orientation-aware line support is gated into encoder skip features before decoder fusion, so the decoder can form continuous center-frame evidence before the final mask logits.

## Architecture

The model preserves an ABI-223/238-style compact temporal-attention U-Net:

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal brightness-temperature-difference features;
- shared per-frame embedding and per-pixel temporal attention over `[-1, 0, 1]`;
- center/change fusion, U-Net encoder, and ASPP bottleneck;
- three decoder stages with skip fusion;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

The ABI-349 change is `PreDecoderLineSupportGate` at encoder skip scales 2, 1, and 0. Each gate computes horizontal, vertical, and dilated diagonal line-support features from the skip, combines them with the current coarser decoder/context state, and applies a bounded learned gate to update the skip before decoder fusion.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, and constant learning rate under the exploratory budget.

## Expected evidence

ABI-349 should be interpreted as capped temporal-eligible exploratory evidence, not whole-validation promotion evidence. Useful signals would include finite non-collapsed training, improved recall/connectivity balance versus ABI-345, and a compact predicted-positive footprint closer to ABI-223/238 than broad recall-sidecar branches.
