# ABI-266 C4 recall-bridge U-Net

## Hypothesis

ABI-249 showed that C4 rotation-shared line context can produce a compact, high-precision operating point, but whole-validation diagnostics found that its remaining deficit versus ABI-202 is fixed-threshold recall and line coverage, especially on MIT. ABI-266 tests a mechanism-changing continuation: keep ABI-249's C4 orientation prior, but add a lightweight gated recall bridge that raises under-confident contrail evidence only when high-resolution detail and C4 line context agree.

This is a family-development continuation, not a promotion claim and not an unchanged repeat. The bridge is architecture-level evidence fusion only; it does not implement threshold selection, postprocessing, morphology, Artifact Filters, losses, metrics, target derivation, data loading, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Comparison Target

Primary comparison targets:

- ABI-249 (`run_20260911_111909_dd7ef7` plus whole-validation diagnostic): high-precision C4 comparator with whole-validation filtered Dice 0.4197, precision 0.4865, recall 0.3690, and connectivity 0.3975.
- ABI-248 (`run_20260911_102833_5db7f8`): 12-epoch C4 parent, used to interpret exploratory-budget C4 behavior.
- ABI-202 (`run_20260904_043143_ee0005`): current aggregate whole-validation reference, retained as context rather than a first-run gate.
- ABI-265 (`run_20260912_065321_ceab64`): recent axial line-memory continuation showing useful connectivity but weaker aggregate score and higher activation cost.

## Expected Effect

The expected positive result is not simply higher positive area. Success would look like a finite, non-collapsed exploratory run with improved recall/connectivity over ABI-249-like C4 behavior while keeping precision and negative-patch discipline from collapsing. The gated residual logit is bounded with `tanh`, so it should raise true line evidence without replacing trusted thresholding or turning the model head into postprocessing.

A negative result is useful if the recall bridge raises false positives faster than true positives, confirming that ABI-249's conservative operating point is hard to shift with single-frame C4 evidence alone.

## Implementation Sketch

Start from the validated single-frame ABI-249 C4 steerable line-context U-Net. The model consumes provider-owned `abi_16ch_plus_sza` tensors, normalizes ABI channels 1-16, adds approved-channel thermal BTD feature planes, includes Solar Geometry Input as scaled/cosine features, and learns a small 1x1 channel mixture.

The encoder/decoder remains the compact U-Net with signed-detail stems, ASPP bottleneck, and C4 rotation-shared line context. ABI-266 replaces the simple mask head with `C4RecallBridgeMaskHead`: C4 line context, high-resolution detail support, and an ASPP recall-support path are fused through an agreement gate. The final mask logit is the base fused mask logit plus small bounded recall and line residuals. The model also returns `line_logits` and `centerline_logits` for trusted auxiliary targets.

## Contract Features Used

- `research_problem: goes_abi_contrail_segmentation`.
- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `output_form: mask_logits`.
- Trusted auxiliary targets: Line Target via `line_logits` and Centerline Target via `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Trusted primary loss: `bce_dice`.
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Trusted provider sampling and augmentation: `combined_source_balanced` and `random_mirroring`.
- Batch size 4, max epochs 12, within current exploratory ceilings.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 4, constant learning rate, and the active Workspace Configuration's sample, timeout, prediction-retention, GPU, and parameter ceilings. No late-improving budget is requested for this mechanism-changing first attempt.

## Success Criteria

Continue or diagnose the branch only if the Run is finite, contract-valid, noncollapsed, and at least one of these holds:

- capped recall and/or connectivity improve over ABI-248/249-style C4 behavior without a severe precision collapse;
- aggregate filtered Dice is competitive with recent broad scouts while retaining source-informative MIT and Google filtered Dice;
- the epoch-12 trajectory is still improving and positive area remains bounded rather than all-positive;
- resource use remains in the ABI-249 neighborhood and below the 25M-parameter ceiling.

Do not require this exploratory mechanism-changing candidate to beat ABI-202 or ABI-249 whole-validation Results before any family-development consideration.

## Fallback/Next Decision

If ABI-266 fails contract or smoke validation, repair only if the C4 recall-bridge hypothesis is preserved. If it completes but collapses, is non-finite, or degrades precision without improving recall/connectivity, stop this exact bridge design and broaden. If it produces finite late-improving source-balanced evidence, consider either a bounded late-improving request or a whole-validation diagnostic only if Harness-owned metrics justify that cost under current policy.
