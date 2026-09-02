# ABI-137 full-spectral BTD+SZA ASPP/detail decoder adaptive-logit BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This experiment preserves ABI-130's SZA-aware compact ASPP/detail decoder, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change is an additive adaptive logit-calibration mask head. The head predicts a local foreground-minus-background margin, a small local residual, and a bounded patch-context bias initialized near a mild positive offset. It is intended to test whether ABI-130's whole-validation threshold-sweep upside can be moved toward the Harness fixed threshold through trainable architecture alone, without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, losses, metrics, or target transforms.

Inputs are provider-approved GOES ABI channels 1-16 plus Solar Geometry Input only. Longitude, latitude, reconstructed coordinate features, Dataset Source identity, pretrained weights, network access, and runtime downloads are not used.
