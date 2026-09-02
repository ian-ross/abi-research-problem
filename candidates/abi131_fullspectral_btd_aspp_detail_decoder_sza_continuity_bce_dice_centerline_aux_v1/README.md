# ABI-131 SZA-aware full-spectral BTD ASPP/detail decoder with continuity bridge

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-130's provider-approved `abi_16ch_plus_sza` input, normalized ABI/BTD/SZA front end, compact ASPP/detail encoder-decoder, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, and low-weight provider-derived Centerline Target auxiliary head.

The controlled architecture change is an identity-initialized multi-directional continuity bridge after the existing line-aware refinement block. The bridge adds learned horizontal, vertical, dilated, and high-frequency residual context to the feature map before the mask and centerline heads. Its final projection is initialized to zero so the model begins equivalent to the ABI-130 head path, then can learn continuity/detail corrections during training.

The hypothesis is that this neutral continuity bridge can retain ABI-130's SZA-driven MIT recall and default-threshold aggregate Dice while recovering some ABI-126/ABI-066 connectivity and negative-patch discipline. It does not implement thresholding, postprocessing, Artifact Filters, candidate-owned losses, or candidate-owned target transforms.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
