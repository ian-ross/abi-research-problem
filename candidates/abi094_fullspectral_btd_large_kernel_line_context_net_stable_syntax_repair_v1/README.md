# ABI-094 stable full-spectral BTD large-kernel line-context net syntax repair

Repair Candidate for GOES ABI Contrail Segmentation. ABI-093 (`run_20260830_002454_13b411`) smoke-failed with a Harness-recorded `candidate_bug` caused by a stray `},{` after the `StableFullSpectralBTDLargeKernelLineContextNet` class docstring. ABI-094 fixes only that syntax defect and preserves ABI-093's large-kernel line-context scout hypothesis and comparison targets.

The model uses only provider-approved ABI channels 1-16 plus brightness-temperature-difference planes derived from those same channels. It applies bounded in-model normalization/BTD feature scaling, a learned 1x1 channel mixer, residual-scaled horizontal/vertical/local/dilated large-kernel blocks, pyramid context, and a multi-scale line head. It emits `mask_logits` plus provider-derived `centerline_logits` auxiliary output.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned. The candidate receives no longitude, latitude, or reconstructed coordinate inputs and performs no network access or runtime weight downloads.
