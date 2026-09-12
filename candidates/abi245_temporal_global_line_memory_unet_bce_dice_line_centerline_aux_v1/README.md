# ABI-245 temporal global line-memory U-Net

ABI-245 is a bounded sequential family-development Candidate for GOES ABI Contrail Segmentation. It tests whether a differentiable full-resolution row/column/coarse line-memory module can improve thin-contrail continuity in the provider-owned temporal attention branch.

The model consumes only the trusted `abi_16ch_plus_sza_temporal` input mode with offsets `[-1, 0, 1]` and `temporal_eligible_center` frame selection. Each frame contributes ABI channels 1-16 plus Solar Geometry Input; longitude and latitude are not used. Per-frame finite ABI/SZA/BTD features feed a center-anchored temporal attention/change stem, compact U-Net encoder/decoder, ASPP bottleneck, and high-resolution directional-context decoder. ABI-245 then adds `GlobalLineMemory`, which derives row-wise, column-wise, and coarse pooled memories from decoder activations and gates them back into the full-resolution feature map before the mask, Line, and Centerline heads.

This Candidate keeps all training/data/evaluation behavior Harness-owned: no data loading, temporal lookup, cache reads, missing-frame repair, target derivation, custom loss, metric, Artifact Filter, thresholding, morphology, postprocessing, augmentation implementation, sampling policy implementation, training loop, downloads, coordinate features, Dataset Source identity, or resource scheduling is implemented in Candidate code.

## Intended comparison

Compare against ABI-244 (`run_20260911_072719_ade068`), ABI-238 (`run_20260911_004137_f54c45`), ABI-240 (`run_20260911_031326_43ed12`), ABI-223 (`run_20260908_154531_8c7e2b`), and ABI-202 (`run_20260904_043143_ee0005`). The primary scout question is whether global high-resolution line memory improves connectivity without merely increasing predicted-positive area.
