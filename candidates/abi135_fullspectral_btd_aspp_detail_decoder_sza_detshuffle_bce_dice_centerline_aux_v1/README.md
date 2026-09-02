# ABI-135 full-spectral BTD+SZA ASPP/detail decoder deterministic-shuffle BCE-Dice centerline auxiliary

Family-development data-policy continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-130's compact ASPP/detail encoder-decoder, provider-approved ABI+Solar Geometry input, deterministic raw-plus-BTD-plus-SZA front end, trusted BCE-Dice primary loss, trusted random mirroring, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change is manifest-only: `data.sampling_policy` changes from `combined_source_balanced` to provider-owned `deterministic_shuffle`. Candidate code does not implement sampling; the trusted Harness/provider continues to own bounded record selection, source/split semantics, sampling implementation, augmentation, loss, metrics, Artifact Filters, and lifecycle behavior.

The hypothesis is that ABI-130's near-best but oscillatory SZA-aware ASPP/detail branch may benefit from a less rigid source-balanced traversal over the same trusted representative selected records, potentially improving calibration/source integration without adding another architecture head or candidate-owned postprocessing.
