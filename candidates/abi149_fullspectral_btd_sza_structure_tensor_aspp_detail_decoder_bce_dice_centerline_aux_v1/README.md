# ABI-149 full-spectral BTD+SZA structure-tensor ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps the ABI-130 SZA-aware ASPP/detail decoder training contract and adds a differentiable structure-tensor evidence front end computed from provider-approved ABI channels, thermal BTD planes, and Solar Geometry Input.

The controlled change is architectural: a small learned evidence projection is converted into Sobel-gradient structure-tensor features, including local line energy, coherence, and orientation-balance planes. These planes are concatenated before the existing ASPP/detail encoder-decoder so the model can learn to distinguish elongated contrail-like evidence from blob-like negative-patch clutter without candidate-owned thresholding, postprocessing, Artifact Filters, losses, targets, data loading, or sampling.

The model receives only `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus provider-approved Solar Geometry Input. It receives no longitude, latitude, reconstructed coordinate features, Dataset Source identity, external weights, or runtime downloads.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
