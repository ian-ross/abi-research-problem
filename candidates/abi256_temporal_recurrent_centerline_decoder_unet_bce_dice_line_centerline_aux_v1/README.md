# ABI-256 temporal recurrent centerline-decoder U-Net

ABI-256 is a mechanism-changing temporal family-development Candidate after ABI-255. It keeps the provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`, but adds a high-resolution centerline-preserving decoder bridge before the logits.

The model reuses the compact bidirectional ConvGRU-style temporal change-state stem because ABI-255 showed near-frontier temporal overlap and source-informative behavior. The new decoder bridge fuses refined decoder features, the full-resolution skip, temporal-stem evidence, and learnable horizontal/vertical/dilated directional context to sharpen line evidence before the mask and trusted Line/Centerline auxiliary heads.

Candidate code remains architecture-only. It does not implement data loading, temporal lookup, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
