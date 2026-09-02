# ABI-180 Full-Spectral BTD+SZA UPerNet Directional Line-Context BCE-Dice Line+Centerline Auxiliary v1

ABI-180 is a focused UPerNet-family continuation for GOES ABI Contrail Segmentation. It keeps ABI-179's UPerNet-style pyramid/detail hierarchy and adds additive directional line-context propagation plus trusted Line and Centerline auxiliary supervision to address ABI-179's weak filtered connectivity and MIT retention.

It uses only provider-approved `abi_16ch_plus_sza` tensors. The model front end normalizes GOES ABI channels 1-16, derives deterministic thermal BTD planes from those approved ABI channels, adds normalized/cosine Solar Geometry Input features, and learns a small 1x1 spectral projection. Longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights are not candidate inputs.

The architecture includes:

- a compact residual encoder;
- bottleneck pyramid pooling at 1/2/4 pooled scales;
- a top-down UPerNet-style lateral feature pyramid;
- high-resolution signed-detail feature fusion; and
- a final non-postprocessing directional line-context refiner that uses fixed feature-space averages along horizontal, vertical, and both diagonal orientations with a bounded additive residual.

The manifest keeps trusted BCE-Dice primary loss, provider-derived Line Target auxiliary supervision with `weighted_bce` at weight 0.01, provider-derived Centerline Target auxiliary supervision with `weighted_bce` at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW at learning rate 0.0003, batch size 4, max epochs 12, and constant learning rate. Provider/Harness code owns data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, Artifact Filters, resource placement, training lifecycle, and prediction retention.
