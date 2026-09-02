# ABI-079 full-spectral BTD nested-skip U-Net scout

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate broadens away from the ABI-068 frequency-gated line U-Net late-refiner branch by replacing its high/low-frequency skip gates and late feature modules with a compact UNet++-style nested decoder. Dense multi-depth skip fusion is intended to preserve thin high-resolution evidence while allowing deeper cloud-context features to correct false positives before the final mask head.

The model uses provider-approved `abi_16ch` input, normalized ABI channels 1-16, thermal brightness-temperature-difference planes derived only from those approved ABI channels, and a learned 1x1 spectral mixer. It emits primary `mask_logits` and a provider-derived `centerline_logits` auxiliary output. It receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
