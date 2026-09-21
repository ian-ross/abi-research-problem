# ABI-367 temporal center-detail tail support late36

ABI-367 is a temporal family-development continuation of ABI-350 for GOES ABI Contrail Segmentation. It keeps the trusted provider-owned `abi_16ch_plus_sza_temporal` input mode with `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, trusted source-balanced sampling, trusted random mirroring, BCE-Dice loss, and trusted Line/Centerline auxiliary targets.

The architecture preserves ABI-350's temporal-attention U-Net with pre-decoder orientation line-support gates, then adds a bounded center-frame detail tail after high-resolution decoder fusion. The tail builds source-agnostic signed detail from the center frame's ABI+SZA/BTD feature stack and reinjects it only through an architecture-internal line-evidence gate. This tests whether fixed-threshold true-positive evidence and connected-line support can improve without Candidate-owned thresholds, postprocessing, Artifact Filters, losses, metrics, data loading, sampling, temporal lookup, coordinates, Dataset Source identity, or resource scheduling.

The Candidate requests the approved `late_improving` budget because the close parent ABI-350 selected its best checkpoint at epoch 33 and the new module remains in the same compact temporal resource class. If denied, the exploratory budget is an acceptable fallback.
