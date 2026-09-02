# ABI-066 full-spectral BTD frequency-gated line U-Net scout

## Hypothesis

A full-spectral BTD U-Net that explicitly separates high-spatial-frequency line contrast from low-spatial-frequency cloud/background context can reduce the broad small false-positive burden observed in ABI-058/ABI-064 while preserving thin contrail continuity. The frequency split is internal differentiable model structure, not data preprocessing, thresholding, postprocessing, a metric, or an Artifact Filter.

This is a **family scout** for frequency-gated thin-line segmentation. It is not expected to beat the mature canonical MCAST 2.1 baseline immediately. Continuation should depend on finite training, non-degenerate predictions, source behavior, false-positive burden, connectivity, and whether it offers a diagnostically different trade-off from the high-resolution line U-Net and coarse-to-fine branches.

## Comparison Target

Primary local target: ABI-058, `abi058_fullspectral_btd_hrline_unet_oriented_context_cldice_centerline_aux_v1`, Run `run_20260827_171331_c1769a`, because its whole-validation review remains the strongest local full-validation reference by aggregate filtered Dice while still showing broad low-level false positives.

Secondary context: ABI-061 (`run_20260827_194725_c1d6c6`) for the best capped validation score and stronger precision/connectivity signal; ABI-064 (`run_20260827_212811_0e34e2`) for the coarse-to-fine recall/MIT-balance branch whose whole-validation diagnostic did not reduce false positives; canonical MCAST 2.1 as the promotion context at full Working Validation filtered Dice 0.3873.

## Expected Effect

The frequency-gated architecture is expected to:

- improve filtered precision or reduce filtered predicted-positive fraction relative to ABI-058/ABI-064 without all-negative collapse;
- preserve useful filtered recall by keeping a full-resolution decoder and centerline-supervised output;
- improve or at least maintain filtered Contrail Connectivity relative to the coarse-to-fine branch by applying oriented refinement to high-frequency line residuals;
- keep MIT and Google filtered Dice non-catastrophic, avoiding a one-source-only improvement;
- provide a distinct failure mode if false positives are dominated by smooth cloud context rather than local line texture.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The front end normalizes ABI channels 1-16, adds fixed brightness-temperature-difference planes derived only from those approved channels, and learns a 1x1 spectral mixer. A frequency-split stem builds raw, local-detail, and broad-context projections using differentiable average-pool residuals. A three-level residual U-Net encodes and decodes 256, 128, 64, and 32 pixel scales. Decoder skip connections are gated by low-frequency skip context. The final frequency-pyramid fusion combines full-resolution decoder features, local high-pass detail, local and broad smooth context, and projected lower-scale decoder features, then applies an oriented high-frequency line refiner before emitting `mask_logits` and provider-derived `centerline_logits`.

No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `bce_dice_cldice`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially as an unprofiled architecture-family scout under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch or increased concurrency is requested.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.02 of ABI-058 while improving filtered precision, filtered predicted-positive fraction, or negative-patch false-positive diagnostics;
- capped best `val/filtered_dice` above ABI-058 or ABI-061;
- filtered Contrail Connectivity at or above ABI-058 with no larger predicted-positive burden;
- source-balanced behavior with both MIT and Google filtered Dice above 0.25 and a finite late-epoch improving trajectory.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, filtered Dice below 0.25 with no late improvement, or worse precision/false-positive burden than ABI-058 and ABI-064 without compensating recall/connectivity/source-balance gains.

## Fallback/Next Decision

If ABI-066 trains finitely but does not improve any false-positive, source-balance, or connectivity signal, do not repeat this exact frequency-gated U-Net branch; broaden toward a different topology/connectivity mechanism or trusted data/loss policy. If it improves precision or false-positive burden while trailing aggregate Dice modestly, consider one bounded family-development continuation such as a trusted `focal_tversky` loss swap or a small centerline auxiliary-weight adjustment within the allowlist. If it fails contract validation or smoke testing, classify the failure and repair only if the original frequency-gated hypothesis and comparison target are preserved.
