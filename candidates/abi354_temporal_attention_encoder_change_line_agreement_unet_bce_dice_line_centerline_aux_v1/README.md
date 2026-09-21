# ABI-354 temporal-attention encoder change-line agreement U-Net

ABI-354 is an exploratory family-development Candidate for GOES ABI Contrail Segmentation. It follows ABI-350's temporal-attention pre-decoder line-support U-Net, but moves an additional temporal change/detail line-agreement bridge to the encoder entry so continuity evidence is available before skip features are formed.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. It keeps BCE-Dice primary loss, Line and Centerline auxiliary outputs, trusted source-balanced sampling, trusted random mirroring, AdamW, constant learning rate, and batch size 2.

The architectural question is whether early, source-agnostic temporal change plus orientation-line agreement can improve fixed-threshold connected thin-line evidence and MIT-positive-tail behavior without widening negative-patch clutter, after ABI-351 showed that a post-decoder continuity bridge was too late/unstable.

Candidate code defines model architecture only. It does not implement data loading, temporal lookup, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, Dataset Source identity, filesystem probing, networking, or resource scheduling.
