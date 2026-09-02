# ABI-053 Full-Spectral BTD High-Resolution Line U-Net + clDice + Centerline Auxiliary v1

ABI-053 is a sequential capped family scout that broadens beyond the DeepLabV3+ decoder while retaining the useful ABI-052 input/loss policy: approved `abi_16ch` inputs, normalized raw channels, eight explicit thermal BTD planes, a learned 1x1 channel mixer, trusted `bce_dice_cldice`, and a low-weight trusted `centerline` auxiliary head.

The architecture is a randomly initialized, pure-PyTorch high-resolution U-Net-style decoder. It keeps a full-resolution stem/skip path, fuses gated encoder skips during decoding, adds dilated context at the coarsest scale, and applies a full-resolution multi-dilation line refiner before the primary and auxiliary heads. The hypothesis is that preserving more 256x256 line evidence inside the decoder may recover MIT/recalI behavior that plateaued in the DeepLabV3+ BTD auxiliary-weight branch without moving data, loss, target, metric, or Artifact Filter ownership into candidate code.

## Contract summary

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are not used.
- Outputs: `mask_logits` plus manifest-declared `centerline_logits`.
- Trusted policy: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, `weighted_bce` centerline auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Candidate code contains model architecture only. It does not implement data loading, augmentation, sampling, target derivation, losses, metrics, Artifact Filters, training loops, pretrained weights, downloads, GPU placement, or scheduling.
