# ABI-061 full-spectral BTD high-resolution line U-Net focal-Tversky continuation

Family-development continuation of ABI-058. The model keeps the full-spectral BTD high-resolution line U-Net oriented-context architecture and Centerline Target auxiliary output, but selects trusted `focal_tversky` as the primary loss to test whether a loss-policy change improves recall and source balance after decoder-head refinements underperformed.

This candidate uses only provider-approved ABI channels 1-16 and candidate-owned architecture code. It does not use longitude/latitude, custom data loading, custom losses, custom target derivation, augmentation, thresholding, Artifact Filters, or postprocessing.
