# ABI-275 temporal C4 continuity-bridge U-Net

ABI-275 is an exploratory mechanism-changing continuation after ABI-274 for GOES ABI Contrail Segmentation.

It preserves provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs.

The architecture keeps ABI-274's temporal attention/change stem, early orientation-aware line state, line-state injection into each encoder scale, ASPP decoder, and mask/line/centerline heads. It adds a differentiable full-resolution C4 continuity bridge before the heads: a shared rotated line-support filter is applied at 0/90/180/270 degrees, orientation responses are rotated back and fused with the carried temporal line state, and a learned residual gate injects only supported continuity evidence into the decoder features. The goal is to preserve ABI-274's recall/source lift while improving connected thin-line continuity and negative-patch cleanliness.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding or repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.
