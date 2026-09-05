# ABI-210 compact full-spectral BTD+SZA spectral-ridge support ASPP

ABI-210 is a resource-safe family-development continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch after ABI-209 exhausted the exploratory wall-clock budget.

It keeps provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget.

The architecture-only change relative to ABI-209 is compaction: learned front-end projection width 16→12, base feature width 36→32, and a smaller broad smoothing window inside the spectral-ridge support bridge. The bridge remains a feature-space residual using only approved ABI/SZA-derived features; it does not implement thresholding, postprocessing, Artifact Filters, losses, metrics, data loading, target derivation, sampling, augmentation, coordinate features, runtime downloads, persistence writes, or resource scheduling.

Primary comparison: ABI-202 `run_20260904_043143_ee0005`. Resource comparison: ABI-209 `run_20260904_141405_62591c`.

See `PROPOSAL.md` for hypothesis, budget, success criteria, and fallback decisions.
