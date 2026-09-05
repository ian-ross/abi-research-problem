# ABI-183 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-183 is a controlled auxiliary-supervision continuation of the ABI-181 signed-detail full-scale skip ASPP branch. It is not a promotion claim and not a new execution-policy request; it tests one provider-allowlisted mechanism for improving line continuity and MIT/source behavior after ABI-182 showed that the conservative line-consensus late-budget branch raised recall but weakened connectivity.

## Hypothesis

ABI-181 is the current capped aggregate reference, but its selected checkpoint still trails the stronger connectivity behavior of ABI-154 and ABI-068. A low-weight provider-derived Line Target auxiliary head should supply broader line-mask supervision than Centerline Target alone, encouraging continuous thin contrail support while the primary BCE-Dice mask objective preserves ABI-181 overlap and fixed-threshold calibration. Because ABI-180 showed only small gains from line supervision when combined with a weaker UPerNet decoder, the useful test is whether the same trusted Line Target helps the stronger signed-detail full-scale skip ASPP decoder when all other manifest choices are held fixed.

## Comparison Target

The primary comparison target is ABI-181 `run_20260902_150611_cbbf35`: late36 best epoch 22, capped filtered Dice 0.4104, MIT/Google filtered Dice 0.3962/0.4486, filtered precision 0.4423, recall 0.3828, connectivity 0.3639, and filtered predicted-positive fraction 0.00314. Secondary references are ABI-182 `run_20260902_175152_51d2d9` for the line-consensus late-budget tradeoff, ABI-154 `run_20260901_071026_32d3ec` for precision/connectivity, ABI-068 `run_20260828_010836_4ccc77` for source-balanced recall/connectivity, and ABI-180 `run_20260902_063801_88ca01` as prior Line+Centerline auxiliary evidence in a different decoder family.

## Expected Effect

A positive outcome would remain finite and non-collapsed while improving filtered connectivity and/or MIT filtered Dice relative to a comparable 12-epoch signed-detail ASPP reference, without materially expanding filtered predicted-positive fraction or eroding ABI-181-style precision. A stronger outcome would approach ABI-181 aggregate/source filtered Dice despite using only the default exploratory budget, indicating that low-weight Line Target supervision is a better continuity mechanism than the ABI-174/182 line-consensus calibration branch. A negative but useful outcome would show that Line Target supervision mainly shifts the operating point toward lower precision or weaker source metrics, supporting a broader architecture/data-policy frontier rather than more local auxiliary-head variants.

## Implementation Sketch

- Reuse ABI-181 approved-channel feature path: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, and primary `mask_logits`.
- Add one `line_logits` 1x1 auxiliary head from the same refined features used by the mask and centerline heads.
- Keep the existing `centerline_logits` head and provider-derived Centerline Target auxiliary supervision at weight 0.02.
- Select provider-derived Line Target auxiliary supervision with trusted `weighted_bce` at weight 0.01.
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
6. Family-development success is met if connectivity or MIT filtered Dice improves over nearby signed-detail ASPP/default-budget references without severe precision, aggregate Dice, or positive-area regression. Promotion would require later whole-validation diagnostics and human review; this capped Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-183 is finite but lower on aggregate/source metrics or expands predicted-positive area without a clear connectivity/MIT gain, stop this local Line+Centerline auxiliary continuation and broaden to a different in-contract architecture, data policy, loss, calibration, or preprocessing path. If it improves connectivity or MIT balance while remaining close to ABI-181 aggregate behavior, consider a later late-improving continuation or whole-validation Evaluation Request depending on trajectory and best-epoch timing. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
