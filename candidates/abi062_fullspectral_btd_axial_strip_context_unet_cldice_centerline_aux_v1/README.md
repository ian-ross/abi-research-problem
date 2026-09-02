# ABI-062: full-spectral BTD axial strip-context U-Net

ABI-062 is a family-scout Candidate Experiment for GOES ABI Contrail Segmentation. It explores whether axial strip-context blocks can provide long thin-line evidence and patch-level false-positive control after the high-resolution BTD line U-Net branch produced only narrow whole-validation gains.

## Architecture

- Normalizes provider-approved ABI channels 1-16 using dataset-profile summary statistics.
- Adds explicit thermal brightness-temperature-difference planes derived only from ABI channels.
- Adds a learned 1x1 channel mixer.
- Uses an encoder-decoder with axial strip-context blocks at multiple scales.
- Each strip block combines local residual features, row-pooled context, column-pooled context, and globally pooled channel gates through learned branch weights.
- Emits `mask_logits` and trusted auxiliary `centerline_logits`.

## Contract boundaries

This Candidate does not use longitude/latitude, custom data loading, custom target derivation, custom losses, candidate-owned augmentation, metrics, thresholding, Artifact Filters, postprocessing, filesystem probes, network calls, or pretrained/runtime weight downloads.

## Training configuration

- Input mode: `abi_16ch`
- Sampling: `combined_source_balanced`
- Augmentation: `random_mirroring`
- Loss: trusted `bce_dice_cldice`
- Auxiliary target: trusted `centerline` with `weighted_bce`, weight 0.02
- Optimizer: AdamW
- Learning rate: 0.0003
- Batch size: 4
- Epochs: 12
- Scheduler: `constant_lr`

## Comparison

Primary comparison target is ABI-058 (`run_20260827_171331_c1769a`), the current whole-validation-tested local reference for the high-resolution BTD line U-Net branch. ABI-061 (`run_20260827_194725_c1d6c6`) is secondary context for precision/connectivity and source-transfer behavior under focal-Tversky.
