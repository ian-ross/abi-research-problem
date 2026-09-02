# ABI-166 full-spectral BTD+SZA oriented line-bank ASPP/detail decoder

ABI-166 is a family-development continuation after the ABI-154 full-scale skip ASPP/detail decoder and the negative ABI-158/159/165 local auxiliary/gating follow-ups. It keeps the provider-approved `abi_16ch_plus_sza` input, deterministic thermal brightness-temperature-difference features derived only from GOES ABI channels 1-16, trusted `bce_dice` loss, combined source-balanced traversal, trusted random mirroring, and the provider-derived Centerline Target auxiliary output.

The controlled architecture change is an oriented line-bank refinement at full resolution. The refinement fuses local detail, horizontal context, vertical context, and two fixed no-wrap diagonal average banks before the final mask and centerline heads. The intent is to supply explicit multi-orientation line continuity evidence in feature space, rather than adding more auxiliary heads or candidate-owned threshold/postprocessing logic.

## Contract boundaries

- Candidate code defines only the model architecture over Harness-supplied tensors.
- Candidate inputs are `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input.
- Longitude and latitude source channels are neither requested nor reconstructed.
- Data loading, Leakage-Safe Split, bounded-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, prediction retention, resource placement, and lifecycle remain provider/Harness-owned.
- Outputs are `mask_logits` and provider-requested `centerline_logits`, each shaped `[N, 1, 256, 256]`.

## Comparison targets

Primary local comparison targets are ABI-154 (`run_20260901_071026_32d3ec`), ABI-130 (`run_20260831_121006_7d24be`), ABI-068 (`run_20260828_010836_4ccc77`), and the recent negative ABI-165 auxiliary continuation (`run_20260901_163629_b45b2d`).
