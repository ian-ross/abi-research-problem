# ABI-329 temporal-attention strip-token line-mixer U-Net

ABI-329 is an exploratory temporal-family scout for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

The model starts from the compact temporal-attention U-Net lineage but adds differentiable horizontal/vertical strip-token mixers in the encoder, ASPP context, and decoder. It tests whether connected line evidence can be supported inside the feature hierarchy rather than by C4 tail reinjection, thresholding, postprocessing, or Artifact Filters.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sampling, target construction, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate features, or resource scheduling.
