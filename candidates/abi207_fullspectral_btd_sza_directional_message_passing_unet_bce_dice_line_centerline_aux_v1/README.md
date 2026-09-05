# ABI-207 full-spectral BTD+SZA directional message-passing U-Net

ABI-207 is an exploratory family scout for GOES ABI Contrail Segmentation. It broadens away from the ABI-202 cross-scale directional-consensus ASPP branch's near-timeout local refiner/auxiliary tweaks by testing a compact multi-scale directional message-passing U-Net.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, ABI-channel-derived thermal BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Base-width-32 residual encoder-decoder to keep the scout below the recent near-timeout ABI-202/204/206 resource profile.
- Directional message-passing blocks at full, half, quarter, and bottleneck scales. Each block learns horizontal, vertical, diagonal, and broad context features from approved tensors and fuses them with a bounded residual; it predicts no target and applies no thresholding, filtering, or postprocessing.
- Full-scale skip fusion plus final line-aware refinement before `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line and Centerline auxiliary targets with trusted `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
