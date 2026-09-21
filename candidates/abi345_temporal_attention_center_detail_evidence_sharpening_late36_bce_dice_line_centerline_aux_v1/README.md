# ABI-345 temporal-attention center-detail evidence sharpening late36

ABI-345 is a mechanism-changing close continuation of the ABI-223 temporal-attention branch for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

The model starts from the ABI-223 compact temporal-attention fusion U-Net and replaces the simple mask/Line/Centerline heads with a bounded `CenterDetailEvidenceSharpeningHead`. The head forms an anchor logit from refined decoder features, builds high-resolution evidence from refined decoder, decoder skip, encoder scale-0, and temporal-stem features, and adds only a small bounded residual gated by agreement and anchor uncertainty. The intent is to raise fixed-threshold logits for true thin contrail evidence while preserving ABI-223-style compact connected predictions.

This is architecture-internal logit construction only. Candidate code does not implement data loading, temporal lookup, temporal frame repair, sampling, augmentation, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate features, downloads, resource scheduling, training loops, evaluation, prediction retention, or lifecycle behavior.

## Files

- `manifest.yaml` declares trusted temporal ABI+Solar Geometry Input mode, three-frame offsets, source-balanced sampling, random mirroring, BCE-Dice training, constant LR, batch size 2, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch architecture and `build_model(input_spec, output_spec)` entry point.
- `budget_request.yaml` requests the approved late-improving budget from ABI-223 final-epoch parent evidence.
- `PROPOSAL.md` records the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.

## Expected evidence

Primary capped comparisons are ABI-223 temporal-attention connectivity, ABI-238 directional temporal attention, ABI-324 balanced five-frame temporal C4/detail consensus, and ABI-325 positive-tail recall. Useful evidence would raise recall and MIT/source-balanced Dice over ABI-223 while preserving compactness/connectivity near ABI-223 and avoiding ABI-341/344-style negative-patch clutter.
