# ABI-199 full-spectral BTD+SZA oriented gap bridge ASPP

## Proposal classification

**Family-development continuation.** ABI-199 is a controlled architecture continuation after ABI-196/197/198. It is not a promotion claim; it tests whether moving the next change away from local mask-head calibration and into an ungated, architecture-internal oriented feature bridge can preserve ABI-196's improved recall/source balance while reducing unsupported clutter.

## Hypothesis

ABI-196 is the current strongest whole-validation aggregate filtered-Dice reference, but its failure-bucket review showed more negative-patch false positives than ABI-181 and ABI-184. ABI-197's trusted `bce_dice_cldice` loss-policy probe and ABI-198's consistency-calibrated mask head both weakened the branch and did not improve predicted-positive discipline. A non-thresholding oriented gap bridge may be a better in-contract continuation: it gives the decoder long horizontal, vertical, and dilated gap-spanning evidence before final prediction, without multiplying mask logits by auxiliary outputs or adding another post-refinement gate.

## Comparison Target

The primary comparison target is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147, MIT/Google filtered Dice 0.4026/0.4368, filtered precision 0.4379, filtered recall 0.3938, and filtered connectivity 0.3827. Secondary references are ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-195 `run_20260903_135523_8976a0` as the exploratory ridge-detail parent, ABI-197 `run_20260903_230028_82d11d` as the negative clDice loss-policy probe, and ABI-198 `run_20260904_000632_1a04ae` as the negative local consistency-head probe.

## Expected Effect

A positive exploratory outcome would keep ABI-196/ABI-195 style high-resolution signed-detail learning while recovering cleaner line support: capped filtered Dice should move back toward the ridge-detail family frontier, with better precision or lower filtered predicted-positive fraction than ABI-196-style recall-heavy checkpoints and without a major MIT, recall, or connectivity regression. A negative but useful outcome would show that additional oriented context before prediction still behaves like a clutter-amplifying branch, supporting a broader architecture-family switch rather than further ridge-detail local edits.

## Implementation Sketch

Start from the ABI-196 architecture and trusted manifest policy. Keep approved `abi_16ch_plus_sza` input, normalized raw ABI channels, deterministic ABI-channel-derived thermal BTD planes, SZA features, learned channel projection, signed local/mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, trusted `bce_dice`, `combined_source_balanced`, trusted `random_mirroring`, and provider-derived Line plus Centerline auxiliary targets.

Change only architecture-internal feature fusion. Replace the ridge-detail bridge plus gated line-aware refinement with an `OrientedGapBridge` and `OrientedLineRefinement`. The bridge fuses decoder, stem, full-scale, and high-resolution detail features; uses long horizontal/vertical convolutions and dilated smoothed context branches to span small gaps in line evidence; and adds a bounded zero-initialized residual to the decoder features. The final refinement concatenates ungated local detail, horizontal, vertical, and dilated context branches before the ordinary mask, line, and centerline heads. It does not apply thresholding, postprocessing, Artifact Filters, target transforms, custom losses, sampling, metrics, coordinate features, or filesystem/runtime side effects.

Keep the manifest on the standard exploratory budget: `bce_dice`, Line Target weighted BCE at 0.01, Centerline Target weighted BCE at 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, `max_epochs: 12`, and `constant_lr`.

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
6. The exploratory Result is promising if it improves ABI-195/198-level capped overlap while preserving source-informative recall and either reduces ABI-196's predicted-positive burden or improves connectivity/precision enough to justify one bounded family-development continuation.

## Fallback/Next Decision

If ABI-199 fails validation or smoke due to the new oriented modules, repair the candidate-local implementation without changing the scientific hypothesis. If it completes but regresses like ABI-197/198 or shows volatile clutter amplification, do not request late36 or whole-validation diagnostics for this exact branch; broaden to a materially different line-continuity architecture family or a trusted data/training-policy frontier. If it reaches a credible capped tradeoff near ABI-196 with better precision, connectivity, or predicted-positive discipline, write a Research Note and consider a later whole-validation failure-bucket Evaluation Request or late-improving close-continuation before any promotion claim.
