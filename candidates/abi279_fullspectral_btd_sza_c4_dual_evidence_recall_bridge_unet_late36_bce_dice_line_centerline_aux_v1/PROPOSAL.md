# ABI-279 C4 dual-evidence recall bridge U-Net

## Hypothesis

ABI-249's C4/rotation-aware U-Net is a useful high-precision comparator but remains recall-limited at the trusted fixed threshold. A close continuation that keeps the same full-spectral BTD+SZA encoder/decoder and C4 steerable line context, while replacing the final head with a bounded dual-evidence recall bridge, may recover true contrail extent and connected thin-line support without candidate-owned thresholding or postprocessing.

Classification: family-development continuation within the profiled C4/orientation-prior family.

## Comparison Target

Primary comparison is ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision C4/rotation-aware whole-validation comparator. Secondary context is ABI-202 (`run_20260904_043143_ee0005`) as the aggregate reference and ABI-274/ABI-223 as temporal recall/connectivity comparators on their temporal-eligible population only.

## Expected Effect

The bounded bridge should preserve ABI-249's compact high-precision orientation behavior while adding small learned line/detail residual support to `mask_logits`. Expected useful evidence is higher filtered recall and Contrail Connectivity Metric at threshold 0.5, especially on MIT, with no large negative-patch clutter increase and no excessive Artifact Filter dependence.

## Implementation Sketch

Start from the ABI-249 full-spectral BTD+SZA C4 steerable U-Net. Preserve the normalized approved-channel front end, signed-detail/context stem, ASPP bottleneck, decoder, C4 rotation-shared line context, and trusted Line plus Centerline auxiliary heads. Replace the final mask head with:

- a broad region branch over decoder plus C4 line-context features;
- a detail branch over decoder features, C4 line context, and signed high-resolution detail;
- a learned sigmoid recall gate from region/detail/line evidence;
- `mask_logits = region_logits + 0.20*tanh(line_logits) + 0.15*gate*tanh(detail_logits)`.

The bounded residuals are learned architecture-internal evidence only. They do not choose thresholds, perform morphology, apply Artifact Filters, or postprocess predictions.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- Provider-approved ABI channels, Solar Geometry Input, and ABI-channel-derived BTDs inside the model front end.
- `output_form: mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.
- Trusted `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss and `weighted_bce` auxiliary losses.
- AdamW, constant learning rate, batch size 4, and Harness-owned budget/resource enforcement.

The Candidate does not own data loading, temporal lookup, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for up to 36 epochs via `budget_request.yaml`, falling back to the exploratory 12-epoch budget if denied. This is justified by ABI-249's profiled resource-safe C4 lineage and best checkpoint at epoch 31. The manifest itself remains at the exploratory max-epoch ceiling.

## Success Criteria

Useful continuation evidence would include any of:

- filtered Dice near or above ABI-249 while improving filtered recall by at least about +0.02 without a large precision collapse;
- higher Contrail Connectivity Metric than ABI-249 at a comparable compact predicted-positive fraction;
- improved MIT filtered Dice/source balance while retaining finite non-collapsed Google performance;
- a late finite trajectory indicating the C4 recall bridge remains trainable and not prediction-collapsed.

Promotion-level evidence would require trusted whole-validation diagnostics against ABI-202/249; this capped run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-279 is finite but simply trades precision for clutter without recall/connectivity gain, do not repeat the head unchanged. If it is finite and improves recall/connectivity while staying near ABI-249, request trusted whole-validation failure-bucket diagnostics. If it fails smoke, contract, or finite-state checks, classify the Harness-recorded failure and submit a repair only if the original hypothesis and comparison target are preserved. If it is resource-safe but scientifically weak, broaden toward a different recall-preserving calibration, center-frame detail, or temporal-attention evidence-sharpening mechanism rather than another unchanged late36 continuation.
