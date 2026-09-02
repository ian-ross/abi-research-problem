# ABI-116 full-spectral BTD frequency-gated line U-Net scale-selective ridge-gate continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps ABI-068's full-spectral BTD frequency-gated line U-Net, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary head, source-balanced traversal, and trusted random mirroring, then adds a low-capacity scale-selective ridge gate immediately before the mask and centerline heads.

The hypothesis is that selecting between several local residual scales and anisotropic line averages can give the final logits a cleaner thin-ridge support signal, preserving ABI-068's recall/source-balanced Dice while recovering some of ABI-066's precision, connectivity, or lower negative-patch clutter. The gate is architecture-side feature computation only; it does not implement thresholding, Artifact Filters, postprocessing, metrics, losses, target derivation, sampling, augmentation, resource placement, or lifecycle behavior.

The model uses only provider-approved GOES ABI channels 1-16 plus deterministic BTD planes derived from those channels. It receives no longitude, latitude, reconstructed coordinate inputs, external files, pretrained weights, or network resources.
