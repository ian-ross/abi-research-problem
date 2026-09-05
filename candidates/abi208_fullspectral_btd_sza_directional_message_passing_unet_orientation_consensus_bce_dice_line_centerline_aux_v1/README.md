# ABI-208 orientation-consensus directional message-passing U-Net

Family-development continuation of ABI-207 for GOES ABI Contrail Segmentation. The candidate keeps the provider-approved full-spectral ABI+SZA input, trusted source-balanced sampling/augmentation, BCE-Dice primary loss, and Line plus Centerline auxiliary supervision, but replaces broad directional residual mixing with a lighter orientation-consensus message block and a smaller base width.

Candidate code defines model architecture only. It does not implement data loading, target derivation, custom losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, coordinates, runtime downloads, persistence writes, or scheduling.
