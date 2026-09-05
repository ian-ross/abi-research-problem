# ABI-190 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Feature Calibration BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-190 is a controlled exploratory continuation within the signed-detail full-scale skip ASPP family. It is not a promotion claim and not a late-budget request. It follows the ABI-184 whole-validation lesson: direct Line plus Centerline auxiliary supervision gives clean, connected predictions but misses too many positive patches, while ABI-189 showed that detached auxiliary-logit boosting buys recall by weakening precision and connectivity.

## Hypothesis

A conservative feature-level line-context calibration path before the primary mask head can recover some of ABI-184's missing recall without the positive-area expansion and connectivity loss seen in ABI-188/189 detached logit fusion. Keeping `line_logits` and `centerline_logits` as direct provider-derived auxiliary outputs while using a zero-initialized bounded residual in feature space should let the trusted BCE-Dice mask objective learn softer foreground support only where line-context features are useful, rather than adding auxiliary logits directly to `mask_logits`.

## Comparison Target

The primary comparison target is ABI-184 `run_20260902_213856_2c04ac`, the late36 Line plus Centerline auxiliary precision/connectivity reference: capped filtered Dice 0.4066, MIT/Google filtered Dice 0.3879/0.4555, filtered precision 0.4850, recall 0.3500, connectivity 0.4634, and filtered predicted-positive fraction 0.00261; whole-validation filtered Dice 0.4093 with precision 0.4893, recall 0.3517, connectivity 0.4763, and strong negative-patch discipline.

Secondary references are ABI-181 `run_20260902_150611_cbbf35`, the whole-validation aggregate reference with filtered Dice 0.4124, recall 0.3832, and connectivity 0.3676; ABI-189 `run_20260903_041610_f244a9`, the detached line-logit fusion late36 negative-to-mixed reference with capped filtered Dice 0.4022, recall 0.4083, precision 0.3964, and connectivity 0.2962; ABI-183 `run_20260902_204128_bba815`, the exploratory Line plus Centerline parent; and ABI-068 `run_20260828_010836_4ccc77`, the broader line-U-Net source-balance/connectivity comparator.

## Expected Effect

A positive result would remain finite and non-collapsed while improving ABI-184 recall or MIT filtered Dice without materially sacrificing ABI-184's precision, Google filtered Dice, connectivity, or small predicted-positive fraction. The strongest outcome would move toward ABI-181 aggregate/recall while retaining materially better connectivity and negative-patch discipline. A useful negative result would show that even zero-initialized feature-level line calibration cannot soften ABI-184 without the same precision/connectivity tradeoff as logit fusion, motivating a broader architecture-family scout or data/loss-policy probe rather than another local calibration variant.

## Implementation Sketch

- Reuse the ABI-184 signed-detail full-scale skip ASPP architecture: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, and primary/auxiliary heads.
- Preserve direct `line_logits` and `centerline_logits` auxiliary outputs with provider-derived Line and Centerline targets using trusted `weighted_bce` losses at weights 0.01 and 0.02.
- Add `ConservativeLineFeatureCalibration` between the shared refined features and `mask_head`. The module builds local-detail, horizontal, vertical, and broad-context feature branches, gates the learned line context, and applies a zero-initialized `1x1` residual projection bounded by `tanh` with scale 0.25.
- Do not add auxiliary logits directly to `mask_logits`; the mask head consumes calibrated features, while auxiliary heads continue to consume the pre-calibration refined features.
- Keep trusted manifest choices unchanged from ABI-184 except for no late-budget request: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning rate, and disabled early stopping.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `line` with `weighted_bce` weight 0.01, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped exploratory Run: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, max epochs 12, 3,600 seconds Docker training wall-clock budget when enforced, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. No `late_improving` budget is requested for this first feature-calibration variant, and no full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if ABI-190 improves ABI-184 recall, MIT filtered Dice, or aggregate filtered Dice while retaining most of ABI-184's precision/connectivity advantage; a smaller positive signal is also useful if the best epoch is late and non-collapsed, making it eligible for a later `late_improving` request.
7. Promotion would require later whole-validation diagnostics and human review; this capped exploratory Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-190 improves recall or MIT overlap without large precision/connectivity loss, consider either a late-improving continuation if the selected checkpoint is near epoch 12, or a later whole-validation Evaluation Request if capped evidence is strong enough and resource behavior is clean. If it expands positive area or loses ABI-184's connectivity like ABI-189, stop this feature-calibration branch and broaden to a new high-resolution line-aware architecture, data-policy comparison, or provider-allowlisted loss/auxiliary configuration. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
