# ABI-345 temporal-attention center-detail evidence sharpening late36

research-figures: []

## Scope

This note records ABI-345, Candidate `abi345_temporal_attention_center_detail_evidence_sharpening_late36_bce_dice_line_centerline_aux_v1`, and Run `run_20260918_133432_9e7947`.

ABI-345 was a mechanism-changing continuation of the three-frame temporal-attention family. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was a center-detail evidence-sharpening head intended to lift uncertain fixed-threshold true contrail logits only when high-resolution center/detail and temporal-stem evidence agreed with the anchor.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-345 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-223 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,139,950, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 3,141,328,384 / 3,506,438,144 bytes.
- Training wall time: 2,956.7 s; validation wall time: 2,993.0 s; total Run wall time: 5,951.7 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 29.

## Best-validation metrics

| Metric | ABI-345 center-detail sharpening | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-324 five-frame balanced C4 | ABI-344 recall sidecar |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 29 | 36 | 29 | 27 | 29 |
| Filtered Dice | 0.411455 | 0.419776 | 0.420235 | 0.429430 | 0.426448 |
| MIT filtered Dice | 0.391239 | 0.398498 | 0.405383 | 0.408188 | 0.412208 |
| Google filtered Dice | 0.464271 | 0.476764 | 0.460838 | 0.487231 | 0.462585 |
| Filtered precision | 0.425462 | 0.483764 | 0.488730 | 0.470412 | 0.426700 |
| Filtered recall | 0.398342 | 0.370738 | 0.368578 | 0.395017 | 0.426196 |
| Filtered connectivity | 0.286565 | 0.412427 | 0.352239 | 0.397925 | 0.315733 |
| Filtered predicted-positive pixels | 511,957 | 419,056 | 412,381 | 459,172 | 546,166 |

ABI-345 achieved the narrow recall objective relative to the three-frame temporal-attention comparators: filtered recall improved by about +0.0276 over ABI-223 and +0.0298 over ABI-238. However, this was not a compact evidence lift. Relative to ABI-223, ABI-345 lost -0.0083 filtered Dice, -0.0073 MIT Dice, -0.0125 Google Dice, -0.0583 precision, and -0.1259 connectivity while adding 92,901 filtered predicted-positive pixels. Relative to ABI-238, it lost -0.0088 filtered Dice, -0.0141 MIT Dice, -0.0633 precision, and -0.0657 connectivity while adding 99,576 filtered predicted-positive pixels.

The comparison to recent five-frame temporal C4 recalls is also unfavorable. ABI-345 has a smaller footprint than ABI-344 and better precision than ABI-341/344, but its aggregate Dice, MIT Dice, recall, and connectivity are lower than ABI-344, and it is far below ABI-324 on aggregate/source Dice and connectivity. The center-detail sharpening head therefore did not recover the compact connected-line behavior that made ABI-223 useful.

At the selected checkpoint, raw Dice was 0.428236 versus filtered Dice 0.411455, raw recall was 0.430493 versus filtered recall 0.398342, and raw predicted-positive pixels were 552,576 versus 511,957 filtered. Artifact Filters removed 40,619 predicted-positive pixels and lowered the score; they did not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.207073 | 0.208196 | 0.204585 | 0.247625 | 0.177933 | 0.175375 | 0.003715 |
| 5 | 0.306963 | 0.285648 | 0.361619 | 0.489010 | 0.223689 | 0.386761 | 0.002365 |
| 10 | 0.370658 | 0.354432 | 0.410869 | 0.437275 | 0.321655 | 0.227868 | 0.003803 |
| 15 | 0.365261 | 0.354123 | 0.392189 | 0.387690 | 0.345285 | 0.190959 | 0.004604 |
| 20 | 0.385723 | 0.360494 | 0.455003 | 0.519119 | 0.306868 | 0.341617 | 0.003056 |
| 25 | 0.378057 | 0.356428 | 0.433223 | 0.488821 | 0.308217 | 0.252700 | 0.003260 |
| 29 | 0.411455 | 0.391239 | 0.464271 | 0.425462 | 0.398342 | 0.286565 | 0.004840 |
| 30 | 0.375257 | 0.352962 | 0.430080 | 0.427773 | 0.334226 | 0.241403 | 0.004039 |
| 32 | 0.396220 | 0.372121 | 0.459758 | 0.466639 | 0.344268 | 0.268068 | 0.003814 |
| 34 | 0.374038 | 0.350591 | 0.435266 | 0.437741 | 0.326520 | 0.204752 | 0.003856 |
| 36 | 0.402763 | 0.378707 | 0.464732 | 0.451519 | 0.363511 | 0.251292 | 0.004162 |

The trajectory was finite, non-collapsed, and source-informative, but the selected checkpoint is an isolated recall-heavy state rather than a stable late improvement. Epoch 20 reached higher precision and connectivity with lower recall; epoch 29 became the best aggregate by broadening the footprint; later epochs did not recover ABI-223/238-level compactness. The final epoch was below the selected checkpoint on filtered Dice, MIT Dice, recall, connectivity, and predicted-positive footprint stability.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3611, 0.3820, 0.5595, and 0.3651. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-345 as finite but negative temporal-attention family-development evidence for this exact center-detail evidence-sharpening head. The head raised fixed-threshold recall over ABI-223/238, but it did so by sacrificing too much precision and connected-line continuity. It did not produce the preregistered pattern of improved recall while preserving compact connectivity, and it does not replace ABI-223 or ABI-238 as a temporal-attention comparator.

Comparator roles after ABI-345:

- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-238 remains the stronger capped three-frame directional temporal-attention comparator by filtered Dice and precision.
- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-344 remains the broad recall-sidecar diagnostic, not a new comparator.
- ABI-345 is evidence that center/detail sharpening can raise recall, but not with adequate compactness or continuity in this implementation.

ABI-345 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-345 and do not request a temporal-eligible failure-bucket diagnostic in this Autonomy Step. The capped result is not an ambiguous near-frontier case: it is below ABI-223/238 on filtered Dice, source balance, precision, and connectivity, and it misses the stated compact-connectivity guard despite the recall lift. Do not submit an unchanged late36 continuation of this exact center-detail evidence-sharpening head.

The next useful temporal-attention work should be mechanism-changing: preserve an ABI-223/238-style compact connected anchor before adding recall, or move to a materially different temporal alignment/evidence mechanism. A simple residual-gain change or another broad uncertainty-band recall residual is not justified by this result.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_133432_9e7947/candidate/PROPOSAL.md`
- `run_20260918_133432_9e7947/candidate/README.md`
- `run_20260918_133432_9e7947/candidate/manifest.yaml`
- `run_20260918_133432_9e7947/candidate/budget_request.yaml`
- `run_20260918_133432_9e7947/resolved_manifest.yaml`
- `run_20260918_133432_9e7947/execution.json`
- `run_20260918_133432_9e7947/run_metadata.json`
- `run_20260918_133432_9e7947/outputs/model_summary.json`
- `run_20260918_133432_9e7947/outputs/best_metrics.json`
- `run_20260918_133432_9e7947/outputs/final_metrics.json`
- `run_20260918_133432_9e7947/outputs/metrics.jsonl`
- `run_20260918_133432_9e7947/outputs/resource_profile.json`
- `run_20260918_133432_9e7947/outputs/validation_postprocessing/index.json`
- `run_20260918_133432_9e7947/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparison context
- `run_20260918_105020_e806bb/outputs/best_metrics.json` and `/history/research-notes/abi344-temporal-fiveframe-connectivity-anchor-recall-sidecar-late36.md` for ABI-344 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
