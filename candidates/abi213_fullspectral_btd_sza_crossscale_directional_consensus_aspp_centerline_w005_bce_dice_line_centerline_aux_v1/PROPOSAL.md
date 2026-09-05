# ABI-213 full-spectral BTD+SZA cross-scale directional-consensus ASPP centerline-w005

## Proposal classification

**Family-development continuation / allowlisted auxiliary-policy probe.** ABI-213 is not a promotion claim. It is a controlled continuation of the ABI-201/202 cross-scale directional-consensus ASPP family after ABI-202 became the current whole-validation aggregate filtered-Dice reference and ABI-203 through ABI-212 did not find a better architecture-level false-positive-control branch.

## Hypothesis

The ABI-202 late36 checkpoint improved whole-validation aggregate filtered Dice, both Dataset Sources, recall, connectivity, and median positive-patch quality, but its failure-bucket review still showed more aggregate false-positive pixels and weaker negative-patch discipline than ABI-184. Recent architecture-heavy support/refiner variants either regressed scientifically or approached/exhausted the exploratory wall-clock budget. A lower-resource next question is whether stronger provider-derived Centerline Target supervision can make the already-viable cross-scale directional-consensus decoder prefer thin continuous line evidence over broader clutter while preserving ABI-202-family recall.

This is a manifest-level, Harness-owned objective-policy probe: Candidate code keeps the ABI-201 architecture unchanged and continues to emit `mask_logits`, `line_logits`, and `centerline_logits`. The only intended variation is increasing the trusted centerline auxiliary `weighted_bce` weight from 0.02 to 0.05 while keeping the trusted Line auxiliary weight at 0.01 and the trusted BCE-Dice primary loss unchanged. Candidate code does not define losses, targets, data loading, sampling behavior, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, training loops, runtime downloads, persistence writes, or resource scheduling.

## Comparison Target

Primary comparison targets:

- ABI-201 `run_20260904_032624_7e855a`, the exploratory architecture parent: capped best `val/filtered_dice` 0.3958 at epoch 12, MIT/Google 0.3751/0.4497, precision 0.4587, recall 0.3481, connectivity 0.4630, and filtered predicted-positive fraction 0.002749.
- ABI-202 `run_20260904_043143_ee0005`, the late36 same-architecture reference and current whole-validation aggregate leader: capped best `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312 with precision 0.4431, recall 0.4199, connectivity 0.4625.

Secondary comparison targets are ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-203 `run_20260904_073913_3edd12` as the foreground-calibrated exploratory head probe, and ABI-210/212 as recent resource-safe but scientifically mixed support-bridge probes.

## Expected Effect

The desired capped exploratory signal is not necessarily an immediate beat of the ABI-202 36-epoch selected checkpoint. A useful Result would show finite, non-collapsed, source-informative learning and move the ABI-201/202 family toward stricter line discipline: better connectivity, precision, or lower filtered predicted-positive fraction than ABI-203/210/212 while preserving more recall and MIT performance than ABI-201. If stronger centerline supervision reduces recall sharply, damages Google performance, or does not improve precision/connectivity/positive-area discipline, the result is negative evidence against this auxiliary-weight direction.

## Implementation Sketch

Copy the ABI-201 model architecture unchanged: provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, ABI-channel-derived thermal brightness-temperature-difference planes, normalized/cosine Solar Geometry Input features, learned 1x1 channel mixture, signed local/mid-scale detail stem, compact residual encoder, ASPP context, full-scale skip fusion, cross-scale directional-consensus feature bridge, line-aware refinement, and primary/auxiliary logit heads.

Change only the manifest-declared auxiliary weighting. Keep trusted `bce_dice` as the primary loss, keep provider-derived Line auxiliary target at `weighted_bce` weight 0.01, and increase provider-derived Centerline auxiliary target from weight 0.02 to weight 0.05. Keep `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, constant scheduler policy, disabled early stopping, and the active Harness-owned resource/prediction limits.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.05, AdamW, learning rate 0.0003, batch size 4, exploratory max epochs 12, and constant scheduler policy.
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
6. The Result is promising if it improves ABI-203/210/212 precision, connectivity, or positive-area discipline while remaining near their capped filtered-Dice/recall range, or if it exceeds ABI-201 capped filtered Dice with better recall and no major source-balance regression.

## Fallback/Next Decision

If ABI-213 fails validation or smoke, repair only candidate-local identifier or manifest issues while preserving the auxiliary-policy hypothesis. If it completes with lower aggregate/source Dice and no precision, connectivity, or predicted-positive-discipline gain, do not request late36 or whole-validation diagnostics for this exact weight. If it produces a strong final-epoch trajectory with finite non-collapsed predictions and a better line-discipline tradeoff than ABI-201/203, write a Research Note and consider a close-continuation late-improving budget request under the approved policy before any whole-validation or promotion claim.
