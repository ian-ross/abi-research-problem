# ABI-371 temporal selective connectivity sidecar late36

ABI-371 is a mechanism-changing family-development continuation of ABI-350 for GOES ABI Contrail Segmentation. It keeps the provider-owned temporal `[-1, 0, 1]` ABI+Solar Geometry Input path and ABI-350 pre-decoder line-support U-Net, then adds a bounded high-resolution selective connectivity sidecar to the mask logits.

## Motivation

ABI-350 is a compact, high-precision temporal line-support comparator but leaves connected-line continuity below the strongest temporal diagnostic references. ABI-370 showed that topology-aware trusted loss can raise connectivity, but broadened predictions and reduced precision/source balance. ABI-371 tests whether an architecture sidecar can recover connected thin-line evidence while remaining spatially selective.

## Architecture

The model consumes only trusted `abi_16ch_plus_sza_temporal` tensors with `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

Main components:

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal BTD feature planes;
- shared per-frame embedding and per-pixel temporal attention;
- center/change fusion, U-Net encoder, and ASPP bottleneck;
- pre-decoder orientation-aware line-support gates on encoder skip scales;
- final decoder refinement with trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs;
- new `SelectiveConnectivitySidecar`, which computes orientation-line support from final features, combines it with decoder/skip detail evidence, predicts a soft selectivity gate, and adds a bounded residual to the base mask logits.

The sidecar is differentiable model architecture only. It is not thresholding, morphology, postprocessing, or an Artifact Filter.

## Contract boundaries

Candidate code does not implement data loading, temporal lookup, S3/NetCDF access, sample selection, target derivation, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest selects trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, constant learning rate, and batch size 2. The local budget request asks for the approved 36-epoch `late_improving` budget with exploratory fallback if denied.

## Expected evidence

ABI-371 produces capped temporal-eligible evidence only. Useful evidence would be higher connectivity than ABI-350 while keeping filtered Dice, MIT/Google source balance, precision, and predicted-positive footprint closer to ABI-350 than ABI-370.
