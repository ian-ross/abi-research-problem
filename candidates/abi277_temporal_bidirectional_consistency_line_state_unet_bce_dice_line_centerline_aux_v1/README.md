# ABI-277 temporal bidirectional-consistency line-state U-Net

ABI-277 is a mechanism-changing temporal-family continuation after ABI-274/275/276 for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and `temporal_eligible_center` selection.

The hypothesis is that ABI-274's temporal line-state branch raised recall/source coverage but fragmented connected thin-line evidence because one-sided temporal changes and persistent contrail evidence were not separated before encoder injection. ABI-277 keeps the early temporal line-state stem, then adds a bidirectional temporal-consistency state built from approved per-frame features: center-minus-previous, next-minus-center, center-minus-neighbor-mean persistence, next-minus-previous motion, absolute before/after agreement, and before/after imbalance. Orientation-aware filters over that consistency state are injected together with the line state at all encoder scales and at the final refinement stage.

The candidate remains architecture/manifest-only. It does not implement data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Expected comparison

Primary comparison targets are ABI-274 for recall/source-balance and ABI-223 for connected-line temporal behavior on the temporal-eligible validation population. Success would be a finite, non-collapsed exploratory run that improves ABI-276 and approaches ABI-274 filtered Dice while lifting selected-checkpoint connectivity above ABI-274/276 without a broad predicted-positive expansion.
