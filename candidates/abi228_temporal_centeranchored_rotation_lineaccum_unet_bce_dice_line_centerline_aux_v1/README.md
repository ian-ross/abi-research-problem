# ABI-228 temporal center-anchored rotation-aware line accumulation U-Net

Candidate Experiment for GOES ABI Contrail Segmentation. This scout consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and predicts `mask_logits` plus trusted Line/Centerline auxiliary outputs.

The model tests whether center-anchored temporal residual support plus differentiable multi-orientation line accumulation can align thin-contrail continuity with filtered Dice better than ABI-227's temporal-line consistency gate. Candidate code is architecture-only and does not own data loading, temporal provisioning, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinates, Dataset Source identity, downloads, or resource scheduling.
