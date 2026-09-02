# ABI-076 Proposal: full-spectral BTD+SZA frequency-gated line U-Net

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice: `run_20260828_010836_4ccc77` achieved whole-validation filtered Dice 0.3951 while preserving non-collapsed MIT and Google behavior. Its weakness is the recall-forward operating shift: relative to ABI-066 it increases true positives but gives back precision, Contrail Connectivity, and negative-patch clutter control.

ABI-076 is a **family-development continuation** of the ABI-068 frequency-gated line U-Net branch. The hypothesis is that adding the provider-approved Solar Geometry Input (`abi_16ch_plus_sza`) can help the same spectral/BTD line backbone condition reflective and thermal evidence on illumination geometry, improving source/threshold stability or false-positive control without moving data loading, sampling, losses, metrics, thresholding, Artifact Filters, or postprocessing into Candidate code.

Recent ABI-074/075 Laplacian-pyramid evidence also argues against continuing with heavier bandpass backbones immediately: ABI-074 exceeded the 25M-parameter smoke ceiling and ABI-075 passed smoke but exhausted the wall-clock budget while showing only mediocre partial validation metrics. ABI-076 therefore broadens along an in-contract input-policy axis while returning to the known resource-safe ABI-068 backbone.

## Comparison Target

Primary comparison target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested frequency-gated focal-Tversky reference and the architecture source for ABI-076.

Secondary comparison target: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the local precision/connectivity-forward reference. ABI-073 (`run_20260828_055812_4ba74e`) is a negative auxiliary-head comparison, and ABI-074/075 are recent resource/bandpass cautionary context. Canonical MCAST 2.1 remains promotion context; this capped Run is not a promotion claim.

## Expected Effect

Adding Solar Geometry Input is expected to:

- preserve ABI-068's aggregate Dice and source-balanced recall while giving the model an explicit illumination cue for reflective-channel reliability;
- reduce some ABI-068 negative-patch clutter or recover precision/connectivity by distinguishing sun-angle-conditioned cloud/surface textures from true thin-line contrails;
- improve Google/MIT transfer stability if part of the source difference is illumination distribution rather than morphology alone;
- keep resource use close to ABI-068 because the only architectural change is adding two low-cost SZA-derived feature planes and including SZA in the learned 1x1 mixer.

A neutral or negative result is still informative: it would indicate that the allowed Solar Geometry Input does not improve the current frequency-gated focal-Tversky operating point under the representative capped policy.

## Implementation Sketch

Start from ABI-068's `model.py`. Switch `input_mode` to `abi_16ch_plus_sza` and require `[17, 256, 256]` input. The front end splits the first 16 provider-approved ABI channels from the seventeenth Solar Geometry Input plane. It normalizes ABI channels with the same dataset-profile summary constants, derives the same thermal BTD planes only from ABI channels 1-16, clamps SZA to a physical 0-180 degree range, appends a centered SZA plane and a cosine-of-SZA plane, and feeds normalized ABI plus centered SZA into the learned 1x1 mixer.

The high/low spatial-frequency split stem, low-frequency-gated skip fusion, dilated bottleneck context, full-resolution frequency-pyramid fusion, oriented high-frequency line refiner, primary `mask_logits` head, and provider-declared `centerline_logits` auxiliary head remain unchanged from ABI-068. No candidate-owned data loading, split logic, sampling, augmentation transform, target derivation, loss, metric, thresholding, Artifact Filter, postprocessing, filesystem access, network access, runtime weight download, pretrained weight, or training loop is introduced.

## Contract Features Used

- `research_problem`: `goes_abi_contrail_segmentation`
- `input_mode`: provider-approved `abi_16ch_plus_sza`; no longitude or latitude inputs
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

One sequential representative capped Run under the active Workspace Configuration: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` prediction artifacts, the configured 25M-parameter smoke ceiling, A100 GPU policy, and the configured 3,600-second Docker training timeout. No Experiment Batch, extra concurrency, GPU selection, data-policy change, full-data promotion evaluation, or candidate-owned resource workaround is requested.

## Success Criteria

Treat ABI-076 as capped family-development evidence, not full-data promotion evidence. Useful success signals include:

- static validation, smoke testing, and finite training completion under the trusted resource limits;
- no persistent all-negative or all-positive prediction collapse;
- aggregate best-validation `val/filtered_dice` matching or exceeding ABI-068, or staying within roughly 0.01 while improving at least one of filtered precision, filtered Contrail Connectivity, filtered predicted-positive fraction, or MIT/Google source balance;
- filtered recall remaining near ABI-068's recall-forward operating point rather than reverting fully to a conservative low-recall profile;
- a late-improving trajectory that suggests the SZA input is useful even if the capped final score is noisy.

Hard stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, resource failure, prediction collapse, aggregate filtered Dice below about 0.34 without late improvement, or a clear ABI-072-like clutter profile with worse precision/connectivity and no source-balance gain.

## Fallback/Next Decision

If ABI-076 improves or credibly ties ABI-068 while recovering precision/connectivity or reducing clutter, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If ABI-076 is finite but neutral, retain ABI-068 as the local aggregate-Dice reference and avoid further simple SZA-only repeats. If it fails for resource or contract reasons, classify the failure and either repair only if the original input-policy hypothesis is preserved or broaden to a different in-contract architecture/training-policy axis. If it is scientifically poor, stop this exact SZA continuation but do not treat the broader campaign or frequency-gated family as exhausted.
