# ABI-230 five-frame temporal window-attention U-NetFormer

ABI-230 is a bounded family-development continuation in the temporal/window-attention branch for GOES ABI Contrail Segmentation. It combines ABI-229's compact local-window U-NetFormer backbone with the provider-owned five-frame temporal input used by ABI-226.

## Summary

- Input: `abi_16ch_plus_sza_temporal` with offsets `[-2, -1, 0, 1, 2]`.
- Frame selection: trusted `temporal_eligible_center`.
- Architecture: shared per-frame ABI+SZA+BTD feature builder, center-anchored five-frame temporal attention/change fusion, compact residual U-NetFormer encoder/decoder with non-shifted 8x8 local window attention.
- Outputs: `mask_logits`, `line_logits`, and `centerline_logits`.
- Loss and auxiliaries: trusted `bce_dice` primary loss plus trusted Line and Centerline weighted-BCE auxiliary targets.
- Budget: default 12-epoch exploratory budget; no late-improving request.

## Contract boundary

Candidate code defines model architecture only. It does not implement data loading, temporal lookup, cache access, missing-frame repair, target derivation, loss functions, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate features, Dataset Source identity features, or resource scheduling.

## Comparison targets

Primary comparisons are ABI-229 (`run_20260910_141659_818da0`) and ABI-226 (`run_20260910_120441_916a03`). ABI-222, ABI-223, and ABI-202 provide broader temporal and whole-validation frontier context.
