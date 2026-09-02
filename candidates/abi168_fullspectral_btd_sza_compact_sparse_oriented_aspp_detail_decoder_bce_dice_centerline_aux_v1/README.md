# ABI-168 full-spectral BTD+SZA compact sparse-oriented ASPP/detail decoder

ABI-168 is a resource-safe family-development continuation after ABI-167 timed out. It keeps the provider-approved `abi_16ch_plus_sza` input, deterministic thermal brightness-temperature-difference features derived only from GOES ABI channels 1-16, trusted `bce_dice` loss, combined source-balanced traversal, trusted random mirroring, and the provider-derived Centerline Target auxiliary output.

The controlled architecture change from ABI-167 is to compact the early-oriented design: the base width is reduced from 40 to 32, the learned front-end mixer is reduced from 16 to 12 channels, full-scale skip fusion branches are reduced, and oriented context is applied sparsely at the stem, mid encoder scales, one decoder scale, and the high-resolution detail branch. This preserves the hypothesis that orientation should shape features before final prediction while avoiding ABI-167's expensive every-scale oriented blocks.

## Contract boundaries

- Candidate code defines only the model architecture over Harness-supplied tensors.
- Candidate inputs are `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input.
- Longitude and latitude source channels are neither requested nor reconstructed.
- Data loading, Leakage-Safe Split, bounded-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, prediction retention, resource placement, and lifecycle remain provider/Harness-owned.
- Outputs are `mask_logits` and provider-requested `centerline_logits`, each shaped `[N, 1, 256, 256]`.

## Comparison targets

Primary local comparison targets are ABI-068 (`run_20260828_010836_4ccc77`) as the current capped filtered-Dice reference, ABI-130 (`run_20260831_121006_7d24be`) as the SZA-aware ASPP/detail BCE-Dice reference, ABI-154 (`run_20260901_071026_32d3ec`) as the high-precision/high-connectivity full-scale skip reference, ABI-166 (`run_20260901_173120_9c74ab`) as the negative late-oriented-line-bank predecessor, and ABI-167 (`run_20260901_182419_ca8406`) as the timed-out dense early-oriented predecessor.
