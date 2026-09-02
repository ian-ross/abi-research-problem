# ABI-055 Full-Spectral BTD High-Resolution Line U-Net Directional Refiner

ABI-055 is a controlled family-development continuation of ABI-053/054. It keeps the approved `abi_16ch` input path, normalized raw-channel plus thermal-BTD front end, trusted `bce_dice_cldice` primary loss, provider-derived `centerline` auxiliary target at weight 0.02, source-balanced sampling, trusted random mirroring, AdamW at 0.0003, batch size 4, and 12 capped epochs.

The architecture-level change is replacing the prior full-resolution isotropic multi-dilation refiner with a directional continuity refiner. The new refiner uses horizontal and vertical 1x7, 7x1, 1x15, and 15x1 convolution branches plus a learned feature gate before the final residual projection. This is intended to preserve elongated thin-line evidence inside the model without candidate-owned postprocessing, skeletonization, artifact filtering, target derivation, or metric logic.

The candidate emits primary `mask_logits` and auxiliary `centerline_logits` only. Longitude, latitude, solar geometry, data loading, splits, capped-record selection, augmentation transforms, losses, metrics, checkpointing, Artifact Filters, prediction retention, and execution lifecycle remain provider/Harness-owned.
