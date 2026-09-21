# ABI-350 temporal-attention pre-decoder line-support late36

research-figures: []

## Scope

This note records ABI-350, Candidate `abi350_temporal_attention_predecoder_line_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_013306_9ca44e`, and Harness-owned Post-Run Evaluation `eval_evalreq_abi350_temporal_eligible_failure_buckets_v1`.

ABI-350 was the approved late-improving continuation of ABI-349. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architecture preserved ABI-349's pre-decoder line-support gates injected into encoder skip features before decoder fusion.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-350 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested `late_improving` budget was approved from ABI-349 parent evidence.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,132,228, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,244,163,584 / 4,766,826,496 bytes.
- Training wall time: 4,026.0 s; validation wall time: 3,150.0 s; total Run wall time: 7,178.3 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 33.

## Temporal-eligible aggregate metrics

| Metric | ABI-350 line support late36 | ABI-349 exploratory parent | ABI-324 balanced five-frame C4 | ABI-337 no-mirroring five-frame C4 | ABI-348 compact five-frame C4 | ABI-223 temporal attention | ABI-238 directional temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 33 | 12 | 27 | 27 | 36 | 36 | 29 |
| Filtered Dice | 0.431103 | 0.389171 | 0.429430 | 0.428894 | 0.427829 | 0.419776 | 0.420235 |
| MIT filtered Dice | 0.409536 | 0.369849 | 0.408188 | 0.411838 | 0.410244 | 0.398498 | 0.405383 |
| Google filtered Dice | 0.490518 | 0.440561 | 0.487231 | 0.476340 | 0.478363 | 0.476764 | 0.460838 |
| Filtered precision | 0.494306 | 0.478850 | 0.470412 | 0.466489 | 0.477546 | 0.483764 | 0.488730 |
| Filtered recall | 0.382230 | 0.327784 | 0.395017 | 0.396906 | 0.387488 | 0.370738 | 0.368578 |
| Filtered connectivity | 0.358283 | 0.337620 | 0.397925 | 0.365326 | 0.300904 | 0.412427 | 0.352239 |
| Filtered predicted-positive pixels | 422,831 | 374,305 | 459,172 | 465,248 | 443,691 | 419,056 | 412,381 |

ABI-350 is a strong late-budget improvement over ABI-349: +0.0419 filtered Dice, +0.0397 MIT Dice, +0.0500 Google Dice, +0.0544 recall, and +0.0207 connectivity, while remaining compact. The late budget answered the ABI-349 trajectory question positively: pre-decoder line support was not merely an exploratory fluke.

ABI-350 is also the best capped temporal-eligible aggregate filtered-Dice Result in this comparison set. It edges ABI-324 by +0.0017 aggregate Dice, ABI-337 by +0.0022, ABI-348 by +0.0033, and ABI-223 by +0.0113. The gain comes from a high-precision, compact, Google-strong checkpoint rather than from broad recall. Compared with ABI-324, ABI-350 is more precise (+0.0239) and smaller (-36,341 filtered predicted-positive pixels), with slightly higher aggregate and Google Dice, but it gives back recall (-0.0128) and connected-line continuity (-0.0396). Compared with ABI-223, it has much higher Dice and modestly higher recall, but still lower connectivity (-0.0541).

At the selected checkpoint, raw Dice was 0.450110 versus filtered Dice 0.431103, raw recall was 0.413544 versus filtered recall 0.382230, and raw predicted-positive pixels were 457,970 versus 422,831 filtered. Artifact Filters removed 35,139 predicted-positive pixels and lowered the score; they did not create the Result.

## Failure-bucket observations

The completed temporal-eligible diagnostic shows a useful but incomplete positive-tail improvement. ABI-350 recovers some complete misses and low-recall positives relative to compact/high-precision comparators, but it does not become a balanced connected-line solution.

| Bucket metric | ABI-350 | ABI-348 | ABI-324 | ABI-337 | ABI-346 | ABI-223 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Positive samples | 719 | 719 | 719 | 719 | 719 | 719 |
| Complete positive misses | 64 | 73 | 72 | 79 | 56 | 77 |
| Positive recall < 0.20 | 149 | 157 | 165 | 162 | 133 | 167 |
| Positive recall < 0.50 | 450 | 452 | 430 | 428 | 397 | 433 |
| Positive median recall | 0.4239 | 0.4082 | 0.4231 | 0.4379 | 0.4564 | 0.4227 |
| Positive median Dice | 0.4365 | 0.4286 | 0.4265 | 0.4308 | 0.4425 | 0.4357 |
| Positive median connectivity | 0.4330 | 0.4230 | 0.4099 | 0.4229 | 0.4197 | 0.4226 |
| Positive connectivity < 0.20 | 139 | 143 | 162 | 148 | 134 | 154 |
| Negative samples with any prediction | 611 | 700 | 533 | 591 | 700 | 515 |
| Negative samples >50 predicted pixels | 275 | 258 | 244 | 298 | 330 | 332 |
| Negative samples >200 predicted pixels | 29 | 28 | 44 | 51 | 64 | 53 |
| Total negative-patch predicted pixels | 41,315 | 39,663 | 40,097 | 49,852 | 56,477 | 51,290 |

The positive-tail signal is mixed-positive. ABI-350 reduces complete positive misses relative to ABI-348, ABI-324, ABI-337, and ABI-223, and has fewer low-connectivity positive patches than ABI-324/337/223. Its positive median Dice and median connectivity are also competitive. However, it still leaves 450 of 719 positive patches below 0.50 recall, worse than ABI-324/337/346/223, and its aggregate connectivity remains far below ABI-324 and ABI-223. The mechanism improves compact aggregate evidence more than it solves continuous thin-line coverage.

The negative-patch clutter result is also mixed. ABI-350 is much cleaner than ABI-346 and ABI-223 on total negative-patch predicted pixels, and its heavy-tail count above 200 pixels is low. It also reduces the number of negative patches touched relative to ABI-348/346. But it touches more negative patches than ABI-324 or ABI-223, and its total negative-patch pixel burden is essentially ABI-324/348-like rather than clearly better.

Source buckets keep the usual MIT difficulty pattern:

| Source bucket | MIT | Google |
| --- | ---: | ---: |
| Positive samples | 423 | 296 |
| Positive median recall | 0.4035 | 0.4527 |
| Positive median Dice | 0.4091 | 0.4838 |
| Positive median connectivity | 0.3947 | 0.4856 |
| Complete positive misses | 37 | 27 |
| Positive recall < 0.25 | 123 | 70 |
| Negative samples | 492 | 403 |
| Negative samples with any prediction | 328 | 283 |
| Negative samples >128 predicted pixels | 67 | 15 |
| Negative samples >512 predicted pixels | 4 | 0 |
| Total negative-patch predicted pixels | 28,046 | 13,269 |

ABI-350's aggregate MIT Dice is competitive, but the residual failures remain MIT-heavy: weaker positive median recall/connectivity and a much larger negative-patch clutter tail than Google. The result is therefore not a source-balance breakthrough.

## Threshold behavior

The threshold sweep shows moderate low-threshold headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low threshold | 0.05 | 0.441614 | 0.409788 | 0.478801 | 638,901 |
| Best filtered Dice | 0.10 | 0.442779 | 0.437717 | 0.447960 | 559,608 |
| Near-balance reference | 0.20 | 0.440499 | 0.461714 | 0.421148 | 498,770 |
| Primary evaluation | 0.50 | 0.431103 | 0.494306 | 0.382230 | 422,831 |
| High-precision reference | 0.70 | 0.421885 | 0.513737 | 0.357896 | 380,938 |

The best diagnostic threshold improves filtered Dice by +0.0117 over the trusted fixed 0.5 threshold. Architecturally, ABI-350 has sub-threshold recall reserve, but this does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, Artifact Filters, or validation selection. The fixed-threshold Result remains a compact/high-precision operating point with residual under-recall.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.208576 | 0.210513 | 0.204325 | 0.208507 | 0.208646 | 0.159844 | 0.005173 |
| 5 | 0.336928 | 0.314057 | 0.393539 | 0.410807 | 0.285572 | 0.244935 | 0.003594 |
| 8 | 0.338775 | 0.313016 | 0.403932 | 0.401347 | 0.293082 | 0.258709 | 0.003775 |
| 12 | 0.390828 | 0.378380 | 0.422679 | 0.387931 | 0.393768 | 0.270923 | 0.005247 |
| 17 | 0.397562 | 0.373063 | 0.459713 | 0.447099 | 0.357907 | 0.289107 | 0.004138 |
| 24 | 0.384274 | 0.353428 | 0.466970 | 0.529359 | 0.301610 | 0.339222 | 0.002945 |
| 27 | 0.405399 | 0.382781 | 0.467351 | 0.527448 | 0.329219 | 0.349236 | 0.003227 |
| 29 | 0.426777 | 0.405619 | 0.484731 | 0.484091 | 0.381597 | 0.355793 | 0.004075 |
| 31 | 0.418052 | 0.398874 | 0.469526 | 0.478383 | 0.371234 | 0.242744 | 0.004012 |
| 33 | 0.431103 | 0.409536 | 0.490518 | 0.494306 | 0.382230 | 0.358283 | 0.003997 |
| 36 | 0.389596 | 0.369943 | 0.440534 | 0.432862 | 0.354193 | 0.208217 | 0.004230 |

The trajectory confirms late-budget value but also instability. ABI-350 did not plateau at the exploratory boundary; the selected epoch 33 is far above the epoch-12 checkpoint and above ABI-349. However, the final epoch regressed sharply, especially on connectivity. The branch can find a strong compact state, but the connected-line quality is not stable across the late budget.

## Interpretation

Classify ABI-350 as mixed-positive capped evidence for temporal-attention pre-decoder line support.

The positive result is real: ABI-350 becomes the top capped temporal-eligible aggregate filtered-Dice Result in the local comparison set and substantially validates ABI-349's pre-decoder line-support mechanism. It improves the ABI-349 parent without broadening into ABI-344-style recall clutter, keeps a compact footprint, and remains finite/source-informative.

The negative result is that ABI-350 does not solve the main connected-line continuity and source-balance residuals. It wins aggregate Dice through a compact high-precision, Google-strong checkpoint. ABI-324 remains the balanced temporal C4/detail-consensus comparator, and ABI-223 remains the temporal-attention connectivity comparator. ABI-350 is best treated as a capped temporal-eligible aggregate/precision comparator and a strong design ingredient, not as whole-validation promotion evidence or a connected-line frontier.

ABI-350 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-350 and do not submit another unchanged late36 continuation of the same pre-decoder line-support architecture. The diagnostic question is answered: the late continuation improves aggregate capped temporal-eligible Dice and validates the mechanism, but it does not close the ABI-324/223 connectivity gap or solve MIT/source-balanced undercoverage.

Future work should be mechanism-changing. A defensible next temporal-attention hypothesis may preserve ABI-350's pre-decoder line-support anchor, but should add explicit continuity or MIT-positive-tail support before final logits: for example, a line-continuity decoder, a temporal alignment/change bridge that lifts continuous center-frame segments, or a source-agnostic detail/Line/Centerline agreement path that raises true contrail logits at threshold 0.5 without widening negative-patch clutter. Simple late-budget repeats, gate-strength tweaks, or Candidate-owned threshold/calibration changes are not justified.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_013306_9ca44e/candidate/PROPOSAL.md`
- `run_20260919_013306_9ca44e/candidate/README.md`
- `run_20260919_013306_9ca44e/candidate/manifest.yaml`
- `run_20260919_013306_9ca44e/candidate/budget_request.yaml`
- `run_20260919_013306_9ca44e/resolved_manifest.yaml`
- `run_20260919_013306_9ca44e/execution.json`
- `run_20260919_013306_9ca44e/run_metadata.json`
- `run_20260919_013306_9ca44e/outputs/model_summary.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json`
- `run_20260919_013306_9ca44e/outputs/final_metrics.json`
- `run_20260919_013306_9ca44e/outputs/metrics.jsonl`
- `run_20260919_013306_9ca44e/outputs/resource_profile.json`
- `run_20260919_013306_9ca44e/outputs/validation_postprocessing/index.json`
- `run_20260919_013306_9ca44e/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/evaluations/eval_evalreq_abi350_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260919_013306_9ca44e/outputs/evaluations/eval_evalreq_abi350_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260919_013306_9ca44e/outputs/evaluations/eval_evalreq_abi350_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260919_013306_9ca44e/outputs/evaluations/eval_evalreq_abi350_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260919_004607_f785f8/outputs/best_metrics.json` and `/history/research-notes/abi349-temporal-attention-predecoder-line-support-unet.md`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_152331_c80150/outputs/evaluations/eval_evalreq_abi346_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/temporal-c4-frontier-reset-after-abi348.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
