# ABI-200 full-spectral BTD+SZA spectral-contrast bridge ASPP

## Proposal classification

**Family-development continuation / broadened architecture-front-end probe.** ABI-200 is not a promotion claim. It follows the ABI-196 through ABI-199 ridge-detail ASPP evidence by moving the next change away from post-head calibration, clutter gates, and extra oriented gap propagation, and instead tests whether a lightweight spectral-contrast reliability bridge can reduce cloud-edge clutter before final mask prediction.

## Hypothesis

ABI-196 is the current strongest whole-validation aggregate filtered-Dice reference, but its failure-bucket review showed higher negative-patch false-positive burden than ABI-181 and ABI-184. ABI-197, ABI-198, and ABI-199 did not solve that tradeoff with trusted clDice, line/centerline consistency calibration, or an ungated oriented gap bridge. A spectral-contrast bridge may be a safer in-contract direction: BTD planes plus Solar Geometry Input describe thin-ice/cloud-contrast reliability, while signed high-resolution detail describes candidate line structure. Fusing these signals inside the feature decoder may preserve ABI-196-style MIT/median-positive recall while rejecting unsupported detail clutter, without thresholding, postprocessing, Artifact Filters, custom losses, sampling changes, or coordinate features.

## Comparison Target

Primary comparison target: ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whole-validation filtered Dice 0.4147 with MIT/Google filtered Dice 0.4026/0.4368, precision 0.4379, recall 0.3938, connectivity 0.3827, and known excess negative-patch false positives.

Secondary references: ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference; ABI-195 `run_20260903_135523_8976a0` as the high-precision ridge-detail parent; ABI-197/198/199 as negative local loss/head/oriented-bridge probes; and ABI-181/192 as whole-validation aggregate/directional-context comparators.

## Expected Effect

A useful exploratory outcome would not need to beat ABI-196 immediately. It should show source-informative, non-collapsed predictions and move the tradeoff in a diagnostically useful direction: either lower filtered predicted-positive fraction or higher precision/connectivity than ABI-196-like recall-heavy checkpoints, while avoiding a large MIT or recall collapse. A negative outcome would show that BTD/SZA contrast reliability is not enough to fix the current false-positive burden inside this signed-detail ASPP lineage, supporting a broader architecture-family switch rather than another local bridge.

## Implementation Sketch

Start from the finite ABI-196 signed-detail full-scale skip ASPP architecture and trusted manifest policy. Keep approved `abi_16ch_plus_sza` input, normalized ABI channels, deterministic ABI-channel-derived thermal BTD planes, SZA features, learned 1x1 projection, signed local/mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, trusted `bce_dice`, `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, and provider-derived Line plus Centerline auxiliary targets.

Change only architecture-internal feature fusion. Replace the ridge-preserving detail bridge with `SpectralContrastDetailBridge`. The bridge receives only already-approved front-end features, using the eight BTD planes plus scaled/cosine SZA slice as contrast evidence. It projects raw, signed local, signed mid-scale, and broad contrast features; fuses them with signed-detail and decoder-context features; applies a learned reliability gate to contrast features; and adds a bounded zero-initialized residual before the ordinary line-aware refinement and mask/line/centerline heads. It predicts no target and performs no filtering or thresholding.

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
2. Parameter count remains within the 25,000,000 smoke ceiling and the run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The Result is promising if it improves on ABI-199's capped filtered Dice while recovering some ABI-184/196 precision, connectivity, or positive-area discipline without a major recall/source-balance regression.

## Fallback/Next Decision

If ABI-200 fails validation or smoke because of the new bridge, repair the candidate-local implementation while preserving the hypothesis. If it completes but regresses below ABI-199 or repeats ABI-197/198/199-style clutter/connection degradation, do not request late36 or whole-validation diagnostics for this exact branch. If it reaches a credible capped tradeoff near ABI-196 with better precision, connectivity, or predicted-positive discipline, write a Research Note and consider either a whole-validation failure-bucket Evaluation Request or a late-improving close-continuation under the approved budget policy before any promotion claim.
