# ABI-265 selective axial line-memory U-Net late-improving continuation

ABI-265 is a close late-improving continuation of ABI-264 for GOES ABI Contrail Segmentation. It keeps the ABI-264 selective axial line-memory U-Net architecture unchanged and requests the approved `late_improving` budget because ABI-264 selected epoch 12 as its best checkpoint with a sharp final-epoch improvement in filtered Dice, connectivity, and both Dataset Source metrics.

The Candidate uses only provider-approved `abi_16ch_plus_sza` tensors. It derives normalized ABI and ABI-channel BTD features inside model architecture, requests trusted Line and Centerline auxiliary targets, and uses trusted `bce_dice`, source-balanced sampling, random mirroring, AdamW, and constant learning rate.

Candidate code does not implement data loading, splits, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

Primary comparison target: ABI-264 (`run_20260912_055445_9221de`). Broader context: ABI-260/262/263 broad scouts, ABI-249 C4 line-context, and ABI-202 aggregate frontier.
