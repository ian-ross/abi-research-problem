# ABI-291 five-frame temporal persistence-attention directional U-Net

## Hypothesis

ABI-223/238 showed that provider-owned three-frame temporal attention can be a strong temporal-family comparator, while recent ABI-286 through ABI-290 continuity/recall heads often moved along an unstable precision-recall curve instead of forming cleaner connected evidence. A five-frame temporal window may let the model distinguish persistent thin contrail evidence from one-frame cloud-edge clutter using architecture-internal persistence attention and bounded change features, without candidate-owned temporal lookup, thresholds, losses, metrics, Artifact Filters, or postprocessing. This is a mechanism-changing temporal family-development scout, not a promotion candidate.

## Comparison Target

The primary comparison targets are ABI-238 (`run_20260911_004137_f54c45`) and ABI-223 (`run_20260908_154531_8c7e2b`) on the temporal-eligible capped validation population. ABI-238 reached capped best `val/filtered_dice` 0.420235 with precision 0.488730, recall 0.368578, MIT filtered Dice 0.405383, Google filtered Dice 0.460838, and connectivity 0.352239. ABI-223 reached 0.419776 filtered Dice with precision 0.483764, recall 0.370738, MIT 0.398498, Google 0.476764, and stronger connectivity 0.412427. ABI-285/286/287/290 provide recent C4/continuity context, and ABI-202 remains the aggregate whole-validation reference but is not the direct temporal-window scout target.

## Expected Effect

The expected effect is not an immediate mature-frontier win. Useful evidence would be a finite, resource-safe Run showing that five-frame persistence improves recall or connected-line continuity at similar compactness compared with the three-frame temporal-attention branch, or showing that longer provider-owned temporal context adds clutter/instability and should not receive more budget. A successful scout would preserve source-informative MIT/Google behavior, avoid persistent prediction collapse, and preferably move toward ABI-223/238 Dice while improving at least one of filtered recall or Contrail Connectivity Metric.

## Implementation Sketch

Start from the finite ABI-238 compact temporal-attention directional U-Net. The model consumes only the provider-advertised `abi_16ch_plus_sza_temporal` tensor with offsets `[-2, -1, 0, 1, 2]`, reshapes the channel-stacked tensor into five 17-channel frames, and builds bounded per-frame ABI/SZA/BTD features from candidate-visible channels only. A shared per-frame projection feeds per-pixel temporal attention over all five frames around the center frame. The stem adds persistence/change features: center minus near-neighbor mean, center minus outer-neighbor mean, center minus all-neighbor mean, immediate before/after difference, outer before/after difference, and absolute center-to-neighbor residual. The rest of the network keeps the compact U-Net encoder, ASPP bottleneck, decoder skips, and high-resolution directional-context bridge before `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`, an allowlisted trusted temporal window.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, and `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, S3/NetCDF access, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the default exploratory budget only: 12 epochs, current trusted sample ceiling, batch size 2, constant learning rate 0.0003, disabled early stopping, and Harness-owned resource/timeout policy. The five-frame input has a materially different activation profile from the three-frame parent branch, so it should run sequentially as a scout before any late-improving budget is considered.

## Success Criteria

Treat ABI-291 as useful if it completes finitely under the default budget and either approaches the ABI-223/238 temporal comparator band while improving recall or connectivity, improves over recent ABI-288/289/290 temporal mechanism tests without widening the predicted-positive footprint excessively, or shows a late/ambiguous improving trajectory that justifies one close continuation. Strong evidence would include filtered Dice near or above 0.40, source-balanced MIT/Google behavior, non-degenerate predicted-positive fractions, and better connectivity than ABI-238 or recall above ABI-223 at tolerable precision. Low score alone should not eliminate five-frame temporal modeling if the trajectory is finite and improving, but collapse, non-finite behavior, clear instability, or severe source imbalance would stop this exact branch.

## Fallback/Next Decision

If ABI-291 fails static validation or smoke testing due to Candidate code, create at most one narrow repair preserving this five-frame persistence hypothesis. If it completes with collapsed predictions, non-finite state, severe clutter, or a clearly poor trajectory, stop the five-frame extension of ABI-238 and pivot to a different architecture family or a trusted diagnostic request if failure buckets are needed. If it completes with finite source-informative learning and late improvement, consider a mechanism-preserving late-improving continuation only if Harness evidence supports the approved budget criteria.
