# ABI-096 full-spectral BTD frequency-gated line U-Net deterministic-shuffle focal-Tversky continuation

Data-policy Candidate for GOES ABI Contrail Segmentation. This candidate preserves the ABI-068 frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD planes, trusted `focal_tversky` primary loss, and provider-derived `centerline_logits` auxiliary output at weight 0.02. The controlled change is the manifest-selected trusted sampling policy: `deterministic_shuffle` instead of `combined_source_balanced`.

The hypothesis is that a less positive/source-balanced training traversal may expose more ordinary negative ABI Patches during the fixed 12-epoch budget, reducing ABI-068 whole-validation negative-patch clutter and improving precision/connectivity while retaining enough recall through focal-Tversky and centerline supervision. This is capped family-development/data-policy evidence, not a full-data promotion claim.

All data loading, split logic, sampling implementation, augmentation implementation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned. The model receives no longitude, latitude, or reconstructed coordinate inputs.
