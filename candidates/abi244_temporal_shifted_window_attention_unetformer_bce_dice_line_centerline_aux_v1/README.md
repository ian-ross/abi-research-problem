# ABI-244 temporal shifted-window attention U-NetFormer

ABI-244 is a bounded family-development continuation of the temporal/modern-backbone branch. It tests whether shifted Swin-style local attention can reduce fixed-window fragmentation seen in compact temporal window-attention models.

The Candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`; each frame contains ABI channels 1-16 plus Solar Geometry Input. The target remains the zero-offset center Contrail Mask.

Architecture summary:

- finite per-frame ABI+SZA+BTD feature builder;
- three-frame temporal attention/change fusion stem;
- compact U-NetFormer encoder/decoder with shifted-window attention blocks;
- atrous bottleneck context;
- primary `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

Candidate code is architecture-only. It does not implement data loading, temporal lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, downloads, coordinate features, Dataset Source identity, or resource scheduling.
