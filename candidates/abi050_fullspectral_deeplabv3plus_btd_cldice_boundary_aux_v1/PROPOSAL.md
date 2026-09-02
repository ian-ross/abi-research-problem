# ABI-050 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Boundary Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ BTD-mixer branch after ABI-049 became the current capped best by best `val/filtered_dice`. It is not a promotion claim or full-data request.

## Hypothesis

ABI-049 improved best aggregate filtered Dice to 0.219242 and raised filtered recall to 0.270130 by adding a low-weight trusted `line` auxiliary target to the ABI-048 BTD-mixer + `bce_dice_cldice` branch. However, that gain came with lower filtered precision (0.184488) and lower best-checkpoint filtered connectivity (0.215240) than ABI-048, while the final epoch converged back toward ABI-048-like aggregate Dice near 0.210.

Replacing the `line` auxiliary target with the provider-declared `boundary` auxiliary target at the same low weight should test whether edge/extent supervision can recover some boundary precision and predicted-positive-area control without abandoning ABI-048's continuity-aware primary loss or the BTD spectral front end. Because target derivation and auxiliary loss remain provider/Harness-owned, this is an in-contract probe of auxiliary-supervision geometry rather than candidate-owned postprocessing or target engineering.

## Comparison Target

The primary comparison target is ABI-049 `abi049_fullspectral_deeplabv3plus_btd_cldice_line_aux_v1`, Run `run_20260827_114945_e5f83e`: best epoch 11, 12 total epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `abi_16ch`, `bce_dice_cldice`, `random_mirroring`, aggregate best `val/filtered_dice` 0.219242, MIT filtered Dice 0.218872, Google filtered Dice 0.220016, filtered precision 0.184488, filtered recall 0.270130, filtered connectivity 0.215240, and filtered predicted-positive fraction 0.00531.

The secondary comparison target is ABI-048 `abi048_fullspectral_deeplabv3plus_btd_cldice_v1`, Run `run_20260827_112338_82a3a6`: best epoch 10, aggregate best `val/filtered_dice` 0.216950, MIT filtered Dice 0.217877, Google filtered Dice 0.215015, filtered precision 0.196350, filtered recall 0.242379, filtered connectivity 0.260749, and filtered predicted-positive fraction 0.00447.

ABI-046 Run `run_20260826_204203_732aee` remains the BCE-Dice BTD-mixer family baseline: filtered Dice 0.208350, precision 0.254612, recall 0.176315, connectivity 0.383943, MIT filtered Dice 0.195981, Google filtered Dice 0.241080, and filtered predicted-positive fraction 0.00251. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context, not a strict gate for this capped family-development run.

## Expected Effect

The trusted `boundary` auxiliary target should emphasize mask extent and edge evidence around thin contrail structures. A useful positive result would preserve or credibly tie ABI-049/ABI-048 aggregate filtered Dice while improving precision, filtered connectivity, source balance, or predicted-positive fraction control. A useful negative result would show that low-weight boundary supervision does not repair the recall/precision trade-off introduced by the line auxiliary head under the active capped budget.

## Implementation Sketch

- Reuse the ABI-048/ABI-049 candidate-owned front end exactly: normalize provider-approved ABI channels 1-16, compute eight explicit thermal BTD planes from approved thermal bands, and concatenate a 16-channel learned 1x1 GELU projection of normalized raw channels.
- Reuse the ABI-048/ABI-049 SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, no encoder weights, and no pretrained weights.
- Use a two-channel final decoder output and split it into `mask_logits` and `boundary_logits`.
- Preserve trusted `bce_dice_cldice` as the primary loss for `mask_logits`.
- Add one manifest-declared provider-owned auxiliary target: `boundary` -> `boundary_logits`, trusted `weighted_bce`, weight 0.05.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `boundary_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `boundary`, auxiliary loss `weighted_bce`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
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
6. Relative to ABI-049 and ABI-048, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves precision/recall balance, improves Contrail Connectivity Metric, narrows source imbalance, stabilizes predicted-positive fraction, or clearly shows that low-weight Boundary Target auxiliary supervision is not useful for this BTD clDice branch.

## Continuation and hard stop

Continue DeepLabV3+ BTD-mixer auxiliary-target development only if this variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-049/ABI-048 family baseline or offer a useful boundary-supervision trade-off, document the result and broaden to a different architecture-family scout or a separately proposed BCE-Dice-only auxiliary variant rather than stacking additional auxiliary heads in the same decoder. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
