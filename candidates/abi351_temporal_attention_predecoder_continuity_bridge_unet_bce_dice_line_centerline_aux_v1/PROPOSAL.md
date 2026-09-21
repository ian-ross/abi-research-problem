# ABI-351 temporal-attention pre-decoder continuity bridge

## Classification

Family-development continuation in the temporal-attention architecture family. This is a mechanism-changing exploratory follow-up to ABI-350, not a promotion claim and not whole-validation evidence.

## Hypothesis

ABI-350 validated ABI-349's pre-decoder line-support mechanism and became the strongest capped temporal-eligible aggregate filtered-Dice Result in the local comparison set, but its selected checkpoint remained compact/high-precision and did not close the connected-line continuity or MIT-positive-tail gaps against ABI-324 and ABI-223. The failure mode appears to be insufficient connected true-positive evidence before fixed-threshold logits, not simply a need for another late-budget repeat or final-head calibration.

ABI-351 keeps ABI-350's temporal-attention stem and pre-decoder line-supported skips, then adds a differentiable final continuity bridge between the high-resolution decoder feature and the mask/Line/Centerline heads. The bridge uses horizontal/vertical strip context, dilated diagonal context, local context, and a high-resolution skip gate to reinforce continuous thin-line features before logits while avoiding Candidate-owned thresholding, morphology, postprocessing, or Artifact Filters.

Expected effect: improve fixed-threshold connected-line continuity and positive-tail recall relative to ABI-350/349 while keeping the compact footprint and source-informative behavior that made ABI-350 useful.

## Comparison Target

- ABI-350 (`run_20260919_013306_9ca44e`): direct late-budget parent and strongest local temporal-attention aggregate comparator.
- ABI-349 (`run_20260919_004607_f785f8`): direct exploratory parent before late continuation.
- ABI-324 (`run_20260916_184108_954ec7`): balanced five-frame temporal C4/detail-consensus comparator on temporal-eligible validation.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator.
- ABI-348 (`run_20260918_215534_a35ab9`): compact five-frame C4 comparator with weak connectivity.

## Implementation sketch

Start from ABI-350's provider-owned `[-1, 0, 1]` temporal ABI+SZA input path: finite ABI/SZA/BTD feature building, shared per-frame projection, per-pixel temporal attention and change stem, compact U-Net encoder, ASPP context, and orientation-aware pre-decoder line support at skip scales 2, 1, and 0.

Add `FinalContinuityBridge` after the existing high-resolution decoder refinement and before all logits. The bridge computes a bounded anchor feature, depthwise long horizontal and vertical strip responses, medium/wide dilated diagonal responses, and smoothed local context. It projects these into a support feature and gates the support plus the scale-0 line-supported skip into the final decoder feature. The mask, Line, and Centerline logits are produced from the bridged feature.

This remains differentiable model architecture only. It does not implement data loading, temporal lookup, target derivation, loss/metric definitions, sample selection, augmentation, threshold selection, calibration, postprocessing, morphology, Artifact Filters, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice`.
- Trusted auxiliary targets: Line and Centerline with `weighted_bce`.
- Optimizer/scheduler: AdamW with constant learning rate.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 2, under the Harness-owned resource and timeout limits. No late-improving budget is requested for this first mechanism-changing variant. If the exploratory trajectory is finite, non-collapsed, source-informative, and best-at-end or otherwise late-improving, a later close continuation may request the approved late-improving budget.

## Success criteria

ABI-351 is useful if it completes finitely and shows at least several of:

- higher temporal-eligible connectivity than ABI-350 without a major aggregate Dice regression;
- fewer complete positive misses or low-connectivity positive patches than ABI-350/348;
- fixed-threshold recall improvement without ABI-344-style broad negative-patch clutter;
- MIT and Google filtered Dice remain source-informative with no source collapse;
- compact predicted-positive footprint remains closer to ABI-350/223 than to broad recall-sidecar variants;
- a learning trajectory that justifies either a late-improving continuation or a clear mechanism-level stop.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, clear resource incompatibility, or a finite plateau that worsens ABI-350's aggregate score while failing to improve connectivity/positive-tail behavior.

## Fallback decision

If ABI-351 improves connectivity or positive-tail diagnostics but is undertrained at epoch 12, consider a late-improving continuation with the same mechanism. If it increases footprint/clutter without connectivity gains, stop this bridge variant and broaden to a different temporal alignment/change mechanism or to a single-frame C4 anchor with cross-scale detail support. If it fails contract or resource checks, repair only if the failure is a narrow implementation bug that preserves the hypothesis.
