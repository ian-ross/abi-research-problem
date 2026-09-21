# ABI-347 temporal C4 orientation-bridge compact recall late36

ABI-347 is a mechanism-changing close continuation of the three-frame temporal C4 line-state branch. It keeps ABI-346/306's trusted temporal input contract (`abi_16ch_plus_sza_temporal`, `temporal_eligible_center`, offsets `[-1, 0, 1]`), BCE-Dice primary loss, Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, AdamW, constant LR, and batch size 2.

The architectural change is the final logit head. ABI-346 recovered true-positive area but failed to improve connected-line continuity. ABI-347 replaces the connected-recall ladder with an orientation-bridge compact-recall head: a learned C4-style multi-orientation bridge over head features gates any bounded uncertainty-band mask-logit lift, and weak line/centerline/bridge evidence applies a compactness veto. The goal is to retain ABI-306-style compact precision while lifting only continuous true-contrail segments to the fixed 0.5 threshold.

Candidate code defines only architecture and allowed manifest choices. It does not own temporal lookup, data loading, sampling implementation, losses, metrics, Artifact Filters, threshold selection, postprocessing, coordinates, downloads, resource scheduling, or lifecycle behavior.
