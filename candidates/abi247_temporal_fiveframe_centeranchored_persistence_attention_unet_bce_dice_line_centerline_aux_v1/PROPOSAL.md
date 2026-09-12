# ABI-247 five-frame center-anchored persistence-attention U-Net

## Hypothesis

ABI-223 showed that provider-owned three-frame temporal attention is the strongest temporal branch so far, reaching capped filtered Dice 0.419776 at epoch 36 with strong precision, Google Dice, and connectivity. ABI-226 and ABI-230 proved that the allowlisted five-frame window `[-2, -1, 0, 1, 2]` is resource-feasible, but their wider temporal fusion diluted line continuity and peaked before the exploratory ceiling. ABI-247 tests a materially different five-frame scout: keep ABI-223's compact U-Net decoder and simple mask head, but replace the three-frame stem with a center-anchored five-frame persistence-attention stem that gives the target frame an explicit architectural prior while adding near/far change and persistence features.

This is a sequential family scout / family-development bridge, not a promotion candidate. The goal is to determine whether the wider trusted temporal window can improve same-budget recall and source balance without the connectivity collapse observed in earlier five-frame and line-memory branches.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-223 (`run_20260908_154531_8c7e2b`), late36 temporal-attention frontier: filtered Dice 0.419776, precision 0.483764, recall 0.370738, MIT filtered Dice 0.398498, Google filtered Dice 0.476764, connectivity 0.412427.
- ABI-226 (`run_20260910_120441_916a03`), five-frame attention/difference scout: filtered Dice 0.378604, precision 0.428061, recall 0.339391, MIT filtered Dice 0.366586, Google filtered Dice 0.409886, connectivity 0.224851.
- ABI-222 (`run_20260908_150315_9aea3f`), three-frame ABI-223 exploratory parent: filtered Dice 0.374329 and connectivity 0.281396.

Recent negative/mixed context includes ABI-230 five-frame window attention, ABI-241 high-resolution change skip, ABI-244 shifted-window U-NetFormer, ABI-245 global line memory, and ABI-246 dual-logit consensus. ABI-202 remains the mature single-frame whole-validation-tested frontier context only.

## Expected Effect

Center anchoring should reduce the failure mode where far temporal frames dilute the zero-offset Contrail Mask evidence. Near/far persistence and change features should still expose whether thin line evidence persists, advects, or changes across the five provider-supplied frames. A useful result would improve over ABI-226 and ABI-222 on filtered Dice or recall while preserving materially better connectivity than ABI-226/230 and avoiding a large predicted-positive expansion.

## Implementation Sketch

Start from the ABI-223 architecture and make one material change in the temporal stem:

- consume provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`;
- build the same finite per-frame ABI+SZA+BTD features as ABI-223, with no candidate-owned loading or temporal lookup;
- project all five frames through a shared compact residual frame encoder;
- compute per-pixel attention logits against the center frame, with a small fixed center-bias prior before softmax;
- form explicit near/far mean, short/long temporal-difference, and center-to-neighbor absolute-change features;
- fuse attended temporal evidence back through a learned center gate so the final stem remains anchored to the target frame;
- keep ABI-223's encoder, ASPP context, decoder, simple mask head, and trusted Line/Centerline auxiliary outputs.

The fixed center-bias and change features are architecture-internal tensor operations over provider-visible channels only. They are not sample selection, thresholding, postprocessing, morphology, Artifact Filtering, target derivation, or an auxiliary loss.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, learning rate 0.0003, batch size 2, `scheduler.policy: constant_lr`, exploratory `max_epochs: 12`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, capped temporal-eligible source-balanced samples, and the current Harness-owned resource limits. No `late_improving` budget is requested for this first center-anchored five-frame formulation.

## Success Criteria

ABI-247 is useful if it completes finitely within resource limits and exceeds ABI-226's five-frame scout on filtered Dice by at least about 0.005 while also improving either filtered connectivity, MIT filtered Dice, or recall without a large filtered predicted-positive expansion. A stronger result would approach ABI-222/223 connectivity while retaining five-frame recall. If the selected checkpoint is at epoch 12 with noncollapsed source-informative metrics and a positive trajectory, it may justify a later approved late-improving continuation.

## Fallback/Next Decision

If ABI-247 fails contract, smoke, shape, finite-state, or resource validation due to Candidate code, create at most one narrow repair preserving the center-anchored five-frame persistence-attention hypothesis. If it completes but underperforms ABI-226, collapses connectivity below prior five-frame scouts, or peaks early then regresses, stop this exact five-frame stem and broaden to a different temporal mechanism or a non-temporal rotation-aware/modern-backbone scout. Do not request whole-validation diagnostics from capped evidence alone.
