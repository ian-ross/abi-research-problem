# ABI-093 stable full-spectral BTD large-kernel line-context net

Repair Candidate for GOES ABI Contrail Segmentation. ABI-092 failed with a Harness-recorded non-finite training state in the learned channel mixer gradient at epoch 2 batch 212. ABI-093 preserves the large-kernel line-context scout hypothesis while reducing residual amplification and lowering the allowlisted constant learning rate.

The model uses only provider-approved ABI channels 1-16 plus brightness-temperature-difference planes derived from those same channels. It applies bounded in-model normalization/BTD feature scaling, a learned 1x1 channel mixer, residual-scaled horizontal/vertical/local/dilated large-kernel blocks, pyramid context, and a multi-scale line head. It emits `mask_logits` plus provider-derived `centerline_logits` auxiliary output.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned. The candidate receives no longitude, latitude, or reconstructed coordinate inputs and performs no network access or runtime weight downloads.
