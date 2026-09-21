# ABI-360 temporal-attention continuity-stabilized line support late36

## Hypothesis

ABI-350 remains the strongest recent temporal-attention pre-decoder line-support operating point, but its late trajectory was unstable and its connectivity did not match the ABI-223 temporal-attention connectivity reference. ABI-359 showed that earlier C4/orientation continuity evidence can materially raise connected-line metrics, but its head/decoder did not stably combine that continuity signal with ABI-350-like compact precision. This family-development continuation tests whether a bounded learned continuity-stabilized evidence head on top of ABI-350's pre-decoder line-support U-Net can preserve compact fixed-threshold Dice while injecting useful connected-line evidence before final logits.

## Comparison Target

Primary comparison is ABI-350 (`run_20260919_013306_9ca44e`) as the temporal-attention pre-decoder line-support comparator. ABI-359 (`run_20260919_175950_ac7b89`) is the mechanism-positive continuity parent, and ABI-358 (`run_20260919_151507_2ec383`) is the compact C4-sidecar parent. Secondary temporal-eligible comparators are ABI-356, ABI-348/324, and ABI-223. This is capped temporal-eligible evidence only, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

The expected effect is ABI-350-like compact filtered Dice and precision with more stable connected-line evidence. Useful evidence would be temporal-eligible `val/filtered_dice` in the ABI-350/348/324 band, MIT and Google filtered Dice remaining source-balanced and finite, connectivity above ABI-350 or ABI-358, and no ABI-356-style broad low-precision footprint. A mixed but useful outcome would preserve ABI-350 precision/compactness while improving positive-tail connectivity or reducing fragmented positives in a later diagnostic.

## Implementation Sketch

Start from ABI-350's provider-owned three-frame temporal-attention U-Net: finite ABI+SZA+BTD per-frame features, per-pixel temporal attention, compact U-Net encoder/decoder, ASPP context, and orientation-aware line support injected into encoder skips before decoder fusion. Replace the direct final logits with a `ContinuityStabilizedEvidenceHead`:

- keep the refined decoder output as a compact anchor;
- project the full-resolution line-supported skip and decoder detail features;
- build differentiable orientation-line evidence from the concatenated anchor/detail/line-support features;
- add that evidence back through a bounded learned agreement gate before mask, Line, and Centerline logits;
- avoid Candidate-owned thresholds, calibration, morphology, postprocessing, or Artifact Filters.

The model returns `mask_logits`, `line_logits`, and `centerline_logits` with shape `[1, 256, 256]`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked frames only.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, and batch size 2.
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce` losses.

The candidate does not implement data loading, temporal lookup, S3/NetCDF access, padding, sample selection, losses, metrics, Artifact Filters, postprocessing, thresholds, target derivation, augmentation, resource scheduling, coordinate/location features, or Dataset Source identity features.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs through `budget_request.yaml`. ABI-350 selected its best checkpoint at epoch 33, ABI-359 at epoch 27, and ABI-358 at epoch 30 with meaningful late precision/recall/connectivity oscillations. This close mechanism-changing continuation targets a late-emerging fixed-threshold trade-off; an exploratory 12-epoch result remains a valid fallback if the Harness denies the request.

## Success Criteria

Treat this as family-development evidence, not a promotion claim. Success is any of:

- temporal-eligible `val/filtered_dice` at or above the ABI-350/324/348 capped band while improving connectivity over ABI-350 or ABI-358;
- filtered precision and positive footprint comparable to ABI-350 with recall not materially worse than ABI-350;
- source-balanced MIT and Google filtered Dice remaining finite and non-collapsed while connected-line metrics improve over the immediate parents.

Source-stratified metrics must remain finite and non-collapsed, with no evidence of coordinate, Artifact Filter, threshold, or Dataset Source identity dependence.

## Fallback/Next Decision

If ABI-360 fails to match ABI-350's compact Dice/precision and does not improve connectivity, stop this exact continuity-stabilized head branch and broaden to a different temporal alignment/backbone or single-frame C4/detail mechanism. If it improves continuity with acceptable compactness but remains below ABI-350/324 on aggregate Dice, request a temporal-eligible failure-bucket diagnostic before deciding whether one further mechanism-changing continuation is justified. Do not request Candidate-owned thresholds, postprocessing, losses, metrics, data loading, temporal lookup, or Artifact Filters.
