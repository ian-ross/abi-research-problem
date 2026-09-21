# ABI-321 temporal-attention center-detail evidence-sharpening U-Net

## Hypothesis

Recent temporal shift-bank/C4 head refinements (ABI-319 and ABI-320) improved or preserved connected-line cleanliness but failed to raise enough true contrail logits at the fixed 0.5 threshold. ABI-321 broadens away from local shift-bank/C4 head refinements and returns to an ABI-223-style provider-owned three-frame temporal-attention family. The hypothesis is that lightweight temporal attention, center-frame signed detail, and a bounded multi-evidence sharpening head can recover recall/source balance without candidate-owned thresholds, postprocessing, losses, metrics, sampling, or temporal lookup.

This is a **family-development continuation** in the temporal-attention/evidence-sharpening direction, not a promotion claim and not an unchanged continuation of ABI-319/320.

## Comparison Target

Primary comparison targets:

- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention late36 comparator with strong temporal-eligible filtered Dice/connectivity.
- ABI-319 (`run_20260915_162050_163586`): shift-bank/C4 alignment-confidence continuation that improved cleanliness over ABI-315 but under-recalled.
- ABI-320 (`run_20260915_172705_4d6463`): center-detail recall-gated shift-bank/C4 continuation that regressed versus ABI-319.
- ABI-311/306/309 remain temporal C4 context for balanced, compact, and recall-heavy operating points.

## Expected Effect

If the failure in ABI-319/320 is over-dependence on local shift agreement and late gated heads, ABI-321 should produce a cleaner temporal-attention operating point with better fixed-threshold recall than ABI-319/320 and better aggregate/source Dice than ABI-320. Useful positive evidence would include finite non-collapsed predictions, higher temporal-eligible filtered Dice, MIT Dice, or recall versus ABI-320, and no broad predicted-positive-area expansion. A strong result would approach ABI-223/306/309/311 temporal comparators while retaining a compact footprint.

## Implementation Sketch

The model consumes provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It normalizes each frame, derives approved-channel BTD planes, and encodes Solar Geometry Input features. A compact per-pixel temporal-attention stem fuses previous, center, and next frames without candidate-owned temporal lookup. A center-detail branch preserves signed high-resolution detail from the zero-offset frame. A compact U-Net decoder fuses temporal attention, skip features, and center detail.

The final head learns Line and Centerline auxiliary logits and adds only a bounded architecture-internal mask-logit residual when region, line, centerline, and center-detail evidence agree. The head does not threshold, postprocess, apply morphology, implement Artifact Filters, or alter Harness metrics.

## Contract Features Used

- `research_problem: goes_abi_contrail_segmentation`.
- `input_mode: abi_16ch_plus_sza_temporal`; no longitude or latitude inputs.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `output_form: mask_logits`.
- Trusted Line and Centerline auxiliary targets via `line_logits` and `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Trusted primary loss: `bce_dice`.
- Trusted sampling/augmentation: `combined_source_balanced` and `random_mirroring`.
- AdamW, constant learning rate 0.0003, batch size 2, exploratory 12-epoch budget.

Candidate code defines architecture only. It does not implement data loading, split logic, target derivation, sampling, augmentation transforms, losses, metrics, Artifact Filters, thresholding, postprocessing, training loops, temporal cache access, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and the Harness-owned exploratory timeout. Do not request the late-improving budget for this first mechanism-changing temporal-attention evidence-sharpening scout; resource and trajectory behavior should be profiled before any longer close continuation.

## Success Criteria

Continue or diagnose this direction if the Run is finite, resource-safe, and any of these hold:

- improves ABI-320 on temporal-eligible filtered Dice, MIT Dice, Google Dice, recall, or connectivity without a large footprint increase;
- approaches ABI-319 while improving recall or source balance;
- shows late improving, source-informative behavior with non-collapsed predictions;
- exposes a useful trade-off distinct from shift-bank/C4 head refinements.

Do not require ABI-321 to beat mature late36 comparators such as ABI-223/311 before considering bounded family-development evidence.

## Fallback/Next Decision

If ABI-321 fails contract/smoke, repair only if the temporal-attention center-detail evidence-sharpening hypothesis is preserved. If it completes but regresses below ABI-319/320 without useful secondary-metric evidence, stop this exact head and broaden to a different temporal evidence-sharpening design or a non-temporal line-continuity mechanism rather than submitting another local gated-head refinement.
