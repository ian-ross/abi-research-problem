# ABI-274 temporal line-state attention U-Net late36

ABI-274 is an exact late-improving close continuation of ABI-273 for GOES ABI Contrail Segmentation.

It preserves provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code only defines the PyTorch architecture copied from ABI-273, with the Candidate identifier updated.

The architecture carries an early temporal line state through the encoder pyramid. A temporal-attention stem forms appearance/change evidence and an orientation-aware line-state branch at full resolution; lightweight learned gates inject that bounded line state into each encoder scale before the ASPP decoder and simple mask/line/centerline heads. The late36 request tests whether ABI-273 final-epoch improving, source-informative trajectory is truncated by the exploratory budget.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding or repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.
