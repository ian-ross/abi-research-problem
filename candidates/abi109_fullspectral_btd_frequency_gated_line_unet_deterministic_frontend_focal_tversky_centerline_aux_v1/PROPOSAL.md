# ABI-109 deterministic-front-end frequency-gated line U-Net

## Hypothesis

ABI-109 is a family-development continuation of the full-spectral BTD frequency-gated line U-Net branch. ABI-068 is the current local aggregate-Dice reference, while ABI-066 remains the precision/connectivity-forward reference. The hypothesis is that ABI-068's learned 1x1 spectral mixer contributes to recall-forward negative-patch clutter and to the learned-mixer non-finite sensitivity seen in later large-kernel/ConvNeXt scouts; replacing it with deterministic normalized raw ABI channels plus explicit thermal BTD planes may preserve most focal-Tversky recall while improving precision, connectivity, positive-area discipline, or run stability.

## Comparison Target

Primary comparison target: ABI-068, `run_20260828_010836_4ccc77`, the frequency-gated line U-Net with learned spectral mixer, trusted focal-Tversky loss, and Centerline Target auxiliary supervision.

Secondary reference: ABI-066, `run_20260827_230540_bf4ce3`, the same frequency-gated family with trusted BCE-Dice-clDice loss and stronger precision/connectivity behavior.

## Expected Effect

Removing the learned mixer is expected to reduce early spectral over-parameterization and force the encoder to use bounded normalized raw bands plus physically motivated thermal BTD contrasts. Useful evidence would be a capped representative run that stays within about 0.01 filtered Dice of ABI-068 while improving filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction, or that shows a cleaner ABI-066-like operating profile without all-negative/all-positive collapse.

## Implementation Sketch

Start from ABI-068's model topology: normalized full-spectral ABI input, explicit thermal BTD planes, frequency-split stem, high/low spatial-frequency skip gating, dilated context, frequency-pyramid fusion, final mask head, and trusted `centerline_logits` auxiliary output. The controlled architecture change is only the front end: remove the learned 1x1 mixer and concatenate deterministic normalized raw ABI channels with the existing approved-channel BTD planes. No custom target, loss, metric, sampler, augmentation, thresholding, postprocessing, Artifact Filter, filesystem, network, or resource logic is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude and latitude are not read, reconstructed, or supplied.
- Output form: `mask_logits` plus provider-declared auxiliary `centerline_logits`.
- Primary loss: trusted `focal_tversky`.
- Auxiliary target: provider-derived `centerline` with trusted `weighted_bce`, weight 0.02.
- Data policies: provider-owned `combined_source_balanced` traversal and trusted `random_mirroring` augmentation.
- Scheduler/early stopping: trusted `constant_lr`, disabled early stopping.

## Budget Requested

Use the active Workspace Configuration ceilings: provider-selected representative cap of 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, AdamW learning rate 0.0003, constant learning rate, disabled early stopping, fixed first-four prediction retention, A100 execution under Harness ownership, and the 3,600-second Docker training timeout. Expected parameters are below the 25M smoke ceiling and lower than ABI-068 because the learned mixer is removed.

## Success Criteria

Classify ABI-109 as useful positive or mixed-positive capped family-development evidence if it trains finitely, avoids persistent all-negative/all-positive prediction collapse, keeps both MIT and Google filtered Dice above 0.35, and satisfies at least one of:

- aggregate `val/filtered_dice` is within 0.01 of ABI-068 while filtered precision or filtered connectivity improves;
- filtered predicted-positive fraction decreases by at least 10% relative to ABI-068 without dropping filtered recall by more than 0.03;
- aggregate filtered Dice exceeds ABI-066 while retaining at least ABI-066-like filtered precision or connectivity within 0.05.

A whole-validation Evaluation Request would be justified only if capped evidence is competitive with ABI-068/066 on aggregate and at least one secondary operating-profile axis.

## Fallback/Next Decision

If ABI-109 is non-finite, all-negative/all-positive, source-catastrophic, or more than about 0.02 below ABI-068 without a meaningful precision/connectivity/positive-area gain, stop this deterministic-front-end ablation and do not repair unless the failure is a clear implementation bug. If it is finite but slower-learning with a late-improving trajectory, consider whether a later in-contract learning-rate or loss-axis continuation is warranted. If it is clean but not competitive, broaden to a materially different architecture or trusted policy axis rather than adding another late suppressor/gate to ABI-068.
