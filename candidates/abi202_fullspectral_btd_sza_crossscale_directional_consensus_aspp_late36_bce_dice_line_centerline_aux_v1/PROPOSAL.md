# ABI-202 full-spectral BTD+SZA cross-scale directional-consensus ASPP late36

## Proposal classification

**Family-development continuation / late-improving close-continuation.** ABI-202 is not a promotion claim. It repeats the ABI-201 cross-scale directional-consensus architecture and training policy while requesting the approved Harness-owned 36-epoch late-improving budget because ABI-201 selected its final exploratory epoch as best after a volatile late recovery.

## Hypothesis

ABI-201 showed that cross-scale directional consensus can restore precision, connectivity, Google filtered Dice, and conservative predicted-positive area relative to ABI-199/200, but its 12-epoch exploratory Run ended exactly at its best checkpoint after a late recovery. Extending this exact resource-safe branch under the approved late-improving budget may allow the model to recover MIT/source balance and recall while preserving the high-connectivity/low-clutter operating point. The hypothesis is about training-horizon truncation of an already finite architecture, not about changing data loading, sampling, augmentation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinates, scheduler policy, or resource placement.

## Comparison Target

Primary comparison target: ABI-201 `run_20260904_032624_7e855a`, which reached capped `val/filtered_dice` 0.3958 at epoch 12 with MIT/Google filtered Dice 0.3751/0.4497, filtered precision 0.4587, filtered recall 0.3481, filtered connectivity 0.4630, and filtered predicted-positive fraction 0.002749.

Promotion/frontier context: ABI-196 `run_20260903_195527_248472` remains the current capped aggregate reference for this branch family at filtered Dice 0.4133 after late36, with ABI-181 as the whole-validation frontier and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Secondary recent bridge references are ABI-199 and ABI-200.

## Expected Effect

A useful Result should complete finitely and show whether ABI-201's final-epoch jump was a truncated learning signal or noise. The intended improvement is higher aggregate and MIT filtered Dice and/or recall than ABI-201 while retaining its strong connectivity, Google filtered Dice, precision, and conservative predicted-positive fraction. A negative but informative outcome would plateau, overfit, or trade away the ABI-201 connectivity/positive-area discipline, supporting a move away from this exact bridge rather than further late-budget repeats.

## Implementation Sketch

Copy the validated ABI-201 Candidate architecture unchanged. Keep approved `abi_16ch_plus_sza` inputs, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry features, learned 1x1 channel mixture, signed local/mid-scale detail stem, compact residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, line-aware refinement, and `mask_logits`, `line_logits`, and `centerline_logits` heads.

Keep the manifest choices unchanged from ABI-201: trusted `bce_dice`, trusted `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, provider-derived Line plus Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, exploratory `max_epochs: 12`, and `constant_lr` scheduling. Add only a candidate-local `budget_request.yaml` requesting `late_improving` with `requested_max_epochs: 36`, parent Run `run_20260904_032624_7e855a`, and `fallback_if_denied: run_exploratory_budget`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and constant scheduler policy.
- Candidate-local budget request: `schema_version: candidate_budget_request.v1`, `budget_class: late_improving`, `requested_max_epochs: 36`, parent Run `run_20260904_032624_7e855a`, and fallback to the exploratory budget if denied.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, effective epoch limit, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped close-continuation Run with the approved `late_improving` budget request: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, requested 36 effective epochs, the 10,800-second late-improving Docker timeout if approved, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. If the Harness denies the request, run under the exploratory 12-epoch/3,600-second budget and treat that bounded Result as valid.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted resource envelope for the effective budget.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The close-continuation is promising if it improves ABI-201 aggregate/MIT filtered Dice or recall while retaining near-ABI-201 precision, Google Dice, connectivity, and predicted-positive discipline, or if it reaches a credible capped tradeoff near ABI-196/184.

## Fallback/Next Decision

If ABI-202 fails validation or smoke despite unchanged model code, classify and repair only the candidate-local packaging/budget-request issue while preserving the hypothesis. If the late-improving request is denied, accept the exploratory-budget Result and do not stop for human approval solely because the longer budget was denied. If the Run completes but plateaus or loses ABI-201's connectivity/positive-area discipline, do not request another late-budget repeat of this exact branch; broaden to a materially different decoder/training/data/loss frontier. If it improves capped aggregate/source balance while preserving ABI-201's secondary strengths, write a Research Note and consider a whole-validation failure-bucket Evaluation Request before any promotion claim.
