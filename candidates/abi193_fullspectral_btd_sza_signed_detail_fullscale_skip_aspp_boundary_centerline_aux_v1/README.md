# ABI-193 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Boundary+Centerline Auxiliary v1

ABI-193 is a contract-compliant auxiliary-policy probe of the ABI-181 signed-detail full-scale skip ASPP decoder. It keeps approved `abi_16ch_plus_sza` inputs, deterministic approved-channel BTD features, signed detail streams, ASPP context, full-scale skip fusion, and line-aware refinement, then adds a low-weight provider-derived Boundary Target head alongside the existing Centerline Target head.

The intended test is whether boundary supervision improves precision, connectivity, and negative-patch clutter relative to ABI-181/192 without the larger recall loss observed in ABI-184 line+centerline supervision. Candidate code defines architecture only; the provider/Harness owns data loading, splits, capped selection, sampling, augmentation, losses, metrics, Artifact Filters, thresholding, prediction retention, resources, and lifecycle.

Requested budget: one sequential exploratory capped Run with `bce_dice`, Boundary Target `weighted_bce` weight 0.01, Centerline Target `weighted_bce` weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, and constant learning rate.
