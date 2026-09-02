# ABI-108 full-spectral BTD frequency-gated line U-Net with line and centerline auxiliaries

Family-development continuation of ABI-068. This candidate keeps the full-spectral BTD frequency-gated line U-Net architecture and trusted focal-Tversky primary loss, then adds a low-weight provider-derived `line_logits` auxiliary head alongside the existing `centerline_logits` head.

The intent is to test whether trusted Line Target supervision improves thin-line connectivity or precision without candidate-owned losses, target derivation, postprocessing, thresholding, Artifact Filters, data loading, sampling, augmentation, resource placement, pretrained weights, network access, longitude inputs, or latitude inputs.
