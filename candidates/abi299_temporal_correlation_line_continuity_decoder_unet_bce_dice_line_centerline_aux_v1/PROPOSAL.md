# ABI-299 temporal correlation line-continuity decoder U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family. This is a mechanism-changing follow-up to ABI-296/297/298, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-296 showed that 3x3 local temporal correlation can raise fixed-threshold recall, but its best checkpoint used a broad lower-precision footprint. ABI-297 showed that hard orientation agreement compacts predictions but over-suppresses recall. ABI-298 showed that soft orientation agreement recovers much of the recall but remains a near tie with ABI-296 and does not solve temporal line-continuity or precision.

ABI-299 tests the next mechanism boundary: keep local-correlation support, but add an explicit differentiable line-continuity decoder bridge over center-line, temporal-line, and multiscale decoder support. The bridge should boost connected thin-line evidence and make temporal support more coherent without using Candidate-owned thresholding, morphology, postprocessing, Artifact Filters, metrics, or losses. The intended effect is to retain ABI-296/298 recall while improving connectivity/precision enough to narrow the gap to ABI-223/238/285.

## Comparison Target

Primary comparisons are ABI-296 local correlation and ABI-298 soft-agreement local correlation. ABI-297 is the hard-agreement negative control. Temporal-family comparators are ABI-223, ABI-238, and ABI-285 on the temporal-eligible validation population. Secondary broader references are ABI-202 aggregate whole-validation reference and ABI-249 high-precision C4 comparator, acknowledging that temporal-eligible capped evidence is not whole-validation promotion evidence.

## Expected Effect

A useful result does not need to beat the whole-validation frontier. ABI-299 should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered Dice above ABI-296/298 through better precision/connectivity at comparable recall;
- filtered connectivity closer to ABI-223/238 while avoiding ABI-297's recall suppression;
- filtered predicted-positive fraction below ABI-296/298 without a large MIT or recall collapse;
- a learning trajectory showing line-continuity evidence rather than another head-only precision/recall oscillation.

A negative but useful result would show that adding differentiable continuity to local-correlation support still cannot close the temporal gap, motivating a broader pivot back to ABI-223/238-style temporal attention with evidence sharpening or away from temporal local matching.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, padding, temporal selection, or frame repair is implemented.
- Build per-frame normalized ABI, approved-channel thermal BTD, and Solar Geometry Input features.
- Encode all frames with a shared compact convolutional stem.
- Compute differentiable 3x3 local correlation volumes between center features and previous/next features, preserving ABI-296/298's small-displacement matching mechanism.
- Preserve center-frame signed detail independent of neighbor support.
- Use a compact U-Net decoder with base width 24 for resource margin after ABI-297/298 ran close to the exploratory timeout.
- Add a Line Continuity Bridge that applies horizontal, vertical, and dilated diagonal depthwise line context to center-line, temporal-line, and multiscale decoder support. The bridge output is a gated additive feature used by the mask, line, and centerline heads; it does not threshold, postprocess, or filter predictions.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-299 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this is a mechanism-changing exploratory continuation and ABI-296/297/298 showed precision/recall oscillation rather than clean late improvement.

## Success Criteria

Continue this branch only if the Run completes, remains finite and source-informative, and improves the precision/recall/connectivity trade-off relative to ABI-296/298 or approaches ABI-223/238/285 in filtered Dice without sacrificing MIT balance. A later late-improving follow-up would require a best checkpoint near the exploratory budget end plus non-collapsed, source-informative metrics and a trajectory suggesting unresolved optimization rather than oscillation.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the line-continuity local-correlation hypothesis and Comparison Target. If it is resource-infeasible, reduce continuity-bridge cost or abandon this mechanism under the current exploratory budget. If it completes but still repeats ABI-296/298 broad clutter or ABI-297 recall suppression, stop the immediate local-correlation branch and broaden to a stronger temporal-attention evidence-sharpening mechanism or another architecture family.
