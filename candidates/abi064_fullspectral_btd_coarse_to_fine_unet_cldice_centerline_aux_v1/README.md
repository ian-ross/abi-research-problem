# ABI-064 full-spectral BTD coarse-to-fine U-Net

Family-scout Candidate for GOES ABI Contrail Segmentation. The model uses only provider-approved full-spectral ABI channel inputs, explicit thermal BTD planes derived from those channels, and a learned spectral mixer. It adds an internal 64-pixel soft mask prior that gates a full-resolution decoder refiner before emitting `mask_logits` and the provider-derived `centerline_logits` auxiliary output.

The coarse prior is part of the neural architecture only: it is not thresholding, postprocessing, metric logic, target derivation, or an Artifact Filter.
