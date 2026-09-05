# ABI-205 full-spectral BTD+SZA cross-scale directional-consensus ASPP focal-Tversky probe

## Proposal classification

**Family-development continuation / controlled loss-policy probe.** ABI-205 is not a promotion claim. It keeps the finite ABI-201/202 cross-scale directional-consensus ASPP architecture fixed and changes only the trusted primary loss from `bce_dice` to allowlisted `focal_tversky` under the exploratory budget.

## Hypothesis

ABI-202 is the current whole-validation aggregate filtered-Dice reference, with strong recall, Google Dice, connectivity, and median positive-patch quality, but its failure-bucket review still shows more whole-split predicted-positive area and false-positive burden than the stricter ABI-184 reference. ABI-203 and ABI-204 tried architecture-local foreground/support gates and reduced useful line evidence. A safer next probe is to leave the architecture unchanged and ask whether trusted focal-Tversky optimization shifts the same model toward a better precision/recall or false-positive tradeoff without adding near-timeout architectural complexity or candidate-owned postprocessing.

This tests a Harness-owned loss choice only. Candidate code still defines model architecture only and does not implement data loading, loss logic, metrics, thresholding, Artifact Filters, sampling, augmentation, target transforms, training loops, runtime downloads, persistence writes, resource placement, or coordinate features.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, whose late-improving selected checkpoint reached capped `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312 with MIT/Google filtered Dice 0.4141/0.4644, precision 0.4431, recall 0.4199, and connectivity 0.4625.

Secondary references: ABI-201 `run_20260904_032624_7e855a` as the 12-epoch same-architecture BCE-Dice parent; ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference; ABI-203/204 as negative evidence for added calibration/support gates; canonical MCAST 1.1/2.1 from the trusted campaign context for baseline context only.

## Expected Effect

A useful result should complete finitely with non-collapsed, Dataset Source-informative predictions. It would be promising if, relative to ABI-201 at the same 12-epoch exploratory budget, it improves precision, reduces filtered predicted-positive fraction, or improves false-positive discipline while preserving most of the cross-scale branch's recall/connectivity and avoiding MIT or Google source collapse. A negative outcome would indicate that focal-Tversky is not a cleaner way to control ABI-202's remaining false positives and would support either a different allowlisted auxiliary/loss configuration or a broader architecture-family scout rather than more local gates.

## Implementation Sketch

Copy the ABI-201/202 architecture unchanged: provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine Solar Geometry features, learned 1x1 channel mixture, signed local/mid-scale detail stem, compact base-width-36 residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, line-aware refinement, and primary/Line/Centerline logits.

The manifest-only change is `training.loss: focal_tversky`. Keep trusted `combined_source_balanced` sampling traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, 12 exploratory epochs, constant learning rate, and provider-derived Line plus Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, exploratory max epochs 12, and constant scheduler policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run with at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, the 3,600-second exploratory Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. No late-improving budget, full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The Result is promising if it improves same-budget ABI-201 precision or positive-area discipline while retaining source-balanced filtered Dice near the ABI-201/203 range, or if it shows late improvement justifying an approved `late_improving` continuation.

## Fallback/Next Decision

If ABI-205 fails validation or smoke, repair only candidate-local contract or implementation errors while preserving the fixed-architecture focal-Tversky hypothesis. If it completes but regresses in Dice, recall, connectivity, and source balance, do not request late36 or whole-validation diagnostics for this exact loss probe. If it produces a credible same-budget tradeoff, write a Research Note and consider either a late-improving close-continuation under the approved budget policy or a whole-validation failure-bucket Evaluation Request before any promotion claim.
