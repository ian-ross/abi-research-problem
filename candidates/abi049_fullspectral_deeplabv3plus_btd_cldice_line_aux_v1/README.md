# ABI-049 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Line Auxiliary v1

Family-development continuation for GOES ABI Contrail Segmentation.

This candidate keeps the ABI-048 spectral front end and DeepLabV3+ ResNet-18 backbone:

- normalized approved ABI channels 1-16;
- eight thermal brightness-temperature-difference planes from approved thermal bands;
- a 16-channel learned 1x1 projection of normalized raw channels;
- a 40-channel tensor passed to a randomly initialized SMP DeepLabV3+ decoder.

The intended controlled change from ABI-048 is adding one provider-declared low-weight `line` auxiliary target with model output `line_logits` and trusted `weighted_bce` auxiliary loss at weight 0.05. The primary `mask_logits` output and trusted `bce_dice_cldice` primary loss are preserved.

Candidate code does not use longitude, latitude, Solar Geometry Input, pretrained weights, custom losses, data loading, sampling, augmentation transforms, metrics, artifact filters, training loops, network access, GPU placement, scheduling, or external persistence.

Primary comparison target: ABI-048 `run_20260827_112338_82a3a6`.
Family baseline reference: ABI-046 `run_20260826_204203_732aee`.
Recall/precision trade-off reference: ABI-047 `run_20260827_110027_1c679a`.
