# ABI-314 temporal shift-bank alignment detail U-Net

## Classification

Family-development continuation in the provider-owned temporal-input family, with a mechanism-changing pivot away from the recently characterized temporal C4 calibration-head branch and away from scalar local-correlation volumes. This is not a promotion candidate; it is a bounded scout of differentiable temporal feature alignment for fixed-threshold recall and connected-line support.

## Hypothesis

Recent temporal Runs sharpened the current failure mode. ABI-311 became the best balanced five-frame temporal C4 comparator, but ABI-312/313 showed that late residual calibration heads either broaden predictions or suppress true positives while losing connected-line quality. ABI-296/299 showed that scalar local correlation can supply recall/compactness evidence, but it did not consistently couple that evidence to connected thin-line continuity.

ABI-314 tests whether replacing scalar correlation maps with a small differentiable shift-bank feature alignment can preserve more neighbor-frame line evidence before decoding. The model learns previous/next frame keys and values, scores nine one-pixel shifts per neighbor against the center frame, softmax-aligns neighbor features, and fuses aligned temporal support with an explicit center-detail path. The intended effect is to tolerate small temporal displacement/advection while avoiding another post-decoder threshold or residual-head interpolation.

## Comparison Target

Primary temporal-eligible comparisons are ABI-311 as the balanced five-frame temporal C4 comparator, ABI-309 as the recall-heavy temporal C4 comparator, ABI-306 as the compact high-precision temporal C4 comparator, ABI-223/238 as temporal-attention continuity comparators, and ABI-296/299 as local-correlation branch references. ABI-202 and ABI-249 remain broader full Working Validation Split references but are not direct temporal-eligible promotion targets for this capped scout.

## Expected Effect

A useful ABI-314 result should complete under the exploratory budget and show finite, source-informative temporal-eligible behavior. Success does not require beating ABI-202. Useful evidence would be one of:

- higher fixed-threshold recall than ABI-223/238 while avoiding ABI-309-like large negative-patch footprint cost;
- higher filtered Dice or MIT filtered Dice than ABI-296/299 local-correlation references at comparable or better connectivity;
- a better precision/recall/connectivity compromise than ABI-312/313, indicating that pre-decoder aligned temporal features are more selective than late residual calibration;
- a late or source-balanced trajectory close enough to ABI-223/238/311 to justify a mechanism-changing continuation.

A negative but useful result would show that one-pixel shift-bank alignment still rides the same precision/recall/connectivity trade-off, helping decide whether to broaden further away from temporal matching.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside model forward only; do not load data, inspect caches, pad/repair temporal windows, or choose samples.
- Build finite per-frame normalized ABI, approved-channel thermal BTD, and Solar Geometry Input features.
- Encode all frames through a shared compact convolutional stem.
- Project center and neighbor features into a key space and neighbor value space. For each neighbor, compare center keys with nine shifted neighbor keys, softmax the score bank, and form an aligned neighbor feature as the weighted sum of shifted neighbor values.
- Fuse aligned previous/next support, alignment confidence, aligned disagreement, and center-to-aligned change features before the U-Net decoder.
- Preserve a center-frame detail stem and use a bounded evidence head to emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-314 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this shift-bank alignment mechanism is an unprofiled scout.

## Success Criteria

Continue this branch only if the Run completes, remains finite and non-collapsed, and improves a target temporal trade-off: filtered Dice/MIT Dice versus ABI-296/299, recall at a less cluttered footprint than ABI-309, connectivity at comparable recall versus ABI-312/313, or a late improving trajectory that approaches ABI-223/238/311 without source collapse. A late36 continuation would require Harness-validated evidence that the exploratory ceiling truncated a promising trajectory.

## Fallback/Next Decision

If the Run fails due to a candidate bug, classify and repair only if the fix preserves the shift-bank alignment hypothesis. If it is resource-infeasible, reduce width or abandon this mechanism under the current policy. If it completes but repeats broad low-connectivity clutter or compact under-recall without a late-improving trajectory, do not request an unchanged late36 continuation; broaden away from temporal matching toward a different line-continuity, calibration, data-policy, or architecture family.
