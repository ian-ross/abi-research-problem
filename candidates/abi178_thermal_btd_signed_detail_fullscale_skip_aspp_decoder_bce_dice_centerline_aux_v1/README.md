# ABI-178 thermal BTD signed-detail full-scale skip ASPP decoder BCE-Dice centerline auxiliary v1

ABI-178 is an input/preprocessing-frontier continuation after recent SZA-aware signed-detail/full-scale and recurrent-line ASPP variants. It intentionally removes reflective ABI channels and Solar Geometry Input by selecting provider-approved `abi_thermal_10ch`, while retaining deterministic thermal brightness-temperature-difference features, signed local/mid-scale thermal detail streams, compact ASPP context, full-scale skip aggregation, trusted BCE-Dice primary loss, and provider-derived Centerline Target auxiliary supervision.

The hypothesis is that ABI-173's recall gain may partly be offset by reflective/SZA-driven negative-patch clutter and weak connected-line calibration. A thermal-only BTD signed-detail decoder should force the model to use ice-cloud/window/water-vapor thermal contrasts and patch-local signed thermal anomalies, potentially improving MIT/Google transfer, connectivity, or false-positive discipline without candidate-owned thresholding or postprocessing.

Contract boundaries:

- Input mode: `abi_thermal_10ch`; only GOES ABI channels 7-16 are exposed. Longitude/latitude, reconstructed coordinates, Dataset Source identity, and Solar Geometry Input are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `bce_dice`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture and approved-channel deterministic feature construction only. It does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
