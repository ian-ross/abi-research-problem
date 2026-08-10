# abi_spectral_resunet_scout_v1

First scientific **family scout** for GOES ABI Contrail Segmentation.

The candidate accepts only `abi_16ch` and emits one `[1, 256, 256]` `mask_logits` tensor. Its architecture combines rounded campaign-profile normalization, selected ABI spectral bands, explicit thermal brightness-temperature differences, learned channel mixtures, residual encoder-decoder skips, and bounded dilated context.

All data loading, Leakage-Safe Split logic, Source-Balanced Sampling implementation, random mirroring, loss computation, metrics, checkpoint selection, Artifact Filters, and Baseline Segmenter comparisons remain trusted provider/Harness responsibilities. The candidate uses no longitude, latitude, network access, runtime downloads, or pretrained weights.

See `PROPOSAL.md` for the hypothesis, bounded budget, continuation criteria, and hard stops.
