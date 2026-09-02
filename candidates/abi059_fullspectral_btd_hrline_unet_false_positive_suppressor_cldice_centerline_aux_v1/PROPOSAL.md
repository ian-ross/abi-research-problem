# ABI-059 Full-Spectral BTD High-Resolution Line U-Net + False-Positive Suppressor + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up within the full-spectral BTD high-resolution line U-Net family after ABI-053 through ABI-058 and whole-validation diagnostics for ABI-056 and ABI-058. It is not a promotion claim, not a full-data training request, and not an Experiment Batch candidate.

## Hypothesis

ABI-058 is the current local whole-validation-tested reference in this branch: whole-validation filtered Dice 0.3233 versus ABI-056 at 0.3198, but the gain is narrow and comes mainly from recall and extra predicted-positive area. ABI-058 produced 508,486 filtered false-positive pixels, 1,685/2,003 negative validation patches with some filtered predicted-positive pixels, and lower precision than ABI-056. Threshold sweep was nearly flat, so pure calibration is unlikely to solve the issue.

ABI-059 tests a model-architecture false-positive-control mechanism while keeping the trusted data, loss, augmentation, and auxiliary-target policy fixed. A trainable low-resolution negative-evidence branch is fused with the full-resolution oriented-context features and subtracts a non-negative suppression term from `mask_logits`. The suppressor is initialized near zero, so the model starts close to ABI-058 but can learn to lower diffuse background logits where the trusted primary loss identifies false positives.

## Comparison Target

Primary family comparison targets are:

- ABI-058 `abi058_fullspectral_btd_hrline_unet_oriented_context_cldice_centerline_aux_v1`, Run `run_20260827_171331_c1769a`: capped best filtered Dice 0.3248 and whole-validation filtered Dice 0.3233, with recall-oriented gains but broad negative-patch false positives.
- ABI-056 `abi056_fullspectral_btd_hrline_unet_multiscale_skip_fusion_cldice_centerline_aux_v1`, Run `run_20260827_153716_1ac9d4`: capped best filtered Dice 0.3225 and whole-validation filtered Dice 0.3198, slightly lower recall but better precision and fewer false-positive pixels than ABI-058.
- ABI-057 `abi057_fullspectral_btd_hrline_unet_line_gated_mask_refiner_cldice_centerline_aux_v1`, Run `run_20260827_162936_6294f6`: capped filtered Dice 0.3188 with better precision/connectivity and lower predicted-positive fraction, but recall suppression.
- Canonical MCAST 2.1 remains full Working Validation Split promotion context at filtered Dice 0.3873; ABI-059 is representative capped family-development evidence only.

## Expected Effect

If ABI-058's residual gap is partly driven by diffuse false-positive logits on background patches, ABI-059 should lower filtered predicted-positive fraction and improve precision without ABI-057-like recall collapse. A useful positive result would tie or exceed ABI-058 capped filtered Dice while reducing false-positive tendency, preserving MIT/Google non-collapse, and keeping filtered recall near ABI-058. A useful mixed result would reduce predicted-positive burden or improve connectivity/precision enough to guide a later false-positive-control branch even if aggregate Dice does not improve.

## Implementation Sketch

- Reuse the approved ABI-058 front end: normalized provider-approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Keep the high-resolution line U-Net encoder, dilated coarsest context, gated decoder skips, multi-scale skip fusion, and oriented full-resolution context refiner.
- Replace the direct mask head with a `FalsePositiveSuppressorHead`:
  - average-pool oriented features to low resolution, process them with residual convolutional context, and upsample them back to full resolution;
  - fuse low-resolution context with full-resolution oriented features;
  - predict base `mask_logits` and a non-negative learned suppression term;
  - return final `mask_logits = base_logits - 0.25 * suppression`, with the suppression conv bias initialized negative so the initial model is close to ABI-058.
- Keep a provider-declared `centerline_logits` auxiliary head from the fused features.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because the Agent-visible parallel cap is one and this is a controlled but materially different decoder-head branch.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, sampling policy, augmentation, target derivation, losses, metrics, artifact filtering, postprocessing, thresholding, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, Post-Run Evaluation, full-data training claim, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, checkpoints, and both output heads remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-058, the continuation is extension-positive if it improves or credibly ties capped filtered Dice while lowering filtered predicted-positive fraction, improving precision, preserving recall/source balance, or improving connectivity.

## Continuation and hard stop

Low capped Dice alone should not eliminate the high-resolution line U-Net family if ABI-059 remains finite, non-degenerate, source-informative, or diagnostically distinct. Do not repeat this exact false-positive suppressor unchanged if it underperforms ABI-058/ABI-056 without useful precision, predicted-positive, connectivity, stability, or source-balance gains. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-059 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but over-suppresses recall or fails to improve false-positive behavior, document the result and broaden away from high-resolution decoder refinements toward a different architecture family or trusted policy axis. If it reduces false positives while preserving ABI-058-like Dice, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
