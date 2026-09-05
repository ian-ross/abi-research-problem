# ABI-195 ridge-preserving detail bridge ASPP follow-up

## Hypothesis

A family-development continuation that moves line-continuity support earlier into the high-resolution decoder can recover some of ABI-184's precision/connectivity discipline without ABI-194's learned clutter-gate suppression penalty. An additive ridge-preserving bridge from signed high-resolution detail features into the fused decoder context should let trusted BCE-Dice plus provider-derived Line and Centerline auxiliaries learn connected thin-contrail evidence while avoiding candidate-owned thresholding or postprocessing.

## Comparison Target

Primary capped comparison target: ABI-184 `run_20260902_213856_2c04ac`, the line+centerline late36 precision/connectivity reference. Secondary targets: ABI-181 `run_20260902_150611_cbbf35` for whole-validation aggregate filtered Dice, ABI-192 `run_20260903_085513_f395ad` for recall-balanced directional context, and ABI-194 `run_20260903_125403_548c08` as the negative clutter-gate result.

## Expected Effect

Relative to ABI-194, the bridge should raise filtered Dice, recall, and especially contrail connectivity by preserving rather than suppressing line-support features. Relative to ABI-184, success would be a comparable or improved capped filtered Dice with less loss of recall while retaining useful precision/connectivity and a non-inflated filtered predicted-positive fraction.

## Implementation Sketch

Start from the ABI-184 signed-detail full-scale skip ASPP decoder with approved ABI+SZA inputs, thermal BTD planes, full-scale skip fusion, line-aware refinement, and trusted Line plus Centerline auxiliary outputs. Add a `RidgePreservingDetailBridge` between the fused decoder representation and final line-aware refinement. The bridge fuses decoder context, high-resolution signed-detail features, and stem features through horizontal/vertical ridge convolutions, broad context smoothing, a learned feature gate, and a zero-initialized additive residual update. It predicts no masks or targets internally and performs no thresholding.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; longitude/latitude are not requested or reconstructed.
- `output_form: mask_logits` with provider-declared `line_logits` and `centerline_logits` auxiliary outputs.
- Trusted primary loss `bce_dice` and trusted auxiliary `weighted_bce` losses.
- Trusted `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- AdamW, constant learning rate, batch size 4, 12 exploratory epochs under the active Workspace Configuration.
- Candidate code defines model architecture only; it contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, runtime downloads, filesystem persistence, or scheduling.

## Budget Requested

Exploratory default budget only: 12 epochs, batch size 4, constant learning rate, and the configured 1,024-record per Dataset Source/split cap. No `budget_request.yaml` is included. A later late-improving continuation would require a final-epoch or near-final-epoch improving, finite, non-collapsed trajectory with distinctive source-balanced precision/recall/connectivity evidence.

## Success Criteria

Continue this branch if the capped Run is finite and non-collapsed and either (a) reaches within about 0.01 filtered Dice of ABI-184/ABI-181 while improving recall or source balance, (b) materially improves over ABI-194 in connectivity and aggregate filtered Dice without a large predicted-positive inflation, or (c) shows a still-improving final-epoch trajectory with source-informative metrics that plausibly merits a late-improving budget request. Promotion-level evidence would require whole-validation diagnostics and operator review; capped evidence alone is feasibility evidence.

## Fallback/Next Decision

If the Run is a contract/resource/candidate failure, classify and repair only if the hypothesis is preserved. If it is finite but below ABI-194 or collapses connectivity/precision, stop this exact bridge branch and broaden to a more distinct high-resolution architecture or an in-contract data/loss-policy probe rather than adding another post-refinement gate. If it is finite and promising, write a Research Note and consider either a late-improving close-continuation or a request-gated whole-validation failure-bucket evaluation according to the observed trajectory.
