# ABI-067 full-spectral BTD frequency-gated line U-Net centerline-weight continuation

## Hypothesis

ABI-066s frequency-gated high/low spatial-feature line U-Net produced the strongest local whole-validation-tested Candidate so far, but its remaining gap to canonical MCAST 2.1 is mostly recall and operating-point calibration rather than false-positive burden. Lowering the trusted provider-derived `centerline` auxiliary loss weight from 0.02 to 0.01 may relax thin-line over-regularization enough to recover additional recall and improve filtered Dice, while the unchanged frequency-gated architecture preserves the false-positive suppression and connectivity gains.

This is a **family-development continuation** within the ABI-066 frequency-gated branch. It is not a promotion claim; it is a controlled in-contract test of one manifest-declared auxiliary-loss weight after positive capped and whole-validation diagnostic evidence.

## Comparison Target

Primary target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`. ABI-066 reached capped best `val/filtered_dice` 0.3825 and whole-validation filtered Dice 0.3811, with filtered precision 0.4434, recall 0.3342, connectivity 0.4766, MIT filtered Dice 0.3639, and Google filtered Dice 0.4130.

Secondary context: ABI-058 and ABI-064 whole-validation diagnostics, which showed lower aggregate filtered Dice and substantially larger negative-patch false-positive burden; canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873 and higher recall.

## Expected Effect

The lower centerline auxiliary weight is expected to:

- increase filtered recall relative to ABI-066 at the primary threshold without broad all-positive drift;
- maintain most of ABI-066s precision, connectivity, and low predicted-positive burden through the unchanged frequency-gated topology;
- improve or credibly tie ABI-066 by capped `val/filtered_dice`, especially if the threshold-sweep calibration signal from the ABI-066 whole-validation review reflects mild underprediction;
- keep both MIT and Google source filtered Dice non-catastrophic and preferably above the ABI-066 local-reference floors.

## Implementation Sketch

The Candidate copies the ABI-066 model architecture unchanged. It uses provider-approved `abi_16ch` input only, normalizes ABI channels 1-16, derives explicit thermal brightness-temperature-difference planes only from those approved channels, learns a spectral 1x1 mixer, and applies the internal differentiable frequency split, low-frequency-gated U-Net skips, frequency-pyramid fusion, and oriented high-frequency line refiner before emitting `mask_logits` and `centerline_logits`.

The only intended experimental change is in `manifest.yaml`: set the provider-derived `centerline` auxiliary `weighted_bce` weight to 0.01 instead of ABI-066s 0.02. The primary loss remains trusted `bce_dice_cldice`.

No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.01.
- Primary loss: trusted `bce_dice_cldice`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially as a controlled family-development continuation under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch or increased concurrency is requested.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` matching or exceeding ABI-066s 0.3825;
- filtered recall improved by at least 0.02 over ABI-066 while retaining aggregate filtered Dice within 0.01 and filtered precision above 0.40;
- filtered connectivity remaining above 0.40 with predicted-positive fraction not materially above ABI-066s low-burden profile;
- both MIT and Google filtered Dice above 0.34 with a finite late-epoch trajectory.

Hard stop evidence for this exact auxiliary-weight branch would be smoke failure, non-finite behavior, prediction collapse, filtered Dice below 0.34 with no late improvement, or a loss of ABI-066s false-positive/connectivity advantage without compensating recall.

## Fallback/Next Decision

If the lower auxiliary weight improves recall or Dice while preserving ABI-066s false-positive control, request whole-validation diagnostics before making further family-development decisions. If it weakens precision/connectivity or source balance, retain ABI-066 as the local full-validation-tested frequency-gated reference and avoid further simple centerline-weight sweeps. A later alternative could test an architecture-level recall path within frequency-gated fusion, but pure post-hoc threshold selection should remain Harness-owned diagnostic or operator-reviewed policy rather than Candidate-owned behavior.
