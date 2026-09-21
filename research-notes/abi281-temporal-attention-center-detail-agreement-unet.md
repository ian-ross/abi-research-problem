# ABI-281 temporal-attention center-detail agreement U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-281, Candidate `abi281_temporal_attention_center_detail_agreement_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_050456_f4352b`.

ABI-281 was a mechanism-changing temporal-family continuation after ABI-223, ABI-274, and ABI-278. It returned to the compact ABI-223-style temporal-attention U-Net pattern and added a center-frame detail agreement head before logits. The hypothesis was that comparing high-resolution temporal decoder features with provider-visible center-frame ABI/Solar Geometry Input/BTD detail could raise true thin-line evidence at the trusted 0.5 threshold without repeating ABI-278's final oriented line-logit bridge or ABI-274's early line-state injector.

The Candidate used provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` frame selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. It remained architecture/manifest-only and did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Execution result

ABI-281 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,131,478, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.12 / 3.40 GiB.
- Training wall time: 1,009.0 s; validation wall time: 983.6 s; total Run wall time: 1,994.4 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-281 best epoch 11 | ABI-278 line-logit bridge | ABI-277 bidirectional scout | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.375376 | 0.353766 | 0.384239 | 0.419364 | 0.419776 |
| Raw Dice | 0.392039 | 0.370630 | 0.401624 | 0.436760 | 0.438487 |
| Filtered precision | 0.418431 | 0.433119 | 0.457624 | 0.454127 | 0.483764 |
| Filtered recall | 0.340355 | 0.298988 | 0.331138 | 0.389545 | 0.370738 |
| Filtered connectivity | 0.251147 | 0.199816 | 0.263442 | 0.282911 | 0.412427 |
| MIT filtered Dice | 0.365315 | 0.334650 | 0.364664 | 0.399386 | 0.398498 |
| Google filtered Dice | 0.400773 | 0.401941 | 0.436066 | 0.472606 | 0.476764 |
| Filtered predicted-positive fraction | 0.004205 | 0.003569 | 0.003741 | 0.004434 | 0.003962 |
| Filtered predicted-positive pixels | 444,781 | 377,471 | — | 469,049 | 419,056 |

Relative to ABI-278, ABI-281 is a partial improvement: filtered Dice is higher by about +0.0216, MIT Dice by +0.0307, recall by +0.0414, and connectivity by +0.0513. However, precision is lower by about -0.0147, the filtered footprint is broader by 67,310 pixels, and Google Dice is essentially unchanged/slightly lower. The center-detail agreement location is therefore better than ABI-278's final line-logit bridge, but it does not reach the stronger temporal comparator band.

Relative to ABI-277, ABI-281 is lower by about -0.0089 filtered Dice, -0.0392 precision, -0.0123 connectivity, and -0.0353 Google Dice, while recall is slightly higher (+0.0092) and MIT Dice is essentially tied. Relative to ABI-223 and ABI-274, ABI-281 remains far behind on aggregate filtered Dice (-0.0444 versus ABI-223; -0.0440 versus ABI-274), and it does not achieve either ABI-223's connected-line behavior or ABI-274's recall/source lift.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.210581 | 0.213610 | 0.203985 | 0.231578 | 0.193075 | 0.154811 | 0.004310 |
| 2 | 0.201718 | 0.190377 | 0.229628 | 0.337831 | 0.143786 | 0.169634 | 0.002200 |
| 3 | 0.278516 | 0.262040 | 0.319948 | 0.434066 | 0.205039 | 0.367165 | 0.002442 |
| 4 | 0.269278 | 0.252384 | 0.310134 | 0.367188 | 0.212590 | 0.147053 | 0.002993 |
| 5 | 0.334873 | 0.326093 | 0.355786 | 0.362126 | 0.311434 | 0.186306 | 0.004446 |
| 6 | 0.345439 | 0.341203 | 0.356262 | 0.370561 | 0.323506 | 0.184427 | 0.004513 |
| 7 | 0.346325 | 0.329372 | 0.391936 | 0.521526 | 0.259237 | 0.359433 | 0.002570 |
| 8 | 0.338594 | 0.322680 | 0.376372 | 0.352055 | 0.326125 | 0.199490 | 0.004789 |
| 9 | 0.375213 | 0.366271 | 0.397093 | 0.356340 | 0.396196 | 0.252343 | 0.005748 |
| 10 | 0.375274 | 0.358124 | 0.419803 | 0.437575 | 0.328502 | 0.319036 | 0.003881 |
| 11 | 0.375376 | 0.365315 | 0.400773 | 0.418431 | 0.340355 | 0.251147 | 0.004205 |
| 12 | 0.332082 | 0.336354 | 0.323210 | 0.270190 | 0.430753 | 0.153040 | 0.008242 |

The trajectory is finite and non-collapsed, but the late behavior is unstable. Epochs 9 through 11 form a narrow best-Dice plateau with different operating points: epoch 9 is recall-heavy and broad, epoch 10 is higher-precision and higher-connectivity, and epoch 11 is the selected intermediate. The final epoch then shifts sharply into a very broad low-precision state: filtered recall rises to 0.4308, but filtered precision falls to 0.2702, connectivity to 0.1530, Google Dice to 0.3232, and filtered positive pixels almost double to 871,760.

This instability is important for budget interpretation. Although the selected checkpoint is near the exploratory ceiling, the final epoch does not show a clean late-improving trajectory. Instead, the head oscillates between compact under-coverage and broad cluttered recall. That does not justify an unchanged late36 continuation of this exact center-detail agreement branch.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2175, 0.1913, 0.4924, and 0.2341. This is consistent with finite non-collapsed predictions and substantial per-sample variability, but it does not establish promotion evidence.

At the selected checkpoint, Artifact Filters removed 34,259 predicted-positive pixels (`479,040` raw predicted-positive pixels versus `444,781` filtered). Raw Dice was 0.3920 versus filtered Dice 0.3754, so filtering lowers rather than creates the Result. At the final epoch the model broadened to `939,055` raw and `871,760` filtered predicted-positive pixels, confirming that the degradation is an operating-point shift rather than an Artifact Filter artifact.

## Interpretation

Classify ABI-281 as a finite but negative mechanism test with one useful local lesson. The center-frame detail agreement head is more effective than ABI-278's final oriented line-logit bridge at raising recall and connectivity from the weak ABI-278 baseline, especially on MIT. However, it still fails the primary temporal-family objective: it does not approach ABI-223/274 filtered Dice, does not recover ABI-223 connectivity, and does not preserve ABI-274 recall/source strength with acceptable precision.

The mechanism appears to expose more center-frame detail, but without enough temporal/line organization to decide which detail should survive at threshold 0.5. When the branch broadens, precision and connectivity degrade; when it compacts, recall is still below the comparator band. This is not persistent collapse, so it does not eliminate temporal attention or center-frame detail preservation as broad families. It does narrow the exact integration: a post-decoder center-detail agreement residual by itself is insufficient.

ABI-223 remains the temporal-attention connectivity comparator, ABI-274 remains the temporal recall/source-balance comparator, ABI-255 remains the compact recurrent temporal comparator, ABI-249 remains the high-precision C4 whole-validation comparator, and ABI-202 remains the aggregate whole-validation reference.

## Decision

Do not promote ABI-281, do not request temporal-eligible failure-bucket diagnostics for this Result, and do not request a late-improving budget for this exact center-detail agreement branch. The selected checkpoint is too far below ABI-223/274, the final epoch deteriorates into broad low-precision predictions, and the mechanism does not deliver the intended recall/connectivity tradeoff.

Do not repeat ABI-281 unchanged. Future temporal work should be mechanism-changing: integrate center-frame detail earlier with stronger cross-scale or orientation consensus, or broaden to a different architecture-level calibration/continuity mechanism that raises true contrail logits without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_050456_f4352b/candidate/PROPOSAL.md`
- `run_20260913_050456_f4352b/candidate/README.md`
- `run_20260913_050456_f4352b/candidate/manifest.yaml`
- `run_20260913_050456_f4352b/resolved_manifest.yaml`
- `run_20260913_050456_f4352b/outputs/model_summary.json`
- `run_20260913_050456_f4352b/outputs/best_metrics.json`
- `run_20260913_050456_f4352b/outputs/final_metrics.json`
- `run_20260913_050456_f4352b/outputs/metrics.jsonl`
- `run_20260913_050456_f4352b/outputs/resource_profile.json`
- `run_20260913_050456_f4352b/outputs/validation_postprocessing/index.json`
- `run_20260913_050456_f4352b/outputs/prediction_samples/samples.json`
- `run_20260912_232028_0c31f7/outputs/best_metrics.json` for ABI-278 line-logit bridge comparison context
- `run_20260912_222529_d1a74a/outputs/best_metrics.json` for ABI-277 bidirectional-consistency comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `/history/research-notes/abi278-temporal-attention-line-logit-bridge-unet.md`
- `/history/research-notes/abi274-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
