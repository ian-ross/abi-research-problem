# ABI-325 temporal five-frame positive-tail evidence reinjector late36

ABI-325 is a bounded late-improving Candidate Experiment for GOES ABI Contrail Segmentation. It continues the ABI-324 five-frame temporal C4 detail-consensus branch after temporal-eligible diagnostics showed a real aggregate/connectivity gain but remaining positive-patch undercoverage and MIT positive-tail weakness.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It reuses ABI-324's finite temporal ABI/Solar Geometry Input feature builder, persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injection, high-resolution directional context, and trusted Line/Centerline auxiliary outputs. The mechanism change is a `PositiveTailEvidenceReinjector` before the final detail-consensus head: it projects decoder, center-frame detail, and early temporal line-state evidence into a shared full-resolution memory, then applies a bounded residual to decoder features only where learned detail-line agreement and background guards support the pixel.

This is architecture-internal evidence construction only. Candidate code does not implement data loading, temporal lookup, frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, temporal-eligible center selection, five-frame offsets, combined source-balanced sampling, random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-324/311/306 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-324, ABI-311, ABI-306, ABI-309, and ABI-223 on the temporal-eligible validation population. A useful result should preserve ABI-324's cleaner footprint and aggregate/source gains while reducing positive-patch undercoverage through higher fixed-threshold recall or connectivity without ABI-309-scale clutter broadening.
