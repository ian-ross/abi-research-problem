# ABI-190 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Feature Calibration

ABI-190 is an exploratory family-development continuation of the signed-detail full-scale skip ASPP branch. It starts from the ABI-184 direct Line plus Centerline auxiliary architecture and adds a conservative feature-level line-context calibration module before the primary mask head.

The candidate keeps provider-approved `abi_16ch_plus_sza` input, deterministic BTD features from approved ABI channels 1-16, Solar Geometry Input, trusted `bce_dice`, provider-derived `line` and `centerline` auxiliary targets, combined source-balanced traversal, trusted random mirroring, AdamW at learning rate 0.0003, batch size 4, max epochs 12, and constant learning rate.

The new module does not implement thresholding, postprocessing, Artifact Filters, target derivation, sampling, augmentation, loss, metric, data loading, resource placement, or lifecycle behavior. It keeps the auxiliary logits separate and only calibrates mask-head features through a zero-initialized bounded residual path.
