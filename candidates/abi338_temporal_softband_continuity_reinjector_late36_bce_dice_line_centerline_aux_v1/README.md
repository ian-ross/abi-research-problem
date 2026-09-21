# ABI-338 temporal soft-band continuity reinjector late36

ABI-338 is a mechanism-changing family-development continuation of the five-frame temporal C4/detail-consensus branch after ABI-324 and ABI-337. It targets the observed split between compact high-connectivity temporal states and higher-recall but more fragmented/cluttered states.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. It keeps the profiled ABI-324 temporal stem, early C4 orientation line state, compact encoder/decoder, line-state injection, and trusted Line/Centerline auxiliary outputs. The mechanism change is a `SoftBandContinuityReinjectorHead`: it keeps a bounded consensus recall residual and adds a second bounded positive continuity residual only where base mask probability is softly uncertain and learned Line, Centerline, center-frame detail, and temporal C4 line-state evidence agree.

This is architecture-internal evidence construction only. Candidate code does not implement data loading, temporal lookup, temporal frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate features, downloads, resource scheduling, training loops, evaluation, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, five-frame offsets, source-balanced sampling, random mirroring, BCE-Dice training, constant LR, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch architecture and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-324/337/328 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparisons, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-324, ABI-337, ABI-328, and ABI-223 on the temporal-eligible validation population. Useful evidence would improve recall, MIT balance, or connected-line continuity without ABI-325/309-scale negative-patch clutter broadening. Whole-validation promotion would require separate trusted evaluation.
