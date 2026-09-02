# ABI-054 Full-Spectral BTD High-Resolution Line U-Net + clDice + Centerline Auxiliary Weight 0.05 v1

## Proposal classification

**Family-development continuation.** ABI-054 is a controlled follow-up to ABI-053, the high-resolution line U-Net scout. It keeps the same architecture, approved full-spectral BTD front end, trusted primary loss, data policy, augmentation policy, optimizer, learning rate, batch size, and 12-epoch capped execution request. The only intended manifest change is increasing the provider-derived `centerline` auxiliary target weight from 0.02 to 0.05.

## Hypothesis

ABI-053 is the current strongest local capped Candidate Result by `val/filtered_dice`: Run `run_20260827_134629_3ace34` reached best filtered Dice 0.3221 at epoch 9, with MIT/Google filtered Dice 0.3119/0.3467, filtered precision 0.3005, filtered recall 0.3472, and filtered predicted-positive fraction 0.00419. It materially improved over the ABI-052 DeepLabV3+ BTD centerline-weight reference but traded away connectivity: ABI-053 best-checkpoint filtered connectivity was 0.2347, while ABI-052 had 0.3391 and the ABI-053 final epoch partially recovered connectivity to 0.3019 while retaining filtered Dice 0.3152.

A stronger trusted Centerline Target auxiliary weight may bias the same high-resolution decoder toward more continuous, centerline-consistent contrail structures, improving checkpoint stability and filtered connectivity without returning to the lower-performing DeepLabV3+ decoder. Because the architecture and input/loss policy are unchanged, this tests whether the ABI-053 continuity trade-off is tunable through an already allowlisted provider-derived auxiliary objective.

## Comparison Target

The primary comparison target is ABI-053 `abi053_fullspectral_btd_hrline_unet_cldice_centerline_aux_v1`, Run `run_20260827_134629_3ace34`: best epoch 9, capped filtered Dice 0.3221, MIT/Google filtered Dice 0.3119/0.3467, filtered precision 0.3005, filtered recall 0.3472, filtered connectivity 0.2347, and filtered predicted-positive fraction 0.00419; final epoch filtered Dice 0.3152 with filtered connectivity 0.3019.

Secondary references are ABI-052 `run_20260827_131644_b76d09` (DeepLabV3+ BTD + `bce_dice_cldice` + centerline weight 0.02; filtered Dice 0.2214, connectivity 0.3391) and ABI-051 `run_20260827_124640_fc6836` (DeepLabV3+ BTD + centerline weight 0.05; filtered Dice 0.2187, connectivity 0.3176). Canonical MCAST 2.1 filtered Dice 0.3873 remains full-validation promotion context only; this capped Run is not promotion-grade evidence.

## Expected Effect

If ABI-053's weaker best-checkpoint connectivity is partly due to underweighted centerline supervision rather than decoder geometry, ABI-054 should improve filtered connectivity, final-epoch stability, precision/recall balance, or predicted-positive fraction while preserving most of ABI-053's large aggregate and source-stratified Dice gains. A favorable result would credibly tie ABI-053 filtered Dice while improving connectivity or final-epoch stability, or would remain close to ABI-053 while improving source balance or precision/recall behavior. A negative but useful result would show that stronger auxiliary centerline supervision sacrifices too much recall or aggregate Dice in this decoder, redirecting the next branch toward architecture-level continuity refinement.

## Implementation Sketch

- Reuse the ABI-053 pure-PyTorch high-resolution line U-Net model implementation unchanged except for candidate identifier strings.
- Preserve the candidate-visible front end: normalized approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Preserve the full-resolution stem path, residual encoder, coarsest-scale multi-dilation context, bilinear gated skip decoder, and full-resolution multi-dilation line refiner.
- Produce separate `mask_logits` and `centerline_logits` heads. The auxiliary target and auxiliary `weighted_bce` loss are declared in the manifest and remain provider/Harness-owned.
- Change only the manifest auxiliary target weight from 0.02 to 0.05.
- Keep trusted `bce_dice_cldice`, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run; no Experiment Batch, concurrency request, candidate-owned scheduling, or resource workaround is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.05, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
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
6. Relative to ABI-053, the continuation is extension-positive if it credibly ties or improves capped filtered Dice while improving filtered connectivity, final-epoch stability, source balance, precision/recall balance, or predicted-positive fraction. It is also useful if it clearly establishes that centerline weight 0.05 over-regularizes the high-resolution decoder.

## Continuation and hard stop

Do not require ABI-054 to beat canonical MCAST 2.1, because this is capped family-development evidence. Continue the high-resolution line U-Net family if ABI-054 remains finite, non-degenerate, source-informative, and improves any of the targeted stability/connectivity trade-offs without a large Dice/recall collapse. Do not repeat this exact auxiliary-weight branch if it shows persistent non-finite behavior, resource failure, persistent prediction collapse, clear optimization failure, severe Dataset Source collapse, or a decisive drop in both aggregate Dice and the targeted continuity/stability diagnostics.

## Fallback/Next Decision

If ABI-054 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but sacrifices too much recall or Dice, document the result and move to an architecture-level continuity refinement of the high-resolution decoder, such as a lighter refiner or skip-fusion adjustment, rather than returning to DeepLabV3+ auxiliary-head tuning. If it unexpectedly exceeds the current capped family best and remains source-balanced, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
