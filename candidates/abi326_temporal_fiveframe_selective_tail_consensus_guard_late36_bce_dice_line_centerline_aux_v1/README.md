# ABI-326 temporal five-frame selective tail consensus guard late36

ABI-326 is a bounded late-improving Candidate Experiment for GOES ABI Contrail Segmentation. It continues the ABI-324/325 five-frame temporal C4 branch after diagnostics showed that ABI-325 repaired some positive-patch low-recall tails but broadened predictions and increased negative-patch clutter.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It reuses ABI-324/325 finite temporal ABI/Solar Geometry Input feature building, persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injection, high-resolution directional context, and trusted Line/Centerline auxiliary outputs. The mechanism change is a `SelectiveTailConsensusGuard` before the final detail-consensus head: it reuses decoder, center-frame detail, and early temporal line-state evidence but applies a smaller bounded residual only when feature-level detail, line-state, and memory agreement exceed neutral support and learned guards do not indicate background disagreement.

This is architecture-internal evidence construction only. Candidate code does not implement data loading, temporal lookup, frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, temporal-eligible center selection, five-frame offsets, combined source-balanced sampling, random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-325/324/311 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-324, ABI-325, ABI-311, ABI-306, ABI-309, and ABI-223 on the temporal-eligible validation population. A useful result should retain part of ABI-325's MIT/positive-tail recall gain while recovering ABI-324-like compactness, precision, source balance, and connectivity.
