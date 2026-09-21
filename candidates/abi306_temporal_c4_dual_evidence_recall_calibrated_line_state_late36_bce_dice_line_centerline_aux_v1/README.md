# ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 U-Net

ABI-306 is a mechanism-changing temporal C4 family-development Candidate after ABI-285. ABI-285 produced the strongest capped temporal-eligible aggregate filtered Dice in the temporal C4 line-state branch but still traded connected-line continuity for recall. ABI-306 keeps the ABI-285 provider-owned three-frame temporal C4 line-state backbone and replaces only the final simple segmentation head with a dual-evidence recall-calibrated logit head.

The head learns base mask logits, Line logits, Centerline logits, and a bounded recall residual. A learned gate consumes decoder features plus internal base-mask/Line/Centerline probabilities, then adds a bounded residual to the mask logits. This is architecture-internal logit formation only; the Candidate does not select thresholds, postprocess predictions, implement morphology, or alter Artifact Filters.

## Contract boundaries

- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal frame offsets: `[-1, 0, 1]`.
- Trusted frame selection: `temporal_eligible_center`.
- Trusted sampling: `combined_source_balanced`.
- Trusted augmentation: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line (`line_logits`, weight 0.01) and Centerline (`centerline_logits`, weight 0.02).
- Optimizer/scheduler: AdamW with constant learning rate.
- Batch size: 2.

Candidate code defines only the model architecture. It does not load data, inspect temporal caches, fetch or repair frames, derive targets, implement losses or metrics, select samples, use longitude/latitude, use Dataset Source identity, download weights, schedule resources, run training, change thresholds, postprocess outputs, or implement Artifact Filters.

## Comparison target

The direct parent comparator is ABI-285 (`run_20260913_100333_a250df`). Additional temporal comparators are ABI-223, ABI-238, ABI-296/299, and ABI-305. This Candidate is capped temporal-eligible family-development evidence, not a whole-validation promotion claim.

## Budget

A `late_improving` budget request is included because ABI-285's useful checkpoint occurred at epoch 32 after the ABI-284 exploratory parent peaked at epoch 12. If denied, the Harness should run the exploratory budget and the resulting bounded evidence should be accepted.
