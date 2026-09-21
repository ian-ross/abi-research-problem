# ABI-298 temporal soft-agreement correlation recall U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family. This is a mechanism-changing follow-up to ABI-296 and ABI-297, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-296 showed that 3x3 local temporal correlation can raise fixed-threshold recall and connectivity relative to recent temporal negatives, but the selected checkpoint widened the prediction footprint and lost precision. ABI-297 showed that orientation agreement can compact predictions and improve precision, but using agreement as a hard temporal-support veto suppressed too much recall.

ABI-298 tests the next mechanism boundary: keep ABI-296-style local-correlation recall support, but use ABI-297-style center/temporal orientation agreement only as a soft additive calibration branch. Agreement boosts temporal-support logits where center-frame line context and temporal line context are consistent; disagreement applies only a small bounded penalty rather than vetoing center/detail recall paths. The intended effect is precision-preserving recall: recover ABI-296-like support while avoiding ABI-297's underprediction.

## Comparison Target

Primary comparisons are ABI-296 local correlation and ABI-297 orientation-agreement correlation. Temporal-family comparators are ABI-223, ABI-238, and ABI-285 on the temporal-eligible validation population. Secondary comparisons are ABI-289/290/291 for recent temporal recall/continuity mechanisms and ABI-202/249 as broader aggregate and high-precision references.

## Expected Effect

A useful result does not need to beat the whole-validation frontier. ABI-298 should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered recall closer to ABI-296 than ABI-297 while improving precision or footprint relative to ABI-296;
- filtered Dice above ABI-297 and closer to ABI-223/238/285 through a better precision/recall balance;
- connectivity comparable to ABI-296/297 without the ABI-297 recall collapse;
- a learning trajectory that distinguishes soft agreement calibration from hard agreement vetoing.

A negative but useful result would show that local-correlation support cannot be compacted without sacrificing recall under this family, motivating a broader temporal or non-temporal pivot.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, padding, temporal selection, or frame repair is implemented.
- Build per-frame normalized ABI, approved-channel thermal BTD, and Solar Geometry Input features.
- Encode all frames with a shared compact convolutional stem.
- Compute differentiable 3x3 local correlation volumes between center features and previous/next features, preserving ABI-296's small-displacement matching mechanism.
- Preserve center-frame signed detail independent of neighbor support.
- Decode with the resource-profiled compact width-28 U-Net used by ABI-297.
- In the head, build directional line context for both center-frame features and temporal-correlation support. Use orientation agreement as a soft boost for temporal support while preserving independent center/detail recall paths and applying only a small bounded disagreement penalty.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-298 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this is a mechanism-changing exploratory continuation and ABI-296/297 showed precision/recall oscillation rather than clean late improvement.

## Success Criteria

Continue this branch only if the Run completes, remains finite and source-informative, and improves the precision/recall/footprint trade-off relative to ABI-296 and ABI-297 or approaches ABI-223/238/285 in filtered Dice without sacrificing connectivity. A later late-improving follow-up would require a best checkpoint near the exploratory budget end plus non-collapsed, source-informative metrics and a trajectory suggesting unresolved optimization rather than oscillation.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the soft-agreement correlation recall hypothesis and Comparison Target. If it is resource-infeasible, reduce head cost or abandon this mechanism under the current exploratory budget. If it completes but still suppresses recall or repeats ABI-296's broad clutter, broaden away from local temporal matching rather than spending another close continuation.
