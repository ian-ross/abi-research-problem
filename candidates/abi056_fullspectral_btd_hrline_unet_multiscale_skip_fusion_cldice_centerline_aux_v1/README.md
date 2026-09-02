# ABI-056 Full-Spectral BTD High-Resolution Line U-Net Multi-Scale Skip Fusion

Family-development continuation after ABI-053/054/055 for GOES ABI Contrail Segmentation.

## Summary

This candidate keeps the ABI-053 policy stack fixed:

- provider-approved `abi_16ch` inputs only;
- normalized raw ABI channels plus explicit thermal BTD planes derived only from ABI channels 1-16;
- learned 1x1 channel mixer;
- high-resolution line U-Net encoder/decoder;
- trusted `bce_dice_cldice` primary loss;
- provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02;
- `combined_source_balanced` sampling and trusted `random_mirroring` augmentation;
- AdamW, learning rate 0.0003, batch size 4, max epochs 12.

The controlled architecture change is a `MultiScaleSkipFusion` module that projects decoder features from multiple scales back to full resolution, gates them together with stem and full-resolution decoder features, and fuses them before the full-resolution line refiner.

## Contract boundaries

Candidate code defines model architecture only. It does not implement data loading, splits, sampling policy, augmentation, losses, target derivation, metrics, Artifact Filters, postprocessing, training loops, device placement, scheduling, external persistence, pretrained weights, or runtime downloads. Longitude and latitude are never model inputs.

## Expected diagnostic signal

Compared with ABI-053/054/055, this continuation tests whether cross-scale decoder fusion improves final-epoch stability, source balance, and filtered connectivity while preserving ABI-053-like recall under the representative capped budget.
