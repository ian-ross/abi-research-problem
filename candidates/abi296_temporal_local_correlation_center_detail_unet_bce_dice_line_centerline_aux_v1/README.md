# ABI-296 temporal local-correlation center-detail U-Net

ABI-296 is a bounded temporal family-development scout for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors for offsets `[-1, 0, 1]` with trusted `temporal_eligible_center` selection.

The model replaces recent temporal-attention variants with a differentiable 3x3 local-correlation mechanism between projected center-frame features and previous/next-frame features. These correlation volumes are fused with center-frame spectral/BTD/Solar Geometry Input detail and directional line context in a compact U-Net. The intended effect is to allow modest temporal displacement while preserving center-frame thin-line evidence, improving fixed-threshold recall and connectivity without candidate-owned temporal lookup, thresholding, losses, metrics, Artifact Filters, data loading, postprocessing, coordinates, or resource scheduling.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets.
