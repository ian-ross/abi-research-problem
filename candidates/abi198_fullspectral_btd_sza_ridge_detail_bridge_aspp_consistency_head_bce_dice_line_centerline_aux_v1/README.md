# ABI-198 full-spectral BTD+SZA ridge-detail bridge ASPP consistency head

Candidate `abi198_fullspectral_btd_sza_ridge_detail_bridge_aspp_consistency_head_bce_dice_line_centerline_aux_v1` is an exploratory family-development continuation of ABI-196.

It keeps the ABI-196 in-contract setup: provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel-derived BTD features, signed-detail streams, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, trusted BCE-Dice primary loss, trusted Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW at 0.0003, batch size 4, 12 exploratory epochs, and constant learning rate.

The architecture-only change is a differentiable `ConsistencyCalibratedMaskHead`. The model predicts `line_logits` and `centerline_logits` as auxiliary outputs, then uses their soft sigmoid/tanh support to gate a small learned residual on top of a base mask-logit head. This is intended to test whether learned line/centerline consistency can reduce unsupported false-positive texture without candidate-owned thresholding or postprocessing.

This Candidate does not use longitude/latitude, data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, filesystem writes, network access, runtime downloads, or Candidate-owned scheduling.
