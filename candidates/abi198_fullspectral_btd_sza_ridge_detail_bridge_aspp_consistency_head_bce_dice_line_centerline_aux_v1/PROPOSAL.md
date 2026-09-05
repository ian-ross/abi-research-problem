# ABI-198 ridge-detail bridge ASPP consistency-calibrated head

## Proposal classification

**Family-development continuation.** ABI-198 is a controlled architecture continuation of the ABI-196 ridge-detail bridge ASPP branch. It is not a promotion claim; it tests one in-contract calibration/fusion change aimed at ABI-196's remaining negative-patch false-positive burden while preserving the branch's improved MIT and median-positive recall.

## Hypothesis

ABI-196 became the strongest whole-validation aggregate filtered-Dice Result in local Research History, but its failure-bucket review showed that the gain came with more negative-patch false positives than ABI-181 and much more than ABI-184. ABI-197 showed that changing the trusted primary loss to `bce_dice_cldice` weakened this branch rather than fixing clutter. A differentiable mask-logit head that conditions the final mask logits on the model's own soft Line and Centerline auxiliary evidence may reduce unsupported texture/ridge false positives without using thresholding, postprocessing, Artifact Filters, or candidate-owned losses.

## Comparison Target

The primary comparison target is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147, MIT/Google filtered Dice 0.4026/0.4368, filtered precision 0.4379, filtered recall 0.3938, and filtered connectivity 0.3827. Secondary references are ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-181 `run_20260902_150611_cbbf35` as the prior aggregate reference, and ABI-197 `run_20260903_230028_82d11d` as the negative clDice loss-policy probe.

## Expected Effect

A positive exploratory outcome would recover ABI-196/ABI-195 style ridge-detail learning while shifting the capped operating point toward ABI-184-like discipline: higher precision and/or lower filtered predicted-positive fraction than ABI-196-style heads, with no large loss of recall, MIT filtered Dice, or connectivity. A negative but useful outcome would show that line/centerline-conditioned mask calibration behaves like another local gate and suppresses useful contrail evidence or fails to distinguish clutter from true thin lines.

## Implementation Sketch

Start from the ABI-196 model architecture and trusted manifest policy. Keep approved `abi_16ch_plus_sza` input, normalized raw ABI channels, deterministic ABI-channel-derived thermal BTD planes, SZA features, learned channel projection, signed local/mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, final line-aware refinement, and provider-derived Line plus Centerline auxiliary targets.

Change only the final architecture head: compute `line_logits` and `centerline_logits` from refined features as before, then compute `mask_logits` with a new `ConsistencyCalibratedMaskHead`. This head concatenates refined features, refined features softly weighted by `sigmoid(line_logits)` and `sigmoid(centerline_logits)`, and bounded `tanh` auxiliary logits. It predicts a small bounded residual added to an ordinary base mask head through a learned sigmoid gate. The residual is fully differentiable and trained only by the Harness-owned primary mask loss plus the existing trusted auxiliary losses; it performs no thresholding, filtering, sample selection, postprocessing, target construction, or metric calculation.

Keep trusted manifest choices unchanged from ABI-196 except use the standard exploratory budget: `bce_dice`, Line Target weighted BCE at 0.01, Centerline Target weighted BCE at 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, `max_epochs: 12`, and `constant_lr`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, exploratory max epochs 12, constant scheduler policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, the 3,600-second exploratory Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. No late-improving budget, full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The exploratory Result is promising if, relative to the ABI-195/196 ridge-detail family at comparable capped evidence, it improves precision or predicted-positive discipline while retaining a capped filtered Dice near the family frontier and avoiding major recall/connectivity regression.

## Fallback/Next Decision

If ABI-198 fails validation or smoke due to the new head, repair the candidate-local implementation without changing the scientific hypothesis. If it completes but regresses like ABI-197 or ABI-194, do not request late36 or whole-validation diagnostics for this exact head; broaden away from local post-refinement calibration toward a distinct architecture family or a trusted data/loss-policy frontier. If it reaches a credible capped tradeoff near ABI-196 with improved precision or lower predicted-positive burden, write a Research Note and consider a later late-improving continuation or whole-validation failure-bucket evaluation before any promotion claim.
