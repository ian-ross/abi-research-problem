# ABI-058 Full-Spectral BTD High-Resolution Line U-Net Oriented Context

Family-development continuation for GOES ABI Contrail Segmentation after ABI-053 through ABI-057.

## Summary

This candidate keeps the successful ABI-056 policy stack fixed:

- provider-approved `abi_16ch` inputs only;
- normalized raw ABI channels plus explicit thermal BTD planes derived only from ABI channels 1-16;
- learned 1x1 channel mixer;
- high-resolution line U-Net encoder/decoder with multi-scale skip fusion;
- trusted `bce_dice_cldice` primary loss;
- provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02;
- `combined_source_balanced` sampling and trusted `random_mirroring` augmentation;
- AdamW, learning rate 0.0003, batch size 4, max epochs 12.

The controlled architecture change replaces the isotropic full-resolution line refiner with an `OrientedContextRefiner`. It applies local, horizontal strip, vertical strip, and broad dilated context branches at full resolution, learns a differentiable per-pixel soft orientation mixture, and fuses that oriented context back into the mask and centerline heads. This is model architecture only, not candidate-owned thresholding, postprocessing, target derivation, or Artifact Filtering.

## Contract boundaries

Candidate code defines model architecture and approved manifest choices only. It does not implement data loading, splits, sampling policy, augmentation, losses, target derivation, metrics, Artifact Filters, postprocessing, training loops, device placement, scheduling, external persistence, pretrained weights, or runtime downloads. Longitude and latitude are never model inputs.

## Expected diagnostic signal

Compared with ABI-056 and ABI-057, this continuation tests whether explicit orientation-bank context can strengthen thin-line continuity and source-balanced overlap without using centerline logits as a hard or soft postprocessing gate. A useful result would recover ABI-056-like filtered Dice while improving connectivity or precision/recall balance, or provide clear evidence that this high-resolution line U-Net branch should give way to a different family.
