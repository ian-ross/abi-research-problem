# ABI-057 Full-Spectral BTD High-Resolution Line U-Net + Line-Gated Mask Refiner + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up within the full-spectral BTD high-resolution line U-Net family after ABI-053 through ABI-056 and the ABI-056 whole-validation failure-bucket review. It is not a promotion claim, not a full-data training request, and not an Experiment Batch candidate.

## Hypothesis

ABI-056 is the current local capped best in this family: capped best `val/filtered_dice` 0.3225, final `val/filtered_dice` 0.3221, MIT/Google best filtered Dice 0.3108/0.3492, and non-degenerate predictions. Its whole-validation diagnostic was stable at filtered Dice 0.3198, but showed a persistent false-positive and miss balance: 1,695/2,003 negative validation patches had at least some filtered predicted-positive pixels, while positive-patch recall remained incomplete. Threshold sweep was nearly flat, so calibration alone is unlikely to close the gap.

ABI-057 tests whether separating a supervised centerline-proposal branch from the final mask-refinement branch can reduce broad low-level background positives while retaining the recall benefits of the high-resolution BTD line U-Net. The centerline branch remains an ordinary differentiable model path trained only through the provider-derived `centerline` auxiliary target. It is not candidate-owned postprocessing, thresholding, artifact filtering, target derivation, or sampling.

## Comparison Target

Primary family comparison targets are:

- ABI-056 `abi056_fullspectral_btd_hrline_unet_multiscale_skip_fusion_cldice_centerline_aux_v1`, Run `run_20260827_153716_1ac9d4`: capped best filtered Dice 0.3225, final filtered Dice 0.3221, whole-validation filtered Dice 0.3198, whole-validation filtered precision/recall 0.3310/0.3094, and broad negative-patch false positives in the failure-bucket review.
- ABI-053 `abi053_fullspectral_btd_hrline_unet_cldice_centerline_aux_v1`, Run `run_20260827_134629_3ace34`: capped best filtered Dice 0.3221 and higher best-checkpoint recall/connectivity than ABI-056, but weaker final-epoch stability.
- Canonical MCAST 2.1 remains full Working Validation Split promotion context at filtered Dice 0.3873; ABI-057 is representative capped family-development evidence only.

## Expected Effect

If the ABI-056 bottleneck is diffuse mask activation rather than missing spectral evidence, a centerline-supervised line proposal used as internal attention should improve precision or reduce filtered predicted-positive fraction without collapsing source-balanced recall. A useful positive result would credibly tie ABI-056 filtered Dice while improving precision, predicted-positive fraction, negative-patch behavior in retained samples, or connectivity; exceed ABI-056 filtered Dice; or show a clearer late-epoch trajectory. A useful negative result would indicate that line-attention coupling at the decoder head is not sufficient and that later work should broaden to a different architecture family or trusted policy axis.

## Implementation Sketch

- Reuse the approved ABI-056 front end: normalized provider-approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Keep ABI-056's high-resolution line U-Net encoder, dilated coarsest context, gated decoder skips, and multi-scale skip fusion.
- Replace the single shared full-resolution refiner/head with a `LineGatedMaskRefiner`:
  - refine the fused full-resolution features through a line branch and emit `centerline_logits` for the provider-derived Centerline Target;
  - refine a separate mask branch from the same fused features;
  - convert centerline logits to differentiable line attention and use it only inside the model to gate line and mask features;
  - concatenate original fused features, gated mask features, and gated line features, then fuse them before producing `mask_logits`.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because the decoder-head architecture is materially different and the Agent-visible parallel cap is one.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, sampling policy, augmentation, target derivation, losses, metrics, artifact filtering, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, Post-Run Evaluation, full-data training claim, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, checkpoints, and both output heads remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-056, the continuation is extension-positive if it improves or credibly ties capped filtered Dice while improving precision, lowering broad predicted-positive tendency, improving filtered connectivity, preserving source-balanced recall, or providing a diagnostically useful late-epoch trajectory.

## Continuation and hard stop

Low capped Dice alone should not eliminate the high-resolution line U-Net family if ABI-057 remains finite, non-degenerate, source-informative, or diagnostically distinct. Do not repeat this exact line-gated head unchanged if it reduces aggregate Dice and connectivity without precision, false-positive, stability, or source-balance gains. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-057 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-056 and ABI-053 without useful false-positive or connectivity signal, document the result and broaden to a different architecture family or trusted policy axis rather than repeating centerline-weight, directional-refiner, skip-fusion, or this line-gated-head change unchanged. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-validation diagnostics rather than claiming promotion from capped data.
