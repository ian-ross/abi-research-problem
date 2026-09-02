# ABI-122 Full-Spectral BTD ASPP/Detail Decoder Directional-Continuity Focal-Tversky Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-121 established finite, resource-feasible, non-collapsed, strongly positive capped evidence for the compact ASPP/detail decoder under trusted `focal_tversky` and low-weight Centerline Target auxiliary supervision. ABI-122 keeps the same data policy, loss policy, input mode, auxiliary target, and budget, and changes only the architecture by adding a minimal non-suppressive directional-continuity feature refinement before the output heads.

## Hypothesis

ABI-121 nearly matched the ABI-068 aggregate-Dice reference and improved ABI-120 recall and source balance, but its filtered connectivity was weak: 0.2315 versus ABI-068 at 0.3900 and ABI-066 at 0.4731. This suggests the ASPP/detail focal-Tversky branch can find contrail area but may fragment or thicken line structure. A small high-resolution residual refinement that exposes short and long horizontal/vertical line context to the mask and centerline heads should improve connectivity and precision discipline without suppressing ABI-121's recall-oriented representation.

## Comparison Target

The primary family comparison target is ABI-121 `abi121_fullspectral_btd_aspp_detail_decoder_focal_tversky_centerline_aux_v1`, Run `run_20260831_041559_43da35`: ASPP/detail decoder with trusted `focal_tversky` and Centerline Target auxiliary weight 0.02. ABI-121 selected epoch 12 with filtered Dice 0.3884, MIT/Google filtered Dice 0.3835/0.4005, filtered precision 0.3526, filtered recall 0.4323, filtered connectivity 0.2315, and filtered predicted-positive fraction 0.00444.

Secondary capped references are ABI-068 `run_20260828_010836_4ccc77` as the local aggregate-Dice reference, ABI-066 `run_20260827_230540_bf4ce3` as the precision/connectivity reference, and ABI-120 `run_20260831_033037_bad0bb` as the ASPP/detail clDice scout. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a strict gate for this capped continuation.

## Expected Effect

If the added directional-continuity refinement is useful, ABI-122 should increase ABI-121 filtered connectivity and preferably precision while keeping aggregate/source filtered Dice close to or above ABI-121. A useful result need not beat ABI-068 immediately; it can justify further ASPP/detail development if it preserves ABI-121's high recall and source balance while materially narrowing the connectivity gap to ABI-068 or ABI-066. A negative result would show that the ASPP/detail branch's low connectivity is not fixed by this minimal high-resolution line-context residual and should push the campaign toward diagnostics or a different architecture frontier.

## Implementation Sketch

- Reuse ABI-121's normalized provider-approved GOES ABI channels 1-16, eight deterministic thermal BTD planes derived only from those channels, learned 16-channel 1x1 projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck with dilation rates 2/4/8 plus image-level context, bilinear decoder fusions, second high-resolution detail path, and existing line-aware refinement.
- Add a new `DirectionalContinuityRefinement` module after the existing final line-aware refinement and before the heads.
- The new module builds learned local, short-horizontal, short-vertical, long-horizontal, long-vertical, and dilated-local feature branches at full resolution, computes a feature-space consensus gate, and adds a bounded residual update to the incoming feature map. The residual design is non-suppressive: the ABI-121 feature map remains in the direct path.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the refined feature map.
- Preserve provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, trusted primary `focal_tversky` loss, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As ASPP/detail family-development evidence, the result is useful if it improves ABI-121 filtered connectivity, improves or preserves ABI-121 precision at similar recall, keeps aggregate filtered Dice within roughly 0.02 of ABI-121 while improving a secondary line-quality metric, or shows a finite late improving trajectory that motivates one more bounded connectivity-focused ASPP/detail follow-up.

## Continuation and hard stop

Continue the ASPP/detail directional-continuity branch only if ABI-122 is finite, non-degenerate, source-informative, and improves a meaningful family diagnostic relative to ABI-121, especially filtered connectivity, precision/recall balance, source balance, positive-area discipline, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not family-wide elimination proof, but a clear miss on ABI-121-relative connectivity and Dice diagnostics would be enough to stop this exact continuity-refinement branch.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the ABI-121-preserving hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but loses ABI-121 recall/Dice without improving connectivity or precision discipline, document the continuation and either request whole-validation diagnostics for ABI-121 or broaden to a different contract-compliant frontier rather than repeating this same refinement. If it unexpectedly challenges ABI-068, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
