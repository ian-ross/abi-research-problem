# ABI-104 full-spectral BTD dual-stream line-consensus U-Net

Family-development Candidate for GOES ABI Contrail Segmentation. ABI-104 follows ABI-103's dual-stream spectral-specialization scout, which was finite and recall-positive but too low in precision and Contrail Connectivity Metric. This continuation keeps the provider-approved reflective, thermal, and ABI-channel-derived BTD streams, but replaces the final decoder refinement with a stronger consensus-gated line decoder that asks high-resolution detail, smoothed context, and horizontal/vertical/broad line branches to agree before the mask and centerline heads.

The hypothesis is that ABI-103's source-balanced recall can be retained while suppressing blob-like false positives and improving line continuity. The model uses only provider-approved ABI channels 1-16 and deterministic BTD features derived from those channels. It receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
