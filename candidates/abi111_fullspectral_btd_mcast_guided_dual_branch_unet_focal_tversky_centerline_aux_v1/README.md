# ABI-111 full-spectral BTD MCAST-guided dual-branch U-Net

ABI-111 is a family-scout Candidate Experiment for GOES ABI Contrail Segmentation. It keeps provider-approved `abi_16ch` input, derives deterministic thermal BTD planes from GOES ABI channels 1-16, and adds a separate MCAST-like thermal support branch using approved ABI channels 11, 14, and 13-minus-15. The branch is fused inside the architecture through soft feature-space guidance gates rather than candidate-owned thresholding or postprocessing.

The Run should use trusted `focal_tversky` primary loss, provider-derived `centerline_logits` auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` sampling, trusted `random_mirroring`, batch size 4, 12 epochs, constant learning rate, and the Harness-owned representative capped-record policy.

This scout tests whether a robust MCAST-lineage thermal support stream can improve calibration and false-positive discipline relative to recent local ABI-068 head/front-end tweaks while preserving the stronger full-spectral BTD recall and source balance. Candidate code owns only model architecture and uses no longitude/latitude inputs, data loading, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, thresholding, postprocessing, resource placement, filesystem writes, network access, or pretrained weights.
