# ABI-315 temporal shift-bank alignment detail U-Net syntax repair

## Classification

Repair Candidate for ABI-314 after `run_20260915_100315_94315b` smoke-failed with Harness-recorded `candidate_bug`: `SyntaxError: unmatched '}'` at `model.py` line 320. ABI-315 preserves ABI-314's hypothesis, comparison target, manifest policy, architecture, and exploratory budget, changing only the accidental `},{` characters after the `ShiftBankEvidenceHead` docstring.

## Hypothesis

ABI-314 proposed a mechanism-changing temporal family-development scout: replace scalar local-correlation maps and recent temporal C4 residual calibration heads with differentiable small-displacement feature alignment before decoding. Previous and next frame features are scored over a nine-shift bank against center-frame keys, softmax-aligned, and fused with center-frame detail and directional line context. ABI-315 keeps that same hypothesis so the shift-bank alignment mechanism can be evaluated rather than discarded because of an import-time syntax defect.

## Comparison Target

Primary temporal-eligible comparisons remain ABI-311 as the balanced five-frame temporal C4 comparator, ABI-309 as the recall-heavy temporal C4 comparator, ABI-306 as the compact high-precision temporal C4 comparator, ABI-223/238 as temporal-attention continuity comparators, and ABI-296/299 as local-correlation branch references. ABI-202 and ABI-249 remain broader full Working Validation Split references but are not direct temporal-eligible promotion targets for this capped repair scout.

## Expected Effect

Expected success is first lifecycle feasibility: static validation, smoke import, and a completed finite 12-epoch capped Run. Scientific success is unchanged from ABI-314: source-informative evidence that shift-bank alignment improves at least one temporal trade-off, such as higher recall than ABI-223/238 without ABI-309-like negative-patch footprint cost, better filtered Dice or MIT Dice than ABI-296/299 at comparable connectivity, or a better precision/recall/connectivity compromise than ABI-312/313.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.
- Split the provider-stacked tensor into previous, center, and next frames inside model forward only; do not load data, inspect caches, pad/repair temporal windows, or choose samples.
- Preserve ABI-314's per-frame normalization, approved-channel BTD features, shared compact convolutional stem, shift-bank key/value alignment, U-Net decoder, center-frame detail path, and bounded evidence head.
- Repair only the unmatched brace sequence after `ShiftBankEvidenceHead`'s docstring so the intended class definition imports.
- Emit trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs for Harness-owned primary and auxiliary losses.

## Contract Features Used

ABI-315 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. The manifest declares repair lineage to ABI-314's candidate-bug smoke failure. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, trusted temporal-eligible selection, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this is only an import-syntax repair for an unprofiled scout.

## Success Criteria

Continue this branch only if the Run completes, remains finite and non-collapsed, and improves a target temporal trade-off: filtered Dice/MIT Dice versus ABI-296/299, recall at a less cluttered footprint than ABI-309, connectivity at comparable recall versus ABI-312/313, or a late improving trajectory that approaches ABI-223/238/311 without source collapse. A late36 continuation would require Harness-validated evidence that the exploratory ceiling truncated a promising trajectory.

## Fallback/Next Decision

If ABI-315 smoke-fails again with a candidate bug, classify the exact defect before deciding whether another repair is worthwhile. If it is resource-infeasible, reduce width or abandon this mechanism under the current policy. If it completes but repeats broad low-connectivity clutter or compact under-recall without a late-improving trajectory, do not request an unchanged late36 continuation; broaden away from temporal matching toward a different line-continuity, calibration, data-policy, or architecture family.
