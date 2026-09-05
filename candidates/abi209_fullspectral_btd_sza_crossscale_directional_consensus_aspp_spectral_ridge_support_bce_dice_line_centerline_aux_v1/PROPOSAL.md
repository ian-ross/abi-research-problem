# ABI-209 full-spectral BTD+SZA cross-scale directional-consensus ASPP spectral-ridge support

## Proposal classification

**Family-development continuation.** ABI-209 is a bounded exploratory continuation of the ABI-201/202 cross-scale directional-consensus ASPP family, not a promotion claim and not a request for the late-improving budget.

## Hypothesis

ABI-202 is the current strongest whole-validation aggregate reference, but its failure-bucket review still shows more aggregate false-positive pixels and lower precision than ABI-184. Recent direct suppression attempts were too blunt: ABI-203's mask-head calibration reduced positive area without improving precision, ABI-204/206 over-constrained support or source balance, and ABI-208 showed that orientation consensus alone can trade away recall. A lightweight representation-level spectral-ridge support bridge before final line-aware refinement may reduce unsupported clutter while preserving ABI-202's cross-source recall and connectivity, because it lets approved-channel spectral/BTD evidence and signed ridge detail modulate features before the final heads rather than thresholding logits or adding an Artifact Filter.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, with capped best `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312, MIT/Google 0.4141/0.4644, precision 0.4431, recall 0.4199, and connectivity 0.4625.

Secondary targets: ABI-203 `run_20260904_073913_3edd12` as the negative foreground-calibrated head probe, ABI-206 `run_20260904_105645_8f8ab1` as the negative boundary/compactness probe, ABI-208 `run_20260904_130809_8896f4` as the over-constrained orientation-consensus lesson, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

## Expected Effect

The desired exploratory signal is higher precision or lower predicted-positive fraction than ABI-202/203 at similar aggregate filtered Dice, with less MIT/recall/connectivity cost than ABI-206/208. A useful positive result would remain source-informative, improve over ABI-203's capped aggregate or precision/recall balance, and approach ABI-202's recall/connectivity trajectory by epoch 12. A useful negative result would show that even representation-level spectral-ridge support over-constrains the ABI-202 path, motivating a broader architecture family or data/loss-policy frontier rather than more local clutter gates.

## Implementation Sketch

Start from the validated ABI-202 architecture: approved `abi_16ch_plus_sza` input, normalized ABI channels 1-16, deterministic BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input, signed local/mid-scale detail stems, residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, line-aware refinement, and `mask_logits`, `line_logits`, and `centerline_logits` heads.

Add a small `SpectralRidgeSupportBridge` between the cross-scale consensus bridge and the existing final line-aware refinement. The bridge projects the already constructed spectral/BTD/SZA feature tensor, signed ridge detail features, broad decoder/full-scale context, and local disagreement into a soft support gate. It applies only a bounded zero-initialized feature residual, so initial behavior remains close to ABI-202 while allowing training to learn modest spectral/ridge support corrections. It predicts no target and performs no thresholding, postprocessing, Artifact Filtering, sampling, augmentation, loss computation, metric computation, or coordinate use.

Keep the manifest policy unchanged from ABI-202 except for using the default exploratory budget: trusted `bce_dice`, `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, manifest `max_epochs: 12`, disabled early stopping, and constant scheduler policy.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and `constant_lr` scheduler.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential exploratory capped Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 effective epochs, batch size 4, 3,600-second Docker timeout, at most four Harness-selected `first_n` prediction artifacts, 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested for this first spectral-ridge support variant.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and runtime stays within the exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it improves ABI-203's aggregate filtered Dice or precision/recall balance, improves precision or predicted-positive discipline versus ABI-202 without large recall/connectivity loss, or finishes at epoch 12 with a finite, improving, source-balanced trajectory that justifies a later close-continuation decision.

## Fallback/Next Decision

If ABI-209 fails validation or smoke, classify the failure and repair only a candidate-local implementation issue while preserving this hypothesis. If it completes but loses source balance, recall, or connectivity like ABI-206/208, do not request late36 for this exact branch and broaden to a different architecture family or training/data/loss-policy frontier. If it completes with a useful precision/area-discipline gain near ABI-202's aggregate tradeoff, write a Research Note and consider whole-validation failure-bucket evaluation or, only if the best checkpoint is near epoch 12 with a late-improving trajectory, a future late-improving close-continuation request.
