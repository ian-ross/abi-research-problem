# ABI-334 temporal persistence/detail focal-Tversky U-Net

ABI-334 is a one-factor trusted loss-policy continuation of the ABI-331/332 compact three-frame temporal persistence/detail line-gate U-Net. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection over offsets `[-1, 0, 1]`.

The architecture is intentionally kept identical to the ABI-331 compact persistence/detail line-gate model: center-frame spectral/BTD/Solar Geometry Input features, neighbor mean support, center-vs-neighbor temporal-difference features, signed center detail, and a guarded line/detail head. The mechanism change is not candidate-owned loss code; the manifest selects the trusted `focal_tversky` primary loss to test whether the branch's under-recall and positive-patch tail failures are partly optimization-objective limited rather than architectural only.

Candidate code defines architecture only. It does not own data loading, temporal lookup, sampling, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or training lifecycle behavior.
