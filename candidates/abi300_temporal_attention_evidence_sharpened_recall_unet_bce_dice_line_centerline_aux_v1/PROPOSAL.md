# ABI-300 temporal attention evidence-sharpened recall U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family. This is a mechanism-changing return to ABI-223/238-style temporal attention after the ABI-296/297/298/299 local-correlation branch, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-223/238 and ABI-285 remain the temporal-eligible comparators. ABI-223/238 preserve useful precision and connected-line behavior but leave recall below ABI-285, while ABI-285 recovers recall/source-balanced Dice at the cost of low selected-checkpoint connectivity. ABI-296/298/299 showed that local temporal correlation can raise recall, but that branch repeated oscillatory precision/recall/connectivity trade-offs and did not approach the temporal-attention frontier.

ABI-300 tests whether temporal-attention fusion can be sharpened at the architecture head rather than replaced by local matching. It keeps the ABI-223/238 temporal-attention U-Net backbone and directional full-resolution context, then adds region, line, detail, and agreement streams that provide small bounded recall support in uncertain logit bands. The intended mechanism is to raise true contrail logits at the fixed 0.5 threshold while avoiding broad clutter through a learned disagreement/clutter gate. This is not Candidate-owned thresholding, postprocessing, morphology, a loss, a metric, or an Artifact Filter.

## Comparison Target

Primary temporal-eligible comparisons are ABI-223 temporal-attention fusion, ABI-238 temporal-attention directional context, and ABI-285 temporal C4 line-state late36. Secondary local-branch references are ABI-296 and ABI-299 because they motivated recall-support design but are not the mechanism target. Broader context remains ABI-202 as the aggregate whole-validation reference and ABI-249 as the high-precision C4 comparator, acknowledging that this Run will be capped temporal-eligible feasibility evidence only.

## Expected Effect

A useful result does not need to beat the whole-validation frontier. ABI-300 should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered Dice or MIT filtered Dice closer to ABI-223/238/285 than ABI-296/299 without a large precision collapse;
- filtered recall above ABI-223/238 while preserving materially better precision/connectivity than the local-correlation branch;
- reduced negative-patch clutter relative to ABI-296/299 at comparable recall, visible through lower predicted-positive fraction or higher precision;
- a source-informative learning trajectory showing threshold-evidence sharpening rather than local-correlation oscillation.

A negative but useful result would show that recall-preserving calibration-style heads still trade off against precision/connectivity under temporal attention, motivating either a different temporal continuity mechanism or a non-temporal frontier pivot.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, temporal selection, padding, missing-frame repair, or frame discovery is implemented.
- Build per-frame finite normalized ABI, ABI-channel-derived thermal BTD, and Solar Geometry Input features.
- Use shared per-frame projection and per-pixel temporal attention relative to the center frame, preserving ABI-223/238's provider-owned temporal input pattern.
- Decode with a compact U-Net/ASPP backbone and full-resolution directional context.
- Replace the single direct mask head with an Evidence Sharpening Head: region, line, detail, and agreement streams contribute bounded support through an uncertainty-band gate; a learned clutter/disagreement gate can subtract a small penalty from confident mismatches.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-300 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because ABI-300 changes the temporal-attention head mechanism and should first profile finite/resource behavior and early evidence under the default budget.

## Success Criteria

Continue this branch only if the Run completes, remains finite and source-informative, and improves the temporal-attention recall/precision/connectivity compromise relative to ABI-223/238 or clearly outperforms ABI-296/299 local-correlation results without new clutter. A late-improving follow-up would require a best checkpoint near epoch 12, finite non-collapsed predictions, source-informative metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the temporal-attention evidence-sharpening hypothesis and Comparison Target. If it is resource-infeasible, reduce head width/branches rather than changing data or Harness-owned policy. If it completes but simply shifts along the same precision/recall/connectivity trade-off as ABI-223/238 or ABI-296/299, stop this exact head design and broaden to a different temporal continuity mechanism or a non-temporal recall/connectivity architecture family.
