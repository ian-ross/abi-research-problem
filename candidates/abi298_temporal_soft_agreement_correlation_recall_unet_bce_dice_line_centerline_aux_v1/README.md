# ABI-298 temporal soft-agreement correlation recall U-Net

ABI-298 is a bounded temporal family-development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors for offsets `[-1, 0, 1]` with trusted `temporal_eligible_center` selection.

The model follows ABI-296's differentiable local-correlation approach and ABI-297's orientation-agreement evidence, but changes the mechanism: orientation agreement is a soft additive calibration signal rather than a hard temporal-support veto. The head keeps center/detail recall paths active, boosts temporal support when center-frame and temporal directional line context agree, and applies only a small bounded disagreement penalty.

The intended effect is to retain ABI-296's fixed-threshold recall and connectivity support while avoiding ABI-297's recall suppression and reducing ABI-296's broad lower-precision footprint. Candidate code does not own temporal lookup, data loading, target derivation, sampling, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets.
