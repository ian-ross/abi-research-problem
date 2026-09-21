# ABI-297 temporal orientation-agreement correlation U-Net

ABI-297 is a bounded temporal family-development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors for offsets `[-1, 0, 1]` with trusted `temporal_eligible_center` selection.

The model follows ABI-296's differentiable local-correlation approach but constrains temporal support with orientation agreement. It computes small-displacement previous/next-to-center correlation features, preserves center-frame spectral/BTD/Solar Geometry Input detail, and then compares center-frame directional line context with temporal-support directional line context. Temporal recall support is added only through learned agreement/support gates, while disagreement contributes a bounded compact veto.

The intended effect is to retain ABI-296's fixed-threshold recall and connectivity improvement while reducing its broad, lower-precision footprint relative to stronger temporal comparators. Candidate code does not own temporal lookup, data loading, target derivation, sampling, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets.
