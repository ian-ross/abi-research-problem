# ABI-282 temporal C4 detail-continuity U-Net

ABI-282 is a temporal-family development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection.

The model keeps a compact temporal-attention U-Net backbone, then adds a differentiable C4 rotation-shared detail-continuity head. The head compares high-resolution temporal decoder features with center-frame ABI/SZA/BTD detail features, applies rotation-shared anisotropic line context, and emits `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

This Candidate does not implement data loading, temporal lookup, frame repair, sample selection, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, target derivation, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior. Those remain Harness/provider owned.
