# ABI-339 temporal-attention bottleneck line-token bridge U-Net

ABI-339 is a bounded temporal-attention mechanism scout for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

The model starts from an ABI-223-style compact temporal-attention U-Net and adds a cheap `BottleneckLineTokenBridge` after the ASPP context. The bridge operates only on the 32x32 bottleneck feature map: it summarizes learned features along rows and columns, expands those token summaries back to the bottleneck grid, and fuses them through a bounded learned gate before decoding. This tests whether long-axis line context can be injected before decoding without repeating the resource-failed full-resolution strip-token hierarchy from ABI-329/330 or the head-only orientation bridge from ABI-333.

This is architecture-internal feature construction only. Candidate code does not implement data loading, temporal lookup, temporal frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate features, downloads, resource scheduling, training loops, evaluation, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, three-frame offsets, source-balanced sampling, random mirroring, BCE-Dice training, constant LR, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch architecture and `build_model(input_spec, output_spec)` entry point.
- `PROPOSAL.md` records the hypothesis, comparisons, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-223/238 temporal attention, ABI-324 temporal C4 detail consensus, ABI-333 head-only orientation consensus, and ABI-329/330 resource-failed strip-token attempts. Useful evidence would complete within the exploratory budget and improve connected-line evidence or source-balanced fixed-threshold Dice without broadening negative-patch clutter.
