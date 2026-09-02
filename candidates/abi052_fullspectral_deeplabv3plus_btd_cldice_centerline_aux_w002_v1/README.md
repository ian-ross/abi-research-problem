# ABI-052 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Centerline Auxiliary Weight 0.02 v1

Family-development continuation for GOES ABI Contrail Segmentation.

This candidate keeps the ABI-051 architecture and changes only the trusted manifest-declared Centerline Target auxiliary-loss weight from 0.05 to 0.02. It preserves:

- provider-approved `abi_16ch` inputs only;
- normalized ABI channels 1-16;
- eight explicit thermal brightness-temperature-difference planes from approved thermal bands;
- a learned 16-channel 1x1 projection of normalized raw channels;
- a randomly initialized SMP DeepLabV3+ ResNet-18 decoder producing `mask_logits` and `centerline_logits`;
- trusted `bce_dice_cldice` primary loss, `combined_source_balanced` sampling traversal, and `random_mirroring` augmentation.

The hypothesis is that a lighter centerline auxiliary signal may retain ABI-051s precision/connectivity and final-epoch stability while reducing the recall suppression and MIT weakness seen at auxiliary weight 0.05.

Candidate code does not use longitude, latitude, Solar Geometry Input, pretrained weights, custom losses, data loading, sampling, augmentation transforms, metrics, artifact filters, training loops, network access, GPU placement, scheduling, or external persistence.

Primary comparison target: ABI-051 `run_20260827_124640_fc6836`.
Auxiliary-target references: ABI-048 `run_20260827_112338_82a3a6` and ABI-049 `run_20260827_114945_e5f83e`.
Family baseline reference: ABI-046 `run_20260826_204203_732aee`.
