# ABI-075 Repair Proposal: compact full-spectral BTD Laplacian-pyramid U-Net

## Hypothesis

ABI-074 failed before training because its Laplacian-pyramid U-Net exceeded the active 25,000,000-parameter smoke ceiling (`27,653,274` parameters reported for `run_20260828_065112_f43340`). ABI-075 is a **family scout repair** that preserves the original bandpass-feature hypothesis while reducing only the architecture width so the branch can receive bounded evidence under the trusted resource contract.

The scientific hypothesis is unchanged: repeatedly exposing narrow, middle, and broad Laplacian-style bandpass feature bands inside the backbone may preserve ABI-068's source-balanced focal-Tversky recall while recovering some ABI-066-style precision/connectivity through architecture-side multi-scale feature separation rather than candidate-owned postprocessing, thresholding, Artifact Filters, or additional output-head stacking.

## Comparison Target

Primary local comparison target remains ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested Candidate by aggregate filtered Dice and the focal-Tversky recall-forward reference. The immediate repair target is ABI-074's smoke failure (`run_20260828_065112_f43340`): ABI-075 should pass the same contract and parameter ceiling while preserving the Laplacian-pyramid mechanism.

Secondary operating-profile context remains ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward reference, plus recent negative branch evidence from ABI-071, ABI-072, and ABI-073 showing that soft gates, dense ridge context, and boundary-auxiliary stacking did not improve ABI-068. Canonical MCAST 2.1 remains the broader promotion context; this capped repair scout is not a promotion claim.

## Expected Effect

The compact repair should test whether explicit multi-scale bandpass feature fusion is a viable broadening direction once brought under the resource ceiling. Expected useful signals include:

- finite smoke/training/validation under the configured parameter and wall-clock limits;
- non-collapsed source-balanced behavior on both MIT and Google Dataset Sources;
- filtered Dice near the focal-Tversky line-family references while improving at least one of filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction;
- less broad-clutter behavior than ABI-072 because Laplacian bands separate local ridge-like detail from smoother cloud context at each scale instead of densely inserting oriented context everywhere.

Because the only implementation change from ABI-074 is capacity reduction (`base = 40` to `base = 32`), a lower score than ABI-068 would still be interpretable as compact Laplacian-pyramid evidence rather than a changed data, loss, sampling, or evaluation policy.

## Implementation Sketch

Use provider-approved `abi_16ch` inputs only. The front end normalizes ABI channels 1-16, appends explicit thermal BTD planes derived only from those ABI channels, and appends a learned 1x1 channel mixture. The backbone remains a GroupNorm/GELU U-Net with `LaplacianBandBlock` modules that compute smoothed feature maps at multiple kernel sizes and derive narrow, middle, and broad bandpass features (`x - smooth5`, `smooth5 - smooth13`, and `smooth13 - smooth31`). The blocks learn a soft per-pixel mixture across raw and bandpass branches and project the mixture back into the residual feature stream.

The repair reduces base width from 40 to 32 while retaining the stem, encoder, bottleneck, decoder, full-resolution pyramid-fusion block, primary `mask_logits` head, and provider-declared `centerline_logits` auxiliary head. No boundary head, confidence suppressor head, candidate-owned thresholding, postprocessing, Artifact Filter, target derivation, data loading, sampling, augmentation, metrics, training loop, data-root access, network access, runtime weight download, or pretrained weights are introduced.

## Contract Features Used

- `research_problem`: `goes_abi_contrail_segmentation`
- `input_mode`: provider-approved `abi_16ch`; no longitude or latitude inputs
- `output_form`: primary `mask_logits` with shape `[1, 256, 256]`
- `auxiliary_targets`: provider-derived `centerline` target emitted as `centerline_logits`, trusted `weighted_bce`, weight `0.02`
- `training.loss`: trusted `focal_tversky`
- `training.optimizer`: `adamw`
- `training.learning_rate`: `0.0003`
- `training.batch_size`: `4`
- `training.max_epochs`: `12`
- `training.scheduler.policy`: trusted `constant_lr`
- `data.sampling_policy`: provider/Harness-owned `combined_source_balanced`
- `data.frame_selection_policy`: provider/Harness-owned `all_target_frames`
- `data.augmentation_policy`: provider/Harness-owned `random_mirroring`

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` prediction artifacts, the configured 25M-parameter smoke ceiling, A100 GPU policy, and the configured 3,600-second Docker training timeout. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Treat this as capped repair-scout evidence, not full-data promotion evidence. ABI-075 is successful enough for continued bounded development if it:

- passes static validation and smoke testing, demonstrating that the compact repair fixes ABI-074's parameter-budget failure;
- completes finite training/validation without contract, resource, or non-finite failure;
- avoids persistent all-negative or all-positive prediction collapse;
- reaches aggregate best-validation `val/filtered_dice` within roughly 0.03 of ABI-068 while improving at least one of filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction; or
- shows a clearly improving late trajectory with a diagnostically different precision/recall/clutter profile even if it does not immediately beat ABI-068.

A stronger success signal would be capped filtered Dice matching or exceeding ABI-068 while moving precision/connectivity or negative-patch-clutter proxies back toward ABI-066.

Hard stop evidence for this exact compact branch would be another contract/smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 without late improvement, a high-clutter low-connectivity profile like ABI-072, or materially worse source balance with no compensating precision/connectivity evidence.

## Fallback/Next Decision

If ABI-075 still fails validation or smoke, stop this exact Laplacian-pyramid implementation and broaden to a different in-contract architecture or trusted-policy axis rather than increasing Candidate-owned resource use. If it completes but collapses or diverges, mark this exact branch as stopped. If it is finite but mixed, compare source-stratified precision/recall/connectivity and decide whether one bounded Laplacian-pyramid family-development follow-up is justified. If it clearly improves the ABI-068 trade-off, request whole-validation failure-bucket diagnostics before any promotion interpretation.
