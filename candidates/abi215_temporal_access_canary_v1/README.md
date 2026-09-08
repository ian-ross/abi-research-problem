# ABI-215 temporal access canary

ABI-215 is a deliberately small Candidate Experiment whose success criterion is temporal data access, not segmentation quality. It selects the provider-owned `abi_16ch_plus_sza_temporal` input mode with `temporal_frame_offsets: [-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center` so Candidate Execution must use trusted SQLite temporal-cache evidence and materialized non-zero neighbor patches.

## Architecture

- Splits the channel-stacked 51-channel tensor into ordered -1, 0, and +1 ABI+SZA frames.
- Normalizes each frame's ABI channels and SZA, then concatenates the three frames, their temporal mean, and simple finite differences between previous/center/next frames.
- Feeds those temporal features to a tiny three-layer fully convolutional segmentation head.
- Produces only `mask_logits` with shape `[1, 256, 256]`.

Candidate code defines architecture only. It does not implement data loading, temporal-neighbor selection, cache reads, target derivation, loss, metrics, Artifact Filters, augmentation, sampling, training loops, persistence, resource placement, runtime downloads, or coordinate-derived features. Longitude and latitude remain forbidden provider-side channels and are not requested or reconstructed.

## Manifest policy

The manifest requests trusted sequential traversal, no augmentation, provider-owned BCE-Dice loss, AdamW learning rate 0.001, batch size 2, one epoch, and constant learning rate scheduling. A failed run due to absent/stale/incomplete temporal cache evidence should be interpreted as a trusted temporal provisioning problem rather than as a model-quality result.
