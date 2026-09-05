# ABI-184 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux Late36 BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-184 is a close late-improving continuation of ABI-183, not a new architecture family and not a promotion claim. It preserves the ABI-183 signed-detail full-scale skip ASPP architecture with trusted Line plus Centerline auxiliary supervision, and changes only the Harness-reviewed budget request path to test whether ABI-183's final-epoch improvement was truncated by the exploratory ceiling.

## Hypothesis

ABI-183 showed that low-weight provider-derived Line Target supervision can recover strong connected-line behavior in the signed-detail full-scale skip ASPP branch: its exploratory best checkpoint reached filtered connectivity 0.4546 with filtered Dice 0.3966 and restrained filtered predicted-positive fraction 0.00289. However, ABI-183 selected epoch 12, the final exploratory epoch, after a late jump from epoch 11 to 12 and still trailed ABI-181's late36 aggregate/source filtered Dice. A 36-epoch trusted late-improving continuation should determine whether the same direct line-supervised branch can recover ABI-181-like aggregate and source overlap while preserving ABI-183's connectivity and positive-area discipline, without any Candidate-owned changes to training policy or provider-owned responsibilities.

## Comparison Target

The primary comparison target is ABI-183 `run_20260902_204128_bba815`: exploratory best epoch 12, capped filtered Dice 0.3966, MIT/Google filtered Dice 0.3805/0.4389, filtered precision 0.4468, recall 0.3565, connectivity 0.4546, and filtered predicted-positive fraction 0.00289. The main aggregate reference is ABI-181 `run_20260902_150611_cbbf35`: late36 best epoch 22, capped filtered Dice 0.4104, MIT/Google filtered Dice 0.3962/0.4486, precision 0.4423, recall 0.3828, connectivity 0.3639, and whole-validation filtered Dice 0.4124. Secondary references are ABI-173 `run_20260901_234732_bd5917`, ABI-182 `run_20260902_175152_51d2d9`, ABI-154 `run_20260901_071026_32d3ec`, and ABI-068 `run_20260828_010836_4ccc77`.

## Expected Effect

A positive outcome would remain finite and non-collapsed while improving ABI-183's aggregate and source filtered Dice, preserving materially higher connectivity than ABI-181, and avoiding a large increase in filtered predicted-positive fraction or false-positive-prone low-threshold behavior. The strongest outcome would approach or exceed ABI-181's aggregate/source filtered Dice while keeping ABI-183-style connectivity, making the direct Line Target auxiliary branch a better continuation point than the ABI-182 line-consensus late-budget branch. A negative but useful outcome would show that the Line Target auxiliary branch's connectivity benefit trades off against recall or MIT overlap under longer optimization, motivating a different in-contract architecture/calibration mechanism rather than another unchanged repeat.

## Implementation Sketch

- Reuse ABI-183 model code unchanged: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, and primary `mask_logits`.
- Keep the `line_logits` auxiliary head and provider-derived Line Target auxiliary supervision with trusted `weighted_bce` at weight 0.01.
- Keep the `centerline_logits` auxiliary head and provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` at weight 0.02.
- Keep trusted manifest choices otherwise unchanged: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning rate, and disabled early stopping.
- Add only candidate-local `budget_request.yaml` requesting the reviewed `late_improving` budget for 36 effective epochs, with fallback to the exploratory budget if denied.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `line` with `weighted_bce` weight 0.01, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Candidate-local budget request: `late_improving`, requested max epochs 36, parent Run `run_20260902_204128_bba815`, fallback `run_exploratory_budget` if denied.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped Run with the reviewed late-improving budget request: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, requested effective max epochs 36, requested 10,800 seconds Docker training wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. If the Harness denies the request, run under the exploratory budget and treat that result as valid bounded evidence. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if the late-improving continuation improves ABI-183 aggregate/source filtered Dice or recall while retaining a clear connectivity advantage over ABI-181 and without severe precision or positive-area regression. Promotion would require later whole-validation diagnostics and human review; this capped Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-184 improves aggregate/source filtered Dice while preserving ABI-183's connectivity gain, consider a bounded whole-validation Evaluation Request in a later Autonomy Step to test whether the capped tradeoff survives the full Working Validation Split. If it improves overlap only by losing the connectivity advantage, treat ABI-181 as the stronger aggregate reference and broaden to a different line-continuity/calibration mechanism. If it plateaus below ABI-183 or expands positive-area clutter, stop this exact Line+Centerline late-budget branch rather than repeating it unchanged. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
