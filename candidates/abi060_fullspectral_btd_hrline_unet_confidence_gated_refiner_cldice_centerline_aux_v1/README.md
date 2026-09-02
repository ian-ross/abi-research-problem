# ABI-060 Full-Spectral BTD High-Resolution Line U-Net Confidence-Gated Refiner

Family-development continuation for GOES ABI Contrail Segmentation after ABI-059 showed that subtractive false-positive suppression was not useful.

## Summary

This candidate keeps the ABI-058/ABI-059 policy stack fixed:

- provider-approved `abi_16ch` inputs only;
- normalized raw ABI channels plus explicit thermal BTD planes derived only from ABI channels 1-16;
- learned 1x1 channel mixer;
- high-resolution line U-Net encoder/decoder with multi-scale skip fusion and oriented full-resolution context;
- trusted `bce_dice_cldice` primary loss;
- provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02;
- `combined_source_balanced` sampling and trusted `random_mirroring` augmentation;
- AdamW, learning rate 0.0003, batch size 4, max epochs 12.

The controlled architecture change replaces ABI-059's subtractive suppressor with a confidence-gated feature-selection head. A low-resolution context branch and oriented line branch learn soft gates that decide how strongly full-resolution line features should enter the final mask refinement. The gates are differentiable neural layers, initialized conservatively, and do not implement thresholding, postprocessing, target derivation, or Artifact Filtering.

## Contract boundaries

Candidate code defines model architecture and approved manifest choices only. It does not implement data loading, splits, sampling policy, augmentation, losses, target derivation, metrics, Artifact Filters, postprocessing, training loops, device placement, scheduling, external persistence, pretrained weights, or runtime downloads. Longitude and latitude are never model inputs.

## Expected diagnostic signal

ABI-058 improved recall but produced broad low-level false positives; ABI-059's subtractive suppression reduced neither predicted-positive burden nor connectivity. ABI-060 tests whether confidence-gated feature selection can keep the oriented-context recall signal while selecting fewer diffuse background activations.
