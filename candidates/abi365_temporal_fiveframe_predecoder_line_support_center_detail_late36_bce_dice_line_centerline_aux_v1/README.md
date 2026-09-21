# ABI-365 temporal five-frame pre-decoder line-support center-detail late36

ABI-365 is a temporal-family development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`.

The model extends ABI-350's pre-decoder orientation line-support idea from three frames to five frames. A center-anchored temporal-attention stem derives near/far temporal-change evidence before decoder fusion, then orientation-aware line-support blocks inject continuity evidence into encoder skips. The intended test is whether five-frame persistence can improve connected true-contrail evidence and MIT/source-balanced recall without Candidate-owned thresholds, postprocessing, temporal lookup, data loading, losses, metrics, Artifact Filters, coordinate features, Dataset Source identity, or resource scheduling.

Trusted manifest choices use BCE-Dice primary loss, provider-owned Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW with constant learning rate, batch size 2, and a late-improving budget request with exploratory fallback.
