# ABI-071 full-spectral BTD frequency-gated line U-Net soft-evidence-gate focal-Tversky continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate starts from ABI-068, the strongest local whole-validation-tested frequency-gated line U-Net branch, and adds one controlled architecture change: a neutral-initialized, low-amplitude soft evidence gate in feature space before the primary mask head.

The soft gate uses refined decoder features, high-frequency detail, broad smoothed context, and the jointly trained provider-derived centerline auxiliary prediction to apply a small bounded feature residual. It is initialized as an identity path so training starts from the ABI-068 operating point rather than from a pre-suppressed detector. The intent is to recover some of ABI-066's precision/connectivity and reduce ABI-068's negative-patch clutter without repeating ABI-069's over-suppressive confidence head or ABI-070's output-logit residual tradeoff.

The candidate uses provider-approved `abi_16ch` inputs, normalized raw ABI channels, brightness-temperature-difference planes derived only from ABI channels 1-16, and learned spectral mixing. It receives no longitude, latitude, reconstructed coordinate inputs, source metadata, or raw data paths.

All data loading, split logic, sampling, augmentation, losses, auxiliary target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
