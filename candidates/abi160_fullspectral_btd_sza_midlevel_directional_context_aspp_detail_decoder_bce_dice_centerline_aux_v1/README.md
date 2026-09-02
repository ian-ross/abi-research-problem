# ABI-160 full-spectral BTD+SZA mid-level directional-context ASPP/detail decoder

ABI-160 is a controlled family-development continuation of the SZA-aware ASPP/detail decoder branch. It starts from the ABI-130 architecture and inserts a bounded mid-level directional context module after the 64 x 64 encoder block and before the deepest ASPP bottleneck.

The model uses only provider-approved `abi_16ch_plus_sza` inputs: GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal brightness-temperature-difference planes from approved ABI channels inside the model and never consumes longitude or latitude.

The candidate keeps the trusted BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling traversal, trusted random mirroring, AdamW at learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, and disabled early stopping. Provider/Harness code retains ownership of data loading, leakage-safe split, capped record selection, augmentation implementation, target derivation, losses, metrics, thresholding, Artifact Filters, execution resources, and lifecycle.
