# ABI-179 Full-Spectral BTD+SZA UPerNet Pyramid/Detail Decoder BCE-Dice Centerline Auxiliary v1

ABI-179 is a UPerNet-style pyramid/detail decoder scout for GOES ABI Contrail Segmentation.

It uses only provider-approved `abi_16ch_plus_sza` tensors. The model front end normalizes GOES ABI channels 1-16, derives deterministic thermal BTD planes from those approved ABI channels, adds normalized/cosine Solar Geometry Input features, and learns a small 1x1 spectral projection. Longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights are not candidate inputs.

The architecture replaces recent ASPP/full-scale-skip local patching with:

- a compact residual encoder;
- bottleneck pyramid pooling at 1/2/4 pooled scales;
- a top-down UPerNet-style lateral feature pyramid;
- high-resolution signed-detail feature fusion; and
- a feature-space line-context refiner before the primary `mask_logits` and auxiliary `centerline_logits` heads.

The manifest keeps trusted BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision with `weighted_bce` at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW at learning rate 0.0003, batch size 4, max epochs 12, and constant learning rate. Provider/Harness code owns data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, Artifact Filters, resource placement, training lifecycle, and prediction retention.
