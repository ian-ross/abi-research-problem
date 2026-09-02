# ABI-100 full-spectral BTD frequency-gated line U-Net deterministic-shuffle clDice continuation

Family-development Candidate for GOES ABI Contrail Segmentation. ABI-100 keeps the ABI-066 frequency-gated line U-Net architecture, trusted `bce_dice_cldice` primary loss, and centerline auxiliary supervision unchanged while changing the provider-owned sampling traversal from `combined_source_balanced` to `deterministic_shuffle`.

The hypothesis is that the deterministic-shuffle data policy may improve threshold discipline, filtered precision, or line connectivity for the precision-forward clDice branch without candidate-owned thresholding or postprocessing. The model uses only provider-approved ABI channels 1-16 plus BTD planes derived from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, capped-record selection, epoch sampling implementation, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
