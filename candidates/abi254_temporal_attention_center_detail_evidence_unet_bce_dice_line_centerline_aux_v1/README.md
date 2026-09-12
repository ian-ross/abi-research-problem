# ABI-254 temporal attention center-detail evidence U-Net

ABI-254 is a family-development continuation of the ABI-223 temporal-attention branch for GOES ABI Contrail Segmentation.

The candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `temporal_eligible_center` frame selection. It keeps trusted source-balanced sampling, random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets.

## Architecture summary

The model starts from the compact ABI-223-style temporal-attention fusion U-Net:

- per-frame ABI/SZA normalization and approved-channel BTD features;
- lightweight attention over previous, center, and next frame embeddings;
- temporal change features from center-minus-neighbor and before/after differences;
- compact U-Net encoder, ASPP context, decoder, and mask/line/centerline heads.

ABI-254 adds a `CenterDetailEvidenceBridge` before final refinement. The bridge projects center-frame detail features, broad temporal support, horizontal/vertical line cues, and high-resolution encoder support into a bounded zero-initialized residual on the decoder feature. It is architecture-internal feature fusion only.

## Contract boundaries

Candidate code does not implement data loading, temporal lookup, temporal-cache reads, missing-frame handling, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, augmentation transforms, sampling policies, training loops, downloads, filesystem probes, coordinate features, Dataset Source identity, resource scheduling, or lifecycle behavior. Longitude and latitude are not inputs.

See `PROPOSAL.md` for hypothesis, comparison target, budget, success criteria, and fallback decision.
