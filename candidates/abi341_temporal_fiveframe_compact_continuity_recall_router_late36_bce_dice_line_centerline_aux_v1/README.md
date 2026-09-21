# ABI-341 temporal five-frame compact continuity recall router late36

Five-frame temporal C4/detail-consensus U-Net with a compact-state-protected recall router. The Candidate targets the ABI-324/337/338 split between compact connected states and higher-recall cluttered states.

## Summary

The model consumes provider-owned `abi_16ch_plus_sza_temporal` tensors for offsets `[-2, -1, 0, 1, 2]` with trusted `temporal_eligible_center` selection. It keeps the profiled temporal C4/detail-consensus encoder-decoder and replaces the mask head with `CompactContinuityRecallRouterHead`.

The head predicts base mask, Line, and Centerline logits, then adds:

- a small signed compact continuity anchor gated by mask/Line/Centerline/detail/line-state agreement;
- a bounded positive recall lift applied only in the continuous soft uncertainty band around the base mask probability and under the same agreement/conflict gates.

This is architecture-only. The Candidate does not implement data loading, temporal lookup, losses, metrics, thresholds, postprocessing, Artifact Filters, augmentation, sampling, coordinate features, downloads, training loops, resource scheduling, or ledger writes.

## Contract choices

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza_temporal`
- Frame-selection policy: `temporal_eligible_center`
- Temporal offsets: `[-2, -1, 0, 1, 2]`
- Sampling: `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Primary loss: trusted `bce_dice`
- Auxiliary targets: `line_logits` and `centerline_logits`
- Optimizer/scheduler: AdamW, LR 0.0003, constant LR
- Batch size: 2
- Requested budget: `late_improving` to 36 epochs via `budget_request.yaml`; exploratory fallback if denied

## Comparison targets

Primary capped temporal-eligible comparators are ABI-324, ABI-337, ABI-338, and ABI-223. Whole-validation references ABI-202 and ABI-249 are context only; this Candidate is capped temporal-eligible feasibility evidence, not a promotion claim.
