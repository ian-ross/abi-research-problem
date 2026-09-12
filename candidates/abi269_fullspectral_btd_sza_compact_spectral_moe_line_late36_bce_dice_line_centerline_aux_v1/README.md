# ABI-269 compact spectral-regime MoE line U-Net late36

Late-improving close continuation of ABI-268. The Candidate keeps the compact full-spectral ABI+Solar Geometry Input spectral-regime MoE line U-Net architecture unchanged and requests the approved `late_improving` budget based on ABI-268's final-epoch best, finite, source-informative trajectory.

The model consumes only provider-owned `abi_16ch_plus_sza` inputs and returns `mask_logits`, `line_logits`, and `centerline_logits`. It selects trusted `combined_source_balanced` sampling, `random_mirroring`, BCE-Dice primary loss, Line and Centerline weighted-BCE auxiliaries, AdamW with constant learning rate, batch size 4, and manifest `max_epochs: 12`; the longer 36-epoch budget is requested only through `budget_request.yaml`.

Candidate code is architecture-only and does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle control.
