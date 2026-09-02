# ABI-105 full-spectral BTD frequency-gated line U-Net conservative-skip continuation

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but it remains recall-forward and has more negative-patch clutter than ABI-066. Multiple later output-side heads, suppressors, line-coherence gates, dual-stream decoders, and post-decoder refiners failed to improve ABI-068's precision/connectivity trade-off and often expanded positive area. A more useful in-contract test is to change an earlier decoder mechanism: keep ABI-068's backbone, trusted focal-Tversky loss, centerline auxiliary supervision, BTD front end, sampling, augmentation, and training policy, but make skip fusion conservative rather than amplifying.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. ABI-068's skip fusion multiplies high-resolution skip features by `0.5 + sigmoid(gate)`, allowing learned skip amplification up to 1.5x. ABI-105 changes this to `0.35 + 0.65 * sigmoid(gate)`, preserving a trainable skip path while preventing amplification. The hypothesis is that earlier non-amplifying skip fusion can reduce uncorroborated high-resolution clutter and improve precision or connectivity without the failure mode seen in additional late mask heads and consensus modules.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the strongest local capped and whole-validation-tested frequency-gated focal-Tversky reference.

Secondary local target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward reference. Recent negative controls for late gates/refiners include ABI-073, ABI-077, ABI-080, ABI-089, ABI-099, ABI-103, and ABI-104. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this proposed Run is capped family-development evidence, not a promotion claim.

## Expected Effect

The conservative skip change is expected to:

- reduce filtered predicted-positive fraction relative to ABI-068 without using candidate-owned thresholding or postprocessing;
- preserve ABI-068's source-balanced recall better than BCE-Dice/clDice or boundary-only sharpening variants;
- recover some precision and Contrail Connectivity Metric by preventing high-resolution decoder skips from amplifying local cloud-edge clutter;
- test whether the frequency-gated branch's false-positive burden is partly caused by skip amplification rather than focal-Tversky alone or late output-head design;
- keep resource use close to ABI-068 because the change alters only a scalar gate formula inside existing `UpFuseBlock`s.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The model architecture is copied from ABI-068: normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, high/low frequency split stem, multi-dilation coarse context, full-resolution frequency-pyramid fusion, and oriented line refinement. It emits primary `mask_logits` plus provider-derived `centerline_logits`.

The controlled architecture change is in `UpFuseBlock`: the skip gate range changes from `0.5 + sigmoid(gate)` to `0.35 + 0.65 * sigmoid(gate)`. No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, custom evaluation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered precision by at least 0.02 or reducing filtered predicted-positive fraction by at least 10%;
- capped best `val/filtered_dice` matching or exceeding ABI-068 with non-collapsed predictions on both Dataset Sources;
- improving filtered Contrail Connectivity over ABI-068 while keeping filtered recall at least 0.36 and both MIT/Google filtered Dice at least 0.36;
- clearly moving toward ABI-066's precision/connectivity profile while retaining materially higher recall than ABI-066;
- a finite, non-collapsed, late-improving trajectory that isolates skip amplification as a plausible operating-point lever.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 with no late improvement, either Dataset Source below 0.30 filtered Dice, or an ABI-077/099-like recall expansion with lower precision, connectivity, and higher predicted-positive fraction than ABI-068.

## Fallback/Next Decision

If ABI-105 preserves ABI-068-like Dice while improving precision/connectivity or lowering positive-area burden, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it loses recall and Dice without precision/connectivity gains, stop this conservative-skip branch and avoid further small gate-range tuning. If it fails contract validation or smoke testing, classify the failure and repair only if the original skip-fusion hypothesis and Comparison Target are preserved. If it is finite but non-improving, broaden to a materially different thin-line backbone or another provider-approved training/data-policy axis rather than moving provider-owned responsibilities into Candidate code.
