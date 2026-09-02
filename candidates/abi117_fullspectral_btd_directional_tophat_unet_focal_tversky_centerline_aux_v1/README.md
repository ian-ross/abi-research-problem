# ABI-117 full-spectral BTD directional-top-hat U-Net

ABI-117 is a bounded family-development continuation for GOES ABI Contrail Segmentation. It broadens away from recent post-decoder ridge/detail gates by adding directional top-hat residual evidence at the approved-channel front end and stem of the ABI-068 frequency-gated line U-Net.

The Candidate uses only provider-approved `abi_16ch` inputs. It constructs normalized GOES ABI channel features, deterministic thermal brightness-temperature-difference planes from ABI channels 1-16, learned 1x1 spectral mixtures, and horizontal/vertical top-hat residual features derived from those approved channels. It does not use longitude, latitude, candidate-owned data loading, target derivation, losses, metrics, Artifact Filters, postprocessing, runtime downloads, or filesystem writes.

Manifest choices stay within trusted Harness/provider allowlists: `combined_source_balanced` sampling, `random_mirroring`, focal-Tversky primary loss, AdamW, constant learning rate, batch size 4, 12 epochs, and a provider-derived Centerline Target auxiliary output with trusted weighted-BCE loss weight 0.02.
