# ABI-112 full-spectral BTD line-propagation U-Net focal-Tversky continuation

ABI-112 is a family-development continuation of ABI-068. It keeps provider-approved `abi_16ch` input, deterministic approved-channel BTD features, learned 1x1 channel mixing, focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, combined source-balanced traversal, trusted random mirroring, AdamW at 0.0003, batch size 4, and 12 epochs.

The controlled architecture change is the final high-resolution refiner: it replaces ABI-068's oriented convolution refiner with non-wrapping directional feature propagation along horizontal, vertical, and diagonal straight-line paths. The goal is to improve thin-contrail continuity or precision/recall balance without candidate-owned data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, coordinates, external writes, network access, or pretrained weights.

See `PROPOSAL.md` for comparison targets, budget, and success criteria.
