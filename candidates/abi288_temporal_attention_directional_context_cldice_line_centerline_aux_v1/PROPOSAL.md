# ABI-288 temporal attention directional-context clDice scout

## Hypothesis

Recent temporal C4 and continuity-bridge Candidates improved isolated aspects of recall or line support but often destabilized the fixed-threshold precision/recall/connectivity tradeoff. ABI-238 already provides a resource-profiled temporal-attention directional-context architecture with strong precision and useful connected-line evidence. Switching only the trusted primary loss to provider-owned `bce_dice_cldice` may apply training-time connectivity pressure to the same architecture without adding another unstable line-logit or C4 branch.

## Comparison Target

Primary comparison targets are ABI-238 (`run_20260911_004137_f54c45`) and ABI-223 (`run_20260908_154531_8c7e2b`) on the trusted temporal-eligible capped validation population. ABI-285 (`run_20260913_100333_a250df`) is a secondary temporal recall comparator, while ABI-202 remains whole-validation aggregate context only and is not the required success bar for this loss-policy scout.

## Expected Effect

The expected effect is a higher or better-stabilized `val/filtered_contrail_connectivity` than ABI-238/223-style temporal attention at a comparable filtered-Dice band, or at minimum evidence that trusted clDice pressure can move temporal predictions toward connected thin lines without broad negative-patch clutter. A useful outcome may trade a small amount of precision for recall/connectivity, but should remain finite, source-informative, and non-collapsed on both MIT and Google temporal-eligible validation patches.

## Implementation Sketch

Reuse the ABI-238 compact temporal-attention fusion U-Net with per-frame ABI/Solar Geometry Input/BTD feature construction, lightweight temporal attention/change fusion, U-Net encoder/decoder, ASPP bottleneck, and high-resolution directional-context refinement. Keep `mask_logits`, `line_logits`, and `centerline_logits` outputs exactly as expected by the trusted output spec. The only intended mechanism change is the manifest-selected primary loss `bce_dice_cldice` instead of `bce_dice`.

## Contract Features Used

- Provider-owned `abi_16ch_plus_sza_temporal` input mode with `data.temporal_frame_offsets: [-1, 0, 1]`.
- Trusted `data.frame_selection_policy: temporal_eligible_center`.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Trusted `bce_dice_cldice` primary loss, AdamW optimizer, constant learning-rate scheduler, and disabled early stopping by workspace policy.
- Trusted Line and Centerline auxiliary targets through `weighted_bce` on `line_logits` and `centerline_logits`.
- Candidate code remains architecture-only and does not implement data loading, temporal lookup, missing-frame repair, sampling, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 2, learning rate 0.0003, constant learning rate, and current Harness-owned sample/time/resource ceilings. No `late_improving` budget is requested for the first clDice temporal-directional loss-policy scout.

## Success Criteria

- Contract validation and Harness smoke/training complete without non-finite, shape, lifecycle, or resource failure.
- Temporal-eligible validation predictions are finite, non-collapsed, and source-informative for both MIT and Google.
- Compared with ABI-238/223 temporal attention, the result improves connected-line continuity or yields a better Dice/recall/connectivity tradeoff at threshold 0.5.
- A continuation can be considered if the trajectory is finite, near the temporal comparator band, and shows late or ambiguous improvement in filtered Dice/connectivity without broad predicted-positive clutter.

## Fallback/Next Decision

If ABI-288 collapses, fails contract/resource checks, or clearly worsens filtered Dice and connectivity versus ABI-238/223, treat the trusted clDice temporal-directional branch as a negative loss-policy result and do not repeat it unchanged. If it improves connectivity but loses too much recall or source balance, use the result to design a mechanism-changing temporal architecture or a different trusted loss/architecture pairing; do not add candidate-owned thresholds, losses, metrics, postprocessing, Artifact Filters, temporal loading, or sample selection.
