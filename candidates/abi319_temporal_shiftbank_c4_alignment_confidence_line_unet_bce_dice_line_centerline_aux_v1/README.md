# ABI-319 temporal shift-bank C4 alignment-confidence line U-Net

ABI-319 is a bounded exploratory Candidate Experiment for GOES ABI Contrail Segmentation.

It is a mechanism-changing follow-up to ABI-315's temporal shift-bank alignment scout. ABI-315 could align neighboring temporal features but did not stabilize connected thin-line evidence. ABI-319 couples that local alignment path to a C4 orientation-consensus line state, gated by the learned shift-bank confidence map, so temporal line support is added only where previous/next frames align with the center ABI Patch.

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
4. exposes the learned shift-confidence map;
5. derives center-frame signed detail;
6. builds a C4 orientation-consensus line state from aligned temporal support and center detail;
7. gates that C4 line state by alignment confidence before injecting it into the encoder seed and evidence head; and
8. emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Intended comparison

Primary comparisons are ABI-315 for the shift-bank family, ABI-311 for balanced temporal C4 evidence, ABI-306 for compact high precision, ABI-309 for recall-heavy temporal C4 behavior, and ABI-223/238 for temporal-attention continuity context.

This Candidate requests only the default exploratory budget; capped temporal-eligible evidence is feasibility/development evidence, not full-data promotion evidence.
