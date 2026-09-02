# ABI-045 Full-Spectral DeepLabV3+ Focal-Tversky Continuation v1

Controlled DeepLabV3+ family-development continuation after ABI-044.

## What changes

This candidate keeps the ABI-044 full-spectral DeepLabV3+ ResNet-18 architecture, `abi_16ch` input, trusted normalization constants, source-balanced sampling, random mirroring, AdamW learning rate 0.0003, batch size 4, and 12-epoch representative capped budget. The only intended experimental change is the trusted primary loss: `bce_dice` -> `focal_tversky`.

## Why

ABI-044 completed finite and non-degenerate with an improving trajectory, but its final filtered recall was low relative to precision. This run tests whether the provider-owned focal-Tversky loss improves thin-contrail recall or reveals an unfavorable precision/recall trade-off under the same DeepLabV3+ resource envelope.

## Contract notes

- Uses only provider-approved `abi_16ch` tensors.
- Does not use longitude, latitude, Solar Geometry Input, pretrained weights, runtime downloads, data loading, target derivation, custom losses, metrics, artifact filters, training loops, scheduling, or GPU placement.
- Returns one `[1, 256, 256]` `mask_logits` output.
- Requests one sequential bounded Run; no batch or concurrency is requested.
