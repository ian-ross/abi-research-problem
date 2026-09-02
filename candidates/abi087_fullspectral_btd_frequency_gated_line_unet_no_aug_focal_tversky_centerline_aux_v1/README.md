# ABI-087 full-spectral BTD frequency-gated line U-Net no-augmentation focal-Tversky continuation

This Candidate Experiment keeps the ABI-068 frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD planes, trusted focal-Tversky primary loss, trusted Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling, AdamW learning rate 0.0003, batch size 4, 12 epochs, and constant-LR scheduler. The controlled change is selecting the trusted `none` augmentation policy instead of `random_mirroring`.

It does not use longitude/latitude inputs, candidate-owned data loading, custom losses, custom targets, metrics, thresholding, Artifact Filters, postprocessing, network access, resource placement, or pretrained weights.
