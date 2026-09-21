# ABI-331 temporal persistence/detail line-gate U-Net

ABI-331 is a bounded exploratory Candidate Experiment for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection over offsets `[-1, 0, 1]`.

The model tests a cheaper alternative to the resource-failed ABI-329/330 strip-token branch. Instead of full-resolution strip-token mixing, it builds a compact temporal persistence stem from center-vs-neighbor agreement, neighbor mean support, and center-frame signed detail. The decoder head adds only a bounded architecture-internal positive line/detail residual when mask uncertainty, line logits, centerline logits, center detail, and temporal support agree, with a small clutter veto when support is weak.

Candidate code defines architecture only. It does not own data loading, temporal lookup, sampling, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or training lifecycle behavior.
