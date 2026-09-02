# ABI-056 Full-Spectral BTD High-Resolution Line U-Net + Multi-Scale Skip Fusion + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up within the full-spectral BTD high-resolution line U-Net family after ABI-053, ABI-054, and ABI-055. It is not a promotion claim, not a full-data request, and not an Experiment Batch candidate.

## Hypothesis

ABI-053 established the high-resolution line U-Net branch as materially stronger than the earlier full-spectral DeepLabV3+ BTD branch under the same representative cap, with best filtered Dice 0.3221, recall 0.3472, and filtered connectivity 0.2347. ABI-054 improved precision and Google filtered Dice but reduced MIT Dice and recall. ABI-055's axis-aligned directional refiner balanced MIT/Google best-checkpoint Dice but did not improve aggregate Dice, connectivity, or final-epoch stability.

The latest Research Note recommended broadening within the same high-resolution family toward skip-fusion or decoder-scale changes rather than repeating centerline-weight or elongated-kernel tweaks. ABI-056 tests whether explicit full-resolution fusion of decoder features from multiple scales can preserve ABI-053-like recall while improving stability and source balance. The candidate keeps ABI-053's input, trusted loss, trusted auxiliary target, sampling, augmentation, optimizer, learning rate, batch size, and epoch budget fixed, isolating the change to decoder feature fusion.

## Comparison Target

Primary family comparison targets are:

- ABI-053 `abi053_fullspectral_btd_hrline_unet_cldice_centerline_aux_v1`, Run `run_20260827_134629_3ace34`: best epoch 9, capped filtered Dice 0.3221, MIT/Google filtered Dice 0.3119/0.3467, filtered precision 0.3005, filtered recall 0.3472, filtered connectivity 0.2347, filtered predicted-positive fraction 0.00419; final epoch filtered Dice 0.3152 and filtered connectivity 0.3019.
- ABI-054 `abi054_fullspectral_btd_hrline_unet_cldice_centerline_aux_w005_v1`, Run `run_20260827_142319_ec8c29`: best/final epoch 12, capped filtered Dice 0.3160, MIT/Google filtered Dice 0.2952/0.3676, filtered precision 0.3329, filtered recall 0.3006, filtered connectivity 0.2046.
- ABI-055 `abi055_fullspectral_btd_hrline_unet_directional_refiner_cldice_centerline_aux_v1`, Run `run_20260827_145929_e61464`: best epoch 11, capped filtered Dice 0.3152, MIT/Google filtered Dice 0.3155/0.3148, filtered precision 0.3143, filtered recall 0.3162, filtered connectivity 0.2147; final epoch regressed to filtered Dice 0.2910 and connectivity 0.1266.

Canonical MCAST 2.1 filtered Dice 0.3873 remains full Working Validation Split promotion context only; ABI-056 is capped family-development evidence.

## Expected Effect

If ABI-053 loses thin-line evidence when decoder context is compressed into only the final full-resolution stream, multi-scale skip fusion should improve final-epoch stability, maintain recall, and recover continuity without the ABI-055 directional-refiner instability. A useful positive result would exceed or credibly tie ABI-053 filtered Dice, improve ABI-053 final-epoch stability/connectivity, narrow the MIT/Google gap without sacrificing Google Dice, or show a smoother late-epoch trajectory. A useful negative result would indicate that the high-resolution branch's next bottleneck is not cross-scale decoder fusion and would redirect later work toward another architecture family or a trusted policy axis.

## Implementation Sketch

- Reuse the approved ABI-053/054/055 front end: normalize provider-approved ABI channels 1-16, add eight explicit thermal brightness-temperature-difference planes computed only from approved ABI channels, and concatenate a learned 16-channel 1x1 GELU projection.
- Keep the high-resolution line U-Net encoder, three downsampling stages, dilated coarsest context, bilinear decoder upsampling, gated encoder skips, and full-resolution local/dilated line refiner.
- Add a `MultiScaleSkipFusion` module before the line refiner:
  - project the half-resolution and quarter-resolution decoder outputs back to the base full-resolution channel width with 1x1 Conv/GroupNorm/GELU blocks;
  - upsample those projected decoder features to full resolution with bilinear interpolation;
  - apply learned sigmoid gates to the full-resolution decoder stream, projected lower-scale decoder streams, and stem features;
  - concatenate the four gated full-resolution streams and fuse them through residual Conv/GroupNorm/GELU blocks.
- Produce separate `mask_logits` and `centerline_logits` heads. The auxiliary target and loss remain provider/Harness-owned and manifest-declared.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because the branch is a materially expanded decoder relative to the profiled residual U-Net class and the Agent-visible parallel cap is one.

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
6. Relative to ABI-053/054/055, the continuation is extension-positive if it improves or credibly ties capped filtered Dice, improves final-epoch stability, improves filtered connectivity at similar predicted-positive fraction, preserves ABI-053-like recall while improving precision, narrows source imbalance without a large aggregate penalty, or provides a clear late-epoch trajectory signal.

## Continuation and hard stop

Low capped Dice alone should not eliminate the high-resolution line U-Net family if ABI-056 remains finite, non-degenerate, source-informative, or diagnostically distinct. Do not repeat this exact multi-scale skip-fusion branch unchanged if it reduces aggregate Dice and connectivity without stability or source-balance gains. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-056 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-053/054/055 without useful secondary-metric strength, document the result and broaden to a different architecture family or trusted policy axis rather than repeating centerline-weight, directional-refiner, or multi-scale skip-fusion tweaks. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
