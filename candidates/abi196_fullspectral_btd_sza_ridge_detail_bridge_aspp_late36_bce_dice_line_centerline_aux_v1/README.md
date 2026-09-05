# ABI-196 full-spectral BTD+SZA ridge-detail bridge ASPP late36

Candidate `abi196_fullspectral_btd_sza_ridge_detail_bridge_aspp_late36_bce_dice_line_centerline_aux_v1` is a late-improving close-continuation of ABI-195.

It keeps the ABI-195 architecture and in-contract setup unchanged: provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel-derived BTD features, `RidgePreservingDetailBridge`, trusted BCE-Dice primary loss, trusted Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW at 0.0003, batch size 4, and constant learning rate.

The only handoff change is candidate-local `budget_request.yaml`, which asks the Harness for the approved 36-epoch late-improving budget using ABI-195 Run `run_20260903_135523_8976a0` as parent evidence. If denied, the Harness should run the unchanged Candidate under the exploratory fallback budget.

This Candidate does not use longitude/latitude, data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, filesystem writes, network access, runtime downloads, or Candidate-owned scheduling.
