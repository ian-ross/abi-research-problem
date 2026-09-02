# ABI-047 Full-Spectral DeepLabV3+ BTD-Mixer + Focal-Tversky v1

Family-development continuation for GOES ABI Contrail Segmentation.

This candidate keeps the ABI-046 spectral front end and DeepLabV3+ ResNet-18 backbone:

- normalized approved ABI channels 1-16;
- eight thermal brightness-temperature-difference planes from approved thermal bands;
- a 16-channel learned 1x1 projection of normalized raw channels;
- a 40-channel tensor passed to randomly initialized SMP DeepLabV3+.

The only intended training-policy change from ABI-046 is selecting the trusted `focal_tversky` primary loss instead of `bce_dice`. The purpose is to test whether the BTD-mixer front end can keep its precision/source-balance advantage while recovering some of ABI-045's recall-seeking behavior.

Candidate code does not use longitude, latitude, Solar Geometry Input, pretrained weights, custom losses, data loading, sampling, augmentation transforms, metrics, artifact filters, training loops, network access, GPU placement, scheduling, or external persistence.

Primary comparison target: ABI-046 `run_20260826_204203_732aee`.
Recall/precision reference: ABI-045 `run_20260826_120037_b98df4`.
Family scout reference: ABI-044 `run_20260813_145951_a64a37`.
