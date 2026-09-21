# ABI-329 temporal-attention strip-token line-mixer U-Net

## Hypothesis

A temporal-attention U-Net with multi-scale horizontal/vertical strip-token line mixers can improve connected true-positive contrail evidence at the fixed 0.5 threshold without repeating the ABI-324/325/326/327/328 C4 tail-reinjection, salience-gate, consensus-guard, or soft-shift repair mechanisms. This is a mechanism-changing temporal-family scout: instead of adding more late positive tails, it lets differentiable line-token features persist through the encoder, bottleneck, and decoder.

## Comparison Target

Primary comparison target: ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator on the temporal-eligible validation population. Secondary context: ABI-323 as a recent temporal-attention logit-consensus continuation, ABI-324 as the best local balanced five-frame temporal C4 comparator, ABI-328 as negative-to-mixed local temporal C4 soft-shift evidence, and ABI-202/ABI-249 as whole-validation aggregate/high-precision references. This Candidate produces capped temporal-eligible feasibility evidence only.

## Expected Effect

The strip-token mixers should increase connected-line continuity and MIT/source balance relative to recent temporal-attention variants while avoiding the broad footprint of positive-tail reinjection. A useful result would show finite non-collapsed predictions, filtered Dice near the temporal-family frontier, connectivity above ABI-323/328 or close to ABI-223, and recall not materially below ABI-223/324.

## Implementation Sketch

`model.py` defines a PyTorch model only. It consumes the provider-advertised `abi_16ch_plus_sza_temporal` tensor for offsets `[-1, 0, 1]`, builds finite normalized ABI, thermal BTD, and Solar Geometry Input features per frame, and applies shared per-pixel temporal attention over previous/center/next frames. The implementation adds a reusable `StripTokenMixer` that combines residual local features, depthwise horizontal strips, depthwise vertical strips, and global context with a learned gate. The mixer is inserted at the encoder stem/down blocks, ASPP context, decoder fusions, and high-resolution refinement.

The output head emits `mask_logits`, `line_logits`, and `centerline_logits`, using only differentiable architecture-internal logit support. There is no threshold selection, morphology, connected-component logic, postprocessing, Artifact Filtering, data loading, temporal lookup, coordinate input, or Candidate-owned loss/metric code.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate code owns only model architecture over provider-supplied tensors.

## Budget Requested

Exploratory default budget: 12 epochs, batch size 2. No `late_improving` budget is requested because this is a mechanism-changing scout of strip-token line mixing rather than a close continuation with prior late-truncation evidence for this exact mechanism.

## Success Criteria

Continue the family only if the Run is finite, non-collapsed, and source-informative, with at least one of: (1) filtered Dice within roughly 0.01 of ABI-223/323 while improving connectivity, (2) MIT filtered Dice or recall above ABI-223 without Google collapse, (3) a compact filtered-positive footprint with recall not materially below ABI-223/324, or (4) a late positive trajectory indicating the exploratory budget may be truncating learning. Low aggregate Dice alone should not eliminate the family if these diagnostics are favorable.

## Fallback/Next Decision

If ABI-329 fails smoke/contract/numerical validation, repair only the candidate bug while preserving this hypothesis. If it completes but under-recovers recall like ABI-327, do not continue with a more compact gate; consider recall-preserving calibration or trusted loss direction. If it is broad and low-connectivity like ABI-325/328, do not add another positive tail; pivot to a different temporal attention/backbone or request diagnostics only if metrics suggest a hidden favorable failure-bucket trade-off.
