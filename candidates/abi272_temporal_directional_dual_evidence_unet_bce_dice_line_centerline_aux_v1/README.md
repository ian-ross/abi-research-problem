# ABI-272 temporal directional dual-evidence U-Net

ABI-272 is a bounded exploratory family-development continuation of the ABI-223/238 temporal-attention branch for GOES ABI Contrail Segmentation.

It preserves provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code only defines the PyTorch architecture.

The architecture starts from the ABI-238 temporal-attention fusion U-Net with full-resolution directional context, then replaces the independent final logits with a dual-evidence segmentation head. The head learns separate region, line, and centerline logits and adds only a bounded learned residual from line/centerline evidence through a differentiable agreement gate. The intent is to raise true contrail evidence at the fixed 0.5 threshold where directional line support agrees with the region decoder, without repeating ABI-271's loss-driven broad positive expansion or moving thresholding/postprocessing into candidate code.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding or repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.
