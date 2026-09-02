# ABI-050 Full-Spectral DeepLabV3+ BTD-Mixer + clDice + Boundary Auxiliary v1

Family-development continuation for GOES ABI Contrail Segmentation.

This candidate keeps the ABI-048/ABI-049 spectral front end and DeepLabV3+ ResNet-18 backbone:

- normalized approved ABI channels 1-16;
- eight thermal brightness-temperature-difference planes from approved thermal bands;
- a 16-channel learned 1x1 projection of normalized raw channels;
- a 40-channel tensor passed to a randomly initialized SMP DeepLabV3+ decoder.

The intended controlled change from ABI-048 is adding one provider-declared low-weight `boundary` auxiliary target with model output `boundary_logits` and trusted `weighted_bce` auxiliary loss at weight 0.05. Relative to ABI-049, the only scientific change is replacing `line` auxiliary supervision with `boundary` auxiliary supervision. The primary `mask_logits` output and trusted `bce_dice_cldice` primary loss are preserved.

Candidate code does not use longitude, latitude, Solar Geometry Input, pretrained weights, custom losses, data loading, sampling, augmentation transforms, metrics, artifact filters, training loops, network access, GPU placement, scheduling, or external persistence.

Primary comparison target: ABI-049 `run_20260827_114945_e5f83e`.
Secondary comparison target: ABI-048 `run_20260827_112338_82a3a6`.
Family baseline reference: ABI-046 `run_20260826_204203_732aee`.
