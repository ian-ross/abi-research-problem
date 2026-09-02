# Experiment Proposal: ABI-086 full-spectral BTD transformer-bottleneck U-Net

## Hypothesis

A compact full-spectral BTD U-Net with global self-attention only at the 1/16-resolution bottleneck can use non-local cloud-scene context to suppress isolated false-positive clutter while preserving thin-contrail recall. This is a **family scout** for a transformer-bottleneck encoder-decoder path rather than another late feature refiner on ABI-068.

## Comparison Target

Primary comparison is ABI-068 (`run_20260828_010836_4ccc77`), the current strongest capped frequency-gated focal-Tversky reference by `val/filtered_dice` (0.3964) with MIT/Google filtered Dice 0.3886/0.4161. Secondary context includes ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward reference and ABI-085 (`run_20260829_181201_01c5e7`) as evidence that lowering the learning rate alone did not improve ABI-068.

## Expected Effect

The transformer bottleneck should expose each coarse spatial token to the whole ABI Patch before decoding, helping the model distinguish coherent contrail-like structure from local cloud edges or small high-frequency artifacts. Success would be visible as competitive aggregate filtered Dice with less precision/connectivity loss than recent recall-forward variants, non-catastrophic MIT and Google source metrics, and a non-degenerate predicted-positive fraction. As a first scout, a low score alone is not elimination evidence if the Run is finite, source-balanced, and shows an improving trajectory.

## Implementation Sketch

The Candidate uses provider-approved `abi_16ch` input only. The front end normalizes ABI channels 1-16, derives explicit thermal BTD planes from ABI-channel pairs, and learns a 1x1 channel mixer. A compact residual U-Net downsamples to 1/16 resolution, applies two global multi-head self-attention blocks plus dilated convolution context at the bottleneck, then decodes with skip fusion to full resolution. A small detail-aware head emits `mask_logits` and the trusted provider-derived `centerline_logits` auxiliary output. The code defines architecture only and does not implement data loading, losses, targets, metrics, thresholding, postprocessing, Artifact Filters, sampling, augmentation, resource placement, network access, or pretrained weights.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch` (GOES ABI channels 1-16 only; no longitude or latitude)
- Output form: `mask_logits`
- Auxiliary target: provider-derived `centerline` via `centerline_logits`, trusted `weighted_bce`, weight 0.02
- Sampling policy: provider-owned `combined_source_balanced`
- Augmentation policy: trusted `random_mirroring`
- Loss: trusted `focal_tversky`
- Optimizer: `adamw`
- Scheduler: `constant_lr`

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source/split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, one sequential Run under the configured 3,600-second Docker training timeout and 25M-parameter smoke ceiling.

## Success Criteria

For this family scout, the Run should complete finite and non-degenerate, stay below the 25M-parameter smoke ceiling, avoid all-negative/all-positive predictions, and keep both MIT and Google filtered Dice approximately above 0.33. Strong positive evidence would be aggregate `val/filtered_dice` within about 0.02 of ABI-068 while improving either filtered precision, filtered connectivity, or predicted-positive burden versus ABI-068. A clear win would tie or exceed ABI-068's aggregate filtered Dice without worsening both Dataset Sources.

## Fallback/Next Decision

If the Candidate fails static validation or smoke testing because of a candidate bug, prepare a repair preserving the transformer-bottleneck scout hypothesis. If it completes but collapses, diverges, exceeds resource ceilings, or shows a clearly non-improving trajectory with source-specific failure, do not repeat this exact branch. If it completes finite with competitive or diagnostically distinct behavior, write a Research Note comparing it with ABI-068/066/085 and decide whether a bounded whole-validation failure-bucket Evaluation Request or one transformer-family continuation is justified.
