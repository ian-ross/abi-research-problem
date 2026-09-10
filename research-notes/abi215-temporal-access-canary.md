# ABI-215 temporal access canary

research-figures: []

## Scope

This note records the bounded diagnostic Result for ABI-215, Candidate `abi215_temporal_access_canary_v1`, Run `run_20260908_111425_74e4ec`.

ABI-215 was not intended as a segmentation-quality contender. Its purpose was to verify that the trusted Candidate Execution path can provision provider-owned temporal ABI inputs: `abi_16ch_plus_sza_temporal` with frame offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, and no candidate-owned temporal lookup, cache access, padding, data loading, target derivation, loss, metric, Artifact Filter, augmentation, training loop, persistence, runtime download, coordinate feature, or resource scheduling behavior.

The Candidate used a tiny fully convolutional architecture that reshapes the 51-channel provider tensor into three ordered ABI+SZA frames, normalizes/combines them with temporal means and finite differences, and emits only `mask_logits`. The Run used trusted BCE-Dice loss, sequential traversal, no augmentation, AdamW learning rate 0.001, batch size 2, one epoch, constant learning rate, disabled early stopping, and the exploratory resource envelope.

## Temporal provisioning result

ABI-215 completed successfully. This is positive lifecycle evidence for the temporal input path.

Key contract observations from the Run artifacts:

- Status: completed.
- Model summary input mode: `abi_16ch_plus_sza_temporal`.
- Synthetic input shape: `[2, 51, 256, 256]`; per-sample input spec shape: `[51, 256, 256]`.
- Temporal frame offsets: `[-1, 0, 1]` with target frame offset `0` at target frame index `1`.
- Frame layout: channel-stacked temporal frames, 17 channels per frame.
- Candidate-visible per-frame channels: ABI channels 1-16 plus per-frame Solar Geometry Input.
- Forbidden longitude/latitude source channels are explicitly excluded (`16`, `17`).
- Effective frame-selection policy: `temporal_eligible_center`.
- Temporal-eligible counts were recorded for both Dataset Sources before the per-source/split cap was applied: MIT train/validation 3912/915 and Google train/validation 11059/699.
- Provider-owned bounded record selection then selected 8 records per Dataset Source and Leakage-Safe Split, yielding 16 train and 16 validation samples for the canary.

The successful smoke test and one-epoch completion show that the trusted temporal cache and materialized neighbor patch provisioning were available for this bounded run and that candidate code received the expected tensor without needing to discover or repair temporal neighbors.

## Canary metrics

The segmentation metrics are intentionally not architecture-ranking evidence because ABI-215 trained for one epoch on only 16 train samples with an 18,321-parameter canary model.

| Metric | ABI-215 best/final epoch 1 |
| --- | ---: |
| Filtered Dice | 0.001823 |
| Raw Dice | 0.001760 |
| Filtered precision | 0.000917 |
| Filtered recall | 0.159336 |
| Filtered contrail connectivity | 0.001887 |
| Filtered predicted-positive fraction | 0.369290 |
| Raw predicted-positive fraction | 0.482415 |
| MIT filtered Dice | 0.003106 |
| Google filtered Dice | 0.0000247 |
| MIT filtered recall | 0.359105 |
| Google filtered recall | 0.001606 |
| Train loss | 1.725875 |
| Validation loss | 1.670900 |

The output was finite and non-all-negative, but it massively overpredicted positive area with near-zero precision. Source behavior was also not scientifically meaningful: the tiny canary had much higher MIT recall than Google recall. These observations should not be used to reject temporal modeling; they only confirm that the diagnostic model was not a useful segmenter.

## Resource observations

ABI-215 was resource-light:

- Parameter count: 18,321, far below the 25,000,000-parameter ceiling.
- Effective batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 208,446,464 / 270,532,608 bytes.
- Run wall time: 5.60 seconds.
- Training/validation samples processed: 16 / 16.

This profiles the minimal temporal data path as safe. It does not profile a real temporal architecture with multi-frame encoders, temporal attention, recurrent blocks, or larger feature maps; those should still run sequentially until separately measured.

## Interpretation

Classify ABI-215 as a successful temporal-access canary and not as a scientific segmentation result. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, or bad-research-result blocker. The important Result is that provider-owned temporal eligibility filtering, temporal cache access, non-zero neighbor patch provisioning, channel-stacked ABI+SZA tensor construction, coordinate exclusion, smoke testing, training, validation metrics, Artifact Filtering, and prediction-sample retention all executed end-to-end inside the trusted lifecycle.

This removes the immediate temporal-provisioning uncertainty that motivated the canary. It supports broadening to a real sequential temporal scout under the active contract, while keeping candidate code strictly architecture-only.

## Decision

Do not promote ABI-215, do not request whole-validation diagnostics for ABI-215, and do not request a late-improving budget for this exact canary.

Use ABI-215 as positive infrastructure evidence for the next temporal Candidate Experiment. A reasonable next in-contract hypothesis is a compact temporal/change architecture over `abi_16ch_plus_sza_temporal`, such as a Siamese or shared-weight per-frame encoder with center-minus-neighbor residual streams and a lightweight temporal fusion block. The next temporal scout should keep `frame_selection_policy: temporal_eligible_center`, request an allowlisted offset window, remain sequential because true temporal architectures are not yet profiled, and continue to avoid candidate-owned temporal lookup, data loading, coordinates, losses, metrics, Artifact Filters, thresholding, sampling, augmentation, training loops, downloads, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260908_111425_74e4ec/candidate/PROPOSAL.md`
- `run_20260908_111425_74e4ec/candidate/README.md`
- `run_20260908_111425_74e4ec/resolved_manifest.yaml`
- `run_20260908_111425_74e4ec/outputs/model_summary.json`
- `run_20260908_111425_74e4ec/outputs/best_metrics.json`
- `run_20260908_111425_74e4ec/outputs/final_metrics.json`
- `run_20260908_111425_74e4ec/outputs/metrics.jsonl`
- `run_20260908_111425_74e4ec/outputs/resource_profile.json`
- `run_20260908_111425_74e4ec/outputs/validation_postprocessing/index.json`
- `run_20260908_111425_74e4ec/outputs/prediction_samples/samples.json`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
