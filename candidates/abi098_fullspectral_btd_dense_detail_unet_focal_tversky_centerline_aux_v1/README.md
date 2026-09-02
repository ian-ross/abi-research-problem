# ABI-098 full-spectral BTD dense-detail U-Net focal-Tversky centerline auxiliary

ABI-098 is a representative-capped family scout for GOES ABI Contrail Segmentation. It tests whether compact dense local feature reuse and high-resolution detail refinement can preserve thin ABI/BTD line evidence better than recent suppressor or calibration branches.

The candidate uses only provider-approved `abi_16ch` inputs, emits `mask_logits` plus `centerline_logits`, and selects trusted `focal_tversky`, `combined_source_balanced` sampling, `random_mirroring`, AdamW, batch size 4, 12 epochs, and constant LR in `manifest.yaml`. Candidate code owns model architecture only and does not implement data loading, losses, metrics, target derivation, augmentation, thresholding, Artifact Filters, resource placement, network access, pretrained weights, or coordinate inputs.
