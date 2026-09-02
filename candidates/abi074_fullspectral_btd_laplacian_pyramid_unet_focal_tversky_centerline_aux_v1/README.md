# ABI-074 full-spectral BTD Laplacian-pyramid U-Net focal-Tversky centerline-aux scout

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate uses provider-approved `abi_16ch` inputs, ABI-channel-derived thermal BTD planes, and a learned 1x1 spectral mixer, then replaces the recent frequency-gated/head-stacking direction with a U-Net that repeatedly mixes narrow, middle, and broad Laplacian-style bandpass feature bands inside the stem, encoder, bottleneck, decoder, and full-resolution fusion block.

The hypothesis is that multi-scale bandpass feature fusion can recover some of ABI-068's lost precision/connectivity without adding more output heads, suppressive post-decoder gates, thresholding, Artifact Filters, postprocessing, target derivation, losses, sampling, or augmentation to Candidate code. The model emits primary `mask_logits` and one provider-derived `centerline_logits` auxiliary output.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned. The model receives no longitude, latitude, reconstructed coordinate inputs, external data paths, network resources, or pretrained weights.
