# ABI-327 temporal five-frame change-salience C4 line-state late36

ABI-327 is a bounded late-improving Candidate Experiment for GOES ABI Contrail Segmentation. It continues the ABI-324/325/326 five-frame temporal C4 branch after diagnostics showed that final-tail evidence can affect positive-patch recall but either broadens clutter or weakens connected-line behavior.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It reuses ABI-324 finite temporal ABI/Solar Geometry Input feature building, persistence/contrast temporal attention, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injection, high-resolution directional context, and trusted Line/Centerline auxiliary outputs. The mechanism change is earlier than ABI-325/326: the temporal stem computes center-vs-inner motion, center-vs-outer motion, before/after temporal slope, and center-vs-attended gap features, projects them into a bounded change-salience state, and uses that salience to gate the C4 line state before the encoder pyramid.

This is architecture-internal evidence construction only. Candidate code does not implement data loading, temporal lookup, frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, temporal-eligible center selection, five-frame offsets, combined source-balanced sampling, random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-324/311/326 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-324, ABI-326, ABI-325, ABI-311, ABI-306, ABI-309, and ABI-223 on the temporal-eligible validation population. A useful result should improve MIT/positive-tail recall or connected-line continuity without moving toward ABI-325-style broad negative-patch clutter.
