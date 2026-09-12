# ABI-251 full-spectral BTD+SZA line-memory U-NetFormer

ABI-251 is a bounded family scout for a modern lightweight segmentation backbone. It tests whether shifted-window local attention plus differentiable row/column line-memory context can improve contrail recall/connectivity without repeating the ABI-249 C4 support-bridge branch.

## Contract boundary

- Input mode: `abi_16ch_plus_sza` only.
- Candidate-visible features: GOES ABI channels 1-16 plus Solar Geometry Input; no longitude, latitude, Dataset Source identity, scene identity, route/location priors, temporal cache access, or raw data paths.
- Outputs: `mask_logits`, plus trusted Line and Centerline auxiliary outputs (`line_logits`, `centerline_logits`).
- Loss, sampling, augmentation, metrics, Artifact Filters, training loop, resource placement, and lifecycle remain Harness/provider owned.
- Candidate code defines architecture only. It performs no data loading, target derivation, thresholding, morphology, postprocessing, custom losses, custom metrics, downloads, filesystem probing, sampling policy, augmentation transforms, training loops, or scheduling.

## Architecture summary

The model consumes ABI+SZA features through a normalized full-spectral front end with approved-channel thermal BTD planes and a learned channel mixer. A compact U-NetFormer-style encoder-decoder then combines:

1. shifted-window self-attention for local/cross-window thin-structure evidence;
2. differentiable row/column `LineMemoryBlock` context to share line evidence over longer horizontal and vertical spans;
3. an ASPP-like bottleneck context path;
4. a calibrated recall/precision feature-fusion head that merges dilated recall features with line-memory precision features at the model-logit level.

The line-memory and calibrated head are internal differentiable model logic only; they do not threshold, filter, morphologically alter, or postprocess predictions.

## Run intent

Default exploratory budget only. Compare primarily against ABI-202 as the aggregate whole-validation frontier, ABI-249 as the high-precision C4 comparator, and ABI-244 as the closest shifted-window-attention resource precedent. A useful scout signal is finite non-collapsed learning, source-informative Dice, and a recall/connectivity profile close enough to justify bounded family development, even if it does not immediately beat the mature ABI-202 frontier.
