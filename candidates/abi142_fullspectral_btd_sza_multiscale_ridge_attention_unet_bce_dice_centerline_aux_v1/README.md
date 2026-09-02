# ABI-142 Full-Spectral BTD+SZA Multiscale Ridge-Attention U-Net BCE-Dice Centerline Auxiliary v1

ABI-142 is a family-scout candidate that broadens away from recent ASPP/detail decoder head tweaks. It keeps provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from ABI channels 1-16, trusted `bce_dice` loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, and constant learning rate.

The architecture uses a compact U-Net with a multiscale ridge-attention stem and refinement path. The stem projects normalized raw ABI+BTD+SZA features together with fixed fine-detail, broad-context, horizontal-ridge, and vertical-ridge residual views. The final refinement uses learned horizontal/vertical strip context and a bounded feature-space attention gate to calibrate thin linear evidence before the mask and Centerline Target heads.

Outputs:

- `mask_logits`: primary contrail mask logits.
- `centerline_logits`: provider-derived Centerline Target auxiliary output, `weighted_bce` weight 0.02.

The experiment tests whether putting line/ridge evidence into the encoder stem and final feature attention can improve connectivity or source-robust calibration compared with ABI-130/ABI-068 without candidate-owned thresholding or postprocessing. It does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, network access, or resource scheduling.
