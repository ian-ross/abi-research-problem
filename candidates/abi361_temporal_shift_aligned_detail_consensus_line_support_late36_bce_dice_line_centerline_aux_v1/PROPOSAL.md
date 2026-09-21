# ABI-361 temporal shift-aligned detail-consensus line support late36

## Hypothesis

Recent ABI-350/356/358/359/360 temporal Runs show a persistent three-way tension between fixed-threshold recall, compact negative-patch behavior, and connected thin-line continuity. ABI-350 remains the strongest capped temporal-attention pre-decoder line-support comparator, while ABI-359 exposed useful early continuity evidence and ABI-360 showed that another final continuity-stabilized head mostly trades into broad low-precision recall. This family-development continuation tests a different mechanism: align previous and next frame features to the center frame with a learned local shift-consensus block before temporal attention and pre-decoder line support. If neighbor-frame evidence is slightly displaced by advection or sampling geometry, center-aligned detail consensus should raise true contrail logits and continuity before the decoder without relying on final-head residuals, thresholds, or postprocessing.

## Comparison Target

Primary comparison is ABI-350 (`run_20260919_013306_9ca44e`), the current strongest temporal-attention pre-decoder line-support comparator on the capped temporal-eligible population. Secondary comparisons are ABI-359 (`run_20260919_175950_ac7b89`) for early C4/continuity evidence, ABI-360 (`run_20260919_210615_da5139`) for the failed continuity-stabilized head, ABI-356 for recall-heavy temporal evidence, and ABI-324/348/223 for temporal C4/detail and temporal-attention connectivity context. This is capped temporal-eligible evidence only, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

Expected useful evidence is temporal-eligible `val/filtered_dice` near the ABI-350/324/348 band with improved or at least preserved connected-line continuity, source-balanced MIT and Google filtered Dice, and no ABI-356/360-style broad low-precision footprint. A mixed-positive result would improve recall or connectivity over ABI-350 while keeping precision and filtered predicted-positive fraction close to ABI-350. A negative result would show that local shift alignment adds cost or instability without improving the precision-recall-connectivity trade-off.

## Implementation Sketch

Start from ABI-350's three-frame temporal-attention U-Net with ABI+SZA+BTD per-frame features, compact encoder/decoder, ASPP bottleneck, and pre-decoder orientation-line support gates. Replace the temporal stem with a `ShiftAlignmentBlock` for the previous and next frame embeddings:

- project each provider-supplied frame into finite learned features;
- build a small zero-padded integer-shift bank for each non-center feature map;
- score each shifted neighbor against the center feature with a learned per-pixel agreement network;
- softmax over shifts to form aligned previous and next embeddings;
- feed aligned previous, center, aligned next through temporal attention, change features, and detail consensus before the existing line-supported decoder.

The shift bank is differentiable model logic over provider-advertised tensors. It is not temporal lookup, cache access, coordinate use, thresholding, morphology, postprocessing, or an Artifact Filter. The model returns `mask_logits`, `line_logits`, and `centerline_logits` with shape `[1, 256, 256]`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked frames only.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, and batch size 2.
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce` losses.

The candidate does not implement data loading, temporal lookup, S3/NetCDF access, padding or duplication of missing frames, sample selection, losses, metrics, Artifact Filters, postprocessing, thresholds, target derivation, augmentation, resource scheduling, coordinate/location features, Dataset Source identity features, or downloads.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs through `budget_request.yaml`. ABI-350 selected its best checkpoint at epoch 33, ABI-359 at epoch 27, and ABI-360 showed late precision/recall/connectivity oscillation after its selected epoch 22. This is a close mechanism-changing continuation of the same temporal-attention/line-support family and specifically targets a late-emerging temporal alignment/continuity trade-off. If the Harness denies the request, the exploratory 12-epoch fallback remains valid bounded feasibility evidence.

## Success Criteria

Treat this as family-development evidence, not a promotion claim. Success is any of:

- temporal-eligible `val/filtered_dice` at or above the ABI-350/324/348 capped band while improving connectivity over ABI-350 or ABI-359;
- filtered recall above ABI-350 with precision and filtered predicted-positive fraction remaining close to ABI-350;
- source-balanced MIT and Google filtered Dice remaining finite and non-collapsed while connectivity improves over ABI-358/360;
- a stable late trajectory that aligns high-recall and high-connectivity states better than ABI-359/360.

No success criterion depends on Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, coordinates, or Dataset Source identity.

## Fallback/Next Decision

If ABI-361 fails to match ABI-350's aggregate/precision band and does not improve recall or connectivity, stop this exact shift-alignment branch and broaden away from late temporal-attention line-support variants, for example to a single-frame C4/detail anchor with a pre-logit detail sidecar or a genuinely new lightweight backbone with explicit line-continuity decoding. If it improves connectivity or recall with acceptable compactness but remains below ABI-350/324 on aggregate Dice, request temporal-eligible failure-bucket diagnostics before considering one further mechanism-changing continuation. Do not request Candidate-owned thresholds, postprocessing, losses, metrics, data loading, temporal lookup, or Artifact Filters.
