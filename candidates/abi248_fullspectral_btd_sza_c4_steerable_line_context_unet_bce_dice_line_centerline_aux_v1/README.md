# ABI-248 full-spectral BTD+SZA C4 steerable line-context U-Net

ABI-248 is a bounded rotation-aware line-network family scout for GOES ABI Contrail Segmentation. It consumes only provider-approved ABI channels plus Solar Geometry Input and tests whether a C4 rotation-shared anisotropic line-context block can improve thin-line continuity without candidate-owned filtering or postprocessing.

The model emits `mask_logits`, `line_logits`, and `centerline_logits` for Harness-owned BCE-Dice and weighted-BCE auxiliary supervision. It uses source-balanced sampling, trusted random mirroring, the exploratory 12-epoch budget, batch size 4, and constant learning rate.
