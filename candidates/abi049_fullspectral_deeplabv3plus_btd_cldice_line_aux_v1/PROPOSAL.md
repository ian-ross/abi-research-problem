# ABI-049 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Line Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ BTD-mixer branch after ABI-048 became the strongest capped family result so far by best `val/filtered_dice`. It is not a promotion claim or full-data request.

## Hypothesis

ABI-048 kept the ABI-046 BTD-mixer front end and changed the trusted primary loss to `bce_dice_cldice`. Its best checkpoint improved aggregate filtered Dice to 0.216950 with balanced MIT/Google filtered Dice of 0.217877/0.215015, filtered precision 0.196350, filtered recall 0.242379, and filtered predicted-positive fraction 0.00447. This is better aggregate and source-balanced capped evidence than ABI-046, but ABI-046 still had stronger filtered precision 0.254612 and final filtered connectivity 0.383943.

Adding a low-weight provider-declared `line` auxiliary target to the ABI-048 branch should encourage local tolerance-band evidence around thin Contrail Mask positives while leaving primary checkpoint selection and primary loss unchanged. A small auxiliary weight should provide extra supervision for thin-line localization without moving target derivation, losses, metrics, Artifact Filters, or data policy into candidate code.

## Comparison Target

The primary comparison target is ABI-048 `abi048_fullspectral_deeplabv3plus_btd_cldice_v1`, Run `run_20260827_112338_82a3a6`: best epoch 10, 12 total epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `abi_16ch`, `bce_dice_cldice`, `random_mirroring`, aggregate best `val/filtered_dice` 0.216950, MIT filtered Dice 0.217877, Google filtered Dice 0.215015, filtered precision 0.196350, filtered recall 0.242379, filtered connectivity 0.260749, and filtered predicted-positive fraction 0.00447.

ABI-046 Run `run_20260826_204203_732aee` remains the BCE-Dice BTD-mixer family baseline: filtered Dice 0.208350, precision 0.254612, recall 0.176315, connectivity 0.383943, MIT filtered Dice 0.195981, Google filtered Dice 0.241080, and filtered predicted-positive fraction 0.00251. ABI-047 Run `run_20260827_110027_1c679a` remains the focal-Tversky recall/precision trade-off reference. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context, not a strict gate for this capped family-development run.

## Expected Effect

The `line` auxiliary target is a trusted one-pixel tolerance band around positive Contrail Mask pixels. If ABI-048's higher Dice/source balance came from better line evidence but remains under-supervised spatially, the auxiliary head may improve recall or continuity while maintaining acceptable precision. A useful positive result would improve or credibly tie ABI-048 filtered Dice while improving recall, connectivity, source balance, or predicted-positive stability. A useful negative result would show that auxiliary tolerance-band supervision is not beneficial for this branch at weight 0.05 under the active capped budget.

## Implementation Sketch

- Reuse the ABI-048 candidate-owned front end exactly: normalize provider-approved ABI channels 1-16, compute eight explicit thermal BTD planes from approved thermal bands, and concatenate a 16-channel learned 1x1 GELU projection of normalized raw channels.
- Reuse the ABI-048 SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, no encoder weights, and no pretrained weights.
- Change the final decoder output width from one channel to two channels and split it into `mask_logits` and `line_logits`.
- Preserve trusted `bce_dice_cldice` as the primary loss for `mask_logits`.
- Add one manifest-declared provider-owned auxiliary target: `line` -> `line_logits`, trusted `weighted_bce`, weight 0.05.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `line`, auxiliary loss `weighted_bce`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, losses, metrics, artifact filtering, target transforms, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for both primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-048, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves recall/precision balance, improves Contrail Connectivity Metric, narrows source imbalance, stabilizes predicted-positive fraction, or clearly shows that low-weight Line Target auxiliary supervision is not useful for this BTD clDice branch.

## Continuation and hard stop

Continue DeepLabV3+ BTD-mixer auxiliary-target development only if this variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-048 family baseline or offer a useful line-supervision trade-off, document the result and consider a separately proposed centerline auxiliary variant, a BCE-Dice-only auxiliary variant, or a different architecture-family scout. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
