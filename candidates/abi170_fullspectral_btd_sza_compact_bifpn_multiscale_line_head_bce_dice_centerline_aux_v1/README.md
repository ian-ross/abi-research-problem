# ABI-170 Full-Spectral BTD+SZA Compact BiFPN Multiscale Line-Head BCE-Dice Centerline Auxiliary v1

ABI-170 is a family-development continuation of the compact BiFPN line-fusion U-Net branch. It keeps ABI-162's resource-safe full-spectral BTD+SZA front end, compact encoder, bidirectional feature pyramid, BCE-Dice loss, source-balanced traversal, trusted random mirroring, and low-weight Centerline Target auxiliary head. The controlled architecture change is a lightweight multiscale line-continuity head after BiFPN fusion.

The head combines local detail, short 9-pixel horizontal/vertical line context, longer 17-pixel horizontal/vertical line context, and broad feature context through a sigmoid feature-space support gate. The support is residual and differentiable inside the model; it is not thresholding, postprocessing, an Artifact Filter, or a candidate-owned loss/metric.

## Comparison target

Primary target: ABI-162 (`run_20260901_142708_a2f6c9`), which completed safely but remained under-recalled and below current references on connectivity.

Secondary context: ABI-163 focal-Tversky compact BiFPN (`run_20260901_150632_dc4961`), ABI-154 full-scale skip ASPP/detail (`run_20260901_071026_32d3ec`), ABI-130 SZA-aware ASPP/detail (`run_20260831_121006_7d24be`), and ABI-068 frequency-gated line U-Net (`run_20260828_010836_4ccc77`).

## Contract boundaries

- Uses provider-approved `abi_16ch_plus_sza` input only.
- Does not use longitude, latitude, Dataset Source identity, hidden coordinates, external data, pretrained weights, or runtime downloads.
- Emits `mask_logits` and `centerline_logits` only.
- Leaves data loading, split construction, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and lifecycle execution to trusted provider/Harness code.

See `PROPOSAL.md` for the full hypothesis, budget, and decision criteria.
