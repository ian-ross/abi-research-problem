# ABI-286 temporal C4 continuity-evidence bridge U-Net

ABI-286 is a mechanism-changing temporal-family continuation after ABI-285. ABI-285 produced the best current capped temporal-eligible aggregate filtered Dice and recall among recent temporal comparators, but its failure-bucket review showed weak connected-line continuity and broader negative-patch clutter.

This Candidate keeps ABI-285's provider-owned `abi_16ch_plus_sza_temporal` input path, offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` frame selection, per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, and early C4 orientation line-state injected into the encoder. The new mechanism is a full-resolution continuity-evidence bridge after the decoder: it projects the early temporal C4 line state to decoder resolution, applies a second C4 orientation-consensus block conditioned on decoder appearance, gates supported continuity evidence, and feeds a dual evidence head combining region evidence with line-continuity evidence before `mask_logits`.

Hypothesis: full-resolution agreement between decoder appearance and early temporal line state can preserve ABI-285's fixed-threshold recall/source-balance gains while improving connected thin-line organization toward ABI-223/238.

This is an exploratory/default-budget Candidate, not a promotion claim. Candidate code remains architecture-only and does not implement thresholds, morphology, postprocessing, Artifact Filters, metrics, losses, data loading, temporal lookup, frame repair/padding, sample selection, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.
