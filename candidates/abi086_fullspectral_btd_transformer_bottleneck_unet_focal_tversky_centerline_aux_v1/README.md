# ABI-086 full-spectral BTD transformer-bottleneck U-Net

ABI-086 is a family scout for a compact transformer-bottleneck encoder-decoder on GOES ABI Contrail Segmentation.

## Summary

- Uses provider-approved `abi_16ch` tensors only: GOES ABI channels 1-16, no longitude or latitude.
- Builds raw normalized ABI features, explicit thermal brightness-temperature-difference planes, and learned 1x1 channel mixtures inside the model front end.
- Encodes with a residual U-Net, applies global multi-head self-attention at 1/16 resolution, and decodes to full-resolution `mask_logits`.
- Emits provider-declared `centerline_logits` for the trusted `centerline` auxiliary target with `weighted_bce` weight 0.02.
- Selects Harness/provider-owned `combined_source_balanced` sampling, trusted `random_mirroring`, trusted `focal_tversky` primary loss, AdamW, batch size 4, 12 epochs, and `constant_lr`.

## Scientific intent

Recent ABI-068-family continuations showed that extra late refiners, suppressor heads, SZA input, learning-rate reduction, and auxiliary-loss swaps did not reliably improve ABI-068's capped aggregate Dice while preserving precision/connectivity. ABI-086 broadens to a bottleneck-attention family: it gives the decoder non-local scene context before upsampling rather than adding another full-resolution suppressor or post-hoc refiner.

The scout asks whether coarse global context can reduce isolated clutter and preserve source-balanced thin-line recall under the existing trusted data, loss, sampling, augmentation, metric, and Artifact Filter boundaries.

## Contract boundary

Candidate code defines only model architecture. It does not implement or own data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.
