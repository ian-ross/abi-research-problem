# ABI-072 full-spectral BTD steerable ridge U-Net focal-Tversky centerline-aux scout

## Hypothesis

ABI-072 is a **family scout** for a non-suppressive steerable-ridge U-Net backbone. Recent ABI-069/070/071 post-decoder suppressor or gate variants failed to improve ABI-068's recall-forward frequency-gated operating point without losing precision, Dice, or connectivity. A backbone that explicitly models horizontal, vertical, and diagonal thin-line context throughout the encoder, decoder, bottleneck, and multi-scale head may preserve focal-Tversky recall while recovering some ABI-066-style precision/connectivity without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, sampling, losses, metrics, or target derivation.

## Comparison Target

Primary local comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested frequency-gated candidate by aggregate filtered Dice and recall-forward source-balanced behavior.

Secondary operating-profile target: ABI-066 (`run_20260827_230540_bf4ce3`), retained as the precision/connectivity-forward reference within the full-spectral BTD line-model family.

Canonical MCAST 2.1 remains the broader promotion context, but this capped scout is not a promotion claim.

## Expected Effect

The candidate should test whether oriented ridge-context features are a better next broadening direction than post-head suppression. Expected useful signals include:

- filtered Dice near ABI-068 while improving filtered precision, filtered Contrail Connectivity, or filtered predicted-positive burden;
- better line-continuity behavior than ABI-071's soft evidence gate because diagonal line context is integrated before the output heads rather than applied as a late feature modulation;
- non-collapsed behavior on both MIT and Google Dataset Sources under the representative cap;
- stable late-epoch learning that would justify a bounded follow-up if the exact scout does not immediately beat ABI-068.

## Implementation Sketch

Use provider-approved `abi_16ch` inputs only. The front end normalizes ABI channels 1-16, appends explicit ABI-channel-derived thermal BTD planes, and appends a learned 1x1 channel mixture. The model is a compact U-Net with GroupNorm/GELU residual blocks. Its new `SteerableRidgeBlock` computes local detail (`features - avg_pool(features)`) and softly mixes five feature branches: local residual, horizontal depthwise line context, vertical depthwise line context, and two masked diagonal depthwise line-context branches. These blocks appear in the stem, downsampling path, bottleneck, upsampling path, and multi-scale head. The output heads are direct `mask_logits` and provider-declared `centerline_logits`.

No candidate code uses longitude, latitude, data roots, dataset metadata, custom labels, custom losses, custom augmentation, metrics, postprocessing, Artifact Filters, threshold sweeps, pretrained weights, network access, or training loops.

## Contract Features Used

- `research_problem`: `goes_abi_contrail_segmentation`
- `input_mode`: `abi_16ch`
- `output_form`: `mask_logits`
- `training.loss`: trusted `focal_tversky`
- `training.optimizer`: `adamw`
- `training.learning_rate`: `0.0003`
- `training.batch_size`: `4`
- `training.max_epochs`: `12`
- `training.scheduler.policy`: trusted `constant_lr`
- `data.sampling_policy`: provider/Harness-owned `combined_source_balanced`
- `data.frame_selection_policy`: provider/Harness-owned `all_target_frames`
- `data.augmentation_policy`: provider/Harness-owned `random_mirroring`
- `auxiliary_targets`: provider-derived `centerline` target emitted as `centerline_logits`, loss `weighted_bce`, weight `0.02`

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` prediction artifacts, the configured 25M-parameter smoke ceiling, A100 GPU policy, and the configured 3,600-second Docker training timeout.

## Success Criteria

Treat this as capped family-scout evidence, not full-data promotion evidence. The scout is successful enough for continued bounded development if it:

- completes finite smoke/training/validation without contract, resource, or non-finite failure;
- avoids persistent all-negative or all-positive prediction collapse;
- reports aggregate best-validation `val/filtered_dice` at least roughly competitive with ABI-066/ABI-068 local references, or else shows a clearly useful precision/connectivity/clutter tradeoff not captured by aggregate Dice alone;
- keeps both MIT and Google filtered Dice non-catastrophic (target floor about 0.25 for this scout, with source trend considered);
- improves at least one of filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction relative to ABI-068 without a severe recall collapse below about 0.34.

A stronger success signal would be aggregate capped filtered Dice within about 0.01 of ABI-068 while improving ABI-068's precision/connectivity or negative-patch-clutter proxy.

## Fallback/Next Decision

If ABI-072 is non-finite, rejected, smoke-failed, or persistently collapsed, classify the failure before proposing repair or abandonment. If it is finite but clearly below the local family references with no source-balanced precision/connectivity benefit, do not repeat this exact steerable-ridge configuration unchanged. If it is finite with useful line-continuity or clutter-control evidence but weak recall, consider a bounded continuation that reduces ridge-context strength or changes only trusted primary loss/auxiliary weight within the allowlist. If it meaningfully improves the ABI-068 tradeoff, request a whole-validation failure-bucket evaluation before making any promotion interpretation.
