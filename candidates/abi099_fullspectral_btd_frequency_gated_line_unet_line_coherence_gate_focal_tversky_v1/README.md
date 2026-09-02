# ABI-099 full-spectral BTD frequency-gated line U-Net line-coherence gate

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-068 full-spectral BTD frequency-gated line U-Net training/data/loss setup and adds a small directional line-coherence gate after the final frequency-pyramid fusion.

The gate compares horizontal, vertical, and diagonal-like elongated feature context against smoothed blob context, then applies a bounded residual feature update before the primary and centerline heads. The hypothesis is that a trainable in-model coherence mechanism can reduce low-precision blob-like positive expansion while preserving ABI-068's focal-Tversky recall and source-balanced aggregate Dice.

The model uses only provider-approved GOES ABI channels 1-16 and BTD planes derived from those channels. It receives no longitude, latitude, or reconstructed coordinate inputs. All data loading, split logic, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
