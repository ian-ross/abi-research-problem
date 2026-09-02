# ABI-135 Full-Spectral BTD+SZA ASPP/Detail Decoder Deterministic-Shuffle BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation / data-policy diagnostic.** ABI-130 established the strongest whole-validation-tested SZA-aware ASPP/detail branch: full-validation filtered Dice 0.3954, MIT/Google filtered Dice 0.3797/0.4256, precision 0.4436, recall 0.3566, and connectivity 0.3935. ABI-131, ABI-132, and ABI-133 showed that simple SZA-aware ASPP/detail continuity, agreement, and auxiliary-head additions reduced capped performance. ABI-135 therefore keeps ABI-130's architecture and loss fixed and changes only the trusted sampling traversal policy from `combined_source_balanced` to `deterministic_shuffle`.

## Hypothesis

ABI-130's capped and whole-validation evidence suggests a useful default-threshold calibration point, but its epoch trajectory was oscillatory and its remaining weakness is source/recall imbalance rather than lack of another decoder head. A provider-owned deterministic shuffle over the same trusted representative selected records may reduce ordering/cadence effects from strict source-balanced traversal and let the SZA-aware ASPP/detail BCE-Dice branch learn source-integrated calibration while preserving its Google/precision strengths. The hypothesis is not that candidate code should own sampling; it is that an already allowlisted Harness-owned traversal policy is a meaningful training-policy axis for this mature branch.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`, with capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic `eval_evalreq_abi130_wholeval_failure_buckets_v1` confirmed filtered Dice 0.3954 and a real but costly SZA-driven recall gain relative to ABI-126.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice/source-balance reference, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail precision/connectivity reference, and ABI-134 `run_20260831_153303_7701f1` as the SZA-aware frequency-gated BCE-Dice data point. Canonical MCAST 2.1 remains promotion context; this candidate requests capped family-development evidence only.

## Expected Effect

A useful result would keep ABI-130's aggregate filtered Dice within a small margin while improving one of its unresolved diagnostics: MIT filtered Dice/recall, precision/connectivity retention, or epoch stability. Deterministic shuffle could also reveal that ABI-130's strength depends on strict source-balanced traversal, in which case a lower score but finite source-informative result is still useful training-policy evidence. A negative result would show degraded source balance, positive-area discipline, or connectivity without a compensating MIT-recall gain.

## Implementation Sketch

- Reuse ABI-130's torch-only compact full-spectral BTD+SZA ASPP/detail encoder-decoder unchanged: normalized ABI channels 1-16, deterministic thermal BTD planes from provider-approved ABI channels, normalized Solar Geometry Input and `cos(SZA)` features, learned 1x1 spectral/SZA projection, high-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, line-aware refinement, primary mask head, and Centerline Target auxiliary head.
- Preserve `input_mode: abi_16ch_plus_sza`, trusted `bce_dice` primary loss, provider-derived `centerline_logits` auxiliary output supervised by trusted `weighted_bce` at weight 0.02, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Change only `data.sampling_policy` from `combined_source_balanced` to provider-owned `deterministic_shuffle`. Candidate code does not implement shuffling, sampling, class/source weighting, or data access.
- Request one sequential Run only; no Experiment Batch, Post-Run Evaluation, GPU selection, or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, and hidden geolocation priors are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `deterministic_shuffle`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, deterministic-shuffle implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes within the trusted resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it matches ABI-130 within about 0.01 filtered Dice while improving MIT recall/Dice, precision/connectivity, positive-area discipline, or training trajectory stability; or if it cleanly shows that deterministic shuffle harms this branch, thereby narrowing the training-policy frontier.

## Fallback/Next Decision

If ABI-135 fails because of a narrow candidate implementation defect while the data-policy hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-130 across aggregate Dice, source balance, precision/connectivity, and trajectory stability, stop this exact deterministic-shuffle ASPP/detail branch and retain `combined_source_balanced` as the stronger traversal for ABI-130. If it unexpectedly improves the ABI-130/ABI-068 reference band, request separately authorized whole-validation diagnostics before making any promotion or full-data claim. If all simple ASPP/detail data-policy continuations underperform, broaden to a distinct architecture, preprocessing, calibration, or loss frontier rather than stacking more SZA-aware head tweaks.
