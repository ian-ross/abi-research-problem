# ABI-119 full-spectral BTD context-pyramid agreement U-Net shape repair

## Hypothesis

A context-pyramid FPN/U-Net can improve source-robust calibration of thin-contrail predictions by requiring high-resolution local line evidence to agree with low-resolution patch/cloud context before logits are emitted. This is a **Repair Candidate** for ABI-118, preserving ABI-118's **family scout** hypothesis and comparison target after the Harness recorded a candidate-bug smoke failure caused by a decoder spatial mismatch (`32` vs `64` at the first FPN lateral addition). It broadens away from the recent negative oriented/ridge/detail residual branches around ABI-068 while staying inside the same provider-approved full-spectral ABI and BTD evidence space.

## Comparison Target

Primary capped-family references are ABI-068 (`run_20260828_010836_4ccc77`) as the current local aggregate-Dice reference for the full-spectral BTD frequency-gated branch and ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity reference. Recent negative-to-mixed context for the decision includes ABI-114, ABI-116, and ABI-117. Canonical MCAST 2.1 remains the full Working Validation Split promotion context, but this scout requests only capped representative feasibility evidence.

## Expected Effect

The expected effect is not immediate dominance over a mature incumbent. Useful scout evidence would be either: aggregate filtered Dice within roughly 0.02 of ABI-068 while improving filtered precision, Contrail Connectivity, or filtered predicted-positive fraction; or a source-balanced trajectory with both MIT and Google filtered Dice above 0.36 and late-epoch improvement that justifies a bounded family-development continuation. The context pyramid should specifically reduce diffuse/cloud-edge false positives without shifting responsibility for thresholding, Artifact Filters, or postprocessing into Candidate code.

## Implementation Sketch

The model uses a `NormalizedBTDFrontEnd` with normalized provider-approved GOES ABI channels 1-16, eight deterministic thermal BTD planes derived only from those approved channels, and a learned 1x1 ABI mixer. A compact residual encoder feeds a low-resolution `ContextPyramidNeck` with adaptive average-pooling bins plus atrous residual branches. A top-down FPN decoder reuses encoder features without concatenative skip amplification. The ABI-118 repair is limited to upsampling the projected low-resolution neck tensor to the `enc2` lateral feature size before the first additive FPN merge; all intended context-pyramid and agreement-calibration behavior is otherwise unchanged. A differentiable `FeatureAgreementCalibrator` fuses local decoded features with upsampled low-resolution context using a learned agreement gate over local, context, and absolute-difference features. The model returns `mask_logits` and `centerline_logits` only.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch`; no longitude, latitude, or reconstructed coordinate inputs
- Output form: `mask_logits`
- Auxiliary target: provider-derived `centerline` target through `centerline_logits`, trusted `weighted_bce`, weight 0.02
- Data policy: trusted `combined_source_balanced` sampling traversal and trusted `random_mirroring`
- Training policy: trusted `focal_tversky` primary loss, AdamW, learning rate 0.0003, batch size 4, max epochs 12, `constant_lr`, disabled early stopping
- Candidate code owns only architecture; it does not implement data loading, splits, capped-record selection, sampling, augmentation, target construction, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, networking, pretrained weights, or lifecycle behavior

## Budget Requested

Request one standard representative capped Run under the active Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, 3,600-second Docker training wall-clock budget, 25M-parameter smoke ceiling, A100 execution under Harness-owned placement, and fixed first-four prediction retention. The Run should execute sequentially because this repair preserves a new context-calibrated family scout with unprofiled resource behavior.

## Success Criteria

Classify the scout as useful for bounded continuation if it completes finite and non-degenerate and satisfies at least one of the following capped-evidence criteria: (1) aggregate filtered Dice is within 0.02 of ABI-068 while improving filtered precision, filtered connectivity, or filtered predicted-positive fraction; (2) both MIT and Google filtered Dice are at least 0.36 and the best epoch is at or near the end of the 12-epoch budget; or (3) it exposes a distinctly cleaner precision/recall or source-balance tradeoff than ABI-116/117 without an Artifact Filter dependence warning. Treat this as capped feasibility evidence, not as full-data promotion evidence.

## Fallback/Next Decision

If the Run fails static validation, smoke, or finite-state checks again, classify the failure before deciding whether another repair is justified or whether this exact context-pyramid branch should stop. If it completes but remains far below ABI-068 and ABI-066 on aggregate/source Dice and precision/connectivity, stop this exact context-pyramid agreement branch. If it is finite, source-balanced, and diagnostically distinct, consider one bounded family-development continuation that changes only a controlled architecture or allowlisted loss/auxiliary choice. If the evidence shows the current allowlists block the needed calibration or mining mechanism, write a Capability Request rather than adding candidate-owned thresholding, postprocessing, data loading, losses, or sampling.
