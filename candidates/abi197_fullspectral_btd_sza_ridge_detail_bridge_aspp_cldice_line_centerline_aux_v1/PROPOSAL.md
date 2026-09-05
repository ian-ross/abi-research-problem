# ABI-197 ridge-detail bridge ASPP clDice loss-policy probe

## Proposal classification

**Family-development continuation.** ABI-197 is a controlled trusted-loss-policy continuation of ABI-196. It keeps the ridge-detail bridge ASPP architecture unchanged and changes only the primary loss selected in `manifest.yaml` from trusted `bce_dice` to trusted `bce_dice_cldice`.

## Hypothesis

ABI-196 became the strongest local whole-validation aggregate filtered-Dice reference, but its failure-bucket review showed that the gain was paid for with more negative-patch false positives and weaker false-positive discipline than ABI-181 and ABI-184. Selecting the trusted `bce_dice_cldice` primary loss for the same ridge-detail bridge architecture may bias training toward connected thin-line masks and reduce isolated clutter while preserving ABI-196's improved MIT/source-balance and median positive-patch recall. A negative outcome would show that the ridge-detail bridge's false-positive burden is not improved by the current trusted clDice objective and should push the next step away from this local loss-policy axis.

## Comparison Target

The primary comparison target is ABI-196 `run_20260903_195527_248472`: whole-validation filtered Dice 0.4147, MIT/Google filtered Dice 0.4026/0.4368, filtered precision 0.4379, filtered recall 0.3938, filtered connectivity 0.3827, and 88,298 negative-patch false-positive pixels in `eval_evalreq_abi196_wholeval_failure_buckets_v1`. Capped selected-checkpoint comparison uses the same Run's epoch-34 `val/filtered_dice` 0.4133, MIT/Google 0.4007/0.4442, precision 0.4350, recall 0.3936, connectivity 0.3746, and predicted-positive fraction 0.003278.

Secondary references are ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-181 `run_20260902_150611_cbbf35` as the prior aggregate reference and cleaner false-positive comparator, and ABI-192 `run_20260903_085513_f395ad` as the late36 directional-lattice recall comparator.

## Expected Effect

A useful positive result would trade a small amount of ABI-196 recall, if necessary, for improved fixed-threshold precision, higher Contrail Connectivity Metric, a lower filtered predicted-positive fraction, and better MIT/Google source balance than earlier clDice branches. The most useful outcome would remain within about 0.010 capped `val/filtered_dice` of ABI-196 while improving precision/connectivity or reducing positive-area clutter. A useful negative result would confirm that the trusted clDice loss does not repair ABI-196's clutter burden and that the next experiment should broaden to a different architecture or data/loss/front-end policy rather than repeating this exact ridge-detail branch.

## Implementation Sketch

Reuse ABI-196 `model.py` architecture unchanged except for the candidate identifier string: normalized provider-approved GOES ABI channels 1-16 plus Solar Geometry Input, deterministic ABI-channel-derived thermal BTD planes, learned channel projection, signed local/mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, line-aware final refinement, primary `mask_logits`, and auxiliary `line_logits` plus `centerline_logits`. In `manifest.yaml`, select trusted `bce_dice_cldice` instead of `bce_dice`; keep Line Target weighted BCE at 0.01, Centerline Target weighted BCE at 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, max epochs 12, and `constant_lr`. Do not include a late-improving budget request for this first loss-policy probe.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant scheduler policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, 3,600 seconds wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. No full-data claim, promotion decision, late-improving budget request, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted runtime envelope demonstrated by ABI-195/196.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The branch is promising if it preserves source-informative ABI-196-like overlap while improving at least one clutter/structure indicator: filtered precision, filtered connectivity, or filtered predicted-positive fraction relative to ABI-196's capped checkpoint.

## Fallback/Next Decision

If ABI-197 fails smoke or training for a candidate-owned shape or interface error, prepare at most one repair preserving this proposal. If it completes but loses both aggregate filtered Dice and the intended precision/connectivity/positive-area indicators, do not repeat the clDice probe unchanged and broaden away from this exact loss-policy branch. If it improves precision/connectivity or positive-area discipline while staying near ABI-196 on capped filtered Dice, write a Research Note and consider either a late-improving continuation only if the best checkpoint is near epoch 12 with non-collapsed improvement, or a whole-validation failure-bucket Evaluation Request if the capped signal is already competitive and diagnostically important.
