# ABI-236 full-spectral BTD+SZA recall-bypass Radon ASPP decoder

## Hypothesis

ABI-235 showed that a differentiable Radon/Hough-style long-line branch benefits from the approved late-improving budget, improving filtered Dice and recall over ABI-234, but it lost some of ABI-234's selected-checkpoint connectivity. ABI-236 is a **family-development continuation** testing whether a weaker Radon residual plus a learned high-resolution detail bypass can preserve ABI-235's recall gains while recovering stronger line continuity. The candidate stays in the same single-frame Radon family and changes only the architecture-internal fusion path.

## Comparison Target

Primary comparison is ABI-235 (`run_20260910_195407_469d7c`) as the latest Radon-family parent. Secondary context is ABI-234 (`run_20260910_185443_f88be8`) for the high-connectivity/low-recall scout signature, ABI-223 (`run_20260908_154531_8c7e2b`) as the capped temporal-family frontier, and ABI-202 (`run_20260904_043143_ee0005`) as the current whole-validation-tested single-frame frontier. Because this is a controlled Radon continuation under the exploratory budget, interpretation should emphasize ABI-235-relative precision/recall/connectivity/source tradeoffs rather than requiring an immediate ABI-202 win.

## Expected Effect

The weaker Radon residual should reduce over-regularization toward compact positives, while the bounded high-resolution detail bypass should let faint local center/detail features survive when long-line support is uncertain. Positive evidence would be a noncollapsed Run that approaches ABI-235's filtered Dice/recall, improves filtered contrail connectivity, and does not degrade MIT or Google filtered Dice catastrophically. A neutral result would still clarify whether ABI-235's late recall/connectivity tradeoff is caused by Radon fusion strength.

## Implementation Sketch

Start from the ABI-235 full-spectral BTD+Solar Geometry Input signed-detail ASPP U-Net scaffold. Keep normalized ABI channels, approved-channel BTD planes, Solar Geometry Input features, signed-detail stems, ASPP encoder/decoder, full-scale skip fusion, trusted `mask_logits`, `line_logits`, and `centerline_logits`, and the same six-orientation low-resolution differentiable Radon branches. Modify `DifferentiableRadonLineBridge` by reducing the bounded Radon residual amplitude from 0.30 to 0.18 and adding a second zero-initialized bounded residual path from high-resolution seed/detail/full-scale features with its own learned gate and amplitude 0.14. This remains differentiable model logic only; it does not threshold, morphologically postprocess, filter artifacts, load data, define losses, inspect coordinates, or access temporal cache state.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`.
- `output_form: mask_logits` with trusted Line and Centerline auxiliary targets.
- Trusted primary loss `bce_dice`; auxiliary `weighted_bce` with weights 0.01 and 0.02.
- Provider/Harness-owned `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Constant learning rate scheduler, AdamW optimizer, batch size 4, and 12-epoch exploratory budget.
- No Candidate-owned data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling policy implementation, augmentation transforms, coordinates, Dataset Source identity, temporal cache access, downloads, training loops, or resource scheduling.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 4, constant learning rate 0.0003. No `late_improving` budget is requested for this architecture-change continuation. If the Run completes finite/noncollapsed and selects its best checkpoint near epoch 12 with an improving trajectory, a later Autonomy Step may consider a separate approved late-improving close continuation.

## Success Criteria

Family-development success does not require beating ABI-202. Useful positive evidence is ABI-235-neighborhood filtered Dice with improved filtered contrail connectivity, or ABI-234-level connectivity with materially better recall/source balance. A strong result would exceed ABI-235 on filtered Dice while improving connectivity and preserving source-informative MIT/Google metrics. Hard-stop evidence would be contract/smoke failure, non-finite training, prediction collapse, or a clear regression from ABI-234/235 on filtered Dice, recall, connectivity, and both Dataset Sources without a diagnostic tradeoff.

## Fallback/Next Decision

If ABI-236 fails for an implementation bug, repair only the candidate code while preserving this hypothesis and comparison target. If it completes but the detail bypass does not improve the Radon tradeoff, do not keep making small Radon gate tweaks; broaden to a modern lightweight backbone or temporal/radon hybrid only if the hypothesis is materially different and in contract. If it is finite and late-improving at epoch 12, write a Research Note and consider a late-improving continuation under the approved budget policy.
