# ABI-097 full-spectral BTD frequency-gated line U-Net negative-bias focal-Tversky continuation

Candidate Experiment for GOES ABI Contrail Segmentation. This candidate preserves the ABI-068 frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD planes, trusted `focal_tversky` primary loss, combined source-balanced sampling, trusted `random_mirroring`, and provider-derived `centerline_logits` auxiliary output at weight 0.02.

The controlled change is a gentle conservative initialization of the primary mask and centerline output biases (`mask_head.bias = -0.75`, `centerline_head.bias = -1.25`). The hypothesis is that ABI-068's full-validation negative-patch clutter may be partly an optimization/calibration starting-point issue: a mild negative logit prior should discourage early broad positives while focal-Tversky and centerline supervision can still learn thin contrail evidence. This is capped family-development evidence, not a full-data promotion claim.

All data loading, split logic, sampling implementation, augmentation implementation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned. The model receives no longitude, latitude, or reconstructed coordinate inputs.
