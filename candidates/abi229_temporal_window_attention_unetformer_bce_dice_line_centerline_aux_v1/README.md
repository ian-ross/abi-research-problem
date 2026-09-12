# ABI-229 temporal window-attention U-NetFormer

Candidate Experiment for GOES ABI Contrail Segmentation. This family scout consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and predicts `mask_logits` plus trusted Line/Centerline auxiliary outputs.

The model tests whether compact Swin/UNetFormer-style local window attention can improve temporal contrail segmentation relative to the prior convolution-heavy temporal U-Net scouts. It keeps center-frame anchoring and learned temporal change evidence, then uses hierarchical local window self-attention in the encoder/bottleneck/decoder to distinguish persistent thin contrails from local cloud texture and static-looking clutter. Candidate code is architecture-only and does not own data loading, temporal provisioning, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinates, Dataset Source identity, downloads, or resource scheduling.
