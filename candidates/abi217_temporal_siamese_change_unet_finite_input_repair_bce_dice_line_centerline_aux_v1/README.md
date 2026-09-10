# ABI-217 temporal Siamese change U-Net finite-input repair

ABI-217 is a Repair Candidate for ABI-216 (`run_20260908_114141_bf7ae7`), which failed with Harness-recorded `candidate_bug`: `non_finite_training_state` in `output.mask_logits` during epoch 1 batch 134. The diagnostic counted one batch element with all-NaN logits while the other batch element remained finite, which is consistent with a non-finite candidate-visible value or extreme outlier in one provider-supplied temporal frame rather than a resource failure.

## Architecture

ABI-217 preserves the ABI-216 temporal/change hypothesis:

- Uses provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.
- Splits the 51-channel tensor into previous, center, and next ABI+SZA frames.
- Normalizes ABI channels 1-16, derives fixed approved-channel BTD planes per frame, and includes scaled/cosine Solar Geometry Input features.
- Applies one shared-weight encoder to all three frames.
- Fuses center features, temporal means, center-minus-previous, next-minus-center, and next-minus-previous residual streams at every scale.
- Decodes fused temporal evidence with the same compact ASPP U-Net head and emits `mask_logits`, `line_logits`, and `centerline_logits`.

The repair is intentionally narrow: the candidate front end maps non-finite or unbounded approved-channel feature values to bounded neutral feature values before the convolutional encoder, and bounds finite hidden activations. It does not select, load, pad, duplicate, repair, or discover temporal frames.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, persistence, GPU scheduling, runtime downloads, pretrained weights, or coordinate-derived features. Longitude and latitude remain forbidden provider-side channels and are neither requested nor reconstructed.

## Manifest policy

The manifest keeps ABI-216's trusted source-balanced traversal, trusted random mirroring, provider-owned BCE-Dice loss, low-weight Line and Centerline auxiliary supervision, AdamW learning rate 0.0003, batch size 2, 12 exploratory epochs, and constant learning rate. Batch size 2 remains conservative because real temporal encoders are not yet resource-profiled.
