# ABI-065 full-spectral BTD coarse-to-fine U-Net focal-Tversky continuation

## Hypothesis

Changing the ABI-064 full-spectral BTD coarse-to-fine U-Net from trusted `bce_dice_cldice` to trusted `focal_tversky` can move the coarse-prior branch toward the lower predicted-positive burden, higher precision, and higher connectivity seen in late ABI-064 epochs and in ABI-061, while preserving ABI-064's source-balanced capped Dice. This is a **family-development continuation** within the coarse-to-fine branch, not a promotion claim and not full-data evidence.

## Comparison Target

Primary local target: ABI-064, `abi064_fullspectral_btd_coarse_to_fine_unet_cldice_centerline_aux_v1`, Run `run_20260827_212811_0e34e2`. ABI-064 is the current best completed capped Run by `val/filtered_dice` in Research History at 0.3255, with MIT 0.3213, Google 0.3348, precision 0.3016, recall 0.3535, connectivity 0.1972, and filtered predicted-positive fraction 0.00425 at the best checkpoint.

Secondary context: ABI-058, Run `run_20260827_171331_c1769a`, remains the oriented-context high-resolution line U-Net reference at capped filtered Dice 0.3248 and whole-validation filtered Dice 0.3233. ABI-061, Run `run_20260827_194725_c1d6c6`, showed that focal-Tversky on the ABI-058 architecture improved capped precision, Google Dice, connectivity, and predicted-positive burden while sacrificing MIT Dice and aggregate recall.

## Expected Effect

The focal-Tversky loss is expected to test whether ABI-064's coarse semantic gate can reach a cleaner precision/connectivity operating point than the clDice scout without losing the source balance that made ABI-064 promising. Useful evidence would be a capped checkpoint that reduces filtered predicted-positive fraction below ABI-064 or improves filtered precision/connectivity while keeping aggregate filtered Dice near the ABI-064/ABI-058 range and avoiding MIT collapse.

A negative result remains useful if it shows that focal-Tversky's source-transfer/precision shift is architecture-independent and consistently trades away MIT recall, or if it shows that ABI-064's coarse prior needs a different trusted axis than primary-loss selection.

## Implementation Sketch

The candidate reuses the ABI-064 architecture unchanged. The model uses provider-approved `abi_16ch` input tensors only, normalizes ABI channels 1-16, creates fixed thermal brightness-temperature-difference planes only from those approved channels, and learns a 1x1 spectral mixer. A residual U-Net encoder-decoder creates full-resolution and 64-pixel features; an internal differentiable coarse-prior branch produces low-resolution logits and features; bilinear-upsampled coarse probability gates full-resolution decoder detail; an oriented fine refiner emits `mask_logits` and `centerline_logits`.

The controlled manifest change from ABI-064 is `training.loss: focal_tversky`. The provider-derived centerline auxiliary target remains requested as `centerline_logits` with trusted `weighted_bce` at weight 0.02.

No candidate-owned data loading, sampling, augmentation transforms, losses, metrics, target derivation, threshold selection, Artifact Filters, postprocessing, coordinate inputs, filesystem writes, network calls, pretrained weights, or training loop logic are introduced.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or reconstructed coordinate inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, default constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially as a profiled-family continuation under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, increased concurrency, GPU selection, data-policy override, scheduler change, or higher sample/epoch budget is requested.

ABI-064 used the same architecture and completed at 14.55M parameters with 7.55 GiB peak CUDA allocated and 9.55 GiB peak reserved, so this continuation should remain inside the trusted smoke and resource envelope.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` matching or exceeding ABI-064's 0.3255;
- capped best `val/filtered_dice` within 0.02 of ABI-064 while improving filtered precision, filtered connectivity, or filtered predicted-positive fraction;
- both MIT and Google filtered Dice above 0.25 with non-degenerate predictions and no source-specific collapse;
- a late improving trajectory that suggests the focal-Tversky coarse-to-fine branch is still learning under the 12-epoch cap.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, filtered Dice below 0.25 with no late improvement, MIT or Google filtered Dice below 0.20, or the same or worse predicted-positive burden than ABI-064 without a compensating recall/connectivity gain.

## Fallback/Next Decision

If ABI-065 is finite and improves precision/connectivity or reduces predicted-positive burden near ABI-064's aggregate Dice, request bounded whole-validation diagnostics for the stronger of ABI-064/ABI-065 before making promotion-oriented claims. If it reproduces ABI-061's source-asymmetric precision shift, record that loss-family behavior and broaden away from further focal-Tversky retries. If it underperforms without secondary-metric gain, treat ABI-064 as the coarse-to-fine local reference and broaden to another topology/connectivity or trusted-policy hypothesis rather than repeating this exact loss change.
