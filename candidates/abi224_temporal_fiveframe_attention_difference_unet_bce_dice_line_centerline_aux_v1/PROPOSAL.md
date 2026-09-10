# ABI-224 temporal five-frame attention/difference U-Net scout

## Hypothesis

ABI-223 showed the clearest capped evidence so far that provider-owned temporal context helps beyond temporal-eligible population effects: the late36 three-frame temporal-attention model reached `val/filtered_dice` 0.419776, with stronger recall, source Dice, and connectivity than ABI-222 and a large margin over ABI-218's matched single-frame control. Because ABI-223's best checkpoint landed at the current 36-epoch ceiling and the exact three-frame continuation budget is exhausted, the next useful in-contract test is not another longer run but a changed temporal input window. A five-frame temporal-attention/difference scout can test whether wider persistence/advection evidence from offsets `[-2, -1, 0, 1, 2]` improves thin-line recall and connectivity while retaining ABI-223's compact attention calibration.

This is a **family scout / temporal-family broadening step**, not a promotion candidate against the mature ABI-202 whole-validation frontier.

## Comparison Target

The primary temporal comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), the current capped temporal-family frontier, with best epoch 36 filtered Dice 0.419776, raw Dice 0.438487, filtered precision 0.483764, filtered recall 0.370738, MIT filtered Dice 0.398498, Google filtered Dice 0.476764, and filtered connectivity 0.412427. Additional temporal controls are ABI-222 (`run_20260908_150315_9aea3f`, three-frame attention 12ep, filtered Dice 0.374329), ABI-219/220 temporal-difference/change gates, ABI-221 ConvGRU, and ABI-218 (`run_20260908_123030_05ad37`) as the temporal-eligible single-frame control. ABI-202 (`run_20260904_043143_ee0005`) remains the mature single-frame frontier context only.

## Expected Effect

The wider provider-owned temporal window should expose persistence and advective change over a longer neighborhood. If contrail evidence persists coherently across five frames while static geography, scan-edge clutter, and transient cloud edges do not, the architecture should improve filtered recall and/or Contrail Connectivity Metric without expanding predicted-positive fraction into an all-positive or low-precision regime. Useful evidence also includes showing whether five-frame temporal input is resource-safe under the current batch-size and wall-clock limits, even if the first scout does not beat the well-trained ABI-223 late36 Result.

## Implementation Sketch

Start from ABI-223's finite temporal-attention U-Net pattern but change the temporal contract to five channel-stacked ABI+SZA frames. The candidate reshapes the provider tensor into five 17-channel frames in ascending offset order, builds bounded normalized ABI channels, ABI-derived thermal BTD planes, and SZA features for each frame, and projects frames with shared weights. A per-pixel attention module scores each frame relative to the center-frame embedding. The decoder input fuses the attention-weighted temporal embedding, the center embedding, and bounded temporal-difference features: center minus near-neighbor mean, center minus far-neighbor mean, near-span and far-span signed changes, and absolute center-neighbor differences for both near and far offsets. A compact single-stream U-Net/ASPP decoder then predicts `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]` from the allowlisted temporal windows.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings. No `late_improving` budget is requested because this is a changed five-frame family scout with unprofiled temporal input/resource behavior. Run sequentially.

## Success Criteria

Treat ABI-224 as successful five-frame temporal-family evidence if it completes finitely within resource limits and either approaches ABI-223 within about 0.02 filtered Dice while improving filtered recall, MIT filtered Dice, Google filtered Dice, or connectivity, or clearly exceeds ABI-222/219/220 and ABI-218 under the same capped temporal-eligible population. A lower score can still be useful if it provides finite/resource evidence and source-informative noncollapsed trajectory for the five-frame branch.

## Fallback/Next Decision

If ABI-224 fails due to Candidate code, create at most one narrow repair preserving the five-frame temporal-attention/difference hypothesis. If it is resource-heavy or wall-clock limited, compact the stem/decoder before making metric claims. If it completes finitely but underperforms ABI-223 while remaining above the ABI-218 control, continue with bounded five-frame family development only when the trajectory or source-stratified metrics identify a specific repairable weakness. If it collapses, is non-finite after repair, or loses the matched-control temporal margin, stop this exact five-frame attention/difference branch and broaden to another underexplored architecture family rather than requesting more epochs.
