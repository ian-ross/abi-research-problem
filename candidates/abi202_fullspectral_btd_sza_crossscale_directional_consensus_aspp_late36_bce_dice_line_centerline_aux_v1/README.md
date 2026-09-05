# ABI-202 full-spectral BTD+SZA cross-scale directional-consensus ASPP late36

ABI-202 is a late-improving close-continuation of ABI-201 for GOES ABI Contrail Segmentation. It keeps the exact ABI-201 model architecture and approved manifest choices, and adds only a Harness-validated `budget_request.yaml` for the approved 36-epoch `late_improving` budget.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Compact base-width-36 residual encoder, ASPP bottleneck, and full-scale skip fusion adapted from the finite signed-detail ASPP lineage.
- Architecture-internal `CrossScaleDirectionalConsensusBridge` that fuses decoder, signed-detail, stem, and full-scale context features with horizontal, vertical, diagonal, and broad context views. The bridge uses a zero-initialized bounded residual, predicts no target, and applies no thresholding or filtering.
- Final line-aware refinement followed by `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Manifest and budget policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

The candidate-local `budget_request.yaml` requests the approved `late_improving` budget of 36 epochs with parent Run `run_20260904_032624_7e855a`, falling back to the exploratory budget if the Harness denies the request. Candidate code does not implement longer training; budget interpretation remains Harness-owned.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
