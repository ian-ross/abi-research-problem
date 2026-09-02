# ABI-085 full-spectral BTD frequency-gated line U-Net low-LR focal-Tversky continuation

This Candidate Experiment keeps the ABI-068 frequency-gated line U-Net architecture unchanged and lowers the trusted AdamW learning rate from 0.0003 to 0.0001.

It uses provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD planes, trusted focal-Tversky primary loss, trusted Centerline Target auxiliary supervision at weight 0.02, source-balanced sampling, and trusted random mirroring. It does not use longitude/latitude inputs, candidate-owned data loading, custom losses, custom targets, metrics, thresholding, Artifact Filters, postprocessing, network access, or pretrained weights.
