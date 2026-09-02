# ABI-070 full-spectral BTD frequency-gated line U-Net centerline-guided focal-Tversky continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate starts from ABI-068, the current strongest local whole-validation-tested frequency-gated line U-Net branch, and makes one controlled architecture change: the final mask head becomes a bounded centerline-guided residual head.

The direct mask-logit path remains the primary output path. A small additive residual, initialized to zero and bounded by `0.20 * tanh(...)`, is gated by the jointly trained provider-derived centerline auxiliary output. The intent is to recover some of ABI-066's continuity/precision profile without repeating ABI-069's subtractive confidence suppressor, which reduced useful line connectivity.

The candidate uses provider-approved `abi_16ch` inputs, normalized raw ABI channels, brightness-temperature-difference planes derived only from ABI channels 1-16, and learned spectral mixing. It receives no longitude, latitude, reconstructed coordinate inputs, source metadata, or raw data paths.

All data loading, split logic, sampling, augmentation, losses, auxiliary target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
