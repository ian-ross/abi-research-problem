# ABI-291 temporal five-frame persistence-attention directional U-Net

ABI-291 is an exploratory temporal-family scout for GOES ABI Contrail Segmentation. It extends the finite ABI-238 temporal-attention directional U-Net from the provider-owned three-frame window to the allowlisted five-frame `[-2, -1, 0, 1, 2]` ABI+Solar Geometry Input window.

The architecture keeps Candidate code inside the model boundary: bounded per-frame ABI/SZA/BTD feature construction, shared frame projection, five-frame persistence-aware temporal attention, compact U-Net/ASPP decoding, and a high-resolution directional-context bridge with primary mask plus trusted Line and Centerline auxiliary heads.

It relies on the Harness/provider for data loading, temporal cache eligibility, sampling, augmentation, losses, metrics, Artifact Filters, target derivation, thresholds, resource limits, execution, and lifecycle management. It does not use longitude, latitude, Dataset Source identity, candidate-owned temporal lookup, or postprocessing.
