# ABI-046 Full-Spectral DeepLabV3+ BTD-Mixer v1

Family-development continuation for GOES ABI Contrail Segmentation.

This candidate reuses the ABI-044 DeepLabV3+ ResNet-18 backbone and trusted BCE-Dice training policy, but adds a narrow spectral front end:

- normalized approved ABI channels 1-16;
- eight thermal brightness-temperature-difference planes from approved thermal bands;
- a 16-channel learned 1x1 projection of normalized raw channels.

The 40-channel feature tensor is passed to a randomly initialized SMP DeepLabV3+ decoder. Candidate code does not use longitude, latitude, Solar Geometry Input, pretrained weights, custom losses, data loading, sampling, augmentation transforms, metrics, artifact filters, training loops, network access, or external persistence.

Primary comparison target: ABI-044 `run_20260813_145951_a64a37`.
Secondary trade-off reference: ABI-045 `run_20260826_120037_b98df4`.
