# ABI-227 temporal line-consistency attention U-Net

ABI-227 is a temporal-family development Candidate for GOES ABI Contrail Segmentation. It consumes trusted `abi_16ch_plus_sza_temporal` inputs with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model starts from ABI-223's compact temporal-attention U-Net: bounded finite ABI+SZA+BTD features per provider-supplied frame, shared frame projection, per-pixel temporal attention relative to the center frame, signed/absolute change features, and a compact U-Net/ASPP decoder. ABI-227 adds a differentiable temporal-line consistency block in the fused temporal stem. That block uses learned anisotropic and dilated line-context branches and a center/temporal-agreement gate to strengthen line-shaped features before encoding.

This Candidate is compared primarily to ABI-222 at the same exploratory budget, ABI-223 as the late36 temporal-family frontier, ABI-226 as the five-frame wider-window scout, and ABI-218 as the matched temporal-eligible single-frame control. It is not a promotion candidate against ABI-202.

Contract boundaries: no candidate-owned data loading, temporal lookup, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
