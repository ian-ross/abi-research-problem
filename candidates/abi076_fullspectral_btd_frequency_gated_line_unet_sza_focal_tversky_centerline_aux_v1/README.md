# ABI-076: full-spectral BTD+SZA frequency-gated line U-Net

ABI-076 is a family-development continuation from ABI-068. It keeps the ABI-068 frequency-gated line U-Net backbone, trusted focal-Tversky primary loss, and trusted centerline auxiliary target, but switches the provider-approved input mode from `abi_16ch` to `abi_16ch_plus_sza`.

## Architecture

- Accepts only provider-approved `abi_16ch_plus_sza` tensors: GOES ABI channels 1-16 plus Solar Geometry Input.
- Does not receive longitude, latitude, or reconstructed coordinate inputs.
- Normalizes ABI channels 1-16 using dataset-profile summary statistics.
- Adds explicit thermal BTD planes derived only from the approved ABI channels.
- Adds normalized solar-zenith and cosine solar-zenith planes, plus a learned 1x1 mixture over normalized ABI+SZA features.
- Uses the ABI-068 high/low spatial-frequency split stem, gated skip fusion, dilated bottleneck context, frequency-pyramid fusion, and oriented high-frequency line refiner.
- Emits primary `mask_logits` and trusted auxiliary `centerline_logits`.

## Contract boundaries

This Candidate does not implement data loading, split logic, target derivation, custom losses, candidate-owned augmentation, metrics, thresholding, Artifact Filters, postprocessing, filesystem probes, network calls, pretrained weights, runtime weight downloads, or a training loop.

## Training configuration

- Input mode: `abi_16ch_plus_sza`
- Sampling: trusted `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Loss: trusted `focal_tversky`
- Auxiliary target: trusted `centerline` with `weighted_bce`, weight 0.02
- Optimizer: AdamW
- Learning rate: 0.0003
- Batch size: 4
- Epochs: 12
- Scheduler: `constant_lr`

## Comparison

Primary comparison target is ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested frequency-gated focal-Tversky Candidate. ABI-066 (`run_20260827_230540_bf4ce3`) remains secondary precision/connectivity context. ABI-074/075 provide recent evidence that a heavier Laplacian-pyramid branch is not the next safe direction under the current parameter and wall-clock ceilings.
