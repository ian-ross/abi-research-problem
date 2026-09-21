# ABI-348 temporal five-frame dual-state connectivity blend late36

ABI-348 is a family-development continuation in the provider-owned five-frame temporal C4/detail-consensus branch. It keeps the ABI-324 profiled five-frame temporal stem/encoder/decoder and replaces the final evidence head with a dual-state connectivity-preserving blend.

The head predicts a compact connected anchor and a bounded recall candidate, then blends them only where learned decoder/detail/temporal-line agreement, Line evidence, and Centerline evidence support the replacement and a disagreement guard remains low. This is intended to test whether positive-tail recall can be recovered without the broad-footprint connectivity loss seen in ABI-325/341/344 additive recall sidecars.

## Contract use

- Input mode: `abi_16ch_plus_sza_temporal`
- Trusted frame selection: `temporal_eligible_center`
- Temporal offsets: `[-2, -1, 0, 1, 2]`
- Sampling policy: `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Loss: trusted `bce_dice`
- Auxiliary targets: trusted Line and Centerline weighted BCE outputs
- Optimizer/scheduler: AdamW with constant learning rate
- Batch size: 2
- Requested budget: `late_improving` 36 epochs with exploratory fallback if denied

Candidate code defines architecture only. It does not implement data loading, temporal lookup, frame repair, target derivation, custom losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Comparison targets

Use ABI-324 and ABI-337 as compact/balanced five-frame temporal C4 comparators, ABI-344/325 as broad recall diagnostics, ABI-306 as compact high-precision temporal C4 comparator, and ABI-223 as temporal-attention connectivity comparator. This is capped temporal-eligible feasibility evidence, not whole-validation promotion evidence.
