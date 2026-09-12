# ABI-243 temporal recurrent line-state U-Net

ABI-243 is a bounded exploratory Candidate for GOES ABI Contrail Segmentation. It consumes the trusted `abi_16ch_plus_sza_temporal` input with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model keeps ABI-242's compact bidirectional ConvGRU temporal stem over provider-supplied previous/center/next ABI+SZA frame features, then adds a differentiable oriented line-state pyramid. Horizontal, vertical, and dilated local-line depthwise branches build full-resolution continuity evidence from the recurrent temporal stem; that line state is downsampled alongside U-Net skip scales and gates decoder fusion. Final mask logits are produced from a line-refined decoder feature, with trusted `line_logits` and `centerline_logits` auxiliary outputs for provider-owned auxiliary losses.

The hypothesis is that carrying line-state features through the decoder will improve the weak selected-checkpoint connectivity observed in ABI-242, without candidate-owned morphology, thresholding, postprocessing, Artifact Filters, temporal lookup, data loading, target derivation, losses, metrics, augmentation, sampling, training loops, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
