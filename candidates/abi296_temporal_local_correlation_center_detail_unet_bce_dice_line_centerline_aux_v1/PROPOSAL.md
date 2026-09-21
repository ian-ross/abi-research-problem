# ABI-296 temporal local-correlation center-detail U-Net

## Classification

Family-development continuation within the provider-owned temporal-input family, with a mechanism-changing pivot away from recent temporal-attention and five-frame persistence variants. This is not a promotion candidate; it is a bounded scout of local temporal matching as a different evidence-sharpening mechanism.

## Hypothesis

Recent temporal Runs show a repeated precision/recall trade-off: compact predictions preserve precision or some connectivity but suppress true contrail recall, while recall states expand into weak clutter. ABI-296 tests whether explicit small-displacement local correlation between the center ABI Patch and its provider-supplied neighboring frames can sharpen temporal evidence without using candidate-owned temporal lookup, thresholds, losses, metrics, or postprocessing.

The mechanism is intentionally different from ABI-288 through ABI-291 attention variants. Instead of learning global per-frame attention weights, the model builds 3x3 local correlation volumes between projected center-frame features and previous/next-frame features. These correlation maps are fused with center-frame spectral/BTD/Solar Geometry Input detail and directional line context. The goal is to preserve center-frame thin-line detail while allowing modest advection/misalignment in neighbor evidence to raise true contrail logits at the fixed Harness threshold.

## Comparison Target

Primary comparisons are temporal-family comparators ABI-223 and ABI-238 on the temporal-eligible validation population, plus ABI-285 as the recent temporal C4 high-Dice/low-connectivity comparator. Secondary comparisons are ABI-289/290/291 for recent failed temporal recall/continuity mechanisms, and ABI-202/249 as broader aggregate and high-precision references.

## Expected Effect

Expected useful evidence is not necessarily beating ABI-202. A successful temporal-local-correlation scout should complete within the exploratory budget, remain finite and non-collapsed, and show one of:

- filtered recall closer to ABI-223/238/285 than ABI-291 while avoiding ABI-290-style broad low-precision footprints;
- connectivity improved relative to ABI-285/290 at comparable filtered Dice;
- source-stratified metrics that do not sacrifice MIT performance while using temporal-eligible selection;
- a learning trajectory that is source-informative and still improving or clearly diagnostic.

A negative but useful result would show that small-displacement correlation does not solve temporal recall suppression and should redirect temporal work toward a different motion representation or away from temporal mechanisms.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the channel-stacked tensor into previous, center, and next frames inside the model only; no Candidate data loading, cache access, padding, temporal selection, or frame repair is implemented.
- Build per-frame normalized ABI, approved-channel thermal BTD, and Solar Geometry Input features.
- Encode all frames with a shared compact convolutional stem.
- Project encoded features to a low-dimensional key space and compute 3x3 local correlation volumes for previous-vs-center and next-vs-center evidence using differentiable tensor operations.
- Fuse center features, neighbor differences, and local correlations into a temporal support map; keep an explicit center-detail path so neighbor support cannot replace center-frame evidence.
- Decode with a compact U-Net and a bounded evidence head that emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-296 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested for this first local-correlation scout.

## Success Criteria

Continue this local-correlation temporal branch only if the Run completes, remains finite and source-informative, and improves at least one target trade-off relative to recent temporal negatives: higher recall than ABI-291 without a large precision/connectivity collapse, better connectivity than ABI-285/290 at comparable Dice, or a clear late improving trajectory close enough to ABI-223/238 to justify bounded family development.

## Fallback/Next Decision

If the Run fails due to a candidate bug, classify and repair only if the fix preserves the local-correlation hypothesis. If it is resource-infeasible, reduce width or abandon this mechanism under the current exploratory budget. If it completes but repeats compact underprediction or broad low-connectivity clutter, do not request an unchanged late36 continuation; broaden to a different architecture family or write a note summarizing why temporal local matching did not address the fixed-threshold recall/connectivity problem.
