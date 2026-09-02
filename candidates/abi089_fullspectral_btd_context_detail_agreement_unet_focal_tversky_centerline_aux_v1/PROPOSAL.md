# ABI-089 full-spectral BTD context-detail agreement U-Net

## Hypothesis

ABI-068 remains the strongest local whole-validation-tested Candidate by primary filtered Dice, but its improvement over ABI-066 came from a recall-forward operating-point shift with more negative-patch clutter and lower precision/connectivity. Several post-decoder heads, generic gates, SZA expansion, lower learning rate, and internal recalibration did not improve that trade-off. A more targeted architecture continuation is to keep ABI-068's approved full-spectral BTD input front end, source-balanced sampling, focal-Tversky loss, and centerline auxiliary supervision, but replace the single final frequency-pyramid fusion block with a parallel context/detail agreement fusion module.

This is a **family-development continuation** within the full-spectral BTD line U-Net family, not a full-data promotion claim. The expected value is to test whether full-resolution line detail and smoothed multi-scale context should be modeled as separate streams before final oriented refinement, rather than concatenated once and refined immediately.

## Comparison Target

Primary target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested Candidate by filtered Dice and the direct architecture parent.

Secondary target: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward frequency-gated reference. ABI-085 and ABI-088 are context for recent non-improving learning-rate and recalibration continuations. Canonical MCAST 2.1 remains the promotion context; this capped representative Run is family-development evidence only unless later whole-validation diagnostics are requested.

## Expected Effect

The context/detail agreement fusion is expected to:

- preserve ABI-068-like filtered recall by keeping focal-Tversky loss and centerline auxiliary supervision unchanged;
- improve filtered precision or lower filtered predicted-positive fraction by requiring high-frequency detail to interact with smoothed context before the final line refiner;
- recover some of ABI-066's filtered Contrail Connectivity by keeping a dedicated detail stream at full resolution;
- avoid the broad connectivity regression seen in ABI-088 by localizing the new mechanism to the final fusion stage rather than recalibrating every residual block;
- keep Dataset Source behavior non-catastrophic, with MIT and Google filtered Dice remaining near the ABI-068/085 band.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The front end normalizes GOES ABI channels 1-16, derives fixed thermal BTD planes only from approved ABI channels, and learns a 1x1 spectral mixture. The encoder, low-frequency-gated skip fusion, dilated bottleneck context, and oriented line refiner are inherited from ABI-068.

The controlled architecture change is the final fusion module. Instead of concatenating decoder features, high-frequency detail, local smooth context, broad smooth context, and upsampled low-resolution decoder features in a single block, ABI-089 builds a full-resolution detail path from `dec0`, high-frequency residual detail, and the stem; builds a context path from local/broad smoothed `dec0` plus upsampled `dec1` and `dec2`; exchanges learned residual corrections between the paths; and fuses the enhanced streams before the final oriented line refiner. The model emits primary `mask_logits` and trusted provider-derived `centerline_logits`.

No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

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

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` matching or exceeding ABI-068;
- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction relative to ABI-068;
- improving ABI-066's recall while preserving a precision/connectivity profile closer to ABI-066 than the recent ABI-087/088 branches;
- both MIT and Google filtered Dice above 0.36 with a finite, non-collapsed, late-improving trajectory.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 without late improvement, either Dataset Source below 0.32 filtered Dice, or an ABI-088-like connectivity collapse without any primary-metric or precision gain.

## Fallback/Next Decision

If ABI-089 preserves ABI-068's aggregate filtered Dice while improving precision/connectivity or lowering negative-patch clutter, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but non-improving, retain ABI-068 as the aggregate-Dice reference and ABI-066 as the precision/connectivity reference, and broaden to a materially different architecture family rather than adding more gates or auxiliary-head stacks. If it fails contract validation or smoke testing, classify the failure and repair only if the original context/detail agreement hypothesis is preserved.
