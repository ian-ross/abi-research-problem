# ABI-358 temporal recall-preserving C4 sidecar late36

This Candidate is a close, mechanism-changing continuation after ABI-356 and ABI-357 for capped temporal-eligible GOES ABI Contrail Segmentation.

It keeps the provider-owned `abi_16ch_plus_sza_temporal` input with `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. It preserves ABI-356's temporal-attention stem, compact U-Net encoder/decoder, ASPP context, and multi-scale temporal-change/center-detail skip fusion. The change from ABI-357 is final evidence fusion: the C4 rotation-shared line-continuity module no longer gates a compact anchor against recall evidence. Instead, `RecallPreservingC4Sidecar` keeps the decoder/high-resolution temporal support as an additive recall path, feeds the C4 line context to the auxiliary `line_logits` head, and adds only a small gated C4 residual to mask features.

The hypothesis is that this decoupling can recover more of ABI-356's fixed-threshold recall while retaining some of ABI-357's precision/connectivity benefit. Candidate code defines only model architecture and consumes Harness-provided tensors; it does not load data, implement temporal lookup, choose thresholds, define losses or metrics, apply Artifact Filters, derive targets, or use coordinates.

Key contract choices:

- Input mode: `abi_16ch_plus_sza_temporal`
- Temporal offsets: `[-1, 0, 1]`
- Data policy: `combined_source_balanced`, `temporal_eligible_center`, `random_mirroring`
- Loss: trusted `bce_dice`
- Auxiliary targets: trusted Line and Centerline targets via `weighted_bce`
- Optimizer/scheduler: AdamW with constant learning rate
- Default manifest epochs: 12, with a candidate-local late-improving budget request for 36 epochs
