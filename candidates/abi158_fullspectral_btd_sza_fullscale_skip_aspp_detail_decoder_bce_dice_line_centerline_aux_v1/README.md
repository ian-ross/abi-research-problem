# ABI-158 full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice Line+Centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-154's full-spectral BTD+SZA full-scale skip ASPP/detail decoder, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and 12-epoch representative capped budget.

The controlled change is adding a provider-derived `line` auxiliary target head at low trusted `weighted_bce` weight 0.01 alongside the existing `centerline` auxiliary target at weight 0.02. The hypothesis is that explicit line-region supervision may raise fixed-threshold recall and continuity from ABI-154's high-precision/full-scale-skip feature stack without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, target transforms, losses, metrics, or sampling logic.

Inputs are provider-approved GOES ABI channels 1-16 plus Solar Geometry Input only. Longitude, latitude, reconstructed coordinate features, Dataset Source identity, pretrained weights, network access, and runtime downloads are not used.
