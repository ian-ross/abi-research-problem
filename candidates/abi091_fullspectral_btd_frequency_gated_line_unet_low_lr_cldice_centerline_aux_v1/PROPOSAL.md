# ABI-091 full-spectral BTD frequency-gated line U-Net low-LR clDice continuation

## Hypothesis

A lower AdamW learning rate can stabilize the ABI-066 precision/connectivity-forward frequency-gated line U-Net branch under the trusted `bce_dice_cldice` loss, improving or preserving aggregate filtered Dice while retaining the reduced predicted-positive burden and strong Contrail Connectivity Metric that made ABI-066 diagnostically useful.

This is a **family-development continuation**. It is not a promotion claim and it does not require beating the capped ABI-068 focal-Tversky result to remain useful. It tests a trusted training-policy axis on the ABI-066 loss branch rather than adding another post-decoder gate to ABI-068.

## Comparison Target

Primary local target: ABI-066, Run `run_20260827_230540_bf4ce3`, which used the same architecture, `bce_dice_cldice`, Centerline Target auxiliary weight 0.02, random mirroring, batch size 4, 12 epochs, and learning rate 0.0003.

Secondary context: ABI-068, Run `run_20260828_010836_4ccc77`, remains the best capped aggregate filtered-Dice frequency-gated reference; ABI-085, Run `run_20260829_181201_01c5e7`, showed that learning rate 0.0001 is resource-feasible on the same architecture under focal-Tversky but did not improve that loss branch.

## Expected Effect

Lowering the learning rate on the clDice branch should reduce late-epoch oscillation and may trade a small amount of recall for improved precision, connectivity, and positive-area discipline. A useful result would sit near ABI-066/068 aggregate filtered Dice while preserving ABI-066-like filtered precision, filtered connectivity, and low filtered predicted-positive fraction better than recent focal-Tversky post-decoder variants.

## Implementation Sketch

Reuse the ABI-066 model architecture unchanged: normalized full-spectral ABI channels, explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, a learned spectral mixer, frequency-split stem, residual encoder/decoder, low-frequency-gated skip fusion, dilated bottleneck context, frequency-pyramid fusion, and oriented line refiner. Emit `mask_logits` and provider-declared `centerline_logits`.

Change only the manifest learning rate from 0.0003 to 0.0001 while retaining the trusted `bce_dice_cldice` primary loss, AdamW optimizer, batch size 4, 12 epochs, constant learning rate scheduler, combined source-balanced sampling, and trusted random mirroring.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; no longitude, latitude, or reconstructed coordinate inputs.
- Output form: `mask_logits` plus provider-declared auxiliary `centerline_logits`.
- Trusted auxiliary target: `centerline` with `weighted_bce` weight 0.02.
- Trusted primary loss: `bce_dice_cldice`.
- Trusted data policy selections: `combined_source_balanced`, `all_target_frames`, `random_mirroring`.
- Trusted optimizer/scheduler selections: AdamW, learning rate 0.0001, `constant_lr`.

Candidate code owns only neural-network architecture over provider-supplied tensors. It does not implement data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, external filesystem access, network access, pretrained weights, or lifecycle behavior.

## Budget Requested

Run one bounded representative Candidate under the current Workspace Configuration: up to 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, 25M-parameter smoke ceiling, 3,600-second Docker training timeout, and the Harness-owned A100 execution policy.

The model is the same 12.09M-parameter architecture as ABI-066/068/085, which previously completed within the current resource budget.

## Success Criteria

Useful continuation evidence if the Run is finite and non-degenerate, both MIT and Google filtered Dice remain above 0.33, and either:

- aggregate `val/filtered_dice` is within about 0.01 of ABI-066 while filtered precision, filtered connectivity, or filtered predicted-positive fraction improves; or
- aggregate `val/filtered_dice` approaches the ABI-068/085 band while preserving ABI-066-like precision/connectivity better than ABI-085.

A stronger positive signal would be aggregate filtered Dice at or above ABI-066 with filtered precision near 0.44, filtered connectivity near 0.47, and filtered predicted-positive fraction near or below 0.0028.

## Fallback/Next Decision

If the Run is non-finite, all-negative/all-positive, or source-catastrophic, classify the failure before proposing repair. If it is finite but clearly below ABI-066/068/085 without a secondary precision/connectivity or source-balance advantage, do not repeat this low-learning-rate clDice branch. Broaden to a materially different architecture family or another trusted policy axis rather than adding more ABI-068 post-decoder gates.
