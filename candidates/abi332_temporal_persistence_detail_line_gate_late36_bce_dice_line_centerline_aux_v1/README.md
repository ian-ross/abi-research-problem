# ABI-332 temporal persistence/detail line-gate late36

ABI-332 is a late-improving continuation of ABI-331 for GOES ABI Contrail Segmentation. It keeps the same resource-safe three-frame temporal persistence/detail line-gate U-Net and consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection over offsets `[-1, 0, 1]`.

The reason for the continuation is trajectory evidence, not promotion status: ABI-331 improved over ABI-321 on aggregate/source Dice, precision, recall, connectivity, and compactness, and selected its best checkpoint at the final exploratory epoch. ABI-332 requests the approved late-improving budget to test whether the compact persistence/detail mechanism is under-trained under 12 epochs.

Candidate code defines architecture only. It does not own data loading, temporal lookup, sampling, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or training lifecycle behavior.
