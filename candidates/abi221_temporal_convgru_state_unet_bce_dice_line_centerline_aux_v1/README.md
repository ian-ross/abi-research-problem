# ABI-221 temporal ConvGRU state U-Net

ABI-221 is a temporal-family scout/continuation after ABI-220. It consumes provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and the trusted `temporal_eligible_center` frame-selection policy. It broadens beyond explicit temporal-difference gate tuning by learning a compact recurrent temporal state over previous, center, and next ABI+SZA-derived features before a single decoder.

## Architecture

The model reshapes the provider channel-stacked tensor into previous, center, and next ABI+SZA frames. For each frame it normalizes ABI channels 1-16, derives fixed approved-channel thermal BTD planes, adds scaled and cosine Solar Geometry Input planes, and maps non-finite/extreme candidate-visible values to bounded finite features.

A shared frame projector maps each per-frame feature tensor to a compact base-width representation. A bidirectional full-resolution ConvGRU scans the three projected frames in temporal order and reverse temporal order, producing bounded learned temporal states. A small change-summary projection supplies explicit average absolute center-neighbor evidence. A learned fusion gate combines the center-frame embedding, forward/reverse temporal states, and change summary into one center-focused stem for a compact residual U-Net/ASPP encoder-decoder with base width 24.

The Candidate emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted primary and auxiliary losses.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, persistence, GPU scheduling, runtime downloads, pretrained weights, coordinates, Dataset Source identity, or route/location priors.

## Manifest policy

The manifest requests `abi_16ch_plus_sza_temporal`, `data.frame_selection_policy: temporal_eligible_center`, temporal offsets `[-1, 0, 1]`, `combined_source_balanced` sampling, trusted random mirroring, trusted BCE-Dice primary loss, low-weight Line and Centerline auxiliary supervision, AdamW learning rate 0.0003, batch size 2, 12 exploratory epochs, and constant learning rate.
