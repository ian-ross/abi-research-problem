# ABI-088 full-spectral BTD frequency-gated line U-Net SE-recalibrated focal-Tversky continuation

## Hypothesis

ABI-068 remains the strongest local capped frequency-gated line U-Net reference by aggregate filtered Dice, while ABI-066 remains the precision/connectivity-forward reference. Recent output-side heads, suppressors, extra auxiliary stacking, SZA input, no-auxiliary, low-learning-rate, and no-augmentation continuations did not improve ABI-068. A more targeted in-contract continuation is to keep ABI-068s loss, input, sampling, augmentation, and centerline auxiliary policy unchanged while adding low-capacity spectral-spatial feature recalibration inside the residual backbone.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. The hypothesis is that feature-block channel squeeze/excitation plus feature-space spatial recalibration can suppress diffuse cloud/background activations before they reach the decoder and mask head, improving precision/connectivity or predicted-positive discipline without the instability observed from late output-side consensus/suppression modules.

## Comparison Target

Primary comparison target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the strongest local capped aggregate-Dice frequency-gated reference and has whole-validation diagnostic support.

Secondary comparison targets are ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity-forward behavior, ABI-080 (`run_20260829_133850_54dd6e`) as the negative late multi-scale logit-consensus result, ABI-085 (`run_20260829_181201_01c5e7`) for low-learning-rate training-policy evidence, and ABI-087 (`run_20260829_193824_241e30`) for no-augmentation evidence. Canonical MCAST 2.1 remains promotion context, but this capped Run is family-development evidence rather than a full-data promotion claim.

## Expected Effect

The recalibrated residual blocks are expected to:

- preserve ABI-068s focal-Tversky recall and source-balanced aggregate-Dice strength;
- increase filtered precision or reduce filtered predicted-positive fraction by attenuating broad cloud/background activations in feature space;
- recover some ABI-066-like Contrail Connectivity by letting discriminative channels and thin spatial ridges survive through the encoder/decoder;
- avoid the late-head failure mode seen in ABI-080 because recalibration is distributed through feature extraction rather than imposed only at the final logits;
- remain resource-safe because squeeze/excitation and one-channel spatial gates add few parameters relative to the ABI-068 backbone.

## Implementation Sketch

Start from the ABI-068 architecture: provider-approved `abi_16ch` input only, normalized raw ABI channels, explicit thermal brightness-temperature differences derived only from ABI channels 1-16, learned 1x1 spectral mixing, high/low spatial-frequency stem, low-frequency-gated skip fusion, multi-dilation coarse context, full-resolution frequency-pyramid fusion, oriented high-frequency line refiner, primary `mask_logits`, and provider-derived `centerline_logits`.

The controlled code change adds `SpectralSpatialRecalibration` to residual blocks. It computes a channel gate from adaptive average pooled learned features and a spatial gate from learned feature mean/max summaries, then scales the residual activation in feature space. It does not use longitude, latitude, scene metadata, thresholds, target labels, prediction masks, raw data paths, or Artifact Filters.

## Contract Features Used

- Input mode: `abi_16ch`; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, A100 execution under Harness policy, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, full-data run, or custom data-policy request is made.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` matching or exceeding ABI-068s 0.3964 while staying finite and non-degenerate;
- capped best `val/filtered_dice` within about 0.01 of ABI-068 while improving filtered precision above 0.41, Contrail Connectivity above 0.40, or filtered predicted-positive fraction below ABI-068s 0.00357 without recall collapse;
- both MIT and Google filtered Dice above 0.35 with a late-improving or stable trajectory and no all-negative/all-positive collapse;
- a clearly better precision/connectivity tradeoff than ABI-080/087, showing that distributed feature recalibration is preferable to late output-side refinement or removing augmentation.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, aggregate filtered Dice below 0.33 without late improvement, or an ABI-080-like loss of both precision and connectivity with no positive secondary signal.

## Fallback/Next Decision

If ABI-088 improves or closely ties ABI-068 while recovering precision/connectivity or positive-area discipline, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it underperforms ABI-068 but shows a distinctive precision/connectivity gain, keep it as a possible conservative-operating-point reference. If it simply repeats the late-head or no-augmentation regressions, stop this SE-recalibration branch and broaden to a materially different in-contract architecture or trusted data/training-policy axis rather than stacking more gates or moving provider-owned behavior into Candidate code.
