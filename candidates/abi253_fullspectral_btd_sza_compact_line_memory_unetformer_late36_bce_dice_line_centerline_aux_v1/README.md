# ABI-253 compact full-spectral BTD+SZA line-memory U-NetFormer late36

ABI-253 is a late-improving close continuation of ABI-252. It preserves the exact compact line-memory U-NetFormer architecture and manifest policy while requesting the approved `late_improving` budget based on completed parent Run `run_20260911_161019_8c76cd`.

## Contract boundary

- Input mode: `abi_16ch_plus_sza` only.
- Candidate-visible features: GOES ABI channels 1-16 plus Solar Geometry Input; no longitude, latitude, Dataset Source identity, scene identity, route/location priors, temporal cache access, or raw data paths.
- Outputs: `mask_logits`, plus trusted Line and Centerline auxiliary outputs (`line_logits`, `centerline_logits`).
- Loss, sampling, augmentation, metrics, Artifact Filters, training loop, resource placement, budget enforcement, and lifecycle remain Harness/provider owned.
- Candidate code defines architecture only. It performs no data loading, target derivation, thresholding, morphology, postprocessing, custom losses, custom metrics, downloads, filesystem probing, sampling policy, augmentation transforms, training loops, or scheduling.

## Architecture summary

The model is intentionally unchanged from ABI-252:

1. normalized full-spectral ABI+SZA front end with approved-channel thermal BTD planes and learned 1x1 mixer features;
2. compact base width 24 and learned mixer width 12;
3. no full-resolution shifted-window attention in the stem/final refiner;
4. shifted-window attention at downsampled encoder/context/decoder scales;
5. differentiable row/column line-memory context blocks; and
6. trusted Line/Centerline auxiliary outputs.

The line-memory and calibration-like fusion head are internal differentiable model logic only; they do not threshold, filter, morphologically alter, or postprocess predictions.

## Run intent

Request the approved late-improving budget without adding compute or altering the architecture. ABI-252 completed all 12 exploratory epochs, selected epoch 10 as best, remained nearly tied at epoch 11, and shifted toward higher recall at epoch 12 while staying finite, source-informative, and non-collapsed. ABI-253 tests whether that late-ambiguous trajectory matures into a stable improvement over ABI-244's completed U-NetFormer comparator.

Compare primarily against ABI-252 (`run_20260911_161019_8c76cd`), ABI-244 (`run_20260911_072719_ade068`), ABI-249 (`run_20260911_111909_dd7ef7`), and ABI-202 (`run_20260904_043143_ee0005`).
