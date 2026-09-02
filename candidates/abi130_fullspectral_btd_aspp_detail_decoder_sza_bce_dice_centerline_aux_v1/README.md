# ABI-130 full-spectral BTD+SZA ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-126's compact ASPP/detail encoder-decoder, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change is provider-approved Solar Geometry Input: `input_mode` changes from `abi_16ch` to `abi_16ch_plus_sza`. The model uses GOES ABI channels 1-16 for normalized raw and deterministic thermal BTD features, then adds normalized SZA and `cos(SZA)` illumination features to the front end. It receives no longitude, latitude, reconstructed coordinate features, or Dataset Source identity.

The hypothesis is that SZA can help the conservative ABI-126 BCE-Dice branch recover MIT recall and fixed-threshold calibration while retaining its strong positive-area discipline, precision, connectivity, and Google performance.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
