# ABI-324 temporal five-frame detail-consensus stabilized line-state late36

ABI-324 is a bounded late-improving Candidate Experiment for GOES ABI Contrail Segmentation. It continues the ABI-311 five-frame temporal C4 persistence/contrast line-state branch, targeting the diagnosed MIT and positive-patch undercoverage tail while preserving low negative-patch clutter.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It reuses ABI-311's temporal stem, C4 orientation line-state support, compact encoder/decoder, and trusted Line/Centerline auxiliary outputs. The mechanism change is a `DetailConsensusStabilizedHead` that fuses decoder evidence, center-frame temporal-stem detail, and early C4 line-state support, then adds a bounded non-negative recall residual only where learned mask/Line/Centerline and temporal-detail agreement gates survive a learned conflict guard.

This is architecture-internal evidence construction only. Candidate code does not implement data loading, temporal lookup, frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, temporal-eligible center selection, five-frame offsets, combined source-balanced sampling, random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-311/306/309 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-311, ABI-306, ABI-309, and ABI-223 on the temporal-eligible validation population. A useful result should improve MIT/positive-tail fixed-threshold recall or connectivity without ABI-309-scale clutter broadening.
