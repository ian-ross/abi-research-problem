# ABI-101 full-spectral BTD ConvNeXt U-Net focal-Tversky centerline-auxiliary scout

## Hypothesis

This is a **family scout** for a compact full-spectral BTD ConvNeXt-style U-Net. ABI-068 remains the strongest local representative-capped frequency-gated reference, while ABI-066 remains the precision/connectivity-forward reference. Recent deterministic-shuffle, negative-bias, dense-detail, line-coherence, and large-kernel repairs did not improve the frequency-gated family's precision/connectivity tradeoff enough. The hypothesis is that modern depthwise large-kernel residual blocks can supply broad but stable context without the multiplicative feature gates that repeatedly expanded positive area or degraded connectivity.

## Comparison Target

Primary comparison target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, the current strongest local aggregate-Dice reference for the full-spectral BTD frequency-gated family.

Secondary comparison targets: ABI-066, Run `run_20260827_230540_bf4ce3`, for precision/connectivity and positive-area discipline; ABI-085, Run `run_20260829_181201_01c5e7`, for lower-learning-rate focal-Tversky behavior; ABI-098, Run `run_20260830_040621_bb9ebc`, as a recent negative dense-detail scout; and ABI-100, Run `run_20260830_055047_fb5c2f`, as the latest negative deterministic-shuffle clDice evidence.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-101 requests only representative capped family-scout evidence.

## Expected Effect

The expected effect is finite, non-collapsed learning with a less permissive positive-area profile than recent gate/refiner branches. Depthwise 7x7 ConvNeXt blocks should gather local cloud and line context while preserving stable residual optimization through small learnable residual scales. A useful scout would approach ABI-068's aggregate filtered Dice while improving filtered connectivity, filtered precision, or filtered predicted-positive fraction; a diagnostically useful negative result would show whether replacing frequency-gated hand-built refiners with a modern depthwise backbone shifts the precision/recall failure mode.

## Implementation Sketch

The model uses provider-approved `abi_16ch` input only. It constructs normalized raw ABI channels, explicit thermal brightness-temperature-difference planes from approved ABI channels, and a learned 1x1 spectral mixer. The architecture is a compact ConvNeXt-style U-Net: a full-resolution stem, depthwise large-kernel residual blocks with GroupNorm and learnable residual scale, three downsampling stages, a dilated bottleneck, bilinear decoder skip fusion, and a shallow high-resolution refinement head. It emits `mask_logits` and provider-derived `centerline_logits`.

The manifest keeps trusted `combined_source_balanced` sampling, trusted `random_mirroring`, trusted `focal_tversky` primary loss, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and a Centerline Target auxiliary output with trusted `weighted_bce` weight 0.02. Candidate code does not implement data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, resource placement, filesystem writes, network calls, pretrained weights, or coordinate inputs.

## Contract Features Used

- Input mode: provider-approved `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Training policy: AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant LR, disabled early stopping under the active Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. Because this is an unprofiled architecture family, no Experiment Batch, extra concurrency, GPU selection, candidate-owned scheduling, or full-data promotion evaluation is requested.

## Success Criteria

Useful scout evidence would be any of:

- capped best `val/filtered_dice` within 0.02 of ABI-068 while improving filtered connectivity or lowering filtered predicted-positive fraction;
- capped best `val/filtered_dice` above ABI-066 while retaining source-stratified filtered Dice above 0.36 on both MIT and Google;
- filtered connectivity above 0.42 with aggregate filtered Dice above 0.37 and no all-negative/all-positive prediction collapse;
- a late-improving finite trajectory that is source-balanced and diagnostically distinct enough to justify one ConvNeXt-family follow-up.

Hard stop evidence for this exact branch would be smoke failure, non-finite training, persistent prediction collapse, either Dataset Source below about 0.32 filtered Dice, aggregate filtered Dice below 0.35 with no late improvement, or a high-recall/low-precision positive-area expansion without a connectivity advantage.

## Fallback/Next Decision

If ABI-101 approaches ABI-068 while improving connectivity, precision, or positive-area discipline, request a bounded whole-validation failure-bucket diagnostic before any promotion interpretation. If it is finite but below the useful scout floor, do not repeat the ConvNeXt U-Net unchanged; return to ABI-068/066 as references and broaden to another architecture or trusted policy axis. If it fails contract validation or smoke testing, classify the failure and repair only if the ConvNeXt depthwise-backbone hypothesis is preserved.
