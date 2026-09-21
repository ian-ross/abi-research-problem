# ABI-359 temporal alignment C4 center-detail bridge late36

Candidate `abi359_temporal_alignment_c4_center_detail_bridge_late36_bce_dice_line_centerline_aux_v1` is a mechanism-changing temporal family-development continuation after ABI-356/358.

It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The architecture keeps the finite ABI+SZA+BTD per-frame feature builder, temporal-attention stem, compact U-Net encoder/decoder, ASPP bottleneck, and multi-scale temporal-change skip support from the recent temporal branch.

The main change is an early `CenterDetailC4AlignmentBridge`: center-frame detail and before/after temporal-change features seed a C4 rotation-shared line context before encoder downsampling. That context is added as a small learned gated residual to the stem, used by the Line auxiliary head, and blended with the final decoder features. The goal is to make continuity evidence available throughout the decoder without turning the C4 path into a late recall-suppressing veto.

This candidate declares only trusted manifest policies: source-balanced sampling, random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets with weighted BCE, AdamW, constant LR, and batch size 2. It does not implement data loading, temporal lookup, sample selection, losses, metrics, Artifact Filters, postprocessing, threshold selection, augmentation transforms, coordinate features, Dataset Source identity features, downloads, or resource scheduling.

Requested evidence is capped temporal-eligible late-improving feasibility, not full Working Validation Split promotion evidence.
