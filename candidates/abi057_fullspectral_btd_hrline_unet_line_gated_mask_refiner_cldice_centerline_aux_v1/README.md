# ABI-057 Full-Spectral BTD High-Resolution Line U-Net Line-Gated Mask Refiner

Family-development continuation for GOES ABI Contrail Segmentation after ABI-056.

## Summary

This candidate keeps the ABI-056 policy stack fixed:

- provider-approved `abi_16ch` inputs only;
- normalized raw ABI channels plus explicit thermal BTD planes derived only from ABI channels 1-16;
- learned 1x1 channel mixer;
- high-resolution line U-Net encoder/decoder with multi-scale skip fusion;
- trusted `bce_dice_cldice` primary loss;
- provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02;
- `combined_source_balanced` sampling and trusted `random_mirroring` augmentation;
- AdamW, learning rate 0.0003, batch size 4, max epochs 12.

The controlled architecture change is a `LineGatedMaskRefiner`: a centerline-supervised line branch emits `centerline_logits`; those logits form differentiable internal attention that gates line and mask features before the final `mask_logits` head. This is model architecture only, not candidate-owned thresholding, postprocessing, target derivation, or Artifact Filtering.

## Contract boundaries

Candidate code defines model architecture and approved manifest choices only. It does not implement data loading, splits, sampling policy, augmentation, losses, target derivation, metrics, Artifact Filters, postprocessing, training loops, device placement, scheduling, external persistence, pretrained weights, or runtime downloads. Longitude and latitude are never model inputs.

## Expected diagnostic signal

Compared with ABI-056, this continuation tests whether explicit line-proposal attention can reduce broad low-level false positives while preserving source-balanced recall under the representative capped budget.
