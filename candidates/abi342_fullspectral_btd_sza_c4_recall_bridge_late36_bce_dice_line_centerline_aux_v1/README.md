# ABI-342 full-spectral BTD+SZA C4 recall bridge late36

ABI-342 is a mechanism-changing family-development continuation of the ABI-249 single-frame C4/orientation-prior branch. ABI-249 is the compact high-precision C4 comparator but remains recall-limited. ABI-342 keeps the provider-owned `abi_16ch_plus_sza` input and the trusted BCE-Dice, Line Target, Centerline Target, source-balanced sampling, random-mirroring augmentation, AdamW, and constant-LR policies, then changes only architecture internals.

The model preserves ABI-249's full-spectral normalized ABI + thermal-BTD + Solar Geometry Input front end, signed-detail stem, compact U-Net/ASPP decoder, and C4 rotation-shared anisotropic line-context block. The head replaces the direct C4 mask projection with a bounded dual-evidence recall bridge: a compact anchor mask is adjusted by a small signed residual, gated continuously by C4 line context and trusted Line auxiliary evidence. The intent is to raise true contrail logits at the fixed 0.5 threshold without the broad negative-patch clutter seen in recent temporal recall-router branches.

The candidate is architecture-only. It does not implement data loading, sample selection, target derivation, custom losses, metrics, thresholding, postprocessing, Artifact Filters, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.
