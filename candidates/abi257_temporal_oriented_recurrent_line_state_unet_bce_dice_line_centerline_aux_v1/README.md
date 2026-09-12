# ABI-257 temporal oriented recurrent line-state U-Net

ABI-257 is a mechanism-changing temporal recurrent family-development Candidate for GOES ABI Contrail Segmentation. It uses provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model starts from the compact ABI-255 bidirectional ConvGRU temporal change-state U-Net and moves line-continuity support into the temporal stem. Each frame embedding is processed by a learnable oriented line bank, and a center-anchored temporal line delta is fused with bidirectional recurrent state plus explicit before/after change evidence before the encoder. The goal is to improve the thin-line continuity weakness seen in ABI-255 diagnostics without candidate-owned thresholding, morphology, postprocessing, Artifact Filters, temporal lookup, data loading, or sampling.

Training uses trusted BCE-Dice loss, trusted Line and Centerline auxiliary targets, source-balanced sampling, trusted random mirroring, batch size 2, constant learning rate, and the 12-epoch exploratory budget.
