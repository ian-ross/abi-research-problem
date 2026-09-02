# ABI-055 Full-Spectral BTD High-Resolution Line U-Net Directional Refiner + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-055 is a controlled architecture-level continuation of the high-resolution line U-Net family after ABI-053 and ABI-054. It keeps the approved full-spectral BTD front end, trusted primary loss, low-weight trusted Centerline Target auxiliary policy, data policy, augmentation policy, optimizer, learning rate, batch size, and 12-epoch capped execution request. The intended change is replacing the isotropic full-resolution line refiner with a directional continuity refiner inside the model architecture.

## Hypothesis

ABI-053 remains the current local capped best by primary `val/filtered_dice`: Run `run_20260827_134629_3ace34` reached best filtered Dice 0.3221 with MIT/Google filtered Dice 0.3119/0.3467, filtered precision 0.3005, filtered recall 0.3472, and filtered connectivity 0.2347. ABI-054 increased the Centerline Target auxiliary weight to 0.05, but Run `run_20260827_142319_ec8c29` reduced best filtered Dice to 0.3160 and did not recover connectivity, suggesting that simply strengthening the provider-derived auxiliary objective over-regularizes predictions rather than solving the continuity trade-off.

Thin contrails often require preserving elongated evidence at full resolution. A model-internal directional refiner using horizontal and vertical elongated kernels may improve continuity, precision/recall balance, or checkpoint stability without moving Artifact Filters, skeletonization, thresholding, target derivation, or metric logic into candidate code. Returning to the ABI-053 auxiliary weight 0.02 isolates the architecture-level continuity-path change from ABI-054's stronger auxiliary regularization.

## Comparison Target

The primary comparison target is ABI-053 `abi053_fullspectral_btd_hrline_unet_cldice_centerline_aux_v1`, Run `run_20260827_134629_3ace34`: best epoch 9, capped filtered Dice 0.3221, MIT/Google filtered Dice 0.3119/0.3467, filtered precision 0.3005, filtered recall 0.3472, filtered connectivity 0.2347, and filtered predicted-positive fraction 0.00419; final epoch filtered Dice 0.3152 with filtered connectivity 0.3019.

Secondary references are ABI-054 `run_20260827_142319_ec8c29` (same family with centerline weight 0.05; best filtered Dice 0.3160, filtered connectivity 0.2046, precision 0.3329, recall 0.3006) and ABI-052 `run_20260827_131644_b76d09` (DeepLabV3+ BTD + `bce_dice_cldice` + centerline weight 0.02; filtered Dice 0.2214, connectivity 0.3391). Canonical MCAST 2.1 filtered Dice 0.3873 remains full-validation promotion context only; this capped Run is not promotion-grade evidence.

## Expected Effect

If the high-resolution line U-Net's continuity trade-off is partly architectural, ABI-055 should recover ABI-053-like capped filtered Dice and recall while improving filtered connectivity, final-epoch stability, precision/recall balance, source balance, or predicted-positive fraction. A favorable result would tie or improve ABI-053 filtered Dice, or remain close while improving the targeted continuity/stability diagnostics. A negative but useful result would show that axis-aligned elongated full-resolution kernels do not address the trade-off, redirecting the family toward other skip-fusion, decoder-scale, or calibration hypotheses.

## Implementation Sketch

- Reuse the ABI-053/054 approved input and training policy: normalized approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Keep the high-resolution U-Net-style residual encoder, coarsest-scale multi-dilation context, bilinear gated skip decoder, primary `mask_logits` head, and auxiliary `centerline_logits` head.
- Replace the previous full-resolution isotropic local/dilation-2/dilation-4 line refiner with a directional continuity refiner containing horizontal and vertical 1x7, 7x1, 1x15, and 15x1 convolution branches, a 1x1 directional projection, and a learned feature-fusion gate.
- The refiner remains model-internal feature computation only. It does not threshold, filter, skeletonize, postprocess, construct targets, compute losses, compute metrics, or inspect dataset metadata.
- Declare the provider-derived `centerline` auxiliary target with `weighted_bce` loss and weight 0.02, matching ABI-053 and avoiding the ABI-054 over-regularization signal.
- Keep trusted `bce_dice_cldice`, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run; no Experiment Batch, concurrency request, candidate-owned scheduling, or resource workaround is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, sampling policy, augmentation, target derivation, losses, metrics, artifact filtering, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, checkpoints, and both output heads remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-053, the continuation is extension-positive if it credibly ties or improves capped filtered Dice while improving filtered connectivity, final-epoch stability, source balance, precision/recall balance, or predicted-positive fraction. It is also useful if it clearly establishes that this directional refiner worsens the high-resolution line U-Net trade-off.

## Continuation and hard stop

Do not require ABI-055 to beat canonical MCAST 2.1, because this is capped family-development evidence. Continue the high-resolution line U-Net family if ABI-055 remains finite, non-degenerate, source-informative, and improves any targeted stability/connectivity trade-off without a large Dice/recall collapse. Do not repeat this exact directional-refiner branch if it shows persistent non-finite behavior, resource failure, persistent prediction collapse, clear optimization failure, severe Dataset Source collapse, or a decisive drop in both aggregate Dice and the targeted continuity/stability diagnostics.

## Fallback/Next Decision

If ABI-055 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but sacrifices too much recall or Dice, document the result and broaden within the architecture family toward skip-fusion or decoder-scale changes rather than another simple centerline-weight adjustment. If it unexpectedly exceeds the current capped family best and remains source-balanced, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
