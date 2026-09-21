# ABI-278 temporal-attention line-logit bridge U-Net

ABI-278 is a mechanism-changing temporal-family continuation for GOES ABI Contrail Segmentation. It uses provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection.

The model starts from the ABI-223 compact temporal-attention U-Net pattern and adds an oriented line-evidence bridge just before logits. A shared horizontal line-support filter is applied under four right-angle rotations to high-resolution decoder features; fused support features feed a bounded gated residual added to the region mask logits. Line and Centerline auxiliary heads read the same bridge features.

This Candidate defines model architecture and allowlisted manifest choices only. It does not own data loading, temporal lookup, frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling implementation, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.
