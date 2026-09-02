# ABI-124 full-spectral BTD frequency-gated line U-Net stem detail-agreement

ABI-124 is a controlled family-development continuation of ABI-068 (`run_20260828_010836_4ccc77`). It keeps the provider-approved full ABI Channel Input (`abi_16ch`), deterministic raw-plus-BTD front end using only ABI channels 1-16, frequency-gated line U-Net backbone, trusted `focal_tversky` loss, provider-derived Centerline Target auxiliary output at weight 0.02, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping.

The only architectural change is a neutral-initialized pixelwise stem detail-agreement calibrator. The calibrator compares full-resolution stem features, high-frequency detail, and smoothed context, then adds a small bounded residual. It is initialized as an exact no-op so the Run starts from ABI-068-like behavior and can learn only if early detail/context agreement helps reduce negative-patch clutter while preserving line recall.

The Candidate does not use longitude/latitude, candidate-owned data loading, losses, metrics, target derivation, augmentation, thresholding, postprocessing, Artifact Filters, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.
