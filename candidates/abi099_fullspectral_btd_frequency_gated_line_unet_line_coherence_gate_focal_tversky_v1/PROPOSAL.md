# ABI-099 full-spectral BTD frequency-gated line U-Net line-coherence gate

## Hypothesis

Classification: family-development continuation.

ABI-068 remains the strongest capped aggregate-Dice reference in the full-spectral BTD frequency-gated line U-Net family, but later follow-ups repeatedly traded precision/connectivity for recall or broadened positive area. A small trainable line-coherence gate added inside the model, after ABI-068's frequency-pyramid fusion and before the output heads, may improve precision and connectivity by favoring elongated directional feature agreement over smoothed blob-like context while retaining focal-Tversky recall.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the current best capped full-spectral BTD frequency-gated focal-Tversky result: filtered Dice 0.3964, MIT filtered Dice 0.3886, Google filtered Dice 0.4161, filtered precision 0.3992, filtered recall 0.3936, filtered connectivity 0.3900, and filtered predicted-positive fraction 0.00357.

Secondary context: ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity-forward behavior and ABI-098 (`run_20260830_040621_bb9ebc`) as a recent negative example of high-resolution detail reuse expanding low-precision positives.

## Expected Effect

The directional gate should act as an in-architecture feature-selection mechanism rather than postprocessing. Expected useful signals are one or more of:

- preserve ABI-068-like aggregate filtered Dice while improving filtered precision or filtered connectivity;
- reduce filtered predicted-positive fraction relative to recent recall-heavy variants without collapsing recall;
- keep both MIT and Google filtered Dice source-balanced and above the approximate 0.36 continuation floor;
- avoid the ABI-098 failure mode where additional detail capacity increased positive area and lowered connectivity.

## Implementation Sketch

Start from ABI-068's provider-approved ABI-channel and BTD front end, frequency-split stem, residual encoder/decoder, dilated bottleneck, frequency-pyramid fusion, focal-Tversky primary loss, and trusted centerline auxiliary target. Add a `DirectionalCoherenceGate` after the final frequency-pyramid fusion. The gate builds horizontal, vertical, and diagonal-like elongated context branches, computes soft orientation weights, compares the selected line context with smoothed blob context and local detail, then applies a bounded residual feature update before `mask_logits` and `centerline_logits` heads.

The model code remains pure PyTorch architecture code. It does not create labels, losses, metrics, samplers, augmentations, thresholds, Artifact Filters, or postprocessing steps.

## Contract Features Used

- `input_mode: abi_16ch` with GOES ABI channels 1-16 only; no longitude or latitude inputs.
- `output_form: mask_logits` with primary `mask_logits` shaped `[1, 256, 256]`.
- Provider-derived auxiliary target `centerline`, output `centerline_logits`, trusted `weighted_bce`, weight 0.02.
- Trusted primary loss `focal_tversky`.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation policies.
- AdamW optimizer, constant learning rate, batch size 4, and 12 epochs within the active Workspace Configuration.
- Provider/Harness-owned data loading, split logic, sampling implementation, augmentation transforms, target derivation, loss implementation, metrics, Artifact Filters, resource placement, and lifecycle.

## Budget Requested

One sequential representative capped Run under the active limits: 1,024 records per Dataset Source/split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, 3,600-second Docker timeout, and the 25M-parameter smoke ceiling. This is a single unprofiled architectural continuation, not an Experiment Batch.

## Success Criteria

Treat this as capped family-development evidence, not full-data promotion evidence. A useful result should satisfy at least one of the following while remaining finite and non-degenerate:

- filtered Dice ties ABI-068 within about 0.01 and improves either filtered precision or filtered connectivity;
- filtered Dice exceeds ABI-078/085/066-like 0.38 while lowering filtered predicted-positive fraction relative to ABI-068;
- both Dataset Sources remain above 0.36 filtered Dice with no persistent all-negative/all-positive prediction collapse;
- a late-improving finite trajectory reveals a clear precision/connectivity tradeoff worth a subsequent whole-validation diagnostic.

## Fallback/Next Decision

If the Run is a candidate bug, create a Repair Candidate only if the line-coherence hypothesis and comparison target are preserved. If it completes but expands positives or lowers connectivity like ABI-098, do not repeat this line-coherence branch unchanged; broaden toward another architecture or trusted policy axis. If it ties ABI-068 while improving precision/connectivity or positive-area discipline, request a bounded whole-validation failure-bucket evaluation before any promotion interpretation.
