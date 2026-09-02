# ABI-134 Full-Spectral BTD+SZA Frequency-Gated Line U-Net BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-076 showed that adding provider-approved Solar Geometry Input (SZA) to the ABI-068 frequency-gated line U-Net raised recall but made the focal-Tversky branch too permissive, reducing precision, connectivity, Google Dice, and aggregate filtered Dice. ABI-078 showed that switching the same frequency-gated backbone from focal-Tversky to trusted BCE-Dice made the operating point cleaner, although it lost too much recall/connectivity without SZA. ABI-134 fills the in-contract factorial gap: keep the SZA-aware frequency-gated architecture from ABI-076 but change only the trusted primary loss from `focal_tversky` to `bce_dice`.

## Hypothesis

Trusted BCE-Dice may temper the SZA-induced recall/positive-area expansion observed in ABI-076 while preserving enough of SZA's calibration benefit to beat ABI-078 and approach ABI-068/ABI-130-level aggregate Dice. The useful signal would be a cleaner default-threshold operating point than ABI-076, with materially better precision/connectivity and lower predicted-positive fraction, without reverting all the way to ABI-078's lower-recall profile.

## Comparison Target

Primary controlled targets:

- ABI-076 `run_20260828_080008_ce4819`: same SZA-aware frequency-gated architecture with trusted focal-Tversky; capped filtered Dice 0.3790, precision 0.3463, recall 0.4184, connectivity 0.3013, predicted-positive fraction 0.00438.
- ABI-078 `run_20260828_094949_ad2af0`: same frequency-gated architecture and trusted BCE-Dice without SZA; capped filtered Dice 0.3816, precision 0.4072, recall 0.3590, connectivity 0.3061, predicted-positive fraction 0.00320.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the frequency-gated focal-Tversky aggregate/recall reference, ABI-066 `run_20260827_230540_bf4ce3` as the frequency-gated precision/connectivity reference, and ABI-130 `run_20260831_121006_7d24be` as the whole-validation-tested SZA-aware ASPP/detail calibration reference. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful ABI-134 result would improve over ABI-076 on filtered Dice, precision, connectivity, and predicted-positive discipline while retaining more recall than ABI-078. A stronger result would match or exceed ABI-078 aggregate Dice and approach ABI-068 or ABI-130 without severe MIT/Google imbalance. A negative result would indicate that the SZA plus BCE-Dice combination does not solve the frequency-gated line-family calibration trade-off under the current capped policy.

## Implementation Sketch

- Reuse ABI-076's torch-only frequency-gated line U-Net architecture: normalized ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` illumination features, learned 1x1 front-end mixer, high/low spatial-frequency stem, gated skip fusion, dilated bottleneck context, frequency-pyramid fusion, and oriented high-resolution line refiner.
- Preserve provider-approved `abi_16ch_plus_sza` input; the first 16 channels are GOES ABI channels 1-16 and the seventeenth channel is Solar Geometry Input.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` from the refined feature map.
- Change only the trusted primary loss from ABI-076's `focal_tversky` to `bce_dice`.
- Preserve Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the trusted representative cap.
- Request one sequential Run; do not request candidate-owned scheduling, resource placement, thresholding, postprocessing, Artifact Filters, or full-data claims.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, and constant learning-rate policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, Post-Run Evaluation, full-data evidence, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains within the profiled A100 resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-076 precision/connectivity and positive-area discipline while retaining recall above ABI-078, improves aggregate filtered Dice over either ABI-076 or ABI-078, or cleanly falsifies the SZA+BCE-Dice calibration combination.

## Continuation and hard stop

Continue this branch only if ABI-134 is finite, non-degenerate, source-informative, and improves a meaningful ABI-076/ABI-078-relative diagnostic: aggregate Dice, precision/recall balance, connectivity, predicted-positive fraction, source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result below both ABI-076 and ABI-078 on aggregate Dice while not improving precision/connectivity or recall trade-off would stop this exact combination, but would not eliminate SZA, BCE-Dice, or frequency-gated line architectures broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the factorial calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-076/ABI-078 trade-off, document the result and broaden toward a different architecture, calibration, preprocessing, loss/data-policy axis, or whole-validation diagnostic question rather than repeating simple SZA/loss combinations unchanged.
