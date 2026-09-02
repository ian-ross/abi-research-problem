# ABI-084 full-spectral BTD multi-resolution line-HRNet scout

ABI-084 is a family-scout Candidate Experiment for GOES ABI Contrail Segmentation. It uses provider-approved `abi_16ch` tensors only, derives explicit thermal brightness-temperature-difference planes from ABI channels 1-16 inside the model, and keeps a high-resolution branch active while repeatedly fusing medium/low-resolution context.

## Contract boundary

Candidate code defines only the PyTorch model architecture and allowed manifest choices. It does not own data loading, split logic, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights. Longitude and latitude source channels are not requested or reconstructed.

## Manifest choices

- Input mode: `abi_16ch`
- Output form: `mask_logits`
- Primary loss: trusted `focal_tversky`
- Auxiliary target: trusted provider-derived `centerline` with `centerline_logits`, `weighted_bce`, weight 0.02
- Sampling: trusted `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Optimizer/scheduler: AdamW, constant learning rate 0.0003
- Budget: batch size 4, 12 epochs under active Harness ceilings

## Research intent

The comparison target is the frequency-gated line U-Net branch, especially ABI-068 for aggregate Dice and ABI-066 for precision/connectivity. ABI-084 tests whether a parallel multi-resolution architecture can preserve thin high-resolution line evidence while using coarser branches to suppress cloud/background clutter before prediction.
