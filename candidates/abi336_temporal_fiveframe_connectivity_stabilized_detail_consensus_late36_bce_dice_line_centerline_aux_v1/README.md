# ABI-336 temporal five-frame connectivity-stabilized detail consensus late36

ABI-336 is a bounded late-improving Candidate Experiment for GOES ABI Contrail Segmentation. It is a close but mechanism-changing continuation of ABI-324, the current balanced temporal C4/detail-consensus comparator on the temporal-eligible validation population.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. It reuses ABI-324's finite ABI/Solar Geometry Input normalization, five-frame temporal stem, C4 orientation line-state support, compact encoder/decoder, ASPP context, high-resolution directional context, BCE-Dice loss, and Line/Centerline auxiliary outputs.

The mechanism change is a `ConnectivityStabilizedDetailConsensusHead`. It adds learned directional continuity support inside the final head, allows a bounded recall residual only where decoder, center-frame detail, Line, Centerline, temporal line-state, and continuity evidence agree, and applies a small learned isolation veto against decoder-positive but line-discontinuous clutter. This targets the ABI-324/328 recurring failure mode where high-connectivity compact states and higher-recall selected states remained decoupled.

Candidate code does not implement data loading, temporal lookup, frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, temporal-eligible center selection, five-frame offsets, combined source-balanced sampling, random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the Harness-owned late-improving budget from ABI-324/325/328 parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped temporal-eligible comparisons are ABI-324, ABI-325, ABI-328, ABI-311, ABI-306, ABI-309, and ABI-223. A useful result should improve or credibly tie ABI-324 aggregate/source Dice while raising connected-line continuity or positive-tail recall without moving toward ABI-325/309-scale broad footprints.
