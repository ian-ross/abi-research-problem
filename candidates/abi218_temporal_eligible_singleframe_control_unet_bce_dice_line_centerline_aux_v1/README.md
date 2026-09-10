# ABI-218 temporal-eligible single-frame control U-Net

ABI-218 is a matched single-frame control for ABI-217. It uses provider-approved `abi_16ch_plus_sza` input on the trusted `temporal_eligible_center` frame-selection policy, preserving ABI-217's source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, learning rate, batch size, and 12-epoch exploratory budget.

## Architecture

The model consumes only the center ABI+SZA tensor. It normalizes ABI channels 1-16, derives fixed approved-channel thermal BTD planes, adds scaled and cosine Solar Geometry Input planes, and maps non-finite or extreme candidate-visible features to bounded finite values before a compact residual U-Net/ASPP decoder. It emits `mask_logits`, `line_logits`, and `centerline_logits`.

Compared with ABI-217, ABI-218 removes previous/next frames, shared three-frame encoding, and temporal residual fusers. The purpose is diagnostic control rather than promotion: determine whether ABI-217's 0.3491 capped filtered Dice is explained by temporal eligibility/sample effects, center-frame backbone behavior, or true temporal change streams.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, persistence, GPU scheduling, runtime downloads, pretrained weights, or coordinate-derived features. Longitude and latitude remain forbidden provider-side channels and are neither requested nor reconstructed.

## Manifest policy

The manifest requests `abi_16ch_plus_sza`, `data.frame_selection_policy: temporal_eligible_center`, `combined_source_balanced` sampling, trusted random mirroring, trusted BCE-Dice primary loss, low-weight Line and Centerline auxiliary supervision, AdamW learning rate 0.0003, batch size 2, 12 exploratory epochs, and constant learning rate.
