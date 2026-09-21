# ABI-368 temporal recurrent C4 connectivity decoder late36

ABI-368 is a temporal-family development Candidate for GOES ABI Contrail Segmentation. It uses the trusted `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model starts from the ABI-255 compact recurrent-change temporal U-Net: provider-supplied previous/center/next ABI+SZA frames are converted to normalized ABI, SZA, and ABI-channel-derived BTD features, fused with a bidirectional ConvGRU state and explicit change evidence, then decoded by a compact ASPP U-Net.

The mechanism change is a final C4 orientation-shared connectivity decoder. Full-resolution decoder and skip features are refined, passed through a depthwise-separable strip-context block shared across four rotations, blended by learned orientation scores, and fused with local detail evidence before the mask, Line, and Centerline logits. The purpose is to address ABI-255's weak thin-line continuity without changing trusted data, loss, metric, Artifact Filter, sampling, thresholding, or temporal provisioning boundaries.

Candidate code remains architecture-only. It does not implement data loading, temporal lookup, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.
