# ABI-064 full-spectral BTD coarse-to-fine U-Net scout

## Hypothesis

A full-spectral BTD U-Net with an internal low-resolution soft mask prior feeding a full-resolution fine refiner can reduce the broad negative-patch false-positive burden seen in ABI-058 while preserving thin-line recall and connectivity. The coarse branch should learn patch-scale cloud/contrail plausibility before the final high-resolution decoder commits pixel-level detail, providing stronger context than another local decoder refinement without moving thresholding or Artifact Filters into candidate code.

This is a **family scout** for a coarse-to-fine architecture mechanism. It is not expected to beat the mature MCAST 2.1 baseline immediately, and continuation should depend on feasibility, non-degeneracy, trajectory, source behavior, and whether the precision/false-positive profile improves versus the high-resolution line U-Net reference.

## Comparison Target

Primary local target: ABI-058, `abi058_fullspectral_btd_hrline_unet_oriented_context_cldice_centerline_aux_v1`, Run `run_20260827_171331_c1769a`. ABI-058 reached capped best filtered Dice 0.3248 and whole-validation filtered Dice 0.3233, but its diagnostic review showed a broad low-level false-positive tendency on negative validation patches.

Secondary context: ABI-061, `run_20260827_194725_c1d6c6`, which improved capped precision/connectivity and Google Dice under focal-Tversky but did not improve aggregate filtered Dice; ABI-063, `run_20260827_203436_96acf7`, which repaired axial strip-context resource use but did not improve aggregate quality, precision, or connectivity.

## Expected Effect

The low-resolution coarse prior is expected to:

- lower filtered predicted-positive fraction and improve filtered precision versus ABI-058 without collapsing recall;
- keep MIT and Google filtered Dice non-catastrophic and avoid source-specific collapse;
- preserve or improve filtered Contrail Connectivity by using the full-resolution oriented refiner only after coarse semantic gating;
- produce a diagnostically different precision/recall trade-off from both ABI-058 and ABI-061.

A negative but finite result is still useful if it clarifies whether coarse semantic gating helps the current false-positive problem.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` inputs only. The front end normalizes ABI channels 1-16, adds fixed thermal brightness-temperature-difference planes using only those channels, and learns a 1x1 spectral mixer. A three-level residual U-Net encoder-decoder builds features at 256, 128, 64, and 32 pixel scales. From the 64-pixel decoder level, an internal coarse-prior branch predicts differentiable low-resolution logits and features. These logits are upsampled with bilinear interpolation and used as a soft feature gate, not as thresholding or postprocessing. The final head fuses gated full-resolution decoder features, stem features, projected 128-pixel decoder features, projected coarse features, and the upsampled soft prior, then applies an oriented full-resolution refiner before emitting `mask_logits` and the trusted `centerline_logits` auxiliary output.

No candidate-owned data loading, losses, metrics, target derivation, threshold selection, Artifact Filters, postprocessing, sampling, augmentation transforms, coordinate inputs, filesystem writes, network calls, pretrained weights, or training loop logic are introduced.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or reconstructed coordinate inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `bce_dice_cldice`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, default constant learning-rate scheduler, and disabled early stopping under current Workspace Configuration.

## Budget Requested

Run sequentially as an unprofiled architecture-family scout under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch or increased concurrency is requested.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.02 of ABI-058 while improving filtered precision or reducing filtered predicted-positive fraction;
- capped best `val/filtered_dice` above ABI-058 or ABI-061;
- source-balanced non-degenerate behavior with both MIT and Google filtered Dice above 0.25 and a final or late-epoch improving trajectory;
- filtered connectivity at or above ABI-058 without a larger predicted-positive burden.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, filtered Dice below 0.25 with no late improvement, or a precision/false-positive profile worse than ABI-058 and ABI-063 without a compensating recall/connectivity gain.

## Fallback/Next Decision

If the candidate is finite but below ABI-058 while improving precision or predicted-positive burden, consider one bounded family-development follow-up that changes only the trusted loss to `focal_tversky` or tunes the centerline auxiliary weight within the allowlist. If it is finite but does not improve any false-positive, source, or connectivity signal, broaden away from coarse-to-fine U-Nets toward a different topology/connectivity or data-policy hypothesis. If it fails contract validation or smoke testing, classify and repair only if the original coarse-to-fine hypothesis and comparison target are preserved.
