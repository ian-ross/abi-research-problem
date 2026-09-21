# ABI-350 temporal-attention pre-decoder line-support late36

ABI-350 is a late-improving family-development continuation of ABI-349 for GOES ABI Contrail Segmentation. It preserves the ABI-349 architecture and consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-349 showed the pre-decoder line-support mechanism is viable under the exploratory budget: it was finite, compact, source-informative, best at epoch 12, and ahead of historical temporal-attention comparators at the same epoch. The remaining question is whether longer training lets the same mechanism close the recall and connectivity gaps to late-budget ABI-223/238 without becoming another broad final-head recall residual.

## Architecture

The model is intentionally unchanged from ABI-349:

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal brightness-temperature-difference features;
- shared per-frame embedding and per-pixel temporal attention over `[-1, 0, 1]`;
- center/change fusion, U-Net encoder, and ASPP bottleneck;
- `PreDecoderLineSupportGate` modules at encoder skip scales 2, 1, and 0, using horizontal, vertical, and dilated diagonal line-support branches before decoder fusion;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, and constant learning rate. A candidate-local budget request asks the Harness for the approved late-improving 36-epoch budget with exploratory fallback if denied.

## Expected evidence

ABI-350 is capped temporal-eligible evidence, not whole-validation promotion evidence. Success means the late-budget continuation improves over ABI-349 and approaches ABI-223/238 recall/connectivity while preserving the compact predicted-positive footprint that made ABI-349 promising at epoch 12.
