# ABI-115 full-spectral BTD frequency-gated line U-Net MIT-only data-policy continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate reuses the ABI-068 full-spectral BTD frequency-gated line U-Net architecture and changes only the trusted manifest sampling traversal from `combined_source_balanced` to provider-owned `mit_only`.

The hypothesis is that ABI-068's recall-forward full-validation success may still be limited by MIT-source underfitting; a MIT-only traversal can test whether extra MIT gradient emphasis improves MIT filtered Dice and connectivity without modifying candidate-owned data loading, sampling implementation, losses, targets, thresholding, metrics, Artifact Filters, augmentation, resource placement, or lifecycle behavior.

The model uses only provider-approved GOES ABI channels 1-16 plus deterministic BTD planes derived from those channels. It receives no longitude, latitude, reconstructed coordinate inputs, external files, pretrained weights, or network resources.
