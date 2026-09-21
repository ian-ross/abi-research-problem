# ABI-356 temporal-attention multi-scale change-line fusion late36

ABI-356 is a late-improving family-development continuation of ABI-355 for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-355 was finite, source-informative, and the best of the recent ABI-349/351/354 exploratory temporal-attention placement tests. It selected its best checkpoint at epoch 11 and showed late oscillation between recall-heavy and precision/connectivity-heavy states. ABI-356 asks whether the approved 36-epoch budget can stabilize that multi-scale decoder skip-fusion mechanism into a better fixed-threshold recall/connectivity balance.

## Architecture

The model preserves ABI-355s finite ABI+SZA+BTD temporal feature builder, per-pixel temporal-attention stem, compact U-Net encoder/decoder, ASPP bottleneck, and trusted `mask_logits`, `line_logits`, and `centerline_logits` heads. The `MultiScaleTemporalChangeLineFusion` modules at skip scales 2, 1, and 0 combine orientation-aware line support, coarser decoder/context state, center-frame detail, and temporal-change features from the provider-stacked frames.

The fusion is differentiable architecture logic. It is not thresholding, morphology, calibration, postprocessing, target derivation, an Artifact Filter, a metric, or sample selection.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, trusted `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, constant learning rate, batch size 2, and ordinary exploratory manifest fields. The candidate-local `budget_request.yaml` requests the approved `late_improving` 36-epoch budget with exploratory fallback if denied.

## Expected evidence

ABI-356 is capped temporal-eligible evidence only. Success means improving over ABI-355 or giving decisive late-budget evidence about whether multi-scale temporal change-line fusion can approach ABI-350/324/223/348 temporal comparator behavior without candidate-owned thresholds, postprocessing, or temporal data authority.
