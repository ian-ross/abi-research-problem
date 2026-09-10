# ABI-220 temporal change-confidence gated U-Net

ABI-220 is a temporal-family development Candidate after ABI-219. It consumes provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and the trusted `temporal_eligible_center` frame-selection policy. It preserves ABI-219's explicit temporal-difference feature groups, but replaces the simple temporal stem gate with a center-frame path plus learned spatial/channel confidence gates for temporal-change residuals.

## Architecture

The model reshapes the provider channel-stacked tensor into previous, center, and next ABI+SZA frames. For each frame it normalizes ABI channels 1-16, derives fixed approved-channel thermal BTD planes, adds scaled and cosine Solar Geometry Input planes, and maps non-finite/extreme candidate-visible values to bounded finite features.

The temporal front end concatenates center-frame features, center-minus-neighbor-mean features, next-minus-previous features, and average absolute center-neighbor change features. A change-confidence stem projects the center-frame evidence separately from signed and absolute temporal-change evidence. Learned spatial and channel gates then add a bounded change residual to the center path, followed by a small residual calibration block. The fused features feed one compact residual U-Net encoder/decoder with an ASPP bottleneck and base width 24.

The Candidate emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted primary and auxiliary losses.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, persistence, GPU scheduling, runtime downloads, pretrained weights, coordinates, Dataset Source identity, or route/location priors.

## Manifest policy

The manifest requests `abi_16ch_plus_sza_temporal`, `data.frame_selection_policy: temporal_eligible_center`, temporal offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted random mirroring, trusted BCE-Dice primary loss, low-weight Line and Centerline auxiliary supervision, AdamW learning rate 0.0003, batch size 2, 12 exploratory epochs, and constant learning rate.
