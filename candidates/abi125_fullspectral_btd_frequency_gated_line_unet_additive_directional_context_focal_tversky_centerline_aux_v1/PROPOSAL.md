# Proposal: ABI-125 additive directional context frequency-gated line U-Net

## Hypothesis

A non-suppressive additive long-axis context bridge on top of ABI-068 can improve Contrail Mask continuity and false-positive discipline without repeating the precision/connectivity regressions seen in suppressive or agreement-style ABI-123/ABI-124 calibration blocks. This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family, not a promotion claim from capped evidence alone.

## Comparison Target

Primary comparison is ABI-068 (`run_20260828_010836_4ccc77`), the strongest capped aggregate filtered-Dice frequency-gated reference. Secondary interpretation compares against ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity discipline, ABI-121 (`run_20260831_041559_43da35`) for focal-Tversky recall/source balance, and ABI-124 (`run_20260831_065423_01a457`) for the most recent failed agreement-style calibration branch.

## Expected Effect

The additive bridge should supply larger-scale horizontal, vertical, and dilated line context to the final high-resolution feature map while avoiding multiplicative masking of weak contrail evidence. Expected favorable evidence is ABI-068-like or better aggregate filtered Dice, improved filtered precision or Contrail Connectivity Metric relative to ABI-068, retained MIT/Google source balance, and no increase in predicted-positive burden beyond the recent over-recall calibration branches.

## Implementation Sketch

Start from the ABI-068 model. Keep the normalized raw-plus-BTD front end, frequency split stem, residual encoder/decoder, dilated bottleneck, skip fusion, frequency-pyramid fusion, mask head, and Centerline Target auxiliary head. Add one `AdditiveDirectionalContextBridge` after frequency-pyramid fusion. The bridge builds local detail, long horizontal/vertical asymmetric convolutions, dilated horizontal/vertical line context, and smoothed broad context, projects them back to the base feature width, and adds a bounded residual. The final projection is zero-initialized so the extra branch starts as a no-op relative to the ABI-068 architecture.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: provider-approved `abi_16ch`; no longitude or latitude inputs.
- Output form: primary `mask_logits` plus provider-declared `centerline_logits` auxiliary output.
- Losses: trusted `focal_tversky` primary loss and trusted `weighted_bce` Centerline Target auxiliary loss with weight 0.02.
- Data policy: provider/Harness-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Training policy: AdamW, learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping.

Candidate code owns only the model architecture. It does not implement data loading, split policy, capped-record selection, sampling, augmentation transforms, target derivation, losses, metrics, thresholds, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, resource placement, or lifecycle behavior.

## Budget Requested

Use the current trusted capped representative budget: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, fixed first-four prediction retention, 3,600-second Docker training timeout, and the 25M-parameter smoke ceiling. The architecture is a small additive extension of ABI-068's approximately 12.1M-parameter model and should remain in the previously feasible A100 batch-4 resource class, but it should still execute sequentially under the configured concurrency cap.

## Success Criteria

Treat the Run as capped representative family-development evidence. Success would be any of:

- aggregate `val/filtered_dice` matches ABI-068 within about 0.01 while improving either `val/filtered_precision` or `val/filtered_contrail_connectivity`;
- aggregate `val/filtered_dice` exceeds ABI-068 with no Dataset Source filtered Dice below about 0.33;
- the trajectory is finite, non-collapsed, late-improving, and shows a diagnostically useful precision/connectivity recovery versus ABI-123/ABI-124.

Promotion would require later full Working Validation Split diagnostics and operator review; capped evidence alone is not sufficient.

## Fallback/Next Decision

If ABI-125 regresses like ABI-123/ABI-124 by increasing predicted-positive fraction while losing precision/connectivity, stop this additive directional-context branch and broaden away from ABI-068 calibration add-ons. If it matches ABI-068 while improving precision or connectivity, request bounded whole-validation failure-bucket diagnostics before further family development. If it fails static/smoke validation, repair only narrow implementation bugs that preserve this hypothesis and comparison target.
