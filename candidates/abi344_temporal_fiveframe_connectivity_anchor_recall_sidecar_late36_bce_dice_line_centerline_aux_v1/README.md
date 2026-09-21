# ABI-344 temporal five-frame connectivity-anchor recall sidecar

ABI-344 is a mechanism-changing continuation of the ABI-324 five-frame temporal C4/detail-consensus branch for GOES ABI Contrail Segmentation.

It keeps the trusted provider-owned `abi_16ch_plus_sza_temporal` input with `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW, constant LR, and batch size 2. The architecture reuses the ABI-324 temporal frame features, C4 line-state stem, encoder/decoder, line-state injection, ASPP context, and high-resolution directional context. The final head changes to an explicit two-state evidence model:

- a compact connectivity anchor from decoder features plus early C4 line-state support;
- a recall sidecar that can see center-frame detail as well as line support;
- a bounded non-negative recall lift only where anchor uncertainty, Line/Centerline evidence, detail alignment, line-state alignment, and sidecar/anchor agreement all support it;
- no candidate-owned thresholds, postprocessing, Artifact Filters, data loading, losses, metrics, sampling, coordinates, temporal lookup, downloads, resource scheduling, or lifecycle logic.

The intended diagnostic is whether separating a stable compact connectivity anchor from a learned recall sidecar can retain ABI-324-like compactness/connectivity while recovering some of the positive-tail recall seen in ABI-341 without its negative-patch clutter.

See `PROPOSAL.md` for the hypothesis, comparison targets, budget request, success criteria, and fallback decision.
