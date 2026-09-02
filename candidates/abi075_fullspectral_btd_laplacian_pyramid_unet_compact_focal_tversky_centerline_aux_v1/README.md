# ABI-075: compact full-spectral BTD Laplacian-pyramid U-Net

ABI-075 is a repair Candidate Experiment for ABI-074, which failed smoke testing because its base-width 40 Laplacian-pyramid U-Net had 27,653,274 parameters, above the 25M-parameter ceiling. ABI-075 preserves the Laplacian-pyramid bandpass family-scout hypothesis and reduces base width to 32.

## Architecture

- Accepts only provider-approved `abi_16ch` tensors; no longitude or latitude inputs.
- Normalizes ABI channels 1-16 using dataset-profile summary statistics.
- Adds explicit thermal brightness-temperature-difference planes derived only from ABI channels.
- Adds a learned 1x1 channel mixer.
- Uses a compact GroupNorm/GELU encoder-decoder with repeated Laplacian band blocks.
- Each Laplacian band block mixes raw, narrow, middle, and broad bandpass features derived from trusted ABI feature tensors.
- Emits `mask_logits` and trusted auxiliary `centerline_logits`.

## Contract boundaries

This Candidate does not implement data loading, split logic, target derivation, custom losses, candidate-owned augmentation, metrics, thresholding, Artifact Filters, postprocessing, filesystem probes, network calls, or pretrained/runtime weight downloads.

## Training configuration

- Input mode: `abi_16ch`
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

Primary comparison target remains ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested focal-Tversky line-family candidate. ABI-066 (`run_20260827_230540_bf4ce3`) remains secondary precision/connectivity context. ABI-075 first needs to repair ABI-074's parameter-budget smoke failure before any scientific interpretation.
