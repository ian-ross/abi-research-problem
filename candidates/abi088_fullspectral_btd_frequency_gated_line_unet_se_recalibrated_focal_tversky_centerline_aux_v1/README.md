# ABI-088 full-spectral BTD frequency-gated line U-Net SE-recalibrated focal-Tversky continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-068 full-spectral BTD frequency-gated line U-Net training policy, provider-approved `abi_16ch` input, trusted `focal_tversky` primary loss, trusted `random_mirroring`, source-balanced sampling, and low-weight provider-derived `centerline_logits` auxiliary output.

The controlled architecture change is lightweight spectral-spatial recalibration inside residual feature blocks. Channel squeeze/excitation and feature-space spatial gates are applied to learned feature tensors, not to coordinates or postprocessed masks, to test whether the strong ABI-068 operating point can suppress cloud/background clutter and recover ABI-066-like precision/connectivity without a late output-side suppressor head.

The model uses only GOES ABI channels 1-16 and ABI-channel-derived thermal BTD planes. It receives no longitude, latitude, source metadata, data paths, pretrained weights, network resources, candidate-owned losses, target derivations, augmentations, metrics, thresholding, Artifact Filters, postprocessing, training loops, or resource placement authority.
