# ABI-216 temporal Siamese change U-Net

ABI-216 is a sequential temporal family scout for GOES ABI Contrail Segmentation. It uses the provider-owned `abi_16ch_plus_sza_temporal` input mode with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

## Architecture

- Splits the channel-stacked 51-channel tensor into previous, center, and next ABI+SZA frames.
- Normalizes ABI channels 1-16 and per-frame Solar Geometry Input, and derives fixed ABI-channel brightness-temperature-difference planes from approved ABI channels.
- Applies one shared-weight frame encoder to all three frames.
- At each encoder scale, fuses temporal evidence using center features, temporal means, center-minus-previous residuals, next-minus-center residuals, and next-minus-previous drift features.
- Decodes the fused representation with a compact ASPP U-Net head.
- Produces `mask_logits`, `line_logits`, and `centerline_logits` with shape `[1, 256, 256]`.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, persistence, GPU scheduling, runtime downloads, pretrained weights, or coordinate-derived features. Longitude and latitude remain forbidden provider-side channels and are neither requested nor reconstructed.

## Manifest policy

The manifest requests trusted source-balanced traversal, trusted random mirroring, provider-owned BCE-Dice loss, low-weight Line and Centerline auxiliary supervision, AdamW learning rate 0.0003, batch size 2, 12 exploratory epochs, and constant learning rate. Batch size 2 keeps the first real temporal architecture sequential and conservative because temporal encoder resource behavior is not yet profiled.
