# ABI-255 temporal recurrent change-state U-Net late36

ABI-255 is the late-improving close continuation of ABI-242 for GOES ABI Contrail Segmentation. It preserves the trusted `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model is unchanged from ABI-242: a compact bidirectional ConvGRU-style temporal state over provider-supplied previous/center/next frame features, fused with explicit center-neighbor change evidence before a compact ASPP U-Net decoder. Outputs are `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary heads.

The only intended difference from ABI-242 is the candidate-local `budget_request.yaml` requesting the approved late-improving budget. Candidate code remains architecture-only and does not implement data loading, temporal lookup, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
