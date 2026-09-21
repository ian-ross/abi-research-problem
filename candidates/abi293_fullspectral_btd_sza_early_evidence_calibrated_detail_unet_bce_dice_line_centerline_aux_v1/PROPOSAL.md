# ABI-293 early evidence-calibrated detail U-Net

## Classification

Family-development continuation / mechanism-changing pivot from recent C4 recall-calibrator and temporal head variants. This is not a promotion claim; it is a bounded single-frame architecture test meant to determine whether recall support works better when calibration is shared through the encoder/decoder rather than applied only in a late C4 head.

## Hypothesis

Recent ABI-279/280/283/292 C4 work repeatedly alternated between compact high-precision/high-connectivity states and broader recall states. ABI-292 in particular showed that a late soft evidence band can recover only a small amount of recall while damaging precision and connected-line continuity. The hypothesis for ABI-293 is that a single-frame model that injects bounded clean detail/line evidence into skip features before decoding can raise true contrail logits at threshold 0.5 without relying on a broad late soft-band expansion.

The mechanism is early multi-scale evidence calibration: each encoder skip receives a learned reliability gate derived from local residual detail, broad context, and line-like separable context. The final head then combines region logits with bounded, reliability-gated detail and multi-scale line support plus a small clutter-disagreement veto. This keeps thresholding, postprocessing, losses, metrics, sampling, augmentation, Artifact Filters, and target derivation in trusted Harness/provider code.

## Comparison Target

Primary development comparisons are ABI-292 and ABI-283 because they represent the recent C4 recall-calibrator/compact-connectivity trade-off. Secondary comparisons are ABI-249 as the compact high-precision C4 comparator, ABI-279 as the recall/connectivity bridge comparator, and ABI-202 as the aggregate whole-validation reference.

## Expected effect

Success would look like capped representative filtered Dice at or above the ABI-283/249 band while recovering recall toward ABI-279/202, or a diagnostically useful operating point with better MIT/source balance and less negative-patch clutter than recent broad recall-support heads. A smaller success is evidence that early feature calibration improves the precision/recall/connectivity trade-off relative to ABI-292 even if it does not beat ABI-202.

## Contract Features Used

ABI-293 uses only allowlisted `abi_16ch_plus_sza` input, `combined_source_balanced` sampling, `all_target_frames` frame selection, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE.

## Implementation sketch

- Consume only provider-approved `abi_16ch_plus_sza` tensors.
- Build normalized raw ABI channels, approved-channel thermal BTD planes, Solar Geometry Input features, and a learned channel mixer.
- Use a compact U-Net with signed detail/context stem, residual encoder, ASPP bottleneck, and full-resolution decoder.
- Add `EvidenceCalibrationBlock`s at encoder skip levels; these compute reliability-gated detail and separable horizontal/vertical line-context residuals before decoding.
- Use a final calibrated evidence head that adds only bounded `tanh` support to region logits and subtracts a bounded clutter-disagreement veto.
- Emit trusted auxiliary outputs `line_logits` and `centerline_logits` for the allowlisted Line and Centerline targets.

## Contract and safety constraints

Candidate code defines architecture only. It does not load data, discover files, read temporal caches, derive targets, implement losses, metrics, Artifact Filters, sampling, augmentation, thresholds, postprocessing, coordinate features, Dataset Source identity features, downloads, resource placement, training loops, prediction retention, or lifecycle behavior. Longitude and latitude are not inputs.

## Budget

Use the default exploratory budget: capped provider-selected samples, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and trusted A100 execution under the active Workspace Configuration. No late-improving budget is requested.

## Success Criteria

Continue this branch only if the Run is finite, non-collapsed, source-informative, and shows a materially better trade-off than ABI-292: improved filtered Dice and connectivity without a larger false-positive footprint, or recall/source-balance close to ABI-279 with clearly better precision/compactness. A best epoch near the exploratory ceiling alone is insufficient for a late36 request unless the trajectory is improving rather than oscillatory and the precision/recall/connectivity trade-off is competitive.

## Fallback Next Decision

Stop this exact branch if it repeats ABI-292's failure mode (small recall gain with large precision/connectivity loss), collapses to high-precision underprediction, or produces broad low-connectivity clutter. In that case broaden away from C4/late-calibration mechanics rather than repeating an unchanged continuation.
