# ABI-302 cross-scale directional-consensus ASPP with trusted clDice loss

## Hypothesis

Family-development continuation / training-policy scout. ABI-202 remains the whole-validation aggregate reference, but recent C4, temporal, line-memory, and MoE work continues to expose a recurring fixed-threshold trade-off: compact connected predictions suppress recall, while recall-support mechanisms broaden predictions and add clutter. ABI-302 tests whether changing only the trusted primary loss on the ABI-202 cross-scale directional-consensus ASPP architecture from BCE-Dice to BCE-Dice-clDice can add training-time connected-line pressure without adding Candidate-owned losses, thresholds, postprocessing, or artifact filters.

## Comparison Target

Primary comparison target is ABI-202 (`run_20260904_043143_ee0005`), the same architecture with trusted BCE-Dice and the current aggregate whole-validation reference. Secondary context includes ABI-249 as the high-precision compact C4 comparator, ABI-279 as the C4 recall/connectivity bridge diagnostic, ABI-184 as a precision/connectivity reference, and ABI-196 as a prior late36 aggregate comparator.

## Expected Effect

Expected capped effect is a modest improvement in filtered contrail connectivity and thin-line continuity at similar filtered Dice/source balance to ABI-202, or a diagnostically useful shift showing whether provider-owned clDice pressure improves connected-line evidence on the strongest architecture. A useful result would preserve non-degenerate predicted-positive fractions and avoid the common pattern where connectivity gains arrive only through severe recall loss or clutter expansion.

## Implementation Sketch

Reuse the ABI-202 full-spectral BTD+SZA cross-scale directional-consensus ASPP decoder architecture unchanged: normalized ABI+SZA and BTD front end, signed detail/context stem, encoder/ASPP decoder, full-scale skip fusion, cross-scale directional consensus bridge, line-aware refinement, and `mask_logits`, `line_logits`, and `centerline_logits` heads. The manifest changes only `training.loss` from `bce_dice` to trusted `bce_dice_cldice`; all data, augmentation, optimizer, scheduler, auxiliary-target, and resource choices remain Harness/provider-owned and unchanged.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; longitude and latitude are not model inputs.
- `output_form: mask_logits` with trusted Line and Centerline auxiliary targets.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Trusted `bce_dice_cldice` primary loss, AdamW optimizer, constant learning-rate scheduler, and batch size 4.
- Candidate code defines architecture only and does not implement data loading, sample selection, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, downloads, Dataset Source identity, coordinates, resource placement, prediction retention, or lifecycle control.

## Budget Requested

Request the Harness-validated `late_improving` budget for 36 epochs, with fallback to the exploratory budget if denied. The request is justified because the same architecture's ABI-202 parent selected epoch 34 of 36 as best and the earlier ABI-201 exploratory parent was still improving at the 12-epoch ceiling. This Candidate changes one trusted loss-policy factor while preserving the resource-profiled architecture and execution envelope.

## Success Criteria

Continue or consider diagnostics only if the Run is finite, non-collapsed, source-informative, and either (1) matches or improves ABI-202/249 filtered Dice while improving connectivity, or (2) clearly improves connectivity/recall balance over ABI-202 without a major MIT/Google or precision regression. A promotion-like result would need to approach ABI-202 whole-validation aggregate/source scores and not rely on Artifact Filters. A lower Dice result can still be useful if it cleanly answers whether trusted clDice pressure helps or hurts the strongest architecture's connected-line failure mode.

## Fallback/Next Decision

If ABI-302 lowers recall/source balance, expands clutter, or merely trades Dice for connectivity, do not repeat the same loss-policy continuation and do not request another unchanged longer budget. Record it as bounded evidence that BCE-Dice remains preferable for this architecture under the current contract, then broaden to a mechanism-changing architecture or data/training policy rather than another local clDice tweak.
