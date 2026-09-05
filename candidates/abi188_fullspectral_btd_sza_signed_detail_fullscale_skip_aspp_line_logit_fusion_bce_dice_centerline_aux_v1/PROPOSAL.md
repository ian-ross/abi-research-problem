# ABI-188 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Logit Fusion BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-188 is a controlled continuation of the ABI-183/ABI-184 signed-detail full-scale skip ASPP Line plus Centerline branch. It is not a promotion claim and does not request new Harness capability. It tests one in-contract architecture calibration mechanism after ABI-184's whole-validation diagnostic confirmed strong precision/connectivity but under-recall at the fixed threshold, while ABI-185/186/187 showed that shared recall bridges, mask-only sidecars, and focal-Tversky loss did not preserve the useful ABI-184 operating point.

## Hypothesis

ABI-184 learned connected and precise Line plus Centerline evidence, but its primary mask logits are too conservative at the fixed 0.5 threshold, especially for MIT positives. A small bounded positive residual from the supervised `line_logits` and `centerline_logits` into `mask_logits` may recover recall only where the auxiliary line heads already find thin-contrail support. Detaching the auxiliary logits in this residual should keep mask-loss gradients from corrupting the line/centerline heads, addressing the ABI-185 shared-bridge failure mode. Keeping trusted `bce_dice` should preserve more precision/connectivity than the ABI-187 focal-Tversky loss switch.

## Comparison Target

Primary comparison targets are ABI-183 `run_20260902_204128_bba815` and ABI-184 `run_20260902_213856_2c04ac`. ABI-183 was the 12-epoch Line plus Centerline exploratory parent with capped filtered Dice 0.3966, MIT/Google filtered Dice 0.3805/0.4389, precision 0.4468, recall 0.3565, connectivity 0.4546, and filtered predicted-positive fraction 0.00289. ABI-184 was the late36 Line plus Centerline precision/connectivity reference with capped filtered Dice 0.4066 and whole-validation filtered Dice 0.4093; it improved precision/connectivity but retained a recall deficit. Secondary references are ABI-181 `run_20260902_150611_cbbf35` for aggregate Dice/recall, ABI-185/186 for failed recall-bridge and sidecar attempts, ABI-187 for focal-Tversky recall expansion, ABI-154 for precision/connectivity, and ABI-068 for source-balanced recall/connectivity.

## Expected Effect

A positive capped exploratory result would remain finite and non-collapsed while increasing recall or MIT filtered Dice relative to ABI-183, without losing most of ABI-183/184's precision, connectivity, or positive-area discipline. A stronger result would approach ABI-184 precision/connectivity while moving toward ABI-181 recall. A negative but useful result would show that direct auxiliary-logit fusion either still over-expands positives or remains too conservative, supporting a broader architecture/data-policy frontier rather than more local mask-logit calibration patches.

## Implementation Sketch

- Reuse the ABI-183/184 signed-detail full-scale skip ASPP architecture: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, decoder, full-scale skip fusion, line-aware final refinement, and primary/auxiliary heads.
- Emit `line_logits` and `centerline_logits` exactly as provider-declared auxiliary outputs with trusted `weighted_bce` losses at weights 0.01 and 0.02.
- Compute `mask_logits` as the base mask head plus a bounded positive residual from detached `line_logits` and detached `centerline_logits`: `base_mask_logits + 0.25 * relu(tanh(line_logits.detach())) + 0.10 * relu(tanh(centerline_logits.detach()))`.
- Keep trusted manifest choices otherwise unchanged: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, and disabled early stopping.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `line` with `weighted_bce` weight 0.01, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped exploratory Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, max epochs 12, 3,600 seconds Docker training wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. No late-improving budget, full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if recall or MIT filtered Dice improves over ABI-183 while retaining at least most of ABI-183/184's precision/connectivity and avoiding a large positive-area expansion. Promotion would require later whole-validation diagnostics and human review; this capped Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-188 is finite but fails to improve recall/MIT Dice, or improves recall only by materially reducing precision/connectivity or expanding predicted-positive area, stop this exact auxiliary-logit fusion branch and broaden to a different in-contract architecture, data-policy, loss/auxiliary configuration, calibration, or preprocessing path. If it improves the recall/connectivity tradeoff and selects a late/ambiguous best checkpoint, consider a later `late_improving` continuation under the approved budget-request mechanism. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
