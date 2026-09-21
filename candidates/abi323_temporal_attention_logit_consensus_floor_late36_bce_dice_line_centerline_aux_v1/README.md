# ABI-323 temporal-attention logit-consensus floor late36

ABI-323 is a late-improving, close temporal-attention family continuation for GOES ABI Contrail Segmentation. It keeps the ABI-223-style compact three-frame temporal-attention stem, U-Net/ASPP decoder, provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection, and offsets `[-1, 0, 1]`.

The mechanism change is a bounded logit-consensus floor at the output head. The base region logit preserves the compact temporal-attention operating point, while a small non-negative residual is added only when learned line, centerline, high-resolution detail, and decoder-context evidence agree. A learned conflict gate attenuates the lift when detail and region context disagree. This is differentiable model architecture logic only; it is not thresholding, morphology, connected-component logic, postprocessing, an Artifact Filter, custom calibration, a custom loss, a metric, temporal lookup, sample selection, coordinates, Dataset Source identity, or resource scheduling.

## Files

- `manifest.yaml` declares trusted temporal ABI+SZA input, source-balanced sampling, random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW, constant LR, and batch size 2.
- `model.py` defines the PyTorch model and `build_model` entry point.
- `budget_request.yaml` requests the approved `late_improving` budget with ABI-223/ABI-321 parent evidence and exploratory fallback.
- `PROPOSAL.md` records the hypothesis, comparison targets, budget, success criteria, and fallback decision.

## Expected evidence

This is capped temporal-eligible feasibility evidence only. Primary comparisons are ABI-223 (temporal-attention comparator), ABI-321 (lightweight attention/detail sharpening scout), and recent temporal C4 comparators ABI-306/309/311. Continue the branch only if the consensus floor improves threshold-0.5 recall/source balance or connected-line behavior without ABI-321-style instability or excessive footprint broadening.
