# ABI-261 temporal high-resolution line-accumulation recall U-Net

Candidate Experiment for GOES ABI Contrail Segmentation.

ABI-261 is a mechanism-changing temporal family-development scout after ABI-240/255/259. It keeps provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, and trusted Line/Centerline auxiliary targets. The architecture changes the line-continuity mechanism: instead of ABI-240's low-resolution line accumulator or ABI-259's decoder-side support block, it accumulates directional line evidence at the native 256x256 stem plus a half-resolution longer-span path, then uses a bounded recall-preserving mask head to lift supported contrail logits without candidate-owned thresholding or postprocessing.

Candidate code defines model architecture only and does not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, longitude/latitude features, Dataset Source identity, resource scheduling, or lifecycle behavior.
