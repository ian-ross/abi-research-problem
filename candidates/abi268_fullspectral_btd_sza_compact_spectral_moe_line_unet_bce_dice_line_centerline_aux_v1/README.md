# ABI-268 compact spectral-regime MoE line U-Net

ABI-268 is a resource-aware family-development continuation of the ABI-267 spectral/SZA-regime mixture-of-experts idea. ABI-267 failed with a Harness-recorded `resource_failure` after exhausting the exploratory wall-clock budget, so ABI-268 reduces high-resolution MoE usage and channel widths while preserving the hypothesis that gates learned only from provider-approved ABI+SZA features can select useful local, dilated, and line-oriented transformations.

The Candidate consumes only `abi_16ch_plus_sza` tensors. It does not use longitude/latitude, Dataset Source identity, scene identity, route/location priors, temporal lookup, data loading, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, resource scheduling, or lifecycle behavior.
