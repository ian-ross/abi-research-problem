# ABI-339 temporal-attention bottleneck line-token bridge U-Net

research-figures: []

## Scope

This note records ABI-339, Candidate `abi339_temporal_attention_bottleneck_line_token_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260918_014122_15a759`.

ABI-339 was a bounded temporal-attention mechanism scout. It used provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The intended change was a cheap `BottleneckLineTokenBridge` after the ASPP context: row and column token summaries at the 32x32 bottleneck were fused back into the temporal-attention U-Net before decoding.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a promotion comparison against ABI-202 or ABI-249.

## Execution result

ABI-339 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `exploratory`, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,347,804, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 2,856,566,784 / 3,124,756,480 bytes.
- Training wall time: 987.2 s; validation wall time: 938.5 s; total Run wall time: 1,927.5 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 8.

## Best-validation metrics

| Metric | ABI-339 bottleneck line-token bridge | ABI-333 head orientation bridge | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-324 five-frame C4/detail consensus |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 8 | 12 | 36 | 29 | 27 |
| Filtered Dice | 0.368654 | 0.389367 | 0.419776 | 0.420235 | 0.429430 |
| MIT filtered Dice | 0.354366 | 0.374039 | 0.398498 | 0.405383 | 0.408188 |
| Google filtered Dice | 0.402885 | 0.428703 | 0.476764 | 0.460838 | 0.487231 |
| Filtered precision | 0.417601 | 0.446187 | 0.483764 | 0.488730 | 0.470412 |
| Filtered recall | 0.329978 | 0.345384 | 0.370738 | 0.368578 | 0.395017 |
| Filtered connectivity | 0.290142 | 0.345629 | 0.412427 | 0.352239 | 0.397925 |
| Filtered predicted-positive pixels | 432,078 | 423,275 | 419,056 | 412,381 | 459,172 |
| Filtered positive fraction | 0.004085 | 0.004002 | 0.003962 | 0.003899 | 0.004341 |

ABI-339 did not meet its success criteria. The bottleneck-only row/column token bridge was resource-safe, but it did not improve connected-line evidence, source balance, recall, precision, or aggregate filtered Dice. It underperformed even ABI-333, the head-only orientation bridge scout, by about 0.0207 filtered Dice and 0.0555 connectivity, while also staying far below ABI-223/238 temporal-attention comparators and the stronger ABI-324 five-frame temporal C4/detail-consensus comparator.

The result is not a useful compactness/precision trade. ABI-339 predicted a similar filtered footprint to ABI-223 and ABI-333, but with lower precision and recall. At the selected checkpoint, raw Dice was 0.384913 versus filtered Dice 0.368654, raw recall was 0.356603 versus filtered recall 0.329978, and raw predicted-positive pixels were 466,378 versus 432,078 filtered. Artifact Filters reduced footprint and score; they did not create the weak result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.196780 | 0.207396 | 0.176572 | 0.174539 | 0.225518 | 0.150961 | 0.006679 |
| 2 | 0.225295 | 0.223080 | 0.229765 | 0.251057 | 0.204328 | 0.191752 | 0.004207 |
| 3 | 0.270325 | 0.267293 | 0.276494 | 0.281142 | 0.260309 | 0.171211 | 0.004786 |
| 4 | 0.212002 | 0.202824 | 0.232172 | 0.259165 | 0.179361 | 0.177149 | 0.003578 |
| 5 | 0.213820 | 0.223385 | 0.195411 | 0.142122 | 0.431512 | 0.099795 | 0.015696 |
| 6 | 0.334553 | 0.326769 | 0.353149 | 0.353707 | 0.317367 | 0.229800 | 0.004638 |
| 7 | 0.356405 | 0.340679 | 0.396689 | 0.440961 | 0.299059 | 0.284831 | 0.003506 |
| 8 | 0.368654 | 0.354366 | 0.402885 | 0.417601 | 0.329978 | 0.290142 | 0.004085 |
| 9 | 0.367717 | 0.359382 | 0.387311 | 0.349526 | 0.387907 | 0.208413 | 0.005737 |
| 10 | 0.353418 | 0.338145 | 0.390939 | 0.445104 | 0.293053 | 0.266142 | 0.003404 |
| 11 | 0.367661 | 0.348922 | 0.412686 | 0.425394 | 0.323726 | 0.238938 | 0.003934 |
| 12 | 0.343334 | 0.322455 | 0.394395 | 0.433655 | 0.284151 | 0.281494 | 0.003387 |

The trajectory was finite and non-collapsed but weak and unstable. The best checkpoint arrived at epoch 8; later epochs did not improve aggregate Dice and the final epoch fell to 0.343334. Epoch 9 briefly raised recall to 0.387907, but connectivity collapsed to 0.208413 and precision dropped to 0.349526, indicating another fragmented broad-footprint state rather than a useful connected-line improvement. This does not support a late-improving continuation.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3480, 0.4503, 0.5205, and 0.3228. These confirm finite non-collapsed predictions, but they do not override the aggregate/source weakness.

## Interpretation

Classify ABI-339 as negative capped temporal-family evidence for this exact bottleneck line-token bridge mechanism. The cheap bottleneck-only line tokens solved the ABI-329/330 timeout concern, but did not provide enough spatially precise line-continuity evidence before decoding. The likely failure mode is that 32x32 row/column summaries are too coarse: they smear long-axis context without preserving the thin, local, center-frame detail needed at threshold 0.5.

Comparator roles after ABI-339:

- ABI-324 remains the strongest local balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 remains a useful no-mirroring diagnostic control.
- ABI-223 and ABI-238 remain stronger temporal-attention comparators than ABI-339.
- ABI-333 remains a weak but still stronger head-only orientation bridge scout.
- ABI-339 is negative evidence for bottleneck-only row/column token context in the three-frame temporal-attention branch.

ABI-339 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-339 and do not submit an unchanged late36 continuation. The Run was finite and resource-safe, but it missed the intended connectivity and source-balanced Dice improvements and peaked before the exploratory budget ended. No Evaluation Request is needed from ABI-339: the negative result is already clear from aggregate/source metrics and the retained samples do not suggest a hidden favorable failure bucket.

If the temporal family is revisited, prefer a mechanism-changing direction: temporal attention with finer center-frame detail preservation, architecture-level evidence sharpening, or explicit alignment/consensus that avoids coarse bottleneck smearing. Otherwise broaden to a non-temporal C4/orientation-recall or calibrated dual-evidence family rather than another bottleneck token variant.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_014122_15a759/candidate/PROPOSAL.md`
- `run_20260918_014122_15a759/candidate/README.md`
- `run_20260918_014122_15a759/candidate/manifest.yaml`
- `run_20260918_014122_15a759/resolved_manifest.yaml`
- `run_20260918_014122_15a759/execution.json`
- `run_20260918_014122_15a759/outputs/model_summary.json`
- `run_20260918_014122_15a759/outputs/best_metrics.json`
- `run_20260918_014122_15a759/outputs/final_metrics.json`
- `run_20260918_014122_15a759/outputs/metrics.jsonl`
- `run_20260918_014122_15a759/outputs/resource_profile.json`
- `run_20260918_014122_15a759/outputs/validation_postprocessing/index.json`
- `run_20260918_014122_15a759/outputs/prediction_samples/samples.json`
- `run_20260917_142841_02a028/outputs/best_metrics.json` and `/history/research-notes/abi333-temporal-orientation-consensus-line-bridge-unet.md` for ABI-333 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
