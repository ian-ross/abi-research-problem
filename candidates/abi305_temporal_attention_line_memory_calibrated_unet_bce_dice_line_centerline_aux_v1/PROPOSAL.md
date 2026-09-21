# ABI-305 temporal attention line-memory calibrated U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family. This is a mechanism-changing return to ABI-223/238-style temporal attention with internal line-memory calibration after ABI-296/299 local correlation and ABI-304 five-frame additive recall did not organize recovered recall into connected-line evidence. It is not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-223/238 remain the cleaner temporal-attention precision/connectivity comparators, while ABI-285 has stronger temporal-eligible aggregate Dice and recall but weak connectivity and broader negative-patch clutter. ABI-296/299 showed that local displacement matching can raise recall, but the local-correlation branch widened predictions and did not approach the temporal-attention frontier. ABI-304 showed five-frame additive support can recover some recall, but again did not organize it into connected lines.

ABI-305 tests whether full-resolution multi-orientation line memory can calibrate temporal-attention logits before the fixed Harness threshold. The model keeps a temporal-attention U-Net backbone and adds a line-memory head that accumulates horizontal, vertical, and dilated diagonal context in model features. Bounded recall support is added through learned gates, while a learned disagreement/precision gate subtracts a small inconsistent-feature penalty. This is architecture logic only; it is not Candidate-owned thresholding, postprocessing, morphology, a loss, a metric, or an Artifact Filter.

## Comparison Target

Primary temporal-eligible comparisons are ABI-223 temporal-attention fusion, ABI-238 temporal-attention directional context, and ABI-285 temporal C4 line-state late36. Secondary references are ABI-296/299 for the local-correlation branch and ABI-304 for five-frame additive recall support. Broader context remains ABI-202 as the aggregate whole-validation reference and ABI-249 as the high-precision C4 comparator, with the caveat that ABI-305 will produce capped temporal-eligible feasibility evidence only.

## Expected Effect

A useful ABI-305 result does not need to beat the whole-validation frontier. It should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered Dice closer to ABI-223/238/285 than ABI-296/299/304 while avoiding a large precision collapse;
- filtered recall above ABI-223/238 with better connectivity or precision than the local-correlation and five-frame additive branches;
- evidence that line-memory calibration reduces oscillation between compact connected states and broad recall states, visible through a source-informative learning trajectory;
- lower predicted-positive fraction or higher precision than ABI-296/299 at comparable recall.

A negative but useful result would show that another temporal-attention calibration head still slides along the same precision/recall/connectivity trade-off, motivating a non-temporal or more substantially different continuity mechanism.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, temporal selection, padding, missing-frame repair, or frame discovery is implemented.
- Build finite normalized ABI, ABI-channel-derived thermal BTD, and Solar Geometry Input features per frame.
- Use shared per-frame projection and per-pixel temporal attention relative to the center frame, preserving the ABI-223/238 temporal-attention pattern.
- Decode with a compact U-Net/ASPP backbone plus high-resolution directional context.
- Replace direct logits with a line-memory calibration head: full-resolution horizontal, vertical, and dilated diagonal line-memory branches produce a residual memory feature; bounded support and disagreement heads adjust region logits through learned gates.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-305 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because ABI-305 changes the temporal-attention head mechanism and should first profile finite/resource behavior and early evidence under the default budget.

## Success Criteria

Continue this branch only if the Run completes, remains finite and source-informative, and improves the temporal-attention recall/precision/connectivity compromise relative to ABI-223/238 or clearly improves over ABI-296/299/304 without new clutter. A late-improving follow-up would require a best checkpoint near epoch 12, finite non-collapsed predictions, source-informative metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the temporal-attention line-memory calibration hypothesis and Comparison Target. If it is resource-infeasible, reduce line-memory width/branches rather than changing data or Harness-owned policy. If it completes but simply shifts along the same precision/recall/connectivity trade-off as ABI-223/238 or ABI-296/299/304, stop this exact head design and broaden to a different temporal continuity mechanism or a non-temporal recall/connectivity architecture family.
