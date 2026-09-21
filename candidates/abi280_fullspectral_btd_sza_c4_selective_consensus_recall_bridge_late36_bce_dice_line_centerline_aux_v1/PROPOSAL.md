# ABI-280 C4 selective-consensus recall bridge U-Net

## Hypothesis

ABI-279 showed that C4 line/detail residual support can recover fixed-threshold recall and connected-line evidence relative to ABI-249, but its whole-validation diagnostic exposed the cost: lower precision, more negative-patch clutter, and lower Google Dice. A close C4-family continuation that makes the recall bridge selective should retain some of ABI-279's recall/connectivity lift while preserving more of ABI-249's compact high-precision operating point.

Classification: family-development continuation within the profiled C4/orientation-prior family.

## Comparison Target

Primary comparisons are ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision compact C4 comparator and ABI-279 (`run_20260913_000141_3344db`) as the C4 recall/connectivity tradeoff comparator. Secondary context is ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation reference.

## Expected Effect

The selective consensus head should reduce ABI-279-style false-positive broadening by adding line/detail residuals only where learned region, detail, and C4 orientation evidence agree. Expected useful evidence is a filtered-Dice/precision operating point closer to ABI-249 than ABI-279, with recall/connectivity still above ABI-249 and a smaller predicted-positive fraction or negative-patch clutter tail than ABI-279.

## Implementation Sketch

Start from the ABI-279 full-spectral BTD+SZA C4 U-Net. Preserve the normalized approved-channel front end, ABI-channel-derived BTD features, SZA features, signed-detail/context stem, encoder/decoder, ASPP bottleneck, C4 rotation-shared line context, and trusted Line plus Centerline auxiliary outputs.

Replace ABI-279's final dual-evidence bridge with a selective consensus head:

- a region branch over decoder and C4 line-context features;
- a detail branch over decoder features, C4 line context, and signed high-resolution detail;
- a clutter branch over decoder features, C4 line context, and absolute signed-detail magnitude;
- a learned sigmoid consensus gate from region/detail/line evidence;
- bounded logit construction: `region_logits + 0.16*consensus*tanh(line_logits) + 0.10*consensus*detail_gate*tanh(detail_logits) - 0.10*(1-consensus)*clutter_gate*sigmoid(clutter_logits)`.

The bounded residual and veto are learned architecture-internal evidence fusion only. They do not choose thresholds, perform morphology, apply Artifact Filters, or postprocess predictions.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- Provider-approved ABI channels, Solar Geometry Input, and ABI-channel-derived BTDs inside the model front end.
- `output_form: mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.
- Trusted `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss and `weighted_bce` auxiliary losses.
- AdamW, constant learning rate, batch size 4, and Harness-owned budget/resource enforcement.

The Candidate does not own data loading, temporal lookup, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for up to 36 epochs via `budget_request.yaml`, falling back to the exploratory 12-epoch budget if denied. This is justified by ABI-249's selected epoch 31, ABI-279's need for late-budget characterization of the C4 recall bridge, and ABI-280's close resource-similar continuation of that profiled lineage. The manifest itself remains at the exploratory max-epoch ceiling.

## Success Criteria

Useful continuation evidence would include any of:

- filtered precision closer to ABI-249 than ABI-279 while preserving at least part of ABI-279's recall/connectivity lift over ABI-249;
- filtered Dice near or above ABI-249/ABI-279 capped levels with lower predicted-positive fraction than ABI-279;
- improved MIT source balance without a Google collapse;
- finite non-collapsed predictions and a stable or improving late trajectory under Harness-selected `val/filtered_dice`.

Promotion-level evidence would require trusted whole-validation diagnostics against ABI-202, ABI-249, and ABI-279; this capped run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-280 is finite and improves the precision/recall/connectivity tradeoff relative to ABI-249/279, request trusted whole-validation failure-bucket diagnostics in a later Autonomy Step. If it simply suppresses recall back to ABI-249 without improving precision or Dice, do not repeat the selective head unchanged. If it fails smoke, contract, finite-state, or resource checks, classify the Harness-recorded failure and repair only if the original hypothesis can be preserved. If the C4 branch remains clutter-limited, broaden toward a different mechanism such as temporal evidence sharpening with orientation consensus or a source-balanced calibration architecture, without moving thresholds, postprocessing, losses, metrics, or Artifact Filters into Candidate code.
