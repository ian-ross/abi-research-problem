# ABI-195 full-spectral BTD+SZA ridge-detail bridge ASPP

Candidate `abi195_fullspectral_btd_sza_ridge_detail_bridge_aspp_bce_dice_line_centerline_aux_v1` is a bounded family-development continuation of the signed-detail full-scale skip ASPP lineage.

It keeps the ABI-184 in-contract setup: provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel-derived BTD features, trusted BCE-Dice primary loss, trusted Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW at 0.0003, batch size 4, and 12 exploratory epochs.

The architecture-only change is `RidgePreservingDetailBridge`, an additive high-resolution bridge that fuses decoder context with signed-detail and stem features before final line-aware refinement. The bridge uses horizontal/vertical ridge convolutions and smoothed context, with a zero-initialized residual projection to begin close to the ABI-184 reference while allowing training to learn continuity-preserving detail updates.

This Candidate does not use longitude/latitude, data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, filesystem writes, network access, runtime downloads, or Candidate-owned scheduling.
