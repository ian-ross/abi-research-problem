# ABI-297 temporal orientation-agreement correlation U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family. This is a mechanism-changing follow-up to ABI-296, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-296 showed that 3x3 local temporal correlation can recover fixed-threshold recall and some connected-line evidence relative to recent temporal negatives, but its best checkpoint widened the predicted footprint and lost precision against ABI-223/238/285. ABI-297 tests whether local-correlation support should be trusted only when it agrees with center-frame oriented line evidence.

The model keeps ABI-296's provider-stacked previous/center/next frame processing and center-detail preservation, then adds an orientation-agreement gate in the evidence head. Center-frame directional line features and temporal-support directional line features are compared; recall support from temporal correlation is amplified only where the learned agreement gate and existing support gate both fire. Disagreement contributes a bounded compact veto. The intended effect is to preserve ABI-296's recall lift while reducing broad low-precision temporal support at the fixed Harness threshold.

## Comparison Target

Primary comparisons are ABI-296 as the local-correlation family baseline and ABI-223/238/285 as temporal-family comparators on the temporal-eligible validation population. Secondary comparisons are ABI-289/290/291 for recent temporal recall/continuity mechanisms, and ABI-202/249 as broader aggregate and high-precision references.

## Expected Effect

A useful result does not need to beat the whole-validation frontier. ABI-297 should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- higher filtered precision than ABI-296 without giving back all of ABI-296's recall gain;
- filtered Dice closer to ABI-223/238/285 than ABI-296 through a smaller filtered predicted-positive fraction;
- connectivity comparable to or above ABI-296 while improving MIT/source balance;
- a learning trajectory that distinguishes orientation-agreement gating from the broader ABI-296 footprint.

A negative but useful result would show that agreement-gating suppresses the useful recall component or fails to reduce temporal clutter, steering future work away from local-correlation variants.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, padding, temporal selection, or frame repair is implemented.
- Build per-frame normalized ABI, approved-channel thermal BTD, and Solar Geometry Input features.
- Encode all frames with a shared compact convolutional stem.
- Compute differentiable 3x3 local correlation volumes between center features and previous/next features, preserving ABI-296's small-displacement matching mechanism.
- Decode with a compact width-28 U-Net to keep the extra orientation-agreement head within the exploratory wall-clock/resource envelope.
- In the head, build directional line context for both center-frame features and temporal-correlation support. Use their learned agreement plus support gating to add bounded recall support, and use disagreement as a bounded compact veto.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-297 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because ABI-296 peaked before the final quarter and this is a changed architecture mechanism.

## Success Criteria

Continue this branch only if the Run completes, remains finite and source-informative, and improves the precision/recall/footprint trade-off relative to ABI-296 or approaches ABI-223/238/285 in filtered Dice without sacrificing connectivity. A late-improving follow-up would require a best checkpoint near the exploratory budget end plus non-collapsed, source-informative metrics; otherwise do not request an unchanged late36 continuation.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the orientation-agreement correlation hypothesis and Comparison Target. If it is resource-infeasible, reduce head cost or abandon this mechanism under the current exploratory budget. If it completes but simply suppresses recall or repeats broad clutter, broaden away from local temporal matching rather than spending another close continuation.
