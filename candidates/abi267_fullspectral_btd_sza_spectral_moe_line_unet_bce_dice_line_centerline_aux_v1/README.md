# ABI-267 spectral-regime mixture-of-experts line U-Net

ABI-267 is a bounded family scout for GOES ABI Contrail Segmentation. It tests a compact spectral/SZA-regime mixture-of-experts U-Net using only provider-approved `abi_16ch_plus_sza` inputs. Learned gates are derived from approved image features, not Dataset Source identity, coordinates, scene identity, or route/location priors.

The Candidate defines architecture only. Data loading, split logic, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, execution, and lifecycle behavior remain trusted Harness/provider responsibilities.
