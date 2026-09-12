# ABI-264 selective axial line-memory U-Net

ABI-264 is a bounded family scout for GOES ABI Contrail Segmentation. It tests a compact single-frame state-space-style line-continuity mechanism: learned-gated axial prefix-average feature states at multiple U-Net scales, fused with local line convolutions and high-resolution signed-detail evidence.

The Candidate uses only provider-approved `abi_16ch_plus_sza` tensors. It derives normalized ABI and ABI-channel BTD features inside model architecture, requests trusted Line and Centerline auxiliary targets, and uses trusted `bce_dice`, source-balanced sampling, random mirroring, AdamW, and constant learning rate.

Candidate code does not implement data loading, splits, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

Primary comparison context: ABI-260 compact MaxViT, ABI-262/263 overlap SegFormer variants, ABI-249 C4 whole-validation comparator, and ABI-202 aggregate frontier.
