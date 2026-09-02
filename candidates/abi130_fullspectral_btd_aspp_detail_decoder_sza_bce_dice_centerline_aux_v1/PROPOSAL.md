# ABI-130 Full-Spectral BTD+SZA ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-126 established a finite ASPP/detail BCE-Dice branch with strong precision, connectivity, and Google filtered Dice, but whole-validation diagnostics showed conservative fixed-threshold behavior and a MIT under-recall weakness. ABI-130 keeps the ABI-126 architecture, trusted loss, auxiliary target, and training/data policy fixed while changing the provider-approved input mode from `abi_16ch` to `abi_16ch_plus_sza`.

## Hypothesis

Adding Solar Geometry Input as a normalized, non-coordinate illumination feature will help the ASPP/detail BCE-Dice branch calibrate thin-contrail evidence across source/illumination regimes. Because ABI-126's diagnostic threshold sweep showed recoverable recall and its failure buckets localized much of the weakness to MIT positive-patch under-segmentation, a small SZA-aware spectral front end may raise MIT recall at the fixed Harness threshold while preserving ABI-126-like positive-area discipline, Google performance, and connectivity.

## Comparison Target

The primary comparison target is ABI-126 `abi126_fullspectral_btd_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260831_085615_d05ab3`: capped filtered Dice 0.3859, MIT/Google filtered Dice 0.3635/0.4415, filtered precision 0.4746, filtered recall 0.3251, filtered connectivity 0.4517, and filtered predicted-positive fraction 0.00248. Its whole-validation review reported filtered Dice 0.3892, precision 0.4770, recall 0.3288, connectivity 0.4563, strong Google Dice, and lower MIT recall.

Secondary references are ABI-121 `run_20260831_041559_43da35` as the ASPP/detail focal-Tversky recall/source-balance comparator, ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice reference, and ABI-066 `run_20260827_230540_bf4ce3` as the precision/connectivity reference. ABI-076 tested SZA in the frequency-gated branch and became recall-heavier; ABI-130 tests whether the cleaner BCE-Dice ASPP/detail branch can use the same approved input more constructively. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful result would improve ABI-126 MIT filtered Dice or MIT recall without losing its defining precision/connectivity profile. The expected trade-off is a modest increase in filtered predicted-positive fraction and recall; it is useful only if the increase is targeted enough to keep aggregate filtered Dice near or above ABI-126 and retain Google filtered Dice above the local family baseline. A negative result would show that SZA primarily shifts the ASPP/detail BCE-Dice branch toward generic recall or instability rather than source-aware calibration.

## Implementation Sketch

- Reuse ABI-126's compact torch-only ASPP/detail encoder-decoder: normalized ABI spectral features, deterministic thermal BTD planes from approved ABI channels, learned 1x1 spectral projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Change the front end to accept provider-approved `abi_16ch_plus_sza` input. The first 16 channels are treated as GOES ABI channels 1-16; the seventeenth channel is Solar Geometry Input.
- Normalize SZA into `(SZA - 90) / 90`, add `cos(SZA)` as an illumination plane, and include normalized SZA in the learned 1x1 channel mixer. SZA is not longitude, latitude, source identity, thresholding, or postprocessing.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-126 MIT filtered Dice or recall while keeping filtered precision/connectivity close to ABI-126, improves aggregate filtered Dice, or exposes a clear SZA-specific calibration limit for the ASPP/detail BCE-Dice branch.

## Continuation and hard stop

Continue only if ABI-130 is finite, non-degenerate, source-informative, and improves a meaningful ABI-126-relative diagnostic: MIT recall/Dice, aggregate Dice, precision/recall balance, connectivity retention, positive-area stability, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result below ABI-126 on aggregate Dice, MIT recall, and precision/connectivity would be enough to stop this exact SZA ASPP/detail continuation, but would not eliminate Solar Geometry Input or ASPP/detail architectures broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the SZA-calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but SZA trades away ABI-126 precision/connectivity without solving MIT under-recall, document that input-policy result and broaden to a different contract-compliant calibration or line-continuity frontier rather than repeating simple ASPP/detail input/head tweaks. If it unexpectedly challenges ABI-068 or MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
