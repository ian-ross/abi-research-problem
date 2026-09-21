# ABI-335 temporal calibrated dual-evidence line-gate U-Net

ABI-335 is a bounded family-development Candidate Experiment for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection over offsets `[-1, 0, 1]`.

The candidate continues the ABI-331/332 compact temporal persistence/detail branch after ABI-334 showed that recall can be raised by focal-Tversky but at the cost of broad low-precision, weakly connected predictions. ABI-335 returns to trusted `bce_dice` and changes the architecture head: a calibrated dual-evidence gate raises uncertain mask logits only when high-resolution line context, centerline evidence, center-frame detail, and temporal persistence support agree, while a learned disagreement veto suppresses broad support/detail mismatches.

Candidate code defines architecture only. It does not own data loading, temporal lookup, sampling, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or training lifecycle behavior.
