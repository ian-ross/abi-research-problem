# ABI-293 full-spectral BTD+SZA early evidence-calibrated detail U-Net

ABI-293 tests whether recall/connectivity support is more effective when calibrated detail and line evidence are shared early through encoder/decoder skips rather than added as a late C4 soft-band head. It consumes only approved `abi_16ch_plus_sza` inputs and uses trusted source-balanced sampling, random mirroring, BCE-Dice loss, and Line/Centerline auxiliary targets.

The model is a compact residual U-Net with normalized ABI+BTD+Solar Geometry Input features, multi-scale evidence calibration blocks, and a bounded calibrated evidence head. It contains no Candidate-owned data loading, temporal lookup, target derivation, loss, metric, Artifact Filter, threshold, postprocessing, coordinate feature, sampling, augmentation, resource scheduling, or training-loop logic.
