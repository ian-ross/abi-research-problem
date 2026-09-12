# ABI-241 temporal high-resolution change-skip U-Net

ABI-241 is a bounded exploratory Candidate for GOES ABI Contrail Segmentation. It consumes the trusted `abi_16ch_plus_sza_temporal` input with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model keeps the compact temporal-attention ABI+SZA+BTD stem used by the temporal frontier, then adds a full-resolution temporal-difference skip bridge. The bridge forms approved-channel change features from previous/center/next frame tensors, applies learned oriented depthwise support at full spatial resolution, and injects multi-scale change skips into the U-Net decoder path. The goal is to preserve the recall gains seen in ABI-240 while improving filtered contrail connectivity versus low-resolution line accumulation.

Outputs are `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary heads. Candidate code does not implement data loading, temporal lookup, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
