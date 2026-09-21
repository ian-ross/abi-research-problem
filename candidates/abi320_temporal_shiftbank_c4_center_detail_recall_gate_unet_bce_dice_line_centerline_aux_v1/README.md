# ABI-320 temporal shift-bank C4 center-detail recall-gate U-Net

ABI-320 is a bounded exploratory Candidate Experiment for GOES ABI Contrail Segmentation.

It is a mechanism-changing follow-up to ABI-319's alignment-confidence-gated shift-bank/C4 line-state model. ABI-319 cleaned up ABI-315's shift-bank predictions and improved precision/connectivity, but still under-recalled true contrails relative to ABI-311/309. ABI-320 keeps the same provider-owned three-frame temporal input and alignment-confidence/C4 cleanliness, then changes the evidence head: an additional center-detail recall gate can add a small bounded logit lift only where full-resolution center detail, aligned temporal support, and C4 line-state logits agree, with a disagreement/clutter veto when those supports diverge.

## Contract boundary

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame-selection policy: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- Candidate-visible channels: ABI channels 1-16 plus Solar Geometry Input per frame.
- Forbidden: longitude/latitude, Dataset Source identity, data loading, temporal lookup, sample selection, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation implementation, downloads, training loops, resource scheduling, and lifecycle code.

## Architecture summary

The model:

1. builds finite per-frame normalized ABI, thermal-BTD, and Solar Geometry Input features;
2. encodes previous, center, and next frames with a shared stem;
3. aligns previous/next features to the center through a no-wrap nine-shift differentiable shift bank;
4. gates C4 orientation-consensus line state by the learned shift-confidence map;
5. decodes a compact U-Net feature pyramid with aligned temporal, center-detail, and C4 support;
6. uses a center-detail recall-gate head to raise uncertain logits only under temporal/C4/detail agreement and suppress disagreement; and
7. emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Intended comparison

Primary capped temporal-eligible comparisons are ABI-319 for clean shift-bank/C4 behavior, ABI-315 for the original shift-bank scout, ABI-311 for balanced five-frame temporal C4 evidence, ABI-309 for recall-heavy temporal C4 behavior, and ABI-306 for compact high precision.

This Candidate requests only the default exploratory budget; capped temporal-eligible evidence is feasibility/development evidence, not full-data promotion evidence.
