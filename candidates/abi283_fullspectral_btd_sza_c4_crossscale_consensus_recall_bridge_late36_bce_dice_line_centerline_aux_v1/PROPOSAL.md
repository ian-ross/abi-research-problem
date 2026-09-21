# ABI-283 C4 cross-scale consensus recall bridge U-Net

## Hypothesis

ABI-279 showed that C4 line/detail residual support can recover fixed-threshold recall and connected-line evidence relative to ABI-249, but its whole-validation diagnostic exposed lower precision, broader negative-patch clutter, and lower Google Dice. ABI-280 made the residual bridge more selective, but its selected checkpoint still broadened predictions, reduced connectivity, and did not improve the combined tradeoff. A cross-scale consensus bridge should add recall support only where full-resolution C4 line evidence agrees with coarser decoder/context support, reducing clutter while preserving connected thin-line evidence.

Classification: family-development continuation within the profiled C4/orientation-prior family.

## Comparison Target

Primary comparisons are ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision compact C4 comparator, ABI-279 (`run_20260913_000141_3344db`) as the C4 recall/connectivity tradeoff comparator with whole-validation diagnostics, and ABI-280 (`run_20260913_023629_7902f3`) as the selective-consensus negative result. Secondary context is ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation reference.

## Expected Effect

Cross-scale agreement should reject some ABI-279-style single-scale line/detail clutter while preserving more true contrail recall than ABI-249. Useful evidence would be filtered precision and predicted-positive compactness closer to ABI-249/280, with recall/connectivity above ABI-249 and without ABI-280's connectivity loss. Source behavior should remain finite and non-collapsed for both MIT and Google.

## Implementation Sketch

Start from the ABI-249/279/280 full-spectral BTD+SZA C4 U-Net lineage. Preserve the normalized approved-channel front end, ABI-channel-derived BTD features, SZA features, signed-detail/context stem, encoder/decoder, ASPP bottleneck, C4 rotation-shared line context, and trusted Line plus Centerline auxiliary outputs.

Replace ABI-280's final selective-consensus head with a cross-scale consensus head:

- project half-resolution decoder, quarter-resolution decoder, and ASPP-context features to the base channel width and upsample them to full resolution;
- compute full-resolution C4 steerable line context from the final decoder features;
- refine multi-scale support from the C4 line context plus the three projected support maps;
- learn a consensus gate from region, C4 line, detail, multi-scale support, and support-mean features;
- learn a small clutter veto from line/support disagreement and signed-detail magnitude;
- construct logits with bounded architecture-internal residuals:
  `region_logits + 0.14*consensus*tanh(line_logits) + 0.10*consensus*tanh(multiscale_logits) + 0.06*consensus*detail_gate*tanh(detail_logits) - 0.07*(1-consensus)*clutter_gate*sigmoid(clutter_logits)`.

The bounded residual and veto are learned model logic only. They do not choose thresholds, perform morphology, apply Artifact Filters, or postprocess predictions.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- Provider-approved ABI channels, Solar Geometry Input, and ABI-channel-derived BTDs inside the model front end.
- `output_form: mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.
- Trusted `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss and `weighted_bce` auxiliary losses.
- AdamW, constant learning rate, batch size 4, and Harness-owned budget/resource enforcement.

The Candidate does not own data loading, temporal lookup, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for up to 36 epochs via `budget_request.yaml`, falling back to the exploratory 12-epoch budget if denied. This is justified by ABI-249's selected epoch 31, ABI-279's selected epoch 22 with useful whole-validation transfer, ABI-280's selected epoch 22, and the resource-similar, mechanism-changing nature of this C4-family continuation. The manifest itself remains at the exploratory max-epoch ceiling.

## Success Criteria

Useful continuation evidence would include any of:

- filtered precision/predicted-positive compactness closer to ABI-249 than ABI-279 while preserving part of ABI-279's recall/connectivity lift;
- filtered Dice near or above ABI-249/279/280 capped levels with improved connectivity versus ABI-280;
- lower source imbalance or negative-clutter proxy behavior without Google collapse;
- finite non-collapsed predictions and a stable or improving late trajectory under Harness-selected `val/filtered_dice`.

Promotion-level evidence would require trusted whole-validation diagnostics against ABI-202, ABI-249, and ABI-279; this capped run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-283 is finite and improves the precision/recall/connectivity tradeoff relative to ABI-249/279/280, request trusted whole-validation failure-bucket diagnostics in a later Autonomy Step. If it behaves like ABI-280 by oscillating between compact underprediction and broad low-connectivity recall, do not repeat the cross-scale head unchanged. If it fails smoke, contract, finite-state, or resource checks, classify the Harness-recorded failure and repair only if the original hypothesis can be preserved. If the C4 branch remains clutter-limited, broaden toward a different mechanism such as temporal evidence sharpening or a source-balanced calibration architecture without moving thresholds, postprocessing, losses, metrics, or Artifact Filters into Candidate code.
