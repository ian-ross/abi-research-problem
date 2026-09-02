# ABI-167 full-spectral BTD+SZA early-oriented encoder ASPP/detail decoder

ABI-167 is a family-development continuation after ABI-166's negative late oriented line-bank result. It keeps the provider-approved `abi_16ch_plus_sza` input, deterministic thermal brightness-temperature-difference features derived only from GOES ABI channels 1-16, trusted `bce_dice` loss, combined source-balanced traversal, trusted random mirroring, and the provider-derived Centerline Target auxiliary output.

The controlled architecture change is to move orientation evidence earlier: lightweight neutral additive oriented-context blocks are inserted after the stem, at each encoder scale, and in the decoder path before full-scale skip fusion. This tests whether multi-scale horizontal, vertical, and diagonal context must shape features before the ASPP bottleneck and decoder rather than being applied only as a final local refinement.

## Contract boundaries

- Candidate code defines only the model architecture over Harness-supplied tensors.
- Candidate inputs are `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input.
- Longitude and latitude source channels are neither requested nor reconstructed.
- Data loading, Leakage-Safe Split, bounded-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, prediction retention, resource placement, and lifecycle remain provider/Harness-owned.
- Outputs are `mask_logits` and provider-requested `centerline_logits`, each shaped `[N, 1, 256, 256]`.

## Comparison targets

Primary local comparison targets are ABI-068 (`run_20260828_010836_4ccc77`) as the current capped filtered-Dice reference, ABI-130 (`run_20260831_121006_7d24be`) as the SZA-aware ASPP/detail BCE-Dice reference, ABI-154 (`run_20260901_071026_32d3ec`) as the high-precision/high-connectivity full-scale skip reference, and ABI-166 (`run_20260901_173120_9c74ab`) as the negative late-oriented-line-bank predecessor.
