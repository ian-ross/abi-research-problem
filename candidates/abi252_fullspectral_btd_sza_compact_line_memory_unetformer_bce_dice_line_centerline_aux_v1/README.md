# ABI-252 compact full-spectral BTD+SZA line-memory U-NetFormer

ABI-252 is a compact family-development continuation after ABI-251's Harness-recorded resource failure. ABI-251 produced useful partial, non-collapsed, source-informative evidence through epoch 9 but exhausted the 3,600-second exploratory wall-clock budget during epoch 10. ABI-252 keeps the same scientific mechanism while reducing full-resolution attention cost.

## Contract boundary

- Input mode: `abi_16ch_plus_sza` only.
- Candidate-visible features: GOES ABI channels 1-16 plus Solar Geometry Input; no longitude, latitude, Dataset Source identity, scene identity, route/location priors, temporal cache access, or raw data paths.
- Outputs: `mask_logits`, plus trusted Line and Centerline auxiliary outputs (`line_logits`, `centerline_logits`).
- Loss, sampling, augmentation, metrics, Artifact Filters, training loop, resource placement, and lifecycle remain Harness/provider owned.
- Candidate code defines architecture only. It performs no data loading, target derivation, thresholding, morphology, postprocessing, custom losses, custom metrics, downloads, filesystem probing, sampling policy, augmentation transforms, training loops, or scheduling.

## Architecture summary

The model consumes ABI+SZA features through a normalized full-spectral front end with approved-channel thermal BTD planes and learned channel-mixer features. Compared with ABI-251, it:

1. narrows the base width from 32 to 24;
2. narrows learned mixer features from 16 to 12;
3. removes full-resolution shifted-window attention from the stem/final refiner;
4. retains shifted-window attention at downsampled encoder/context/decoder scales;
5. retains differentiable row/column line-memory context and trusted Line/Centerline auxiliary outputs.

The line-memory and calibration-like fusion head are internal differentiable model logic only; they do not threshold, filter, morphologically alter, or postprocess predictions.

## Run intent

Default exploratory budget only. The immediate goal is resource-compatible feasibility and complete 12-epoch evidence for ABI-251's partial line-memory U-NetFormer signal. Compare primarily against ABI-251's epoch-9 partial metrics, ABI-244's completed shifted-window U-NetFormer scout, ABI-249's high-precision line-prior result, and ABI-202 as the mature aggregate frontier context.
