# ABI-197 full-spectral BTD+SZA ridge-detail bridge ASPP clDice loss-policy probe

Candidate `abi197_fullspectral_btd_sza_ridge_detail_bridge_aspp_cldice_line_centerline_aux_v1` is a controlled trusted-loss-policy continuation of ABI-196.

It keeps the ABI-196 architecture and in-contract setup unchanged: provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel-derived BTD features, `RidgePreservingDetailBridge`, trusted Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW at 0.0003, batch size 4, and constant learning rate.

The intended research change is selecting the trusted `bce_dice_cldice` primary loss instead of `bce_dice` for one exploratory 12-epoch run. The hypothesis is that the provider-owned clDice component may encourage connected thin-line structure and reduce ABI-196's negative-patch false-positive burden while preserving the ridge-detail bridge's stronger MIT/source-balance and median positive-patch recall.

This Candidate does not use longitude/latitude, data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, filesystem writes, network access, runtime downloads, or Candidate-owned scheduling.
