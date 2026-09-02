# ABI-078 full-spectral BTD frequency-gated line U-Net BCE-Dice continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-068 frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD planes, learned spectral mixer, and centerline auxiliary output unchanged while changing only the trusted primary loss from `focal_tversky` to allowlisted `bce_dice`.

The hypothesis is that BCE-Dice may recover some of ABI-066s precision/connectivity and reduce ABI-068s negative-patch clutter without adding more late refiner, gating, suppressor, or auxiliary-head capacity. The model uses only provider-approved ABI channels 1-16 plus derived BTD planes from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
