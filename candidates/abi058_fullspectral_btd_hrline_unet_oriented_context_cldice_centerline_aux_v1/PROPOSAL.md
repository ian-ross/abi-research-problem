# ABI-058 Full-Spectral BTD High-Resolution Line U-Net + Oriented Context + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up within the full-spectral BTD high-resolution line U-Net family after ABI-053 through ABI-057 and the ABI-056 whole-validation failure-bucket review. It is not a promotion claim, not a full-data training request, and not an Experiment Batch candidate.

## Hypothesis

ABI-056 remains the current local capped best in this family: capped best `val/filtered_dice` 0.3225, final `val/filtered_dice` 0.3221, and whole-validation filtered Dice 0.3198. Its whole-validation diagnostics showed stable non-degenerate behavior but broad negative-patch false positives and incomplete positive-patch overlap. ABI-057's line-gated mask refiner improved precision, lowered predicted-positive fraction, improved best-checkpoint connectivity, and slightly improved Google filtered Dice, but reduced aggregate filtered Dice and recall relative to ABI-056. That suggests the family still has useful thin-line signals, while direct centerline-logit gating may suppress recall too strongly.

ABI-058 tests a different connectivity mechanism: full-resolution orientation-bank context. Instead of using centerline logits as internal attention, it learns local, horizontal-strip, vertical-strip, and broad dilated feature branches and a differentiable per-pixel soft mixture over those branches before the mask and centerline heads. The goal is to preserve line continuity and reduce diffuse false positives without imposing an explicit line-proposal gate.

## Comparison Target

Primary family comparison targets are:

- ABI-056 `abi056_fullspectral_btd_hrline_unet_multiscale_skip_fusion_cldice_centerline_aux_v1`, Run `run_20260827_153716_1ac9d4`: capped best filtered Dice 0.3225, final filtered Dice 0.3221, whole-validation filtered Dice 0.3198, and stable but small advantage over ABI-053.
- ABI-057 `abi057_fullspectral_btd_hrline_unet_line_gated_mask_refiner_cldice_centerline_aux_v1`, Run `run_20260827_162936_6294f6`: capped best/final filtered Dice 0.3188 with improved precision and connectivity but reduced recall relative to ABI-056.
- ABI-053 `abi053_fullspectral_btd_hrline_unet_cldice_centerline_aux_v1`, Run `run_20260827_134629_3ace34`: capped best filtered Dice 0.3221 and higher best-checkpoint recall than ABI-056, but weaker final-epoch stability.
- Canonical MCAST 2.1 remains full Working Validation Split promotion context at filtered Dice 0.3873; ABI-058 is representative capped family-development evidence only.

## Expected Effect

If ABI-056's residual error comes partly from insufficient orientation-specific full-resolution context, ABI-058 should improve filtered connectivity, precision/recall balance, or source-balanced filtered Dice without ABI-057's recall-suppression cost. A useful positive result would credibly tie or exceed ABI-056 filtered Dice while improving filtered connectivity, lowering broad predicted-positive tendency, preserving MIT/Google balance, or showing a stronger late-epoch trajectory. A useful negative result would indicate that high-resolution decoder refinements around this family are nearing diminishing returns and that the next research step should broaden to a different architecture family or trusted policy axis.

## Implementation Sketch

- Reuse the approved ABI-056 front end: normalized provider-approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Keep ABI-056's high-resolution line U-Net encoder, dilated coarsest context, gated decoder skips, and multi-scale skip fusion.
- Replace ABI-056's isotropic full-resolution line refiner with an `OrientedContextRefiner`:
  - compute a local residual branch, a horizontal strip-convolution branch, a vertical strip-convolution branch, and a broad dilated branch at full resolution;
  - learn a per-pixel softmax over those four branches from their concatenated features;
  - fuse the weighted oriented context with the original full-resolution features before producing `mask_logits` and `centerline_logits`.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because the architecture is a controlled but materially different decoder-refiner branch and the Agent-visible parallel cap is one.

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
6. Relative to ABI-056 and ABI-057, the continuation is extension-positive if it improves or credibly ties capped filtered Dice while improving filtered connectivity, precision/recall balance, predicted-positive fraction, source balance, or late-epoch stability.

## Continuation and hard stop

Low capped Dice alone should not eliminate the high-resolution line U-Net family if ABI-058 remains finite, non-degenerate, source-informative, or diagnostically distinct. Do not repeat this exact oriented-context branch unchanged if it underperforms ABI-056 and ABI-053 without useful connectivity, false-positive, stability, or source-balance gains. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-058 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-056/ABI-053 without useful connectivity or false-positive signal, document the result and broaden away from high-resolution decoder refinements toward a different architecture family or trusted policy axis. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-validation diagnostics rather than claiming promotion from capped data.
