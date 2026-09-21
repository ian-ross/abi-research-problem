# ABI-310 temporal C4 agreement-gated line-support late36

ABI-310 is a mechanism-changing family-development Candidate for GOES ABI Contrail Segmentation. It continues the profiled temporal C4 line-state U-Net branch after ABI-309 recovered fixed-threshold recall over ABI-306 but widened prediction footprint and negative-patch clutter.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It keeps the ABI-309 temporal frame feature builder, temporal attention/C4 orientation line-state stem, compact encoder/ASPP/decoder, line-state scale injectors, and high-resolution directional context. The changed mechanism is an `AgreementGatedLineSupportHead` that permits late line-state recall support only through learned mask/Line/Centerline/support agreement and includes a learned unsupported-evidence suppression term.

This Candidate performs no data loading, temporal lookup, coordinate use, target derivation, custom loss, custom metric, thresholding, postprocessing, Artifact Filtering, augmentation implementation, sampling policy implementation, downloads, or resource scheduling. It selects only trusted manifest capabilities: BCE-Dice primary loss, combined source-balanced sampling, random mirroring, constant LR AdamW, and trusted Line plus Centerline auxiliary targets.

Primary comparison targets are ABI-306 (`run_20260914_124245_de843c`) for compact high-precision temporal C4 behavior and ABI-309 (`run_20260914_205014_1794f8`) for recall-support behavior with excessive footprint. The late-improving budget request is parented to those completed late-budget Runs; if denied, the exploratory budget remains valid bounded evidence.
