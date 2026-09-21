# ABI-299 temporal correlation line-continuity decoder U-Net

ABI-299 is a bounded temporal family-development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors for offsets `[-1, 0, 1]` with trusted `temporal_eligible_center` selection.

The model keeps ABI-296/298's differentiable 3x3 local-correlation support between center and neighboring frames, but adds a lightweight line-continuity bridge inside the decoder/head. The bridge applies differentiable horizontal, vertical, and dilated diagonal depthwise line context to center-line, temporal-line, and multiscale decoder support. Its continuity signal is additive and gated; it is not thresholding, morphology, postprocessing, or an Artifact Filter.

The intended effect is to preserve ABI-296/298 fixed-threshold recall while improving connected thin-line organization and reducing broad local-correlation clutter. To remain resource-aware after ABI-297/298 ran close to the exploratory timeout, ABI-299 uses a compact base width of 24 rather than width 28.

Candidate code does not own temporal lookup, data loading, target derivation, sampling, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets.
