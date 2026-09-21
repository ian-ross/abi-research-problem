# ABI-292 full-spectral BTD+SZA C4 soft-band recall calibrator U-Net

## Hypothesis

ABI-283 showed that cross-scale C4 consensus can recover a compact, high-precision, high-connectivity operating point, but it over-corrected toward underprediction: filtered recall fell to 0.3515 and aggregate/source Dice stayed below ABI-249 and ABI-202. The hypothesis for ABI-292 is that an architecture-internal soft-band recall calibrator can raise weak true-contrail logits at the fixed 0.5 threshold without returning to ABI-279/280-style broad clutter.

This is a **family-development continuation** in the C4/orientation-prior branch, not a promotion claim. It is mechanism-changing relative to ABI-283: instead of requiring all recall support to pass the cross-scale consensus gate, the head adds a separate bounded detail/line calibration path whose influence decays as the learned region logit becomes confident and is vetoed by learned cross-scale clutter disagreement.

## Comparison Target

Primary comparison targets are:

- ABI-283 (`run_20260913_063411_d8a862`), the immediate compact C4 cross-scale consensus parent.
- ABI-249 (`run_20260911_111909_dd7ef7`), the high-precision compact C4 comparator.
- ABI-202 (`run_20260904_043143_ee0005`), the aggregate capped filtered-Dice reference.

Secondary interpretation should track ABI-279 and ABI-280 because they characterize the earlier C4 recall-bridge failure modes: ABI-279 raised recall/connectivity but reduced precision and Google Dice; ABI-280 raised recall but weakened connectivity and compactness.

## Expected Effect

Expected metric movement versus ABI-283:

- Increase filtered recall by at least 0.02 without expanding the filtered predicted-positive fraction beyond the ABI-279/280 broad-footprint range.
- Preserve most of ABI-283's precision/connectivity advantage, targeting filtered precision at or above ABI-249's capped precision band and connectivity clearly above ABI-249.
- Improve aggregate filtered Dice and MIT filtered Dice over ABI-283; Google Dice should not regress materially below ABI-283.

A successful exploratory result does not need to beat ABI-202 immediately. It is useful if it demonstrates a cleaner recall/precision/connectivity trade-off than ABI-279/280/283 and a finite trajectory that could justify a later late-improving request.

## Implementation Sketch

Start from the resource-profiled ABI-283 full-spectral BTD+SZA C4 U-Net:

- Provider-approved `abi_16ch_plus_sza` input only; no longitude or latitude.
- Normalized ABI channels, ABI-channel-derived brightness-temperature-difference planes, Solar Geometry Input features, and a learned 1x1 mixer.
- Signed-detail/context stem, three-scale encoder/decoder, ASPP context, and C4 rotation-shared steerable line context.
- Trusted Line and Centerline auxiliary outputs.

Replace the ABI-283 mask head with `C4SoftBandRecallCalibratorHead`:

- Keep region, line, multiscale, detail, and clutter evidence branches.
- Keep cross-scale consensus support for compact line evidence.
- Add a differentiable soft evidence band `sigmoid(-0.70 * abs(region_logits))` that gives bounded support primarily where the learned region head is uncertain, with no hard threshold or postprocessing.
- Route the soft-band support through learned detail agreement and learned clutter-disagreement vetoes before adding it to `mask_logits`.
- Slightly strengthen the clutter veto relative to ABI-283 to discourage broad negative-patch expansion.

The Candidate returns only `mask_logits`, `line_logits`, and `centerline_logits` expected by the trusted Harness. It does not implement losses, metrics, thresholding, postprocessing, Artifact Filters, data loading, sampling, augmentation, target derivation, resource scheduling, downloads, or ledger writes.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza`.
- Output form: `mask_logits`.
- Dataset/frame policy: `all_target_frames`.
- Sampling policy: trusted `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Primary loss: trusted `bce_dice`.
- Optimizer/scheduler: trusted AdamW with `constant_lr` at learning rate `0.0003`.
- Batch size: 4, within the active ceiling.
- Auxiliary targets: trusted `line` -> `line_logits` with weight 0.01, and trusted `centerline` -> `centerline_logits` with weight 0.02.
- Candidate code defines architecture only and consumes only Harness-provided tensors.

## Budget Requested

Exploratory/default budget: 12 epochs, 3600-second default Candidate timeout if enforced by the Harness, no `budget_request.yaml`.

ABI-292 is a mechanism-changing continuation after an already characterized late36 ABI-283 result, so it should first establish finite resource behavior and trajectory under the default exploratory budget. A future late-improving request would require evidence such as a best checkpoint at or near epoch 12, finite non-collapsed source-informative predictions, and an improving or ambiguous late trajectory.

## Success Criteria

Consider ABI-292 worth further C4-family development if it satisfies most of the following under capped validation:

- Completed Run with finite training/validation metrics and no contract, smoke, shape, numerical, resource, or lifecycle failure.
- Best filtered Dice improves over ABI-283 or is within about 0.005 while improving recall by at least 0.02.
- Filtered precision remains competitive with ABI-249/283 rather than regressing toward ABI-279/280 broad-clutter behavior.
- Connectivity remains above ABI-249 and does not repeat ABI-280's connectivity collapse.
- MIT and Google filtered Dice remain source-informative, with no Dataset Source-specific collapse.
- Predicted-positive fraction remains compact relative to ABI-279/280 and raw-to-filtered differences do not suggest Artifact Filter dependence.

## Fallback/Next Decision

If ABI-292 is finite but only moves along the same precision/recall curve as ABI-279 through ABI-283, do not repeat it unchanged and do not request late36. Broaden away from C4 bridge heads toward a different architecture family or a better calibrated temporal evidence mechanism.

If ABI-292 is finite, source-balanced, and late-improving near epoch 12 with a materially better recall/precision/connectivity trade-off than ABI-283, consider a future late-improving budget request as a separate Autonomy Step.

If ABI-292 fails static validation, smoke, shape, or numerical checks due to candidate code, repair only the implementation bug while preserving this hypothesis and comparison target. If the contract blocks the mechanism itself, write a Capability Request rather than weakening the boundary.
