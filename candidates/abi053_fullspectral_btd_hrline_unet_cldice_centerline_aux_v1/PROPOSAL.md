# ABI-053 Full-Spectral BTD High-Resolution Line U-Net + clDice + Centerline Auxiliary v1

## Proposal classification

**Family scout.** This is the first materially different thin-structure decoder after the full-spectral DeepLabV3+ BTD-mixer auxiliary-target sequence. It preserves the strongest in-contract input/loss policy from ABI-052 but changes the decoder/feature geometry. It is not a promotion claim, not a full-data request, and not an Experiment Batch candidate.

## Hypothesis

ABI-052 is the current capped family best by `val/filtered_dice` at 0.2214, with strong Google filtered Dice 0.2542, filtered precision 0.2619, and filtered connectivity 0.3391. Its weakness is persistent MIT filtered Dice 0.2083 and MIT filtered recall 0.1729. The most recent Research Note concluded that more auxiliary-head-only tuning is unlikely to be the highest-value next step.

A high-resolution U-Net-style decoder that keeps a full-resolution line-evidence path, gated skip fusion, coarsest-scale dilated context, and a final full-resolution multi-dilation line refiner may improve thin Contrail Mask continuity and MIT/recall behavior more directly than the DeepLabV3+ decoder. Retaining the ABI-052 normalized raw + thermal-BTD + learned-mixer front end, trusted `bce_dice_cldice`, and low-weight trusted `centerline` auxiliary target isolates the primary change to feature geometry rather than loss, target, data policy, or Artifact Filters.

## Comparison Target

The primary family comparison target is ABI-052 `abi052_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_w002_v1`, Run `run_20260827_131644_b76d09`: best epoch 12, capped filtered Dice 0.2214, MIT/Google filtered Dice 0.2083/0.2542, filtered precision 0.2619, filtered recall 0.1918, filtered connectivity 0.3391, and filtered predicted-positive fraction 0.00265.

Secondary references are ABI-048 `run_20260827_112338_82a3a6` (BTD mixer + `bce_dice_cldice`, best filtered Dice 0.2169), ABI-049 `run_20260827_114945_e5f83e` (line auxiliary, best filtered Dice 0.2192, higher recall but lower precision/connectivity), ABI-051 `run_20260827_124640_fc6836` (centerline auxiliary weight 0.05, best filtered Dice 0.2187), and ABI-046 `run_20260826_204203_732aee` (BTD-mixer `bce_dice` baseline, best filtered Dice 0.2084). Canonical MCAST 2.1 filtered Dice 0.3873 remains full-validation promotion context only; capped ABI-053 evidence will not be interpreted as promotion-grade evidence.

## Expected Effect

If DeepLabV3+ downsampling/ASPP geometry is limiting thin-line reconstruction, ABI-053 should improve MIT filtered Dice or recall, increase aggregate recall without collapsing precision, or produce stronger filtered connectivity at a similar predicted-positive fraction. A useful positive result would match or exceed ABI-052 filtered Dice, or improve a family diagnostic such as MIT filtered Dice, source balance, recall/connectivity, or late-epoch trajectory. A useful negative result would show that the BTD/clDice/centerline recipe is decoder-sensitive and guide either repair or a different architecture frontier.

## Implementation Sketch

- Reuse the ABI-052 candidate-visible front end: normalize approved ABI channels 1-16, add eight explicit thermal brightness-temperature-difference planes built only from approved ABI channels, and concatenate a learned 16-channel 1x1 GELU channel projection.
- Replace the SMP DeepLabV3+ ResNet-18 network with a pure-PyTorch high-resolution U-Net-style decoder:
  - full-resolution stem and first encoder block;
  - three downsampling stages with residual GroupNorm/GELU blocks;
  - coarsest-scale multi-dilation context;
  - bilinear decoder upsampling with gated skip fusion;
  - full-resolution local/dilated line refiner before prediction heads.
- Produce separate `mask_logits` and `centerline_logits` heads. The auxiliary target and auxiliary loss remain declared in the manifest and provider/Harness-owned.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because this decoder family is unprofiled; no candidate-owned scheduling or resource workaround is introduced.

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
6. Relative to ABI-052 and ABI-048/049/051, the scout is extension-positive if it improves or credibly ties filtered Dice, improves MIT filtered Dice or recall, narrows source imbalance, improves recall/connectivity trade-off, stabilizes predicted-positive fraction, shows an improving late-epoch trajectory, or provides diagnostically clear decoder-family evidence.

## Continuation and hard stop

Because ABI-053 is a first scout for a materially different decoder, low capped Dice alone should not eliminate the family if the trajectory is finite, non-degenerate, improving, or diagnostically distinct. A bounded follow-up budget of one or two later sequential refinements would be justified for finite source-informative evidence, especially if MIT recall, source balance, connectivity, or late-epoch trend improves. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-053 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-052 without a useful trajectory or secondary-metric strength, document the scout and broaden to another architecture family or trusted policy axis rather than repeating DeepLabV3+ auxiliary-head tuning. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
