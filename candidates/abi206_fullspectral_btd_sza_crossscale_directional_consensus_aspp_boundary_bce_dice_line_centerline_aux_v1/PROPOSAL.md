# ABI-206 full-spectral BTD+SZA cross-scale directional-consensus ASPP boundary auxiliary probe

## Proposal classification

**Family-development continuation.** ABI-206 is a controlled auxiliary-policy probe within the ABI-201/202 cross-scale directional-consensus ASPP family. It is not a promotion claim and does not request the late-improving budget.

## Hypothesis

ABI-202 established the strongest current whole-validation aggregate filtered-Dice Result in local Research History, but its failure-bucket review shows residual false-positive burden: 672,206 filtered predicted-positive pixels, 374,370 filtered false-positive pixels, and weaker strict negative-patch discipline than ABI-184. ABI-203 and ABI-204 tried explicit foreground/support gating and lost recall/connectivity; ABI-205 switched to focal-Tversky and became less precise and less connected. A lower-risk in-contract alternative is to keep ABI-202's BCE-Dice optimization and line/connectivity architecture unchanged, but add a very low-weight trusted Boundary Target auxiliary head. Boundary supervision may make the shared decoder attend to mask edges and compact support, reducing diffuse clutter, while the existing Line and Centerline auxiliaries continue to preserve thin-line continuity.

The hypothesis is about trusted auxiliary supervision and architecture-local output heads only. Candidate code will not implement data loading, custom losses, metrics, Artifact Filters, thresholding, postprocessing, target derivation, sampling behavior, augmentation transforms, coordinate features, resource scheduling, filesystem persistence, or runtime downloads.

## Comparison Target

Primary comparison targets:

- ABI-202 `run_20260904_043143_ee0005`, current whole-validation aggregate reference after late36, with capped `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312, MIT/Google 0.4141/0.4644, precision 0.4431, recall 0.4199, and connectivity 0.4625.
- ABI-201 `run_20260904_032624_7e855a`, same architecture under the exploratory budget, with capped filtered Dice 0.3958 at epoch 12, precision 0.4587, recall 0.3481, connectivity 0.4630, and filtered predicted-positive fraction 0.002749.

Secondary references are ABI-184 `run_20260902_213856_2c04ac`, retained as the precision/connectivity and strict negative-patch-discipline reference, and the recent negative ABI-203/204/205 follow-ups.

## Expected Effect

A useful positive Result would improve or hold ABI-201's 12-epoch aggregate/source filtered Dice while increasing precision or lowering filtered predicted-positive fraction without sacrificing the ABI-201/202 connectivity signal. A useful negative Result would show that adding Boundary Target pressure on top of Line and Centerline supervision over-constrains the shared decoder, supporting a move away from local auxiliary/gating changes toward a broader architecture scout.

Because ABI-206 is an exploratory 12-epoch probe, it is not required to beat ABI-202's late36 selected checkpoint. Continuation evidence would include finite non-collapsed predictions, source-informative MIT and Google metrics, capped filtered Dice near or above ABI-201/203, improved positive-area discipline versus ABI-202, and a best checkpoint at or near epoch 12 with an improving or ambiguous trajectory.

## Implementation Sketch

Start from the validated ABI-201/202 cross-scale directional-consensus ASPP decoder: provider-approved `abi_16ch_plus_sza` inputs, normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels only, normalized/cosine Solar Geometry features, learned 1x1 channel mixture, signed local/mid-scale detail stems, compact residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, and line-aware refinement.

Keep the architecture-internal line/detail/context path and existing `mask_logits`, `line_logits`, and `centerline_logits` heads. Add one additional one-by-one convolutional `boundary_logits` head from the same refined feature map. Keep trusted `bce_dice`, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and `constant_lr`. Add the provider-derived Boundary Target auxiliary with trusted `weighted_bce` weight 0.005 while retaining Line weight 0.01 and Centerline weight 0.02.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits`, `boundary_logits`, and `centerline_logits` auxiliary outputs.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line`, `boundary`, and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01, 0.005, and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and constant scheduler policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, effective epoch limit, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential exploratory representative capped Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 effective epochs, batch size 4, 3,600-second Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No `late_improving` budget is requested for this first boundary-auxiliary probe.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The probe is promising if it improves precision, filtered predicted-positive discipline, or MIT/source balance versus ABI-201/203 while keeping filtered Dice near the ABI-201/203 exploratory range and connectivity near ABI-201/202 rather than reproducing the ABI-204/205 connectivity regression.

## Fallback/Next Decision

If ABI-206 fails validation or smoke, classify the failure and repair only the candidate-local packaging or output-spec issue while preserving the hypothesis. If it completes but loses connectivity/recall or falls well below ABI-201/203, do not repeat the boundary-auxiliary addition unchanged; broaden to a cheaper recall-preserving refinement or a materially different architecture family scout. If it completes finitely with improved precision/positive-area discipline while holding source balance and connectivity, write a Research Note and consider either a close-continuation or a whole-validation Evaluation Request only after comparing the capped trajectory against ABI-201, ABI-202, ABI-184, and ABI-203.
