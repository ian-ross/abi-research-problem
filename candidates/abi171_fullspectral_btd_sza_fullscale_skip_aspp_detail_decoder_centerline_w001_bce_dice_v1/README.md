# ABI-171 full-spectral BTD+SZA full-scale skip ASPP/detail decoder centerline weight 0.01 BCE-Dice

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-154's full-spectral BTD+SZA full-scale skip ASPP/detail decoder architecture, provider-approved `abi_16ch_plus_sza` input, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, and 12-epoch representative capped budget.

The controlled manifest change is lowering the provider-derived Centerline Target auxiliary loss weight from 0.02 to 0.01. ABI-154's whole-validation diagnostic showed a useful precision/connectivity profile but under-recall at the fixed threshold. A lower centerline auxiliary weight tests whether slightly relaxing narrow centerline supervision recovers recall and source balance while preserving full-scale skip positive-area discipline, without adding candidate-owned thresholding, losses, targets, sampling, Artifact Filters, or postprocessing.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and it receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
