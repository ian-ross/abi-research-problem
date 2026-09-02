# ABI-048 Full-Spectral DeepLabV3+ BTD-Mixer + BCE-Dice-clDice v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ BTD-mixer branch after ABI-046 became the strongest capped family baseline and ABI-047 showed that focal-Tversky raised recall but reduced aggregate filtered Dice, precision, and connectivity. It is not a promotion claim or full-data request.

## Hypothesis

ABI-046 showed that explicit thermal BTD planes plus a learned raw-channel projection are useful under trusted BCE-Dice: aggregate `val/filtered_dice` 0.208350, MIT 0.195981, Google 0.241080, filtered precision 0.254612, filtered recall 0.176315, filtered connectivity 0.383943, and filtered predicted-positive fraction 0.00251. ABI-047 changed only the trusted loss to focal-Tversky; it stayed finite and non-degenerate, raised filtered recall to 0.226438, and kept both source strata near 0.20 Dice, but aggregate filtered Dice decreased to 0.197039, precision fell to 0.174396, connectivity fell to 0.241859, and predicted-positive fraction rose to 0.00471.

Changing only the ABI-046 BTD-mixer training loss to trusted `bce_dice_cldice` should test whether continuity-aware supervision can improve thin-line connectivity or recover some recall while preserving more of ABI-046 precision than focal-Tversky. Because the branch already contains spectrally cleaner BTD features and a non-collapsed BCE-Dice baseline, this is a targeted loss-continuation rather than a repeat of the earlier MCAST-lineage clDice failure.

## Comparison Target

The primary comparison target is ABI-046 `abi046_fullspectral_deeplabv3plus_btd_mixer_v1`, Run `run_20260826_204203_732aee`: 12 epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `abi_16ch`, `bce_dice`, `random_mirroring`, aggregate `val/filtered_dice` 0.208350, MIT filtered Dice 0.195981, Google filtered Dice 0.241080, filtered precision 0.254612, filtered recall 0.176315, filtered connectivity 0.383943, and filtered predicted-positive fraction 0.00251.

ABI-047 Run `run_20260827_110027_1c679a` is the recall/precision loss-tradeoff reference: filtered Dice 0.197039, precision 0.174396, recall 0.226438, connectivity 0.241859, MIT filtered Dice 0.194474, Google filtered Dice 0.202417, and filtered predicted-positive fraction 0.00471. ABI-044 Run `run_20260813_145951_a64a37` remains the raw-BCE family scout reference. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context, not a strict gate for this capped family-development run.

## Expected Effect

If the BTD-mixer front end gives the decoder cleaner contrail-line evidence, `bce_dice_cldice` may improve continuity-sensitive structure and recover some recall without the wider positive-mask expansion seen under focal-Tversky. A useful positive result would improve or credibly tie ABI-046 aggregate filtered Dice while increasing connectivity, recall, or source balance. A useful negative result would show that continuity-aware primary loss is not beneficial for this BTD DeepLabV3+ branch at the active 12-epoch capped budget, narrowing future work toward architecture refinements, auxiliary targets, or a different family scout.

## Implementation Sketch

- Reuse ABI-046 candidate-owned front end exactly: normalize provider-approved ABI channels 1-16, compute eight explicit thermal BTD planes from approved thermal bands, and concatenate a 16-channel learned 1x1 GELU projection of normalized raw channels.
- Reuse the ABI-046 SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, no encoder weights, and one `mask_logits` output plane.
- Change only the manifest-selected trusted primary loss from `bce_dice` to `bce_dice_cldice`.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, targets, loss implementation, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, losses, metrics, artifact filtering, target transforms, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-046 and ABI-047, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves connectivity, raises recall without ABI-047-like precision loss, or clearly shows that continuity-aware primary loss is not a good fit for the BTD-mixer branch under the active capped budget.

## Continuation and hard stop

Continue DeepLabV3+ BTD-mixer development only if this variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, connectivity, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-046 family baseline or offer a useful continuity/recall trade-off, document the result and consider a separate BCE-Dice BTD architecture refinement, trusted auxiliary-target continuation, or a different architecture-family scout. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
