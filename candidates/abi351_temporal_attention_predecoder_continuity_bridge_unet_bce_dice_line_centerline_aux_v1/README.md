# ABI-351 temporal-attention pre-decoder continuity bridge

ABI-351 is an exploratory, mechanism-changing continuation of ABI-350 for GOES ABI Contrail Segmentation on provider-owned temporal ABI+SZA tensors.

## Hypothesis

ABI-350 validated temporal-attention pre-decoder line support but still left connected-line continuity and MIT-positive-tail undercoverage unresolved. ABI-351 keeps ABI-350's compact temporal-attention U-Net and adds a differentiable final continuity bridge before logits to reinforce continuous thin-line evidence at the fixed 0.5 threshold without Candidate-owned thresholding or postprocessing.

## Architecture

The model consumes `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. Candidate-visible features are finite normalized ABI bands, ABI-derived brightness-temperature differences, and Solar Geometry Input features per frame.

Main components:

- per-frame feature builder using only provider-approved ABI channels and Solar Geometry Input;
- lightweight temporal-attention/change stem over previous, center, and next frames;
- compact U-Net encoder with ASPP bottleneck;
- orientation-aware pre-decoder line-support gates for encoder skips;
- new `FinalContinuityBridge` that combines long horizontal/vertical strip context, dilated diagonal context, local context, and high-resolution skip evidence before all logits;
- trusted-compatible `mask_logits`, `line_logits`, and `centerline_logits` outputs.

The continuity bridge is model-internal differentiable architecture. It is not morphology, thresholding, postprocessing, calibration, target derivation, metric definition, or an Artifact Filter.

## Manifest policy

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `combined_source_balanced`, `temporal_eligible_center`, offsets `[-1, 0, 1]`, trusted `random_mirroring`.
- Loss: trusted `bce_dice` with trusted Line and Centerline weighted-BCE auxiliaries.
- Optimizer: AdamW, constant learning rate `0.0003`.
- Batch size: 2.
- Epochs: default exploratory 12.

## Comparison targets

Primary comparison is ABI-350 (`run_20260919_013306_9ca44e`), with ABI-324, ABI-223, and ABI-348 as temporal-eligible comparator roles.

## Boundary statement

Candidate code defines only the architecture and allowed manifest choices. It does not load data, inspect paths, select samples, implement temporal lookup, use longitude/latitude, use Dataset Source identity, define losses or metrics, implement augmentation, threshold predictions, postprocess masks, implement Artifact Filters, fetch weights, schedule resources, or own lifecycle behavior.
