# ABI-366 temporal dual-evidence line-agreement U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI architecture family, run under the exploratory/default budget because the center/change dual-encoder agreement mechanism is materially different from recent local temporal line-support and five-frame variants.

## Hypothesis

ABI-350 showed that three-frame temporal attention plus pre-decoder line support can be competitive, but ABI-356/359/360/361/365 indicate that local temporal line-support continuations and five-frame near/far residuals oscillate among broad recall, compact precision, and transient connectivity. The failure mode is not simply insufficient temporal context; useful center detail, temporal change, and line continuity appear at different checkpoints or operating points.

ABI-366 tests a different architecture-level mechanism: keep center-frame appearance/detail evidence and temporal-change evidence in separate encoders, then merge them at each scale through agreement gates before line-supported decoder fusion. The expected effect is to raise fixed-threshold true-contrail logits where both center detail and temporal evidence support a thin structure, improving connected-line continuity and recall without ABI-356/360-style broad predicted-positive clutter.

## Comparison Target

- ABI-350 (`run_20260919_013306_9ca44e`): current strong three-frame temporal line-support capped comparator.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention diagnostic comparator on the temporal-eligible population.
- ABI-365 (`run_20260920_081530_7577c1`): negative five-frame pre-decoder line-support continuation.
- ABI-361 (`run_20260919_233003_a91c98`): negative shift-aligned detail-consensus continuation.
- ABI-356/360 (`run_20260919_095725_843317`, `run_20260919_210615_da5139`): recall-biased temporal variants with broad footprints and weak connectivity.

## Expected Effect

A useful result would improve the temporal recall/connectivity trade-off relative to ABI-365/361 and show a source-balanced trajectory plausibly competitive with ABI-350/223 after exploratory training or after a justified late-improving continuation. The desired signature is higher fixed-threshold recall than ABI-350 without ABI-356/360-style footprint broadening, and better selected-checkpoint connectivity than ABI-365's finite but unstable five-frame result.

Hard-stop evidence would be contract/resource failure, non-finite behavior, prediction collapse, clear wall-clock incompatibility, or a completed trajectory that is below ABI-350/223/365 across aggregate Dice, both source Dice scores, recall, connectivity, footprint, and learning behavior.

## Implementation Sketch

Use provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`. Build finite per-frame features from approved ABI channels and Solar Geometry Input, including ABI-channel-derived thermal BTD planes.

1. The center-detail stream projects only the zero-offset frame features.
2. The temporal-change stream projects center-minus-neighbor, next-minus-previous, and absolute neighbor residual features.
3. Separate compact encoders process the center and change streams.
4. At each encoder scale, an agreement gate sees center features, change features, and their absolute difference, then forms a bounded fused skip.
5. Orientation-aware line support is applied to the fused skips before decoder fusion, preserving continuity modeling inside differentiable architecture logic.
6. The final decoder emits compact logits and a bounded recall residual. A learned agreement gate controls the residual before producing `mask_logits`; Line and Centerline auxiliary logits are emitted from the same refined feature.

The agreement gates and logit fusion are model architecture, not threshold selection, calibration policy, morphology, postprocessing, target derivation, Artifact Filtering, metrics, losses, or data selection.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate. Do not request the late-improving budget for this first dual-evidence agreement scout. A late-improving continuation would be justified only if the exploratory Run is finite, non-collapsed, source-informative, and shows a still-improving or ambiguous trajectory near the epoch ceiling.

## Success criteria

This Candidate does not need to beat the whole-validation ABI-202 reference to be useful. It is successful enough for further temporal development if it completes finitely and shows several of these capped temporal-eligible signals:

- filtered Dice close to ABI-223/350 under a shorter exploratory budget, or a late trajectory suggesting undertraining;
- recall better than ABI-350 without the broad-footprint/low-connectivity pattern of ABI-356/360;
- connectivity trending toward ABI-223/350 and above ABI-365's selected checkpoint;
- MIT filtered Dice/source balance not sacrificed for Google-only gains;
- predicted-positive footprint consistent with agreement-supported line evidence rather than broad residual clutter.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent all-negative/all-positive collapse, or a finite result that clearly combines lower aggregate/source Dice with weak connectivity and broad clutter.

## Fallback decision

If ABI-366 is finite and shows useful but undertrained source/recall/connectivity behavior at 12 epochs, propose a late-improving continuation. If it repeats the recent oscillation between compact low-recall and broad low-connectivity states, do not tune gate strengths locally; broaden to a different temporal backbone, a trusted loss/data-policy request, or a single-frame mechanism with explicit recall/connectivity support. If it fails contract or smoke testing, repair only the implementation defect while preserving this hypothesis.
