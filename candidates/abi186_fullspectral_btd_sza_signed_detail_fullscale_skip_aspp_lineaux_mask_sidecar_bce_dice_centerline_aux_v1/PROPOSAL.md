# ABI-186 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux Mask-Sidecar BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-186 is a close exploratory continuation of the signed-detail full-scale skip ASPP Line plus Centerline auxiliary branch. It is not a promotion claim. It changes ABI-184/185 only by replacing ABI-185's shared pre-logit recall bridge with a separate neutral additive mask-logit sidecar that does not feed the Line or Centerline auxiliary heads.

## Hypothesis

ABI-184 showed that direct low-weight Line Target supervision can produce the best recent whole-validation precision/connectivity and negative-patch discipline, but its default-threshold recall and MIT positive-patch recall trail ABI-181. ABI-185 attempted to recover recall with a shared feature-level recall bridge, but it reduced aggregate/source filtered Dice and damaged connectivity, suggesting that shared residual calibration perturbs the line-connected representation.

A less disruptive in-contract mechanism should preserve the line-supervised decoder path while giving the primary mask head a small learned calibration sidecar. A neutral-initialized additive `MaskRecallSidecar`, attached only to `mask_logits`, should be able to raise fixed-threshold recall or MIT positive overlap without forcing the Line and Centerline auxiliary heads to share the same residual bridge.

## Comparison Target

The primary comparison target is ABI-185 `run_20260903_002344_daa8ef`: exploratory best epoch 12, capped filtered Dice 0.3927, MIT/Google filtered Dice 0.3810/0.4228, precision 0.4511, recall 0.3477, connectivity 0.3433, and filtered predicted-positive fraction 0.00279. ABI-185 is the direct negative shared-bridge reference.

The line-connected target is ABI-184 `run_20260902_213856_2c04ac`: late36 best epoch 23, capped filtered Dice 0.4066, MIT/Google filtered Dice 0.3879/0.4555, precision 0.4850, recall 0.3500, connectivity 0.4634, and whole-validation filtered Dice 0.4093. The aggregate reference is ABI-181 `run_20260902_150611_cbbf35`: late36 best epoch 22, capped filtered Dice 0.4104, MIT/Google filtered Dice 0.3962/0.4486, precision 0.4423, recall 0.3828, connectivity 0.3639, and whole-validation filtered Dice 0.4124.

## Expected Effect

A positive outcome would remain finite and non-collapsed, beat ABI-185 on aggregate/source filtered Dice and connectivity, and recover some recall or MIT filtered Dice relative to ABI-184 without materially increasing false-positive-prone predicted-positive area. The strongest outcome would approach ABI-184's precision/connectivity while improving ABI-184 recall, making a separate mask-only calibration sidecar a better continuation point than ABI-185's shared bridge. A negative but useful outcome would show that this signed-detail Line plus Centerline branch cannot recover recall through low-capacity additive mask calibration at the 12-epoch exploratory budget.

## Implementation Sketch

- Reuse ABI-184's architecture and manifest choices: provider-approved `abi_16ch_plus_sza`, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input, learned spectral projection, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, `line_logits`, and `centerline_logits`.
- Add `MaskRecallSidecar`, a small neutral-initialized branch that consumes the final refined mask features plus full-scale skip-fusion features and adds a bounded learned residual only to `mask_logits`.
- Keep Line and Centerline auxiliary outputs attached to the original refined features, not to the sidecar, to preserve the line-connected representation.
- Keep trusted manifest choices: `bce_dice`, `combined_source_balanced`, `random_mirroring`, Line Target auxiliary `weighted_bce` weight 0.01, Centerline Target auxiliary `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, and disabled early stopping.
- Do not include a late-improving budget request on this first mask-sidecar scout; treat it as exploratory evidence.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, Line Target auxiliary with `weighted_bce` weight 0.01, Centerline Target auxiliary with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, and constant learning-rate policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential exploratory capped Run under the active generated Workspace Configuration: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, 3,600-second Docker training wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if ABI-186 beats ABI-185 on filtered Dice and connectivity while improving ABI-184 recall or MIT filtered Dice without a large precision or predicted-positive-fraction regression. A late36 continuation would require a selected best checkpoint near epoch 12 plus finite, non-collapsed, source-informative metrics; it is not requested in this step.

## Fallback/Next Decision

If ABI-186 improves recall or MIT overlap while recovering ABI-184-like connectivity, consider a later whole-validation Evaluation Request or late-improving continuation depending on trajectory and budget-policy evidence. If it improves recall only by losing precision/connectivity or expanding clutter, retain ABI-184 as the precision/connectivity reference and broaden to a different in-contract calibration or data-policy mechanism. If it trails ABI-185 or fails to improve the shared-bridge negative result, stop this exact mask-sidecar branch rather than repeating it unchanged. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
