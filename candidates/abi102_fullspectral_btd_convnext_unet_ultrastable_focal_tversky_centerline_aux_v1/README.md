# ABI-102 full-spectral BTD ConvNeXt U-Net ultra-stable repair

ABI-102 repairs ABI-101 after Run `run_20260830_065055_ef616d` failed with Harness-recorded `candidate_bug` non-finite gradients in `front_end.learned_mixer.0.weight`.

The candidate preserves the ConvNeXt-style depthwise large-kernel U-Net scout hypothesis while removing the specific learned front-end instability point. It uses provider-approved `abi_16ch` inputs, deterministic bounded normalized ABI channels, deterministic thermal BTD planes derived only from ABI channels 1-16, bounded internal ConvNeXt residual activations, trusted `focal_tversky` loss, trusted `random_mirroring`, provider-owned `combined_source_balanced` sampling, AdamW at learning rate `0.00005`, batch size 4, 12 epochs, constant LR, and a provider-derived `centerline_logits` auxiliary output with trusted `weighted_bce` weight 0.02.

Candidate code owns only model architecture and allowed manifest choices. It does not implement data loading, split logic, sampling implementation, augmentation transforms, target derivation, loss definitions, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network calls, pretrained weights, or longitude/latitude inputs.
