# ABI-368 temporal recurrent C4 connectivity decoder late36

## Classification

Family-development continuation. ABI-368 is a mechanism-changing continuation of the ABI-255 compact temporal recurrent-change branch, targeted at the thin-line continuity weakness observed in ABI-255 and recent temporal line-support variants.

## Hypothesis

ABI-255 showed that a compact bidirectional ConvGRU temporal state can train finitely and remain source-informative, but its temporal-eligible connectivity lagged ABI-223 and later C4/line-support temporal comparators. Recent ABI-365/366/367 results suggest local temporal line-support, detail-tail, and agreement-gate variants often separate into compact precision, broad recall, or transient connectivity. ABI-368 tests a different attachment point: keep ABI-255's recurrent temporal stem and U-Net decoder, then apply a C4 orientation-shared connectivity decoder only at the final high-resolution decoder stage before logits. The intended mechanism is to preserve the recurrent branch's temporal overlap signal while giving the selected checkpoint explicit, architecture-internal orientation consensus for continuous thin contrails, without Candidate-owned thresholds, postprocessing, losses, metrics, temporal lookup, coordinates, Dataset Source identity, or sampling changes.

## Comparison Target

Primary capped temporal-eligible comparison targets are ABI-255 (`run_20260911_210922_27f346`) for the recurrent temporal family, ABI-223 (`run_20260908_154531_8c7e2b`) for temporal-attention connectivity, ABI-350 (`run_20260919_013306_9ca44e`) for recent compact temporal line-support performance, ABI-359 (`run_20260919_175950_ac7b89`) for temporal C4/detail continuity evidence, and ABI-367 (`run_20260920_112921_1ee9bd`) as the latest local temporal tail result. ABI-202 and ABI-249 remain whole-validation/single-frame references but are not direct temporal-eligible promotion targets for capped evidence.

## Expected Effect

The intended effect is higher temporal-eligible connected-line continuity than ABI-255 and ABI-367 while retaining a compact enough footprint and enough recall to avoid the recent oscillation between high precision and broad low-connectivity recall. Useful evidence includes improved filtered Dice, MIT filtered Dice, filtered connectivity, and non-degenerate predicted-positive counts on the trusted temporal-eligible capped validation population, with a finite late trajectory rather than an all-negative/all-positive collapse.

## Implementation Sketch

The Candidate consumes only provider-advertised `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`. It preserves ABI-255's finite per-frame ABI+SZA+BTD feature builder, bidirectional ConvGRU temporal recurrent-change stem, single-stream encoder, ASPP context block, and U-Net decoder. The mechanism change is a final `C4ConnectivityDecoder`:

- refines the full-resolution decoder feature with the encoder skip;
- applies a depthwise-separable anisotropic strip block shared across four rotations;
- scores and blends the four orientation contexts into a weighted orientation consensus and a mean context;
- computes local signed-detail evidence from full-resolution features;
- fuses base, orientation consensus, mean context, and local detail through an architecture-internal gate before mask, Line, and Centerline logits.

Line and Centerline auxiliary logits remain ordinary model outputs supervised only by trusted provider-derived auxiliary targets.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only. It does not implement data loading, temporal lookup, S3/NetCDF access, padding, missing-frame fallback, sample selection, target derivation, loss functions, metrics, Artifact Filters, postprocessing, threshold selection, augmentation, coordinates, Dataset Source identity, resource scheduling, retries, downloads, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs with fallback to exploratory if denied. The request is justified because ABI-255 selected its best checkpoint at epoch 36, remained finite and source-informative, and this proposal preserves the same temporal input/training/resource class while adding a bounded final decoder module aimed at ABI-255's explicit continuity failure mode. If the Harness denies the request, the exploratory Run remains valid bounded evidence.

## Success criteria

Success is not limited to beating ABI-202 whole-validation evidence. ABI-368 is promising if it is finite/resource-safe and, on temporal-eligible capped validation, either:

- improves connectivity over ABI-255/367 while staying near their aggregate/source Dice;
- improves aggregate filtered Dice or MIT filtered Dice over ABI-255 without broad low-precision clutter;
- approaches ABI-350/359 aggregate performance while improving the recurrent family's connected-line evidence; or
- shows a late finite trajectory where recall, compactness, and connectivity begin to combine rather than occupy separate epochs.

A hard stop is justified if the Run fails contract/smoke/resource checks, becomes non-finite, persistently collapses predictions, clearly broadens into low-precision clutter, or regresses below ABI-255 without a compensating connectivity/source-balance signal.

## Fallback decision

If ABI-368 is negative, do not repeat the recurrent C4 decoder with only gate-strength, auxiliary-weight, or width tweaks. Broaden away from this recurrent-temporal branch toward a genuinely different temporal backbone, a single-frame C4/detail recall-support mechanism, or a trusted training-policy question only if it directly targets a current failure mode.
