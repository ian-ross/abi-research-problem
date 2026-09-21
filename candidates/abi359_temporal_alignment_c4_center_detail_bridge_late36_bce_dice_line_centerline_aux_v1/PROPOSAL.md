# ABI-359 temporal alignment C4 center-detail bridge late36

## Hypothesis

ABI-356 recovered fixed-threshold temporal recall with multi-scale temporal-change/center-detail fusion, but its positive footprint was broad and its connected-line continuity was weak. ABI-357 and ABI-358 showed that late C4 continuity modules can compact predictions and raise precision, but either suppress recall or fail to improve connectivity. This family-development continuation tests whether moving C4/orientation continuity into the early center-detail and temporal-change alignment path, before the encoder and decoder commit to compact states, can preserve recall while improving connected-line evidence.

## Comparison Target

Primary comparison is ABI-358 (`run_20260919_151507_2ec383`) as the recall-preserving late-C4 sidecar parent, ABI-356 (`run_20260919_095725_843317`) as the recall-positive temporal-change parent, and ABI-350 (`run_20260919_013306_9ca44e`) as the compact predecoder line-support comparator. Secondary temporal-eligible comparators are ABI-357, ABI-324/348, and ABI-223. This is capped temporal-eligible evidence only, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

The expected effect is a more connected version of ABI-358 without ABI-357-style recall suppression. By aligning center-frame detail and neighbor-frame change with C4 line context before the encoder, the model should expose continuity evidence to all decoder scales instead of using it as a late veto. Useful evidence would be filtered Dice in the ABI-350/324/348 band, recall near or above ABI-358, and connectivity above ABI-358 while retaining compact negative-patch behavior.

## Implementation Sketch

Start from the ABI-358 temporal architecture: finite ABI+SZA+BTD per-frame features, temporal attention, compact U-Net encoder/decoder, ASPP bottleneck, and multi-scale temporal-change line-support skip fusion. Replace the late `RecallPreservingC4Sidecar` with an early `CenterDetailC4AlignmentBridge`:

- project center-frame spectral/detail features and temporal-change features at full 256x256 resolution;
- build a C4 rotation-shared line context from the combined temporal-stem, center-detail, and change seed before downsampling;
- add a small learned gated continuity residual to the stem so continuity evidence reaches all encoder scales;
- feed the early line context through the trusted Line auxiliary head and blend it with the final decoder features through a lightweight additive final refiner;
- avoid using the C4 path as a late compacting veto or Candidate-owned postprocessor.

The model returns `mask_logits`, `line_logits`, and `centerline_logits` with shape `[1, 256, 256]`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked frames only.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, and batch size 2.
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce` losses.

The candidate does not implement data loading, temporal lookup, S3/NetCDF access, padding, sample selection, losses, metrics, Artifact Filters, postprocessing, thresholds, target derivation, augmentation, resource scheduling, or coordinate/location features.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs through `budget_request.yaml`. ABI-356, ABI-357, and ABI-358 were finite, resource-safe, late-dependent, and oscillatory; the best ABI-358 checkpoint appeared at epoch 30 and the final checkpoint had a different recall/connectivity trade-off. This close mechanism-changing continuation is likely to require late-budget evidence. An exploratory 12-epoch result is a valid fallback if the Harness denies the request.

## Success Criteria

Treat this as family-development evidence, not a promotion claim. Success is any of:

- temporal-eligible `val/filtered_dice` at or above the ABI-350/324/348 capped band while improving ABI-358 connectivity;
- filtered recall at least comparable to ABI-358 with precision/compactness no worse than ABI-356;
- source-balanced MIT and Google filtered Dice remaining finite and non-collapsed while connectivity improves over ABI-358 or ABI-356.

Source-stratified metrics must remain finite and non-collapsed, with no evidence of coordinate, Artifact Filter, threshold, or Dataset Source identity dependence.

## Fallback/Next Decision

If ABI-359 repeats ABI-357-style recall suppression or fails to improve connectivity over ABI-358, stop this exact early-C4 bridge branch and broaden to a different temporal alignment/backbone or calibration-style architecture. If it improves the recall/connectivity trade-off but remains below ABI-350/324, consider one bounded mechanism-changing follow-up or a temporal-eligible failure-bucket diagnostic. Do not request Candidate-owned thresholds, postprocessing, losses, metrics, data loading, temporal lookup, or Artifact Filters.
