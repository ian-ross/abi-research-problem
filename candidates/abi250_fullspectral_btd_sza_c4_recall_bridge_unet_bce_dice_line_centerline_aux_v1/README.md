# ABI-250 full-spectral BTD+SZA C4 recall-bridge U-Net

ABI-250 is a family-development continuation of ABI-249. It keeps the C4 rotation-shared line-context U-Net policy but adds a high-resolution full-scale support bridge before the C4 head to test whether the branch can recover recall/connectivity without giving up ABI-249's compact high-precision behavior.

## Contract boundary

- Input mode: `abi_16ch_plus_sza` only.
- Candidate-visible features: GOES ABI channels 1-16 plus Solar Geometry Input; no longitude, latitude, Dataset Source identity, scene identity, temporal cache access, or route/location priors.
- Outputs: `mask_logits`, plus trusted Line and Centerline auxiliary outputs (`line_logits`, `centerline_logits`).
- Loss and augmentation are selected only through the manifest allowlists.
- Candidate code defines architecture only. It does not implement data loading, sampling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, training loops, downloads, filesystem probes, or resource scheduling.

## Architecture summary

The model uses the ABI-249 normalized ABI/SZA plus thermal-BTD front end and encoder-decoder backbone. It adds:

1. `FullScaleSkipFusion`: projects stem, encoder, bottleneck, decoder, and high-resolution detail tensors to mask resolution and fuses them.
2. `RecallPreservingSupportBridge`: combines decoder, signed-detail, full-scale support, horizontal/vertical line evidence, and a learned feature gate. The bridge uses a zero-initialized bounded residual so the new support path starts conservatively.
3. The existing C4 rotation-shared anisotropic strip context head produces the primary mask and auxiliary logits.

## Run intent

Default exploratory budget only. Compare primarily to ABI-249 (`run_20260911_111909_dd7ef7`) and use ABI-202 as frontier context. The desired signal is improved recall/connectivity or MIT filtered Dice while preserving non-collapsed, source-informative predictions and acceptable precision.
