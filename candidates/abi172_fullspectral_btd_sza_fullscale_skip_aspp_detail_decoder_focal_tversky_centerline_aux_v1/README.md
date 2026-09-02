# ABI-172 full-spectral BTD+SZA full-scale skip ASPP/detail decoder focal-Tversky centerline auxiliary v1

ABI-172 is a controlled family-development continuation of ABI-154. It preserves the full-spectral BTD+SZA full-scale skip ASPP/detail decoder architecture and trusted Centerline Target auxiliary supervision while changing only the manifest-selected primary loss from `bce_dice` to trusted `focal_tversky`.

The hypothesis is that ABI-154's whole-validation under-recall and lower-threshold upside may be improved by a recall-oriented trusted loss without candidate-owned thresholding or postprocessing. The comparison target is ABI-154 Run `run_20260901_071026_32d3ec`; secondary references are ABI-130, ABI-068, ABI-169, and ABI-171.

Contract boundaries:

- Input mode: `abi_16ch_plus_sza` only; longitude/latitude and reconstructed coordinates are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture only and does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
