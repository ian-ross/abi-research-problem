# ABI-226 temporal five-frame attention/difference U-Net cache-ready repair

## Hypothesis

ABI-223 showed the strongest capped temporal-family evidence so far: the late36 three-frame temporal-attention model reached `val/filtered_dice` 0.419776 with improved recall, Dataset Source-stratified Dice, and Contrail Connectivity over prior temporal scouts and ABI-218's matched single-frame control. The next in-contract broadening step remains ABI-224's five-frame temporal-attention/difference hypothesis: provider-owned offsets `[-2, -1, 0, 1, 2]` may expose wider persistence/advection evidence that improves thin-line recall and continuity without candidate-owned temporal lookup or postprocessing.

This is a **Repair Candidate / temporal-family broadening scout**, not a promotion candidate against the mature ABI-202 whole-validation frontier. It preserves ABI-224's original hypothesis and comparison target after the original Run failed before training because the then-active provider/cache surface produced zero available MIT samples for the five-frame temporal-eligible selection.

## Comparison Target

The immediate repair target is ABI-224, Candidate `abi224_temporal_fiveframe_attention_difference_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_172818_76b0fc`, which failed before training with Harness classification `candidate_bug` and error text indicating no MIT samples were available for `combined_source_balanced` after `temporal_eligible_center` selection. ABI-225 (`run_20260908_173400_4a5aa7`) then failed similarly under `google_only`.

The scientific temporal comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), the current capped temporal-family frontier, with best epoch 36 filtered Dice 0.419776, raw Dice 0.438487, filtered precision 0.483764, filtered recall 0.370738, MIT filtered Dice 0.398498, Google filtered Dice 0.476764, and filtered connectivity 0.412427. Additional context includes ABI-222, ABI-219/220/221, and ABI-218 as the temporal-eligible single-frame matched control. ABI-202 remains the mature single-frame frontier context only.

## Expected Effect

With the trusted five-frame temporal eligibility/cache issue addressed, the same source-balanced five-frame scout should now pass data-loader construction and produce finite resource/metric evidence. If the wider provider-owned window carries useful persistence or motion/change cues, it should improve or approach ABI-223's filtered Dice while strengthening filtered recall, MIT/Google Dice, or Contrail Connectivity without excessive predicted-positive expansion. Even if the first scout trails ABI-223, a finite noncollapsed trajectory will determine whether five-frame temporal modeling is resource-safe and worth bounded family development.

## Implementation Sketch

Reuse ABI-224's architecture-only implementation. The model reshapes the provider tensor into five ascending 17-channel ABI+SZA frames, builds bounded normalized ABI channels, ABI-derived thermal BTD planes, and SZA features for each frame, then applies shared frame projection. A per-pixel temporal-attention module scores each frame relative to the center-frame embedding. The decoder input fuses the attention-weighted temporal embedding, the center embedding, and bounded near/far temporal-difference features: center minus near-neighbor mean, center minus far-neighbor mean, near-span and far-span signed changes, and absolute center-neighbor differences for both near and far offsets. A compact U-Net/ASPP decoder predicts `mask_logits`, `line_logits`, and `centerline_logits`.

The only intentional repair differences from ABI-224 are the new Candidate identity and structured repair lineage in the manifest. Candidate code does not implement any temporal cache repair; it relies solely on the trusted provider-owned temporal mode and refreshed eligibility/cache state.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`, an allowlisted temporal window.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.
- Repair lineage preserving ABI-224's original hypothesis and comparison target.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, cache access, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings. No `late_improving` budget is requested because this is still a five-frame resource/metric scout whose prior attempts did not train. Run sequentially under the Harness concurrency cap.

## Success Criteria

ABI-226 succeeds as a repair if it passes static validation and reaches training with nonzero provider-selected five-frame temporal-eligible samples from both Dataset Sources. It is useful five-frame temporal-family evidence if it completes finitely within resource limits and either approaches ABI-223 within about 0.02 filtered Dice while improving filtered recall, MIT Dice, Google Dice, or connectivity, or clearly exceeds ABI-222/219/220 and ABI-218 under the same capped temporal-eligible policy. A lower finite score can still be useful if the trajectory is source-informative and noncollapsed, because it profiles the wider temporal window.

## Fallback/Next Decision

If ABI-226 again fails before training with zero temporal-eligible samples despite the trusted profile's nonzero selected counts, classify it as a Harness/provider/data-surface inconsistency rather than continuing candidate rewrites, and create a focused Capability Request or Campaign Report in a later Autonomy Step. If it fails from a narrow candidate implementation bug, use at most one additional repair only if it preserves the five-frame hypothesis. If it completes but underperforms ABI-223 while remaining above ABI-218, continue five-frame family development only when the learning trajectory or source-stratified metrics identify a specific repairable weakness. If it collapses, is non-finite after repair, or loses the matched-control temporal margin, stop this exact five-frame attention/difference branch and broaden to another underexplored architecture family.
