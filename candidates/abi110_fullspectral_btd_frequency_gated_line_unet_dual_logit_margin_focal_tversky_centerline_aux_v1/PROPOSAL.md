# ABI-110 dual-logit-margin frequency-gated line U-Net

## Hypothesis

ABI-110 is a family-development continuation of the full-spectral BTD frequency-gated line U-Net branch. ABI-068 remains the local aggregate-Dice reference, while ABI-066 remains the precision/connectivity-forward reference. The hypothesis is that ABI-068's single 1x1 mask-logit head does not explicitly model background evidence, allowing focal-Tversky training to keep a recall-forward operating point with excess clutter. Replacing only that head with a foreground-minus-background dual-logit margin head may improve threshold-0.5 precision, positive-area discipline, or connectivity while preserving ABI-068-like recall and source balance.

## Comparison Target

Primary comparison target: ABI-068, `run_20260828_010836_4ccc77`, the frequency-gated line U-Net with learned spectral mixer, trusted focal-Tversky loss, and Centerline Target auxiliary supervision.

Secondary reference: ABI-066, `run_20260827_230540_bf4ce3`, the same frequency-gated family with trusted BCE-Dice-clDice loss and stronger precision/connectivity behavior.

## Expected Effect

The dual-logit margin head predicts trainable foreground and background evidence from the same refined decoder features, then returns a fixed half-scale foreground-minus-background margin as `mask_logits`. This keeps the Harness-owned thresholding and loss semantics unchanged while requiring positive evidence to exceed learned background evidence in the final logit. Useful evidence would be a capped representative run that retains ABI-068's aggregate/source balance while reducing filtered predicted-positive fraction or improving filtered precision/connectivity, or that recovers ABI-066-like precision/connectivity without collapsing recall.

## Implementation Sketch

Start from ABI-068's topology: normalized full-spectral ABI input, explicit approved-channel thermal BTD planes, learned 1x1 spectral mixer, frequency-split stem, high/low spatial-frequency skip gating, dilated context, frequency-pyramid fusion, and provider-declared `centerline_logits` auxiliary output. The controlled architecture change is the mask head only: replace the single one-channel 1x1 mask head with a two-channel evidence head and return `0.5 * (foreground_logit - background_logit)`. No custom target, loss, metric, sampler, augmentation, thresholding, postprocessing, Artifact Filter, filesystem, network, pretrained-weight, or resource logic is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude and latitude are not read, reconstructed, or supplied.
- Output form: `mask_logits` plus provider-declared auxiliary `centerline_logits`.
- Primary loss: trusted `focal_tversky`.
- Auxiliary target: provider-derived `centerline` with trusted `weighted_bce`, weight 0.02.
- Data policies: provider-owned `combined_source_balanced` traversal and trusted `random_mirroring` augmentation.
- Scheduler/early stopping: trusted `constant_lr`, disabled early stopping.

## Budget Requested

Use the active Workspace Configuration ceilings: provider-selected representative cap of 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, AdamW learning rate 0.0003, constant learning rate, disabled early stopping, fixed first-four prediction retention, A100 execution under Harness ownership, and the 3,600-second Docker training timeout. Expected parameter count is essentially ABI-068-sized and remains below the 25M smoke ceiling.

## Success Criteria

Classify ABI-110 as useful positive or mixed-positive capped family-development evidence if it trains finitely, avoids persistent all-negative/all-positive prediction collapse, keeps both MIT and Google filtered Dice above 0.35, and satisfies at least one of:

- aggregate `val/filtered_dice` is within 0.01 of ABI-068 while filtered precision or filtered connectivity improves;
- filtered predicted-positive fraction decreases by at least 10% relative to ABI-068 without dropping filtered recall by more than 0.03;
- aggregate filtered Dice exceeds ABI-066 while retaining ABI-066-like filtered precision or connectivity within 0.05.

A whole-validation Evaluation Request would be justified only if capped evidence is competitive with ABI-068/066 on aggregate and at least one secondary operating-profile axis.

## Fallback/Next Decision

If ABI-110 is non-finite, all-negative/all-positive, source-catastrophic, or more than about 0.02 below ABI-068 without a meaningful precision/connectivity/positive-area gain, stop this exact dual-logit-margin head branch and do not repair unless the failure is a clear implementation bug. If it is finite but only locally mixed, broaden to a materially different architecture or trusted policy axis rather than continuing small output-head variants.
