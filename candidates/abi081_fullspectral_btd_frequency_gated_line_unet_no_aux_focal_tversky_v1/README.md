# ABI-081 Full-spectral BTD frequency-gated line U-Net without auxiliary supervision

ABI-081 is a controlled family-development continuation of ABI-068. It keeps the full-spectral ABI plus thermal-BTD frequency-gated line U-Net architecture and trusted focal-Tversky primary loss, but removes the provider-derived centerline auxiliary target and `centerline_logits` output.

The purpose is to test whether ABI-068's centerline auxiliary supervision is helping or constraining the focal-Tversky operating point after multiple refiner/head/input follow-ups failed to improve the precision/recall/connectivity trade-off.

Contract boundaries are unchanged: no longitude or latitude inputs, no candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.
