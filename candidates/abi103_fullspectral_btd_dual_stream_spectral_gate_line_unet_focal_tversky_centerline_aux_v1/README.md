# ABI-103 full-spectral BTD dual-stream spectral-gate line U-Net scout

Family-scout Candidate for GOES ABI Contrail Segmentation. ABI-103 broadens away from small frequency-gated line U-Net tweaks by separating reflective ABI channels, thermal ABI channels, and deterministic ABI-channel-derived BTD planes before fusing them with learned cross-stream spectral gates and line-aware decoder context.

The hypothesis is that source-robust threshold behavior may improve if reflective cloud texture and thermal ice-cloud evidence are allowed to specialize before merger, rather than being mixed immediately by a single raw+BTD front end. The model uses only provider-approved ABI channels 1-16 and BTD features derived from those channels. It receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
