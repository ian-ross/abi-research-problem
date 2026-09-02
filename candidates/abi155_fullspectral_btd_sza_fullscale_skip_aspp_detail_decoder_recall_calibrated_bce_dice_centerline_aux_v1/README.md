# ABI-155 full-spectral BTD+SZA full-scale skip ASPP/detail decoder recall-calibrated BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-154's full-spectral BTD+SZA full-scale skip ASPP/detail decoder, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, and provider-derived Centerline Target auxiliary head at weight 0.02.

The controlled architecture change is a conservative recall-calibrated mask-logit head. The head keeps a direct base mask projection from refined full-scale features and adds only a bounded learned local residual plus a small trainable logit bias. It is intended to test whether ABI-154's whole-validation lower-threshold recall upside can be moved toward the Harness fixed threshold without candidate-owned thresholding, Artifact Filters, postprocessing, data loading, losses, metrics, target transforms, or sampling logic.

Inputs are provider-approved GOES ABI channels 1-16 plus Solar Geometry Input only. Longitude, latitude, reconstructed coordinate features, Dataset Source identity, pretrained weights, network access, and runtime downloads are not used.
