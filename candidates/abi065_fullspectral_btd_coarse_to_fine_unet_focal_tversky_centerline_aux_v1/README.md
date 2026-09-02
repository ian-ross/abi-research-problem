# ABI-065 full-spectral BTD coarse-to-fine U-Net focal-Tversky continuation

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps the ABI-064 full-spectral BTD coarse-to-fine U-Net architecture unchanged and changes only the trusted primary loss from `bce_dice_cldice` to `focal_tversky`, retaining the provider-derived `centerline_logits` auxiliary output with trusted weighted-BCE weight 0.02.

The coarse prior is part of the neural architecture only: it is not thresholding, postprocessing, metric logic, target derivation, or an Artifact Filter. The model uses only provider-approved `abi_16ch` inputs and BTD planes derived from ABI channels 1-16.
