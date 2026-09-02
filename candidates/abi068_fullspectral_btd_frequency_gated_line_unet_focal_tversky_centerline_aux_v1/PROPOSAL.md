# ABI-068 full-spectral BTD frequency-gated line U-Net focal-Tversky continuation

## Hypothesis

ABI-066 established the frequency-gated line U-Net as the strongest local whole-validation-tested capped Candidate reference: it achieved high capped filtered Dice, strong precision, and useful connectivity, but still trailed canonical MCAST 2.1 and showed a recall/coverage gap. ABI-067 lowered the centerline auxiliary loss weight and recovered recall, but lost aggregate Dice, precision, Google-source Dice, and connectivity. A more targeted in-contract continuation is to keep the ABI-066 architecture and centerline supervision unchanged while changing only the trusted primary loss from `bce_dice_cldice` to `focal_tversky`.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. It is not a full-data promotion claim. The expected value is to test whether trusted focal-Tversky can move the operating point toward recall without simply weakening centerline regularization or increasing diffuse false positives.

## Comparison Target

Primary local target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it is the strongest current capped frequency-gated reference and the strongest local whole-validation-tested Candidate reference for this branch.

Secondary local target: ABI-067, `run_20260828_001300_16c885`, because it demonstrated recall recovery from centerline-weight reduction but at unacceptable precision/connectivity and Google-source cost. ABI-061 remains context for a prior focal-Tversky loss swap on the oriented-context high-resolution line U-Net branch. Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873, but capped evidence from this Run is feasibility and family-development evidence only.

## Expected Effect

Changing the primary loss to focal-Tversky is expected to:

- increase filtered recall relative to ABI-066 by emphasizing difficult positive Contrail Mask pixels;
- preserve more of ABI-066s filtered precision and Contrail Connectivity than ABI-067s simple centerline-auxiliary weight reduction;
- keep MIT and Google filtered Dice source-balanced rather than recovering recall only on one Dataset Source;
- show whether the frequency-gated architectures conservative prediction profile is loss-sensitive or architecture-limited;
- provide a controlled comparison because architecture, input mode, sampling policy, augmentation, optimizer, learning rate, batch size, epoch budget, and centerline auxiliary weight are unchanged from ABI-066.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The `model.py` architecture is copied from ABI-066: a normalized full-spectral front end, fixed thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, a high/low spatial-frequency split stem, low-frequency-gated skip fusion, multi-dilation coarse context, full-resolution frequency-pyramid fusion, and an oriented high-frequency line refiner. It emits primary `mask_logits` and provider-derived `centerline_logits`.

The manifest changes the trusted primary loss to `focal_tversky`. The centerline auxiliary target remains provider-derived with trusted `weighted_bce` at weight 0.02. No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

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

- capped best `val/filtered_dice` matching or exceeding ABI-066 while improving filtered recall;
- capped best `val/filtered_dice` within 0.01 of ABI-066 with filtered recall at least 0.38 and filtered precision at least 0.40;
- preserving filtered Contrail Connectivity near ABI-066 while improving recall or Dataset Source balance;
- both MIT and Google filtered Dice above 0.33 with a finite, non-collapsed, late-improving trajectory.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.32 with no late improvement, or an ABI-067-like tradeoff where recall improves only by losing ABI-066s precision/connectivity advantage and Google-source behavior.

## Fallback/Next Decision

If ABI-068 improves recall while preserving ABI-066s precision/connectivity profile, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it behaves like ABI-067, retain ABI-066 as the frequency-gated local reference and avoid additional simple loss/auxiliary-weight sweeps. If it fails contract validation or smoke testing, classify the failure and repair only if the original controlled loss-swap hypothesis is preserved. If it is finite but does not improve any operating-profile signal, broaden to a different in-contract architecture mechanism rather than weakening the contract or moving provider-owned policies into Candidate code.
