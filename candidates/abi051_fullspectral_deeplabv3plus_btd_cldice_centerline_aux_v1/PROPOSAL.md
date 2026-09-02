# ABI-051 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ BTD-mixer branch after ABI-048/049/050 tested the trusted `bce_dice_cldice` primary loss and two auxiliary-target variants under the same capped representative budget. It is not a promotion claim or full-data request.

## Hypothesis

ABI-048 kept the ABI-046 BTD-mixer front end and changed the trusted primary loss to `bce_dice_cldice`, improving aggregate filtered Dice to 0.216950 with balanced MIT/Google filtered Dice of 0.217877/0.215015, filtered precision 0.196350, filtered recall 0.242379, filtered connectivity 0.260749, and filtered predicted-positive fraction 0.00447. ABI-049 added a low-weight trusted `line` auxiliary target and became the capped family best by filtered Dice at 0.219242, with MIT/Google 0.218872/0.220016 and recall 0.270130, but lower filtered precision 0.184488 and connectivity 0.215240. ABI-050 added a low-weight trusted `boundary` auxiliary target; it did not improve aggregate filtered Dice (0.208354) but improved Google filtered Dice to 0.234296 and kept precision higher than ABI-049 at 0.239105.

A low-weight provider-declared `centerline` auxiliary target should provide more direct skeleton supervision than `boundary` and less tolerance-band expansion pressure than `line`. It may preserve the source balance and recall gains of the clDice branch while improving thin-contrail continuity or precision. Because `centerline` is already an allowlisted provider-derived auxiliary target, this tests a trusted training signal without moving target derivation, loss, metrics, Artifact Filters, sampling, or augmentation into candidate code.

## Comparison Target

The primary comparison target is ABI-048 `abi048_fullspectral_deeplabv3plus_btd_cldice_v1`, Run `run_20260827_112338_82a3a6`: best epoch 10, 12 total epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `abi_16ch`, `bce_dice_cldice`, `random_mirroring`, aggregate best `val/filtered_dice` 0.216950, MIT filtered Dice 0.217877, Google filtered Dice 0.215015, filtered precision 0.196350, filtered recall 0.242379, filtered connectivity 0.260749, and filtered predicted-positive fraction 0.00447.

Auxiliary-target references are ABI-049 `run_20260827_114945_e5f83e` (`line`, filtered Dice 0.219242, MIT/Google 0.218872/0.220016, precision 0.184488, recall 0.270130, connectivity 0.215240, predicted-positive fraction 0.00531) and ABI-050 `run_20260827_122019_18b5c7` (`boundary`, filtered Dice 0.208354, MIT/Google 0.196402/0.234296, precision 0.239105, recall 0.184611, connectivity 0.259112, predicted-positive fraction 0.00280). ABI-046 `run_20260826_204203_732aee` remains the BCE-Dice BTD-mixer family baseline. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context, not a strict gate for this capped family-development run.

## Expected Effect

If the current clDice branch benefits from explicit medial-line supervision, the `centerline` auxiliary head may improve continuity, source balance, or recall/precision balance relative to ABI-048 while avoiding the lower precision/connectivity seen in ABI-049's `line` auxiliary variant. A useful positive result would improve or credibly tie ABI-048/049 filtered Dice or improve secondary diagnostics such as connectivity, source balance, predicted-positive stability, or precision at comparable recall. A useful negative result would show that low-weight centerline supervision does not add useful information beyond the primary clDice loss for this branch.

## Implementation Sketch

- Reuse the ABI-048/049/050 candidate-owned front end exactly: normalize provider-approved ABI channels 1-16, compute eight explicit thermal BTD planes from approved thermal bands, and concatenate a 16-channel learned 1x1 GELU projection of normalized raw channels.
- Reuse the ABI-048/049/050 SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, and no pretrained weights.
- Keep the decoder output width at two channels and split it into `mask_logits` and `centerline_logits`.
- Preserve trusted `bce_dice_cldice` as the primary loss for `mask_logits`.
- Add one manifest-declared provider-owned auxiliary target: `centerline` -> `centerline_logits`, trusted `weighted_bce`, weight 0.05.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, losses, metrics, artifact filtering, target transforms, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for both primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-048/049/050, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves recall/precision balance, improves Contrail Connectivity Metric, narrows source imbalance, stabilizes predicted-positive fraction, or clearly shows that low-weight Centerline Target auxiliary supervision is not useful for this BTD clDice branch.

## Continuation and hard stop

Continue DeepLabV3+ BTD-mixer auxiliary-target development only if this variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-048 family baseline or offer a useful centerline-supervision trade-off, document the auxiliary-target comparison and broaden the frontier to a BCE-Dice-only auxiliary variant, a different architecture-family scout, or another trusted policy axis. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
