# ABI-141 Full-Spectral BTD+SZA ASPP/Detail Decoder Boundary-Calibrated BCE-Dice Centerline Auxiliary v1

ABI-141 is a controlled family-development continuation of ABI-130. It keeps the SZA-aware full-spectral BTD ASPP/detail encoder-decoder, provider-approved `abi_16ch_plus_sza` input, trusted `bce_dice` loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, and constant learning rate.

The intended change is a low-weight provider-derived Boundary Target auxiliary output plus a neutral-initialized boundary/detail residual mask-logit calibration module. The residual starts at zero and is bounded by `0.15 * tanh(...)`, so the branch begins close to ABI-130 while allowing training to learn edge/detail calibration if useful.

Outputs:

- `mask_logits`: primary contrail mask logits.
- `centerline_logits`: provider-derived Centerline Target auxiliary output, `weighted_bce` weight 0.02.
- `boundary_logits`: provider-derived Boundary Target auxiliary output, `weighted_bce` weight 0.01.

The experiment tests whether boundary/detail supervision can recover some ABI-126/ABI-066 connectivity or negative-patch discipline while preserving ABI-130's SZA-enabled default-threshold recall and Google transfer. It does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, network access, or resource scheduling.
