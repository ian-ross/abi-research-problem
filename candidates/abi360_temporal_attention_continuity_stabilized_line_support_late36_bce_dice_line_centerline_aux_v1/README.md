# ABI-360 temporal-attention continuity-stabilized line support late36

Candidate `abi360_temporal_attention_continuity_stabilized_line_support_late36_bce_dice_line_centerline_aux_v1` is a close, mechanism-changing temporal family-development continuation after ABI-350/358/359.

It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The architecture keeps ABI-350's finite ABI+SZA+BTD per-frame feature builder, temporal-attention stem, compact U-Net encoder/decoder, ASPP bottleneck, and orientation-aware line support injected into encoder skips before decoder fusion.

The main change is a `ContinuityStabilizedEvidenceHead`: the refined decoder feature remains a compact anchor, while the full-resolution line-supported skip and decoder detail features are projected into bounded orientation-line evidence and added through a learned agreement gate before producing `mask_logits`, `line_logits`, and `centerline_logits`. The goal is to stabilize ABI-359's connected-line signal without ABI-356-style broad low-precision footprints or Candidate-owned thresholding/postprocessing.

This candidate declares only trusted manifest policies: source-balanced sampling, random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets with weighted BCE, AdamW, constant LR, and batch size 2. It does not implement data loading, temporal lookup, sample selection, losses, metrics, Artifact Filters, postprocessing, threshold selection, augmentation transforms, coordinate features, Dataset Source identity features, downloads, or resource scheduling.

Requested evidence is capped temporal-eligible late-improving feasibility, not full Working Validation Split promotion evidence.
