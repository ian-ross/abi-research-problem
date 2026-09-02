# ABI-112 full-spectral BTD line-propagation U-Net focal-Tversky continuation

## Hypothesis

Recent ABI-109, ABI-110, and ABI-111 evidence suggests that local front-end, output-head, and soft thermal-support changes are not recovering the ABI-068 operating point. ABI-068 remains the capped aggregate-Dice reference, while ABI-066 remains the precision/connectivity reference. A more targeted in-contract continuation is to keep ABI-068's successful full-spectral BTD frequency-gated encoder/decoder, focal-Tversky loss, and Centerline Target auxiliary supervision, but replace the final high-resolution line refiner with explicit non-wrapping directional feature propagation.

This is a **family-development continuation** within the full-spectral BTD thin-line U-Net family. It is not a full-data promotion claim. The hypothesis is that propagating feature evidence along horizontal, vertical, and diagonal straight-line directions at the final high-resolution stage can improve Contrail Mask continuity and precision/recall balance without moving thresholding, Artifact Filters, losses, metrics, data loading, or sampling into Candidate code.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current capped aggregate-Dice reference for this family.

Secondary target: ABI-066, Run `run_20260827_230540_bf4ce3`, because it is the precision/connectivity reference. ABI-111, Run `run_20260830_201502_afa0c8`, is recent negative evidence for a softer thermal-support branch and motivates a different line-continuity mechanism. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this Run is capped representative feasibility evidence only.

## Expected Effect

The directional propagation refiner is expected to:

- increase or retain filtered Contrail Connectivity relative to ABI-068 by aggregating same-line feature support over non-wrapping radii 1, 2, 4, and 8 pixels;
- reduce isolated blob-like clutter by requiring gated directional agreement before final mask logits;
- avoid ABI-111's recall suppression by applying the mechanism only at high-resolution decoder features rather than adding a separate soft thermal support stream;
- preserve source balance by leaving provider-owned combined source-balanced traversal and trusted random mirroring unchanged;
- stay resource-compatible with prior 12M-parameter frequency-gated variants, adding only lightweight 1x1 gates and residual propagation blocks.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. It retains normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels, and learned 1x1 channel mixing. The encoder, frequency-split stem, low-frequency-gated skip fusion, multi-dilation bottleneck, and full-resolution pyramid fusion remain ABI-068-like.

The controlled architecture change is a `DirectionalLinePropagationRefiner`: high-frequency detail features are propagated along horizontal, vertical, down-diagonal, and up-diagonal directions using non-wrapping replicated-edge shifts. Learned 1x1 gates control how much same-line context updates each branch, branch logits choose a per-pixel orientation mixture, and a bounded context gate fuses propagated line context with the original high-resolution features. The model emits primary `mask_logits` and trusted provider-derived `centerline_logits`.

No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered connectivity or precision;
- capped best `val/filtered_dice` exceeding ABI-066 while retaining filtered connectivity above 0.39;
- both MIT and Google filtered Dice above 0.36 with no prediction collapse and filtered predicted-positive fraction between ABI-066's conservative profile and ABI-105's recall-forward profile;
- a finite, late-improving trajectory that identifies a better precision/connectivity versus recall tradeoff than ABI-109 through ABI-111.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, persistent all-negative or all-positive collapse, aggregate filtered Dice below 0.34 with no late improvement, or a clear ABI-110-like low-precision/high-positive-area shift without a connectivity gain.

## Fallback/Next Decision

If ABI-112 improves connectivity or precision while retaining ABI-068-like aggregate/source behavior, consider a bounded whole-validation failure-bucket Evaluation Request before any promotion interpretation. If it is finite but misses all useful-continuation criteria, stop this exact line-propagation refiner and broaden to another materially different calibration, data-policy, or architecture mechanism. If it fails contract validation or smoke testing, classify and repair only if the original non-wrapping directional-propagation hypothesis is preserved.
