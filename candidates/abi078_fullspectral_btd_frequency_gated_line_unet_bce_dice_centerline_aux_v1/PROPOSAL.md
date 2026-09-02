# ABI-078 full-spectral BTD frequency-gated line U-Net BCE-Dice continuation

## Hypothesis

ABI-068 is the strongest local whole-validation-tested Candidate by primary filtered Dice, but its improvement over ABI-066 is recall-forward: it raises true-positive coverage while giving back precision, Contrail Connectivity, and negative-patch clutter control. Several subsequent ABI-068 extensions that added late refiners, gates, suppressors, SZA input, extra auxiliary heads, or axial/oriented modules failed to improve the operating point. A simpler in-contract continuation is to keep the ABI-068 architecture and centerline auxiliary target unchanged while changing only the trusted primary loss from `focal_tversky` to `bce_dice`.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. It is not a full-data promotion claim. The expected value is to test whether the less recall-aggressive BCE-Dice loss can retain much of ABI-068s aggregate/source-balanced Dice while moving the operating profile back toward ABI-066s stronger precision/connectivity and lower predicted-positive burden.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested frequency-gated Candidate by aggregate filtered Dice.

Secondary local target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it is the precision/connectivity-forward reference for this branch. ABI-076 and ABI-077 provide recent negative evidence that extra input/refiner capacity mostly pushes the branch toward higher recall and more predicted-positive area. Canonical MCAST 2.1 remains the promotion context, but this capped Run is feasibility and family-development evidence only.

## Expected Effect

Changing only the primary loss to BCE-Dice is expected to:

- reduce ABI-068s recall-forward pressure and predicted-positive fraction without introducing candidate-owned thresholds or postprocessing;
- recover some filtered precision and Contrail Connectivity toward ABI-066 while preserving a source-balanced, non-collapsed trajectory;
- test whether ABI-068s precision/connectivity loss is primarily loss-driven rather than architecture-limited;
- avoid the resource and clutter penalties observed when adding late refiners, suppressor heads, boundary stacking, SZA input, axial necks, or heavy steerable/oriented context;
- provide a controlled comparison because architecture, input mode, sampling policy, augmentation, optimizer, learning rate, batch size, epoch budget, and centerline auxiliary weight are unchanged from ABI-068.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The `model.py` architecture is copied from ABI-068: a normalized full-spectral front end, fixed thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, a high/low spatial-frequency split stem, low-frequency-gated skip fusion, multi-dilation coarse context, full-resolution frequency-pyramid fusion, and an oriented high-frequency line refiner. It emits primary `mask_logits` and provider-derived `centerline_logits`.

The manifest changes the trusted primary loss to `bce_dice`. The centerline auxiliary target remains provider-derived with trusted `weighted_bce` at weight 0.02. No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `bce_dice`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.015 of ABI-068 while improving filtered precision or filtered Contrail Connectivity by at least 0.03;
- capped best `val/filtered_dice` at or above ABI-066 while reducing filtered predicted-positive fraction relative to ABI-068;
- both MIT and Google filtered Dice above 0.35 with filtered precision at least 0.40 and no all-negative/all-positive prediction collapse;
- a finite, late-improving trajectory that identifies a cleaner precision/recall operating point for follow-up diagnostics.

Hard stop evidence for this exact loss branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.32 with no late improvement, both precision and recall worse than ABI-068, or an ABI-077-like permissive positive-area profile without compensating Dice/connectivity gains.

## Fallback/Next Decision

If ABI-078 improves precision/connectivity while staying close to ABI-068 on aggregate and source-stratified filtered Dice, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it simply regresses toward lower recall without precision/connectivity gains, keep ABI-068 as the aggregate-Dice reference and ABI-066 as the precision/connectivity reference, then broaden to a materially different architecture or trusted training-policy axis. If it fails contract validation or smoke testing, classify the failure and repair only if the original controlled loss-swap hypothesis is preserved.
