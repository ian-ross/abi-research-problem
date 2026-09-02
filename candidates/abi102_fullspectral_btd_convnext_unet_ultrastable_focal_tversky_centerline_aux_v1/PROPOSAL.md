# ABI-102 full-spectral BTD ConvNeXt U-Net ultra-stable repair

## Hypothesis

This is a **repair candidate** for ABI-101, which failed with Harness-recorded `candidate_bug` non-finite gradients in `front_end.learned_mixer.0.weight` during Run `run_20260830_065055_ef616d`. The repaired hypothesis preserves the ABI-101 ConvNeXt-style depthwise large-kernel U-Net scout: broad residual context without multiplicative gates may shift the ABI-068/066 precision, recall, connectivity, and positive-area tradeoff. The targeted repair is to remove the specific learned front-end instability point, bound raw/BTD and internal activations, and lower learning rate while keeping the same provider-approved input, trusted loss, auxiliary target, sampling, augmentation, and main ConvNeXt encoder-decoder shape.

## Comparison Target

Primary comparison target: ABI-101's intended family-scout comparison target remains ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, the current strongest local representative-capped aggregate-Dice reference.

Secondary comparison targets: ABI-066, Run `run_20260827_230540_bf4ce3`, for precision/connectivity and positive-area discipline; ABI-085, Run `run_20260829_181201_01c5e7`, for lower-learning-rate focal-Tversky behavior; ABI-095, Run `run_20260830_012033_a62afb`, as evidence that deterministic bounded raw+BTD repairs can terminalize learned-mixer non-finite failures but may underpower some branches; and ABI-100, Run `run_20260830_055047_fb5c2f`, as recent precision/connectivity-forward negative evidence.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-102 requests only representative capped repair/family-scout evidence.

## Expected Effect

The minimum expected effect is finite, non-collapsed completion of the ConvNeXt-style scout after removing the learned front-end mixer that produced non-finite gradients. Deterministic bounded normalized ABI channels plus thermal BTD planes should preserve the spectral evidence used by ABI-101 without allowing a front-end 1x1 mixer to amplify gradients. Bounded ConvNeXt residual outputs and lower learning rate should reduce numerical risk while still allowing the depthwise large-kernel backbone to test whether modern residual context improves filtered precision, connectivity, or positive-area discipline relative to recent U-Net variants.

## Implementation Sketch

The model uses provider-approved `abi_16ch` input only. It constructs normalized ABI channels and explicit thermal brightness-temperature-difference planes from approved ABI channels, clamps them to a finite range, and removes ABI-101's learned 1x1 front-end mixer. The architecture remains a compact ConvNeXt-style U-Net: full-resolution stem, depthwise large-kernel residual blocks with GroupNorm and small learnable residual scale, three downsampling stages, a dilated bottleneck, bilinear decoder skip fusion, and high-resolution refinement. Internal activations are clamped in projection and residual blocks. The model emits `mask_logits` and provider-derived `centerline_logits`.

The manifest keeps trusted `combined_source_balanced` sampling, trusted `random_mirroring`, trusted `focal_tversky` primary loss, AdamW, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and a Centerline Target auxiliary output with trusted `weighted_bce` weight 0.02. The only training-policy change from ABI-101 is lowering learning rate from 0.0003 to 0.00005 to support finite repair evidence.

Candidate code does not implement data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, resource placement, filesystem writes, network calls, pretrained weights, or coordinate inputs.

## Contract Features Used

- Input mode: provider-approved `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Training policy: AdamW, learning rate 0.00005, batch size 4, max epochs 12, constant LR, disabled early stopping under the active Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. Because this is a repair for an unprofiled architecture family, no Experiment Batch, extra concurrency, GPU selection, candidate-owned scheduling, or full-data promotion evaluation is requested.

## Success Criteria

Useful repair/scout evidence would be any of:

- finite completion with no all-negative/all-positive prediction collapse and no recurrence of learned-front-end non-finite gradients;
- capped best `val/filtered_dice` within 0.03 of ABI-068 while improving filtered connectivity, filtered precision, or filtered predicted-positive fraction;
- capped best `val/filtered_dice` above ABI-066 while retaining source-stratified filtered Dice above 0.36 on both MIT and Google;
- filtered connectivity above 0.42 with aggregate filtered Dice above 0.37 and source behavior that is not catastrophically imbalanced;
- a late-improving finite trajectory that is source-balanced and diagnostically distinct enough to justify one ConvNeXt-family follow-up.

Hard stop evidence for this repaired branch would be smoke failure, non-finite training after the front-end repair, persistent prediction collapse, either Dataset Source below about 0.32 filtered Dice, aggregate filtered Dice below 0.35 with no late improvement, or a high-recall/low-precision positive-area expansion without a connectivity advantage.

## Fallback/Next Decision

If ABI-102 terminalizes and approaches ABI-068 while improving connectivity, precision, or positive-area discipline, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but below the useful scout floor, do not repeat ConvNeXt U-Net with another minor stability-only tweak; return to ABI-068/066 as references and broaden to another architecture or trusted policy axis. If it fails contract validation or smoke testing, classify the failure and repair only if the ConvNeXt depthwise-backbone hypothesis and comparison target are still preserved.
