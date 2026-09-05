# ABI-191 Full-Spectral BTD+SZA Directional-Lattice Full-Scale ASPP

ABI-191 is an exploratory family-development continuation of ABI-181. It keeps the signed-detail full-scale skip ASPP backbone, provider-approved `abi_16ch_plus_sza` input, deterministic BTD features from approved ABI channels 1-16, trusted `bce_dice`, provider-derived Centerline Target auxiliary supervision, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, and constant learning rate.

The research change is a conservative multi-orientation directional lattice bridge inserted before the final line-aware refinement. The bridge propagates high-resolution features along horizontal, vertical, and diagonal neighborhoods using learned convolutional branches and zero-padded feature shifts, then applies a zero-initialized bounded residual. It is intended to recover connected-line structure and MIT-source detail without adding Line Target auxiliary conservatism or Candidate-owned thresholding.

The candidate does not implement data loading, split logic, capped-record selection, sampling policy, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle behavior.
