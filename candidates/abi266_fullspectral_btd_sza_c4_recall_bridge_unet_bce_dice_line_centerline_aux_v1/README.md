# ABI-266 full-spectral BTD+SZA C4 recall-bridge U-Net

ABI-266 is a mechanism-changing continuation of the C4 steerable line-context branch. It keeps provider-approved ABI+SZA inputs, trusted BCE-Dice training, and Line/Centerline auxiliary targets, while adding a lightweight gated recall bridge to raise under-confident contrail evidence at the model-logit level.

The Candidate defines architecture and allowlisted manifest choices only. It does not own data loading, sampling, losses, metrics, Artifact Filters, thresholding, postprocessing, target derivation, augmentation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.
