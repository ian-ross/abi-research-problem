# ABI-287 temporal C4 recall-protected continuity bridge U-Net

ABI-287 is a mechanism-changing temporal-family continuation after ABI-286. ABI-286 showed that full-resolution continuity support can improve connected-line organization relative to the 12-epoch temporal C4 parent, but its agreement bridge traded away too much ABI-285-style recall and source balance.

This Candidate keeps the provider-owned `abi_16ch_plus_sza_temporal` input path, offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` frame selection, per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, early C4 orientation line-state injected into the encoder, ASPP bottleneck, and high-resolution directional decoder context. The new mechanism is a recall-protected full-resolution continuity sidecar: decoder appearance remains the primary mask path, line-state continuity evidence is added as a bounded residual rather than a suppressive bottleneck, and the mask head includes a small non-negative line-evidence lift initialized near zero.

Hypothesis: a non-suppressive continuity sidecar can recover more fixed-threshold recall/source balance than ABI-286 while retaining useful connected thin-line support from ABI-285/286-style temporal C4 orientation states.

This is an exploratory/default-budget Candidate, not a promotion claim. Candidate code remains architecture-only and does not implement thresholds, morphology, postprocessing, Artifact Filters, metrics, losses, data loading, temporal lookup, frame repair/padding, sample selection, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.
