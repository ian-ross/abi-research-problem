# ABI-157 full-spectral BTD+SZA full-scale skip ASPP/detail decoder deterministic-shuffle BCE-Dice centerline auxiliary

Family-development data-policy continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-154s provider-approved `abi_16ch_plus_sza` architecture, full-spectral raw+BTD+SZA front end, full-scale skip ASPP/detail decoder, trusted BCE-Dice primary loss, trusted random mirroring, AdamW learning rate, and low-weight provider-derived Centerline Target auxiliary head.

The controlled manifest change is `data.sampling_policy: deterministic_shuffle` instead of `combined_source_balanced`. The goal is to test whether a simpler provider-owned traversal over the same representative capped records can recover some of ABI-154s under-recall and late-epoch instability while retaining the precision/connectivity and positive-area discipline that survived ABI-154s whole-validation diagnostic.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
