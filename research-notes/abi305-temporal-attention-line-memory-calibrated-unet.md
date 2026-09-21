# ABI-305 temporal attention line-memory calibrated U-Net

research-figures: []

## Scope

This note records ABI-305, Candidate `abi305_temporal_attention_line_memory_calibrated_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_115424_977db1`.

ABI-305 was a bounded temporal family-development continuation after ABI-296/299 local-correlation work and ABI-304 five-frame additive recall support. It returned to the ABI-223/238 temporal-attention backbone and added an internal multi-orientation line-memory calibration head intended to raise connected recall at the fixed Harness threshold without repeating local-correlation clutter or Candidate-owned postprocessing.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and frame offsets `[-1, 0, 1]`. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Execution result

ABI-305 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 3,203,504, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,496,288,256 / 4,963,958,784 bytes.
- Training wall time: 1,273.0 s; validation wall time: 1,067.5 s; total Run wall time: 2,342.3 s, within the exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-305 line-memory calibrated attention | ABI-304 five-frame additive recall | ABI-300 evidence-sharpened attention | ABI-299 correlation line-continuity | ABI-296 local correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 10 | 9 | 9 | 36 | 29 | 32 |
| Filtered Dice | 0.386468 | 0.380635 | 0.370607 | 0.396406 | 0.395208 | 0.419776 | 0.420235 | 0.422195 |
| MIT filtered Dice | 0.366658 | 0.364758 | 0.357208 | 0.383650 | 0.379768 | 0.398498 | 0.405383 | 0.400831 |
| Google filtered Dice | 0.436547 | 0.420799 | 0.403910 | 0.428424 | 0.433397 | 0.476764 | 0.460838 | 0.477410 |
| Filtered precision | 0.432442 | 0.432089 | 0.420466 | 0.408439 | 0.389486 | 0.483764 | 0.488730 | 0.448400 |
| Filtered recall | 0.349330 | 0.340132 | 0.331319 | 0.385063 | 0.401101 | 0.370738 | 0.368578 | 0.398883 |
| Filtered connectivity | 0.226195 | 0.265446 | 0.242191 | 0.268913 | 0.331894 | 0.412427 | 0.352239 | 0.243387 |
| Filtered predicted-positive fraction | 0.004176 | 0.004069 | 0.004074 | 0.004874 | 0.005324 | 0.003962 | 0.003899 | 0.004599 |
| Filtered predicted-positive pixels | 441,719 | 430,439 | 430,877 | 515,517 | 563,119 | 419,056 | 412,381 | 486,427 |

ABI-305 is a completed mixed-to-negative temporal-attention result. It improves over the immediate ABI-300 evidence-sharpened attention head and ABI-304 five-frame additive recall support on aggregate filtered Dice, source Dice, precision, and recall. It therefore finds a better operating point than those two recent conservative/additive temporal heads.

Relative to ABI-304, ABI-305 improves filtered Dice by about +0.0058, MIT filtered Dice by +0.0019, Google filtered Dice by +0.0157, precision by +0.0004, and recall by +0.0092 at a similar filtered footprint. The cost is worse connectivity (-0.0393). Relative to ABI-300, ABI-305 improves filtered Dice by about +0.0159, MIT Dice by +0.0094, Google Dice by +0.0326, precision by +0.0120, and recall by +0.0180, but still loses some connectivity (-0.0160).

Against the stronger ABI-296/299 local-correlation branch, ABI-305 is more compact and more precise, but it gives up too much recall and connected-line evidence. It trails ABI-296 by about -0.0087 filtered Dice, -0.0518 recall, and -0.1057 connectivity, despite higher precision and slightly higher Google Dice. It trails ABI-299 by about -0.0099 filtered Dice, -0.0357 recall, and -0.0427 connectivity, with higher precision and Google Dice. The multi-orientation line-memory calibration head therefore did not organize temporal attention into a better connected-recall state than local correlation.

Relative to the temporal frontier, ABI-305 remains below ABI-223, ABI-238, and ABI-285 by about -0.0333 to -0.0357 filtered Dice. It also trails ABI-223/238 precision and connectivity by a wide margin. ABI-305 is closer to ABI-285 connectivity but still lower on filtered Dice, recall, precision, and source Dice. This is not a temporal frontier result.

At the selected checkpoint, raw Dice was 0.402748 versus filtered Dice 0.386468, raw recall was 0.376451 versus filtered recall 0.349330, and raw predicted-positive fraction was 0.004494 versus filtered predicted-positive fraction 0.004176. Artifact Filters reduce some footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.197308 | 0.196680 | 0.198624 | 0.225826 | 0.175185 | 0.168376 | 0.004010 |
| 2 | 0.238390 | 0.226879 | 0.266069 | 0.359755 | 0.178255 | 0.197601 | 0.002561 |
| 3 | 0.282229 | 0.266837 | 0.319391 | 0.377573 | 0.225330 | 0.252243 | 0.003085 |
| 4 | 0.279645 | 0.258106 | 0.332323 | 0.395565 | 0.216268 | 0.184884 | 0.002826 |
| 5 | 0.315365 | 0.295891 | 0.367164 | 0.528965 | 0.224649 | 0.355258 | 0.002195 |
| 6 | 0.327699 | 0.305662 | 0.383651 | 0.459435 | 0.254674 | 0.244717 | 0.002866 |
| 7 | 0.260255 | 0.230849 | 0.341218 | 0.613825 | 0.165135 | 0.494472 | 0.001391 |
| 8 | 0.383638 | 0.364471 | 0.435277 | 0.459873 | 0.329084 | 0.343594 | 0.003699 |
| 9 | 0.363376 | 0.350746 | 0.393011 | 0.353406 | 0.373926 | 0.197283 | 0.005470 |
| 10 | 0.351233 | 0.329489 | 0.404847 | 0.436010 | 0.294057 | 0.194148 | 0.003487 |
| 11 | 0.386468 | 0.366658 | 0.436547 | 0.432442 | 0.349330 | 0.226195 | 0.004176 |
| 12 | 0.345306 | 0.334099 | 0.371478 | 0.324151 | 0.369414 | 0.165785 | 0.005891 |

The trajectory is finite, non-collapsed, and source-informative, but it is not a clean late-improving trajectory. Epoch 8 already reaches near-best aggregate/source Dice with better connectivity than the selected checkpoint; epoch 11 selects the best aggregate balance; epoch 12 expands the footprint and recall while sharply lowering precision, source Dice, and connectivity. Earlier epochs show the same trade-off: epoch 7 has very high precision/connectivity with severe under-recall, while epoch 9 has higher recall with lower precision/connectivity.

This oscillation is consistent with the recent temporal branch pattern: the architecture can move among compact connected states and broader recall states, but it does not stabilize high recall, precision, and connectivity together. The best checkpoint at epoch 11 is near the exploratory ceiling, but the final-epoch regression weakens any case for an unchanged late-improving budget.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2074, 0.2813, 0.4004, and 0.2346. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-305 as a finite, resource-safe, scientifically useful but non-frontier temporal-attention calibration result. The internal line-memory calibration head improves over ABI-300 and ABI-304, so it is not a broken mechanism. It also keeps the footprint more compact and precise than ABI-296/299 local correlation.

The negative signal is stronger for the stated hypothesis. ABI-305 does not recover ABI-223/238 temporal-attention precision/connectivity, does not beat ABI-285 aggregate/recalI behavior, and does not improve on ABI-296/299 as a recall/connectivity compromise. The line-memory calibration head appears to slide along the familiar precision/recall/connectivity surface rather than coupling temporal recall to connected thin-line organization.

This should not eliminate temporal modeling or temporal attention broadly. ABI-223/238 remain useful comparators, ABI-285 remains the high-Dice temporal C4 result, and ABI-296/299 remain useful local-correlation mechanism evidence. But the exact ABI-305 head should not be repeated unchanged, and the result does not justify whole-validation or temporal-eligible failure-bucket diagnostics.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-305. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped Result. Do not request an unchanged late36 continuation of this exact temporal-attention line-memory calibration head; the trajectory is oscillatory and the final epoch regresses.

Record ABI-305 as bounded mixed evidence: a better temporal-attention calibration operating point than ABI-300/304, but still below ABI-296/299 and the ABI-223/238/285 temporal comparators on the intended connected-recall frontier. A future temporal follow-up should be mechanism-changing and should explicitly explain how it couples recall to connectivity rather than adding another head that trades among them.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_115424_977db1/candidate/PROPOSAL.md`
- `run_20260914_115424_977db1/candidate/README.md`
- `run_20260914_115424_977db1/candidate/manifest.yaml`
- `run_20260914_115424_977db1/resolved_manifest.yaml`
- `run_20260914_115424_977db1/execution.json`
- `run_20260914_115424_977db1/outputs/model_summary.json`
- `run_20260914_115424_977db1/outputs/best_metrics.json`
- `run_20260914_115424_977db1/outputs/final_metrics.json`
- `run_20260914_115424_977db1/outputs/metrics.jsonl`
- `run_20260914_115424_977db1/outputs/resource_profile.json`
- `run_20260914_115424_977db1/outputs/validation_postprocessing/index.json`
- `run_20260914_115424_977db1/outputs/prediction_samples/samples.json`
- `run_20260914_110002_f591b9/outputs/best_metrics.json` and `/history/research-notes/abi304-temporal-fiveframe-additive-recall-line-consensus-unet.md` for ABI-304 five-frame additive comparison context
- `run_20260914_050146_4e9b36/outputs/best_metrics.json` and `/history/research-notes/abi300-temporal-attention-evidence-sharpened-recall-unet.md` for ABI-300 evidence-sharpening comparison context
- `run_20260914_040326_98380c/outputs/best_metrics.json` and `/history/research-notes/abi299-temporal-correlation-line-continuity-decoder-unet.md` for ABI-299 temporal-correlation comparison context
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 temporal C4 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
