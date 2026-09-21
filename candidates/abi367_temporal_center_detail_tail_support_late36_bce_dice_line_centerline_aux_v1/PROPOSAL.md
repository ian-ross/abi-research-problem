# ABI-367 temporal center-detail tail support late36

## Classification

Family-development continuation. ABI-367 is a close but mechanism-changing continuation of the ABI-350 temporal-attention pre-decoder line-support scaffold, informed by ABI-356 recall-positive temporal fusion and ABI-359 early-C4 continuity evidence.

## Hypothesis

ABI-350 is the strongest capped temporal-eligible aggregate comparator, but its failure-bucket review showed residual MIT-heavy positive-tail under-recall and lower connected-line continuity than ABI-324/223. ABI-356 recovered recall with too much broad footprint, while ABI-359 exposed useful continuity evidence but did not stably combine it with recall. ABI-367 tests whether a source-agnostic center-frame detail tail, injected after ABI-350-style decoder fusion and gated by architecture-internal line evidence, can raise true center-frame contrail logits at the fixed 0.5 threshold without using Candidate-owned thresholds, postprocessing, Artifact Filters, losses, metrics, data loading, temporal lookup, coordinates, Dataset Source identity, or sampling changes.

## Comparison Target

Primary capped temporal-eligible comparison targets are ABI-350 (`run_20260919_013306_9ca44e`) for compact aggregate temporal line-support performance, ABI-356 (`run_20260919_095725_843317`) for recall-biased temporal fusion, ABI-359 (`run_20260919_175950_ac7b89`) for early-C4 continuity evidence, ABI-324/348 as five-frame temporal C4/detail comparators, and ABI-223 as the temporal-attention connectivity comparator. ABI-202 and ABI-249 remain whole-validation/single-frame references but are not direct temporal-eligible promotion targets for capped evidence.

## Expected Effect

The intended improvement is a better joint operating point than ABI-350/356/359: maintain ABI-350-like precision and compact predicted-positive footprint, recover some ABI-356 recall/positive-tail support, and improve connected-line continuity toward ABI-359/324 without widening negative-patch clutter. Useful evidence includes improved filtered Dice, MIT filtered Dice, filtered recall, and connectivity on the trusted temporal-eligible capped validation population, plus non-degenerate predicted-positive counts and finite late-budget trajectory.

## Implementation Sketch

The Candidate consumes only provider-advertised `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`. It preserves ABI-350's temporal frame feature builder, per-pixel temporal-attention stem, single-stream encoder, ASPP context block, and pre-decoder orientation line-support gates. The mechanism change is a new `CenterDetailTailSupport` module after high-resolution decoder refinement:

- builds signed local detail and broad-context features from the provider-supplied center-frame ABI+SZA/BTD feature stack;
- computes line evidence using the existing orientation-line support block on decoder features;
- fuses decoder features, high-resolution skip evidence, center-detail evidence, and line evidence through a bounded residual tail;
- applies a learned architecture-internal gate before adding the tail to final mask features.

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

Request the approved `late_improving` budget for 36 epochs with fallback to exploratory if denied. The request is justified because ABI-350 selected its best checkpoint at epoch 33 and the proposed change preserves the same profiled temporal resource class with a small bounded high-resolution tail module. If the Harness denies the request, the exploratory Run remains valid bounded evidence.

## Success criteria

Success is not limited to beating ABI-202 whole-validation evidence. ABI-367 is promising if it is finite/resource-safe and, on temporal-eligible capped validation, either:

- improves aggregate filtered Dice over ABI-350 while preserving comparable precision and footprint;
- improves MIT filtered Dice and filtered recall over ABI-350 without ABI-356-like broad clutter; or
- materially improves connectivity over ABI-350/356 while remaining near the temporal frontier on aggregate/source Dice.

A hard stop is justified if the Run fails contract/smoke/resource checks, becomes non-finite, persistently collapses predictions, clearly broadens into low-precision clutter, or regresses below ABI-350/356/359 without a compensating source-balance/connectivity signal.

## Fallback decision

If ABI-367 is negative, do not repeat this center-detail tail with only gate-strength or auxiliary-weight tweaks. Broaden to a genuinely different temporal backbone, a trusted training-policy question with explicit failure-mode rationale, or a non-temporal C4/detail architecture only if it changes the mechanism rather than repeating recent local head variants.
