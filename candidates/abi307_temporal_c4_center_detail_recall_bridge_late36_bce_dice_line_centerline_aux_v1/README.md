# ABI-307 temporal C4 center-detail recall bridge late36

ABI-307 is a mechanism-changing family-development continuation of ABI-306 for GOES ABI Contrail Segmentation.

It keeps the provider-owned temporal input contract (`abi_16ch_plus_sza_temporal`, offsets `[-1, 0, 1]`, `temporal_eligible_center`), the ABI-306 temporal C4 orientation line-state U-Net backbone, BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The new mechanism is a compact center-frame detail recall bridge inserted before the logit head.

The bridge projects center-frame ABI/SZA/BTD features, applies local plus horizontal/vertical detail filters, aligns ABI-306's early temporal C4 line state to full resolution, and adds a bounded gated residual to decoder features. The intent is to recover ABI-306's positive-patch under-recall tail while preserving its compact high-precision operating point and avoiding ABI-285-like clutter.

This Candidate does not own data loading, temporal lookup, temporal-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholding, postprocessing, target derivation, coordinate features, Dataset Source identity, downloads, training loops, resource scheduling, or prediction retention.

A `late_improving` budget is requested because the parent ABI-306 run was finite, resource-safe, non-collapsed, and selected its best checkpoint at epoch 36. If denied, the exploratory budget result remains the bounded evidence.
