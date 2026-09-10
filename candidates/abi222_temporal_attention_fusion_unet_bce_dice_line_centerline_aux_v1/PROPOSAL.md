# ABI-222 temporal-attention fusion U-Net

## Hypothesis

A lightweight temporal-attention fusion block over provider-owned `[-1, 0, 1]` ABI+SZA frames can preserve ABI-219/220's matched-control temporal benefit while improving the temporal branch's precision/recall and line-connectivity balance without the memory/time cost of ABI-221's ConvGRU state. This is a temporal-family broadening scout/continuation, not a promotion candidate against the mature ABI-202 frontier.

## Comparison Target

Primary temporal comparison targets are ABI-219 (`run_20260908_130608_80d612`, best capped `val/filtered_dice` 0.367589) and ABI-220 (`run_20260908_134203_8bbb6f`, best capped `val/filtered_dice` 0.368730). ABI-221 (`run_20260908_142018_0ea94f`) is the recurrent temporal-state comparison because it improved precision/connectivity but regressed primary Dice and recall at higher resource cost. ABI-218 (`run_20260908_123030_05ad37`, best capped `val/filtered_dice` 0.345570) remains the matched temporal-eligible single-frame control. ABI-202 remains current mature whole-validation frontier context only.

## Expected Effect

Temporal attention should let the model reweight previous, center, and next frame features per pixel instead of using fixed difference algebra or recurrent hidden state. The expected useful signal is a small but meaningful improvement over ABI-219/220 on capped filtered Dice or an interpretable tradeoff: retaining ABI-219/220 recall while approaching ABI-221 connectivity/precision at lower resource cost. A successful attention scout should remain clearly above ABI-218's single-frame control on filtered Dice, recall, source-stratified Dice, and connectivity.

## Implementation Sketch

Consume only the provider-advertised `abi_16ch_plus_sza_temporal` tensor with offsets `[-1, 0, 1]`. Reshape the channel-stacked tensor into three ABI+SZA frames inside the model. For each frame, build bounded finite ABI channel, fixed ABI-channel-derived BTD, scaled SZA, and SZA-cosine features using the same architecture-owned normalization style as ABI-219/220/221. Project each frame through a shared compact feature projector, compute per-pixel temporal-attention logits from `(frame, center, abs(frame-center))`, softmax across the three frames, and fuse the attention-weighted frame embedding with bounded signed/absolute change embeddings. Feed the fused feature map into the same compact single-stream U-Net/ASPP decoder with `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and current Harness-owned sample/resource ceilings. No `late_improving` budget is requested because ABI-219/220/221 showed oscillating rather than clearly truncated late trajectories.

## Success Criteria

Treat ABI-222 as successful temporal-family evidence if it completes finite within resource limits and either exceeds ABI-220's capped best `val/filtered_dice` by at least about 0.005, or preserves a clear margin over ABI-218 while improving at least two of filtered recall, filtered connectivity, MIT filtered Dice, and Google filtered Dice versus ABI-219/220 without a material precision collapse. A secondary success is a resource profile close to ABI-219/220 and substantially cheaper than ABI-221 while producing comparable or better connectivity.

## Fallback/Next Decision

If ABI-222 fails contract, smoke, or finite-state validation, create at most one narrow Repair Candidate that preserves this attention-fusion hypothesis. If it completes but does not beat ABI-219/220 and offers no useful secondary tradeoff over ABI-218, stop close three-frame temporal-fusion tuning and broaden to a five-frame temporal-difference scout using the allowlisted `[-2, -1, 0, 1, 2]` window, or write a Research Note summarizing why temporal development should shift to a different architecture family. Do not request whole-validation diagnostics or late-improving budget unless the capped Result is strong, source-informative, noncollapsed, and diagnostically warrants it.
