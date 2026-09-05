# ABI-201 full-spectral BTD+SZA cross-scale directional-consensus ASPP

## Proposal classification

**Family-development continuation / broadened line-continuity architecture probe.** ABI-201 is not a promotion claim. It follows the ABI-196 through ABI-200 evidence by broadening away from the exact ridge-detail/local-bridge edit axis and testing a cross-scale directional-consensus feature bridge inside the finite signed-detail ASPP decoder family.

## Hypothesis

ABI-196 is the current whole-validation aggregate filtered-Dice reference, but its failure-bucket review showed excess negative-patch false-positive burden compared with ABI-181 and ABI-184. ABI-197 through ABI-200 adjusted local loss/head/bridge behavior without solving the false-positive/connectivity tradeoff. A feature bridge that requires agreement among high-resolution decoder context, signed detail, stem evidence, full-scale fused context, and directional horizontal/vertical/diagonal views may preserve ABI-196-style MIT/median-positive recall while discouraging unsupported isolated clutter. This remains architecture-internal feature fusion only, not thresholding, postprocessing, Artifact Filtering, target transformation, custom loss, custom metric, sampling, data loading, or coordinate use.

## Comparison Target

Primary comparison target: ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whole-validation filtered Dice 0.4147 with MIT/Google filtered Dice 0.4026/0.4368, precision 0.4379, recall 0.3938, connectivity 0.3827, and known excess negative-patch false positives.

Secondary references: ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference; ABI-195 as the high-precision ridge-detail parent; ABI-199 as a recall-heavy but low-connectivity oriented-gap negative result; ABI-200 as a spectral-contrast bridge negative/mixed result; and ABI-181/192 as whole-validation aggregate/directional-context comparators.

## Expected Effect

A useful exploratory result need not beat ABI-196 immediately. It should complete finitely with non-collapsed, Dataset Source-informative predictions and produce a diagnostically useful tradeoff: higher precision/connectivity or lower filtered predicted-positive fraction than ABI-199/200 while avoiding ABI-195-like under-recall and avoiding a large MIT or Google source regression. A negative outcome would show that cross-scale directional agreement is not enough to correct the current clutter/connectivity burden inside this ASPP lineage and would support moving to a more materially different decoder family or trusted data/training-policy frontier.

## Implementation Sketch

Start from the finite full-spectral BTD+SZA signed-detail full-scale skip ASPP implementation pattern used by ABI-196 through ABI-200, but use a compact base width of 36 to keep the unprofiled bridge within the exploratory resource envelope. Keep approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry features, learned 1x1 channel mixture, signed local/mid-scale detail stem, compact residual encoder, ASPP context, full-scale skip fusion, trusted `bce_dice`, trusted `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, and provider-derived Line plus Centerline auxiliary targets.

Change only architecture-internal feature fusion before final refinement. Replace the spectral/ridge local bridge with `CrossScaleDirectionalConsensusBridge`. The bridge consumes decoder, signed-detail, stem, and full-scale fused features; forms learned horizontal and vertical line-context branches, no-wrap diagonal shifted averages, broad smoothed context, and local signed-detail contrast; uses an agreement gate over decoder/detail/stem/full-scale differences; and adds a bounded zero-initialized residual to the decoder features. It predicts no target, applies no filtering, and does not own any data, loss, metric, threshold, Artifact Filter, or sampling behavior.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, exploratory max epochs 12, and constant scheduler policy.
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
6. The Result is promising if it improves ABI-199/200 precision/connectivity or positive-area discipline while remaining near their capped filtered-Dice/recall range and without a major source-balance regression.

## Fallback/Next Decision

If ABI-201 fails validation or smoke because of the new bridge, repair the candidate-local implementation while preserving the hypothesis. If it completes but regresses below ABI-199/200 or repeats the weak-connectivity/clutter tradeoff, do not request late36 or whole-validation diagnostics for this exact branch. If it reaches a credible capped tradeoff near ABI-196 with better precision, connectivity, or predicted-positive discipline, write a Research Note and consider either a whole-validation failure-bucket Evaluation Request or a late-improving close-continuation under the approved budget policy before any promotion claim.
