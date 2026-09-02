# ABI-133 full-spectral BTD+SZA ASPP/detail decoder BCE-Dice Line+Centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-130's SZA-aware compact ASPP/detail encoder-decoder, normalized raw ABI plus deterministic thermal BTD plus Solar Geometry Input front end, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, and 12-epoch representative capped budget.

The controlled change is adding provider-derived Line Target auxiliary supervision alongside the existing Centerline Target auxiliary head, both with trusted `weighted_bce` weight 0.02. The model emits `mask_logits`, `centerline_logits`, and `line_logits` from the same refined feature map.

The hypothesis is that low-weight Line Target supervision can recover some connectivity and negative-patch discipline lost by ABI-130's SZA recall calibration, without adding candidate-owned thresholding, postprocessing, data loading, target derivation, losses, metrics, Artifact Filters, resource placement, or lifecycle behavior.

Candidate inputs are only provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. Longitude, latitude, reconstructed coordinate features, Dataset Source identity, and raw data access are not used.
