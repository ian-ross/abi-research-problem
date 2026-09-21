# ABI-281 temporal-attention center-detail agreement U-Net

ABI-281 is a mechanism-changing temporal-family continuation for GOES ABI Contrail Segmentation. It uses provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection.

The model returns to the compact ABI-223 temporal-attention U-Net pattern and adds a center-frame detail agreement head before logits. The head projects provider-visible center-frame ABI/SZA/BTD features, compares them with the temporal decoder refinement, and learns bounded agreement-conditioned logit residuals plus Line and Centerline auxiliary logits. The intent is to recover true center-frame thin-line evidence that temporal attention leaves below threshold without repeating ABI-278's final line-logit bridge or ABI-274's fragmented early line-state path.

This Candidate defines model architecture and allowlisted manifest choices only. It does not own data loading, temporal lookup, frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling implementation, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.
