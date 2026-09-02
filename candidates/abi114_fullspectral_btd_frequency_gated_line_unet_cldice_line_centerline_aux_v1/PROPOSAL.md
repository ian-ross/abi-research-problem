# ABI-114 full-spectral BTD frequency-gated line U-Net clDice line+centerline auxiliary continuation

## Hypothesis

ABI-066 showed the strongest precision/connectivity-forward capped profile in the full-spectral BTD frequency-gated line U-Net branch with trusted `bce_dice_cldice` and a Centerline Target auxiliary head. ABI-108 showed that adding a low-weight Line Target auxiliary head under focal-Tversky reduced positive area and improved Google filtered Dice relative to several local continuations, but did not preserve ABI-068 aggregate/source balance. ABI-114 tests whether the Line Target auxiliary signal is more useful when paired with the continuity-aware `bce_dice_cldice` primary loss rather than the recall-forward focal-Tversky objective.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. It is not a full-data promotion claim. The expected scientific value is a controlled allowed-loss/auxiliary-target interaction test: can the ABI-066 connectivity/positive-area regime gain recall or source balance from an extra provider-derived Line Target without moving target derivation, loss implementation, thresholding, metrics, data loading, sampling, augmentation, Artifact Filters, resource placement, or lifecycle behavior into Candidate code?

## Comparison Target

Primary local target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it is the precision/connectivity reference for this branch and uses the same `bce_dice_cldice` primary loss.

Secondary targets: ABI-068, Run `run_20260828_010836_4ccc77`, because it is the capped aggregate filtered-Dice reference; and ABI-108, Run `run_20260830_115800_4a2363`, because it is the same line+centerline auxiliary architecture under focal-Tversky. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this Run is capped representative family-development evidence only.

## Expected Effect

The line+centerline auxiliary plus `bce_dice_cldice` pairing is expected to:

- keep ABI-066's continuity-aware primary objective and ABI-068/108 frequency-gated line architecture;
- add low-weight provider-derived Line Target supervision to reinforce mask extent without candidate-owned target generation;
- improve recall, source balance, or aggregate filtered Dice relative to ABI-066 while retaining more of ABI-066's filtered precision/connectivity and positive-area discipline than ABI-108;
- test a trusted loss/auxiliary-policy interaction rather than another local front-end, suppressor, or post-decoder gate tweak;
- preserve the resource profile of the established approximately 12.09M-parameter frequency-gated line U-Net variants.

## Implementation Sketch

Reuse the ABI-108 full-spectral BTD frequency-gated line U-Net architecture. The candidate uses provider-approved `abi_16ch` input only; computes normalized GOES ABI channels 1-16 plus deterministic thermal BTD planes derived only from those channels; applies the learned 1x1 spectral mixer, frequency-split stem, residual encoder/decoder, frequency pyramid fusion, and line refiner; and emits primary `mask_logits` plus `centerline_logits` and `line_logits` auxiliary outputs.

The controlled manifest change relative to ABI-108 is `training.loss: bce_dice_cldice`. The controlled manifest/model change relative to ABI-066 is adding the provider-derived Line Target auxiliary output at trusted `weighted_bce` weight 0.02 beside the existing Centerline Target auxiliary output at weight 0.02. No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary targets: provider-derived `centerline` emitted as `centerline_logits` and provider-derived `line` emitted as `line_logits`, each with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `bce_dice_cldice`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, custom evaluation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` at or above ABI-066 while improving filtered recall by at least about 0.02 without reducing filtered connectivity below about 0.40;
- capped best `val/filtered_dice` within about 0.01 of ABI-068 while improving precision, connectivity, or positive-area discipline over ABI-068;
- both MIT and Google filtered Dice above about 0.37 with a clearer precision/connectivity tradeoff than ABI-108;
- a finite, late-improving trajectory with no prediction collapse and secondary metrics suggesting the `bce_dice_cldice` plus Line Target pairing deserves one more bounded follow-up.

Hard-stop evidence for this exact branch would be smoke failure, non-finite behavior, persistent all-negative or all-positive collapse, aggregate filtered Dice below about 0.36 with no compensating connectivity/source evidence, source-specific catastrophic degradation, or connectivity/positive-area behavior worse than both ABI-066 and ABI-108.

## Fallback Next Decision

If ABI-114 improves ABI-066 recall/source balance while retaining useful precision/connectivity, consider a bounded whole-validation failure-bucket Evaluation Request before any promotion interpretation. If it is finite but misses all useful-continuation criteria, stop this exact line+centerline auxiliary plus `bce_dice_cldice` branch and broaden to a materially different calibration, data-policy, or architecture-family hypothesis rather than stacking more small auxiliary-head variants. If it fails contract validation or smoke testing, classify and repair only if the original trusted loss/auxiliary interaction hypothesis is preserved.
