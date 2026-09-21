# ABI-273 temporal line-state attention U-Net

ABI-273 is a bounded exploratory family-development continuation of the ABI-223/238 temporal-attention branch for GOES ABI Contrail Segmentation.

It preserves provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code only defines the PyTorch architecture.

The architecture moves line support earlier than the recent negative final-head variants. A temporal-attention stem forms appearance/change evidence and an orientation-aware line-state branch at full resolution. That bounded line state is injected into each encoder scale through lightweight learned gates before the ASPP decoder and a simple shared mask/line/centerline head. The intent is to preserve connected thin-line evidence through the feature pyramid without candidate-owned thresholding, postprocessing, or final logit boosting.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding or repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.
