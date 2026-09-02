# ABI-090 full-spectral BTD dual-decoder region/line U-Net scout

## Hypothesis

Recent ABI-068 descendants that changed post-decoder gates, agreement modules, auxiliary heads, learning rate, augmentation, or input mode did not surpass ABI-068's capped filtered-Dice reference. ABI-089 in particular suggests that a single late context/detail agreement block can increase positive-area burden without preserving precision or connectivity. A better in-contract next step is to separate smooth region context and high-frequency line detail throughout the decoder rather than only after a shared decoder has already fused them.

This is a **family scout** for a full-spectral BTD dual-decoder region/line U-Net branch. It is not a full-data promotion claim. The expected value is to test whether a two-stream decoder can keep broad cloud-context false-positive control and thin-line continuity evidence disentangled enough to improve the precision/recall/connectivity trade-off under the existing trusted focal-Tversky and centerline-auxiliary policy.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it remains the strongest capped frequency-gated reference by primary filtered Dice.

Secondary targets: ABI-066, Run `run_20260827_230540_bf4ce3`, for its precision/connectivity-forward operating point; ABI-085, Run `run_20260829_181201_01c5e7`, for the nearby low-learning-rate focal-Tversky variant; and ABI-089, Run `run_20260829_212901_6bbc6f`, as negative evidence for single-stage post-decoder context/detail agreement. Canonical MCAST 2.1 remains the promotion context, but this capped Run is feasibility and family-scout evidence only.

## Expected Effect

The dual-decoder architecture is expected to:

- preserve ABI-068's full-spectral BTD and focal-Tversky recall advantages while reducing diffuse false positives through a smooth region-context decoder;
- recover part of ABI-066's precision and Contrail Connectivity by keeping a separate high-frequency line-detail decoder with centerline auxiliary supervision;
- avoid ABI-089's single late agreement bottleneck by allowing context and detail features to exchange information at decoder scales before final fusion;
- keep MIT and Google filtered Dice source-balanced because both streams use only provider-approved ABI-channel evidence and provider-owned source-balanced sampling;
- provide a materially different architecture signal if it is finite and non-collapsed, even if it does not immediately beat the mature ABI-068 reference.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. `model.py` builds normalized full-spectral channels, fixed thermal BTD planes derived only from ABI channels 1-16, and a learned 1x1 spectral projection. A shared residual encoder extracts multi-scale features. The decoder then splits into two paths: a region path that emphasizes smoothed skip context and a line path that emphasizes high-frequency residual skip detail. A lightweight cross-path fusion module combines the final region and line features before the primary mask head. The centerline auxiliary output is emitted from the line/detail representation as provider-derived `centerline_logits`.

The manifest selects trusted `focal_tversky` as primary loss and the provider-derived `centerline` auxiliary target with trusted `weighted_bce` at weight 0.02. No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Strong family-scout evidence would be any of:

- capped best `val/filtered_dice` within 0.015 of ABI-068 while improving filtered precision or filtered Contrail Connectivity;
- capped best `val/filtered_dice` matching or exceeding ABI-066 with filtered recall at least 0.38;
- both MIT and Google filtered Dice above 0.35 with finite, non-collapsed predictions and a late-improving trajectory;
- a clearer precision/recall balance than ABI-089, especially lower filtered predicted-positive fraction without all-negative collapse.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, persistent prediction collapse, aggregate filtered Dice below 0.30 with no late improvement, or an ABI-089-like increase in positive-area burden with simultaneous losses in Dice, precision, and connectivity. Because this is a family scout, low score alone should not eliminate all two-stream decoder variants if the Run is finite, improving, and source-balanced.

## Fallback/Next Decision

If ABI-090 improves precision or connectivity while staying near ABI-068/066 aggregate Dice, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but weaker, use the trajectory and source-stratified metrics to decide whether to develop the dual-decoder family or broaden to another in-contract architecture family. If it fails validation or smoke testing, classify the failure and repair only if the repair preserves the two-stream decoder hypothesis without moving provider-owned responsibilities into Candidate code.
