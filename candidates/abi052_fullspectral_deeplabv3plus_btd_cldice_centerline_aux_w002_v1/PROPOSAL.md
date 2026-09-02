# ABI-052 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Centerline Auxiliary Weight 0.02 v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ BTD-mixer branch after ABI-048/049/050/051 tested trusted `bce_dice_cldice` plus auxiliary-target variants under the same capped representative budget. It is not a promotion claim or full-data request.

## Hypothesis

ABI-051 showed that a trusted `centerline` auxiliary target at weight 0.05 nearly tied ABI-049 by best filtered Dice while improving filtered precision, connectivity, final-epoch Dice, and Google source behavior. Its weakness was lower recall and weaker MIT filtered Dice than ABI-049. Lowering only the manifest-declared Centerline Target auxiliary-loss weight from 0.05 to 0.02 should test whether the centerline signal can keep ABI-051s precision/connectivity and late-epoch stability while reducing over-regularization of the primary Contrail Mask objective.

Because `centerline` and `weighted_bce` are provider/Harness-declared contract features, this variation keeps target derivation and auxiliary loss outside candidate code.

## Comparison Target

The primary comparison target is ABI-051 `abi051_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_v1`, Run `run_20260827_124640_fc6836`: same architecture, `abi_16ch` input, `bce_dice_cldice` primary loss, centerline auxiliary target at weight 0.05, best epoch 10, best filtered Dice 0.2187, MIT/Google filtered Dice 0.2104/0.2382, filtered precision 0.2392, filtered recall 0.2015, filtered connectivity 0.3176, and final-epoch filtered Dice 0.2168.

Secondary references are ABI-049 `run_20260827_114945_e5f83e` (`line` auxiliary weight 0.05, best filtered Dice 0.2192, higher recall but lower precision/connectivity), ABI-048 `run_20260827_112338_82a3a6` (no auxiliary target, best filtered Dice 0.2169), and ABI-046 `run_20260826_204203_732aee` (BCE-Dice BTD-mixer family baseline, best filtered Dice 0.2084). Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context, not a strict gate for this capped family-development run.

## Expected Effect

If ABI-051s centerline auxiliary signal is useful but slightly overweighted, reducing its weight to 0.02 may improve MIT filtered Dice and recall while preserving better precision/connectivity than ABI-049s line-auxiliary branch. A useful positive result would improve or credibly tie ABI-049/051 filtered Dice or produce a clearer precision/recall/connectivity trade-off. A useful negative result would show that Centerline Target tuning gives diminishing returns and support broadening beyond auxiliary-head variants.

## Implementation Sketch

- Reuse ABI-051 `model.py` architecture: normalized approved ABI channels 1-16, eight explicit thermal BTD planes, learned 16-channel 1x1 GELU channel projection, and randomly initialized SMP DeepLabV3+ ResNet-18 decoder.
- Keep two decoder output channels split into primary `mask_logits` and auxiliary `centerline_logits`.
- Preserve trusted `bce_dice_cldice` as the primary loss.
- Keep manifest-declared provider-owned auxiliary target `centerline` -> `centerline_logits` with trusted `weighted_bce`, changing only `weight` from 0.05 to 0.02.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
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
6. Relative to ABI-048/049/051, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves MIT filtered Dice or recall without losing ABI-051s precision/connectivity, narrows source imbalance, stabilizes predicted-positive fraction, or clearly shows that centerline auxiliary weight tuning is not useful for this BTD clDice branch.

## Continuation and hard stop

Continue DeepLabV3+ BTD-mixer auxiliary-target development only if this lower-weight centerline variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-048/049/051 family references or offer a useful lower-weight centerline trade-off, document the auxiliary-weight result and broaden the frontier to a materially different thin-structure architecture scout or another trusted policy axis rather than adding more auxiliary-head variants to the same decoder. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
