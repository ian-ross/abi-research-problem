# ABI-111 full-spectral BTD MCAST-guided dual-branch U-Net

## Hypothesis

ABI-111 is a family-scout Candidate Experiment that broadens away from recent local ABI-068 output-head, front-end, and small-gate tweaks. ABI-068 remains the local aggregate-Dice reference, while ABI-066 remains the precision/connectivity-forward reference. The hypothesis is that recent focal-Tversky frequency-gated variants have enough full-spectral BTD evidence for recall, but lack a robust thermal support stream that can regularize clutter and source shifts. A separate MCAST-lineage thermal branch, fused softly into the full-spectral BTD encoder/decoder, may improve calibration, precision, or source balance without moving thresholding, Artifact Filters, losses, metrics, sampling, or postprocessing into Candidate code.

## Comparison Target

Primary comparison target: ABI-068, `run_20260828_010836_4ccc77`, the full-spectral BTD frequency-gated line U-Net with trusted focal-Tversky loss and Centerline Target auxiliary supervision.

Secondary references:

- ABI-066, `run_20260827_230540_bf4ce3`, the precision/connectivity-forward BCE-Dice-clDice frequency-gated branch.
- ABI-105, `run_20260830_091941_139456`, the recall-forward conservative-skip focal-Tversky continuation.
- ABI-110, `run_20260830_192051_6b901b`, the negative dual-logit-margin head continuation that motivates moving beyond local output-head competition.

## Expected Effect

The model keeps full ABI channels and explicit approved-channel thermal BTD evidence for thin-contrail recall, but processes MCAST-like thermal planes in an independent branch: ABI channel 11, ABI channel 14, and ABI channel 13 minus ABI channel 15. Soft feature-space fusion gates allow this robust thermal branch to calibrate spectral/detail features at multiple encoder scales and before the final line refiner. Useful evidence would be finite capped representative training that approaches ABI-068 aggregate/source behavior while improving precision, connectivity, or predicted-positive area discipline relative to the recent recall-forward variants.

This is a family scout, not a promotion claim. Because it changes the feature-fusion family rather than a single local head, a result slightly below ABI-068 could still be useful if it reveals a cleaner or more source-balanced operating point.

## Implementation Sketch

Implement a compact dual-branch U-Net in `model.py`:

- `NormalizedBTDFrontEnd` normalizes GOES ABI channels 1-16, derives deterministic thermal BTD planes only from provider-approved ABI channels, and adds a learned 1x1 spectral mixer.
- `MCASTThermalFrontEnd` derives normalized MCAST-like thermal support planes from approved ABI channels 11, 14, and 13-minus-15.
- Parallel spectral/detail and MCAST support stems feed conservative `GuidedFusion` blocks at each encoder scale.
- A dilated bottleneck and U-Net decoder recover 256 x 256 resolution.
- A final line refiner combines decoder detail, horizontal/vertical/dilated line context, and projected MCAST support before emitting `mask_logits` and provider-declared `centerline_logits`.

The candidate does not add custom data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholds, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, longitude, or latitude.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude and latitude are not read, reconstructed, or supplied.
- Output form: primary `mask_logits` with auxiliary `centerline_logits`.
- Primary loss: trusted `focal_tversky`.
- Auxiliary target: provider-derived `centerline` with trusted `weighted_bce`, weight 0.02.
- Data policies: provider-owned `combined_source_balanced` traversal and trusted `random_mirroring` augmentation.
- Scheduler/early stopping: trusted `constant_lr`, disabled early stopping.

## Budget Requested

Use the active Workspace Configuration ceilings: provider-selected representative cap of 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, AdamW learning rate 0.0003, constant learning rate, disabled early stopping, fixed first-four prediction retention, A100 execution under Harness ownership, and the 3,600-second Docker training timeout. The compact base width is intended to keep the model below the 25M-parameter smoke ceiling despite the second encoder branch.

## Success Criteria

Classify ABI-111 as useful positive or mixed-positive scout evidence if it trains finitely, avoids persistent all-negative/all-positive prediction collapse, keeps both MIT and Google filtered Dice above 0.33, and satisfies at least one of:

- aggregate `val/filtered_dice` is within about 0.02 of ABI-068 while filtered precision, filtered connectivity, or filtered predicted-positive fraction improves;
- aggregate filtered Dice exceeds ABI-066 while retaining at least one ABI-066 strength, such as precision within 0.05 or connectivity within 0.08;
- it beats the recent ABI-105/107/108/109/110 focal-Tversky continuations on aggregate filtered Dice with non-catastrophic source behavior;
- it remains late-improving through epoch 12 with aggregate filtered Dice at or above 0.35 and a clearly cleaner precision/recall or source-balance profile than ABI-110.

A whole-validation Evaluation Request would be justified only if capped evidence is competitive with ABI-068 or uniquely improves the precision/connectivity/source-balance tradeoff.

## Fallback/Next Decision

If ABI-111 is non-finite, all-negative/all-positive, source-catastrophic, above the parameter ceiling, or more than about 0.04 below ABI-068 without a meaningful secondary-metric improvement, stop this exact dual-branch MCAST-guidance design unless a clear implementation bug is found. If it is finite, source-balanced, and late-improving but still below ABI-068, allow at most one bounded family-development continuation that changes a single controlled factor such as base width, learning rate, or trusted primary loss. If it is simply another recall-forward low-precision result, broaden again rather than adding more local output-side suppressors.
