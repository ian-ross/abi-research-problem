# ABI-059 Full-Spectral BTD High-Resolution Line U-Net False-Positive Suppressor

Family-development continuation for GOES ABI Contrail Segmentation after ABI-058 whole-validation diagnostics.

## Summary

This candidate keeps the ABI-058 policy stack fixed:

- provider-approved `abi_16ch` inputs only;
- normalized raw ABI channels plus explicit thermal BTD planes derived only from ABI channels 1-16;
- learned 1x1 channel mixer;
- high-resolution line U-Net encoder/decoder with multi-scale skip fusion and oriented full-resolution context;
- trusted `bce_dice_cldice` primary loss;
- provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02;
- `combined_source_balanced` sampling and trusted `random_mirroring` augmentation;
- AdamW, learning rate 0.0003, batch size 4, max epochs 12.

The controlled architecture change adds a trainable false-positive suppressor head after the oriented-context refiner. A low-resolution context branch is fused back into full-resolution features, and a non-negative learned suppression term is subtracted from the primary mask logits. The suppressor is initialized near zero so the model starts close to ABI-058 and can learn background-evidence suppression only if the trusted primary loss supports it. This is differentiable model architecture only, not candidate-owned thresholding, postprocessing, target derivation, or Artifact Filtering.

## Contract boundaries

Candidate code defines model architecture and approved manifest choices only. It does not implement data loading, splits, sampling policy, augmentation, losses, target derivation, metrics, Artifact Filters, postprocessing, training loops, device placement, scheduling, external persistence, pretrained weights, or runtime downloads. Longitude and latitude are never model inputs.

## Expected diagnostic signal

ABI-058 improved whole-validation filtered Dice only narrowly and did so by increasing recall and predicted-positive area. ABI-059 tests whether a trainable negative-evidence head can reduce the broad low-level false-positive tendency on negative patches while preserving ABI-058's recall and source-balanced behavior.
