# ABI-246 temporal-attention dual-logit consensus U-Net

## Hypothesis

ABI-223 showed that the provider-owned three-frame temporal-attention U-Net can become competitive under late training, with strong precision, Google Dice, and connectivity, but it still trails ABI-202 on recall, MIT Dice, and overall capped filtered Dice. Several later temporal continuity modules (ABI-238 through ABI-245) either preserved overlap while losing connectivity or increased positive area without improving the selected checkpoint. ABI-246 tests a smaller, calibration-oriented continuation: keep ABI-223's temporal-attention encoder/decoder unchanged and replace only the final mask head with a learned dual-logit consensus head that exposes a conservative path and a recall-oriented dilated path to the final `mask_logits` fusion.

This is a sequential family-development continuation, not a promotion candidate and not a request for a longer budget. The goal is to determine whether a mask-head-level consensus mechanism can improve the precision/recall balance without the post-decoder continuity regressions seen in ABI-238/240/244/245.

## Comparison Target

The primary comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), the current capped temporal-family frontier: best epoch 36, filtered Dice 0.419776, precision 0.483764, recall 0.370738, MIT filtered Dice 0.398498, Google filtered Dice 0.476764, connectivity 0.412427, and filtered predicted-positive fraction 0.003962. Because ABI-246 runs only the exploratory 12-epoch budget, it should also be compared to ABI-222 (`run_20260908_150315_9aea3f`), the same ABI-223 architecture before the late budget, with 12-epoch filtered Dice 0.374329 and connectivity 0.281396.

Recent negative/mixed temporal context includes ABI-238 (`run_20260911_004137_f54c45`, filtered Dice 0.420235 but lower connectivity 0.352239), ABI-240 (`run_20260911_031326_43ed12`, filtered Dice 0.414892 and high recall but connectivity 0.264863), ABI-244 (`run_20260911_072719_ade068`, exploratory filtered Dice 0.392808 and connectivity 0.290859), and ABI-245 (`run_20260911_081827_1c0932`, filtered Dice 0.380155 and connectivity 0.239968). ABI-202 remains the mature whole-validation-tested single-frame frontier context only.

## Expected Effect

The expected effect is a modest improvement over ABI-222-like early temporal-attention behavior, not an immediate displacement of ABI-223 late36 or ABI-202. By splitting the final mask decision into conservative and recall-oriented logits and learning a per-pixel consensus gate from their agreement, ABI-246 may preserve compact high-precision evidence while allowing faint center-frame/temporal-recall evidence through when the two internal paths agree. A useful result would improve exploratory filtered Dice, recall, or MIT filtered Dice relative to ABI-222 without a large predicted-positive expansion or connectivity collapse.

## Implementation Sketch

Reuse ABI-223's architecture through the temporal feature builder, temporal attention stem, encoder, ASPP bottleneck, decoder, and trusted Line/Centerline auxiliary heads. Replace only the single 1x1 `mask_head` with `DualLogitConsensusHead`:

- a shared residual projection over the final refined full-resolution features;
- a conservative local branch using standard 3x3 residual features;
- a recall-oriented branch using a dilated 3x3 projection;
- internal conservative and recall logits;
- an agreement signal computed from the two internal sigmoid logits;
- a learned consensus gate and final 1x1 fusion that returns exactly one `mask_logits` tensor.

The internal logits are architecture features only. They are not extra outputs, losses, thresholds, postprocessing, or Artifact Filters. The Candidate still emits only `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, learning rate 0.0003, batch size 2, `scheduler.policy: constant_lr`, and exploratory `max_epochs: 12`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping under Harness-owned policy, and the current capped temporal-eligible sample/resource limits. No `late_improving` budget is requested for this first dual-logit consensus head scout.

## Success Criteria

ABI-246 is useful if it completes finitely within resource limits and, at the selected exploratory checkpoint, either exceeds ABI-222's filtered Dice by at least about 0.005 or preserves ABI-222-level filtered Dice while improving at least two of filtered recall, MIT filtered Dice, connectivity, or predicted-positive stability. It should avoid the main failure mode of ABI-240/244/245: higher recall or overlap paired with a large connectivity drop and expanded positive fraction. A strong exploratory trajectory with the best checkpoint at epoch 12 would justify considering a later `late_improving` close continuation.

## Fallback/Next Decision

If ABI-246 fails contract, smoke, shape, finite-state, or resource validation due to Candidate code, create at most one narrow repair preserving the dual-logit consensus-head hypothesis. If it completes but underperforms ABI-222, collapses connectivity, or peaks early then regresses, stop this exact head formulation and broaden away from temporal head tweaks. If it is finite, source-informative, noncollapsed, and best at the exploratory ceiling, consider one approved late-improving continuation; otherwise do not request whole-validation diagnostics from capped evidence alone.
