# ABI-054 Full-Spectral BTD High-Resolution Line U-Net + clDice + Centerline Auxiliary Weight 0.05 v1

ABI-054 is a sequential capped family-development continuation of ABI-053. It keeps the same high-resolution line U-Net decoder, approved `abi_16ch` inputs, normalized raw channels, eight explicit thermal BTD planes, learned 1x1 channel mixer, trusted `bce_dice_cldice`, combined source-balanced sampling, and trusted random mirroring.

The controlled change is increasing the provider-derived `centerline` auxiliary target weight from 0.02 to 0.05. The hypothesis is that stronger centerline supervision may recover continuity and checkpoint stability in the high-resolution decoder while preserving most of ABI-053's capped Dice, MIT, Google, and recall gains.

## Contract summary

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are not used.
- Outputs: `mask_logits` plus manifest-declared `centerline_logits`.
- Trusted policy: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, `weighted_bce` centerline auxiliary weight 0.05, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Candidate code contains model architecture only. It does not implement data loading, augmentation, sampling, target derivation, losses, metrics, Artifact Filters, training loops, pretrained weights, downloads, GPU placement, or scheduling.
