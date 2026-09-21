# ABI-355 temporal-attention multi-scale change-line fusion

ABI-355 is an exploratory family-development continuation in the temporal-attention family for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-350 showed that pre-decoder line-supported skips can be strong after late training, while ABI-351 and ABI-354 showed that final continuity bridges or encoder-entry change bridges decouple Dice, recall, and connectivity. ABI-355 tests a different placement: temporal change and center-frame detail evidence are injected only during multi-scale decoder skip fusion, leaving the temporal stem and encoder anchor unchanged.

## Architecture

The model keeps the ABI-350 finite ABI+SZA+BTD temporal feature builder, per-pixel temporal-attention stem, U-Net encoder, ASPP bottleneck, decoder, and trusted `mask_logits`, `line_logits`, and `centerline_logits` heads. The mechanism change is `MultiScaleTemporalChangeLineFusion` at skip scales 2, 1, and 0. Each module combines:

- orientation-aware line support from the encoder skip;
- coarser decoder/context state;
- center-frame detail projected to the skip scale;
- temporal-change features from center-minus-neighbor-mean, next-minus-previous, and absolute neighbor differences.

The fusion is a bounded differentiable feature update before decoder fusion. It is not thresholding, morphology, calibration, postprocessing, target derivation, an Artifact Filter, a metric, or sample selection.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, trusted `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, constant learning rate, batch size 2, and the exploratory 12-epoch budget.

## Expected evidence

ABI-355 is capped temporal-eligible exploratory evidence only. Success means finite non-collapsed training that improves over ABI-349/351/354 exploratory temporal-attention variants or gives diagnostically useful evidence toward ABI-350/ABI-223 by increasing fixed-threshold recall/connectivity without broad negative-patch clutter.
