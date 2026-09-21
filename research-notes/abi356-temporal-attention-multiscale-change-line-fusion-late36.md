# ABI-356 temporal-attention multi-scale change-line fusion late36

research-figures: []

## Scope

This note records ABI-356, Candidate `abi356_temporal_attention_multiscale_change_line_fusion_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_095725_843317`, and Post-Run Evaluation `eval_evalreq_abi356_temporal_eligible_failure_buckets_v1`.

ABI-356 was the approved late-improving continuation of ABI-355. It kept provider-owned `abi_16ch_plus_sza_temporal` input with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The narrow question was whether ABI-355's multi-scale temporal-change/center-detail line fusion would stabilize under 36 epochs into a useful fixed-threshold recall/connectivity temporal comparator.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-356 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, with parent Run `run_20260919_090506_bad1ff`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,615,732, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,915,849,728 / 5,435,817,984 bytes.
- Training wall time: 4,727.5 s; validation wall time: 3,307.7 s; total Run wall time: 8,037.5 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at the final epoch 36.

## Best-validation and diagnostic metrics

| Metric | ABI-356 late36 | ABI-355 parent | ABI-350 line-support late36 | ABI-324 five-frame C4 | ABI-348 compact five-frame C4 | ABI-223 temporal attention | ABI-346 recall ladder |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 11 | 33 | 27 | 36 | 36 | 23 |
| Filtered Dice | 0.426056 | 0.393153 | 0.431103 | 0.429430 | 0.427829 | 0.419776 | 0.427835 |
| MIT filtered Dice | 0.411375 | 0.375355 | 0.409536 | 0.408188 | 0.410244 | 0.398498 | 0.407956 |
| Google filtered Dice | 0.465688 | 0.438306 | 0.490518 | 0.487231 | 0.478363 | 0.476764 | 0.480484 |
| Filtered precision | 0.421447 | 0.426347 | 0.494306 | 0.470412 | 0.477546 | 0.483764 | 0.461087 |
| Filtered recall | 0.430766 | 0.364754 | 0.382230 | 0.395017 | 0.387488 | 0.370738 | 0.399057 |
| Filtered connectivity | 0.282116 | 0.312086 | 0.358283 | 0.397925 | 0.300904 | 0.412427 | 0.299258 |
| Filtered predicted-positive pixels | 558,903 | 467,816 | 422,831 | 459,172 | 443,691 | 419,056 | 473,249 |

ABI-356 substantially answers the late-budget question for the ABI-355 mechanism. Relative to ABI-355 it gains +0.0329 filtered Dice, +0.0360 MIT Dice, +0.0274 Google Dice, and +0.0660 recall, but it does so with 91,087 more filtered predicted-positive pixels and lower connectivity (-0.0300). The mechanism clearly recovers additional fixed-threshold contrail evidence, but not connected thin-line continuity.

Relative to the strongest recent temporal comparators, ABI-356 is recall-positive but not frontier. It nearly matches ABI-348/346 aggregate Dice and exceeds ABI-350/324/223/348/346 recall, but its precision and connectivity are substantially weaker and its prediction footprint is much broader. Compared with ABI-350, ABI-356 has +0.0485 recall but -0.0729 precision, -0.0762 connectivity, -0.0050 filtered Dice, and +136,072 filtered-positive pixels. Compared with ABI-324, it has +0.0357 recall but -0.0490 precision, -0.1158 connectivity, and -0.0034 filtered Dice. ABI-356 is therefore a useful recall-biased temporal-attention diagnostic, not a replacement for the balanced temporal C4/detail-consensus or line-support comparators.

At the selected checkpoint, raw Dice was 0.443015 versus filtered Dice 0.426056, raw recall was 0.465941 versus filtered recall 0.430766, and raw predicted-positive pixels were 603,407 versus 558,903 filtered. Artifact Filters removed 44,504 predicted-positive pixels and lowered the primary score, so the Result is not being created by postprocessing.

The retained fixed first-four validation samples had raw sample Dice values 0.4894, 0.1911, 0.4847, and 0.4166. These are traceability artifacts only and do not override aggregate validation metrics.

## Failure-bucket evaluation signal

The completed temporal-eligible failure-bucket evaluation used the same provider-owned 1,614 validation ABI Patches and the trusted fixed threshold 0.5. It confirms that ABI-356's gain is broad recall support with persistent clutter and continuity weakness:

- Positive ABI Patches: 719 total; 57 complete misses, 82 with recall below 0.10, 162 with recall below 0.25, and 355 with recall at least 0.50.
- Positive medians: filtered recall 0.492, Dice 0.429, connectivity 0.402.
- Source positive tails remain imbalanced: Google median recall/Dice/connectivity were 0.531 / 0.470 / 0.472, while MIT medians were 0.461 / 0.396 / 0.362.
- Negative ABI Patches: 895 total; 722 had at least one filtered predicted-positive pixel, but only 202 exceeded 100 pixels and 11 exceeded 500 pixels. Negative-patch filtered positives summed to 68,463 pixels, about 12% of the 558,903 filtered predicted-positive pixels.
- MIT negative-patch clutter was larger than Google clutter: 45,062 versus 23,401 summed filtered-positive pixels.

Threshold-sweep diagnostics do not rescue the branch. The best filtered Dice in the sweep was 0.427155 at threshold 0.30, only +0.0011 above the trusted 0.5 fixed-threshold Dice, with precision 0.4003 and recall 0.4579. This is a broad operating plateau rather than evidence for Candidate-owned threshold selection.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.222680 | 0.230416 | 0.207346 | 0.204809 | 0.243967 | 0.134014 | 0.006158 |
| 5 | 0.350708 | 0.334284 | 0.394156 | 0.458493 | 0.283955 | 0.356123 | 0.003202 |
| 10 | 0.386969 | 0.368382 | 0.434475 | 0.453397 | 0.337518 | 0.365846 | 0.003848 |
| 15 | 0.393431 | 0.370914 | 0.452387 | 0.483019 | 0.331876 | 0.402902 | 0.003552 |
| 20 | 0.391732 | 0.366917 | 0.455369 | 0.474703 | 0.333449 | 0.322013 | 0.003631 |
| 25 | 0.397893 | 0.376606 | 0.454572 | 0.488849 | 0.335474 | 0.310524 | 0.003548 |
| 30 | 0.394494 | 0.372566 | 0.454196 | 0.547514 | 0.308324 | 0.449404 | 0.002911 |
| 31 | 0.397396 | 0.376748 | 0.451681 | 0.515981 | 0.323133 | 0.270415 | 0.003237 |
| 32 | 0.412773 | 0.398302 | 0.448059 | 0.386086 | 0.443423 | 0.213287 | 0.005937 |
| 33 | 0.386096 | 0.365920 | 0.438542 | 0.523024 | 0.305988 | 0.314181 | 0.003024 |
| 34 | 0.410219 | 0.391782 | 0.459517 | 0.424238 | 0.397096 | 0.285247 | 0.004839 |
| 35 | 0.401733 | 0.377760 | 0.465797 | 0.541191 | 0.319422 | 0.392689 | 0.003051 |
| 36 | 0.426056 | 0.411375 | 0.465688 | 0.421447 | 0.430766 | 0.282116 | 0.005284 |

The trajectory is finite, source-informative, and late-budget-dependent. The final epoch is the selected checkpoint and the first epoch to combine >0.42 aggregate Dice with >0.43 recall. However, the late gains are oscillatory: epochs 30 and 35 show compact high-precision/high-connectivity states, while epochs 32, 34, and 36 trade precision and connectivity for broader recall. This supports the interpretation that ABI-356 learned a positive-tail recall mechanism, not a stable connected-line continuity mechanism.

## Interpretation

Classify ABI-356 as mixed-positive late-budget family-development evidence. The exact multi-scale temporal change-line fusion branch should not be dismissed as an optimization failure: it is finite, reaches the top temporal-eligible capped band, improves materially over ABI-355, and gives the campaign a recall-biased temporal-attention comparator.

Do not promote ABI-356. Its advantage is primarily fixed-threshold recall, while precision, negative-patch clutter, and connected-line continuity remain weaker than ABI-350/324/223/348. The completed diagnostic indicates that the added positives include meaningful positive-tail recovery but also a larger MIT clutter burden and persistent source imbalance.

Do not spend another Run on an unchanged ABI-356 late36 continuation or a simple gate-strength/placement shuffle. If this branch continues, the next hypothesis should be mechanism-changing: preserve ABI-356's recall-positive multi-scale skip fusion while adding an explicit compact C4/orientation or line-continuity anchor that constrains the broad positive footprint and raises connectivity. A reasonable next Candidate would be a temporal-attention/C4 hybrid decoder-side support module, not another standalone temporal-attention fusion variant.

ABI-356 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-356 and do not request another diagnostic for this Run; the temporal-eligible failure-bucket evaluation is already complete. Treat ABI-356 as positive evidence that the multi-scale temporal change-line fusion mechanism can recover recall under the late budget, but as negative evidence that the exact mechanism solves connected-line continuity.

A future Autonomy Step may submit one mechanism-changing temporal-attention plus compact C4/orientation-continuity follow-up, or broaden to a different line-continuity/backbone direction if the campaign prioritizes precision/connectivity over recall recovery.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_095725_843317/candidate/PROPOSAL.md`
- `run_20260919_095725_843317/candidate/README.md`
- `run_20260919_095725_843317/candidate/manifest.yaml`
- `run_20260919_095725_843317/candidate/budget_request.yaml`
- `run_20260919_095725_843317/resolved_manifest.yaml`
- `run_20260919_095725_843317/execution.json`
- `run_20260919_095725_843317/run_metadata.json`
- `run_20260919_095725_843317/outputs/model_summary.json`
- `run_20260919_095725_843317/outputs/best_metrics.json`
- `run_20260919_095725_843317/outputs/final_metrics.json`
- `run_20260919_095725_843317/outputs/metrics.jsonl`
- `run_20260919_095725_843317/outputs/resource_profile.json`
- `run_20260919_095725_843317/outputs/validation_postprocessing/index.json`
- `run_20260919_095725_843317/outputs/prediction_samples/samples.json`
- `run_20260919_095725_843317/outputs/evaluations/eval_evalreq_abi356_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260919_095725_843317/outputs/evaluations/eval_evalreq_abi356_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260919_095725_843317/outputs/evaluations/eval_evalreq_abi356_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260919_095725_843317/outputs/evaluations/eval_evalreq_abi356_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260919_090506_bad1ff/outputs/best_metrics.json` and `/history/research-notes/abi355-temporal-attention-multiscale-change-line-fusion.md` for ABI-355 parent context
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparator context
- `run_20260918_215534_a35ab9/outputs/best_metrics.json` and `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md` for ABI-348 comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparator context
- `run_20260918_152331_c80150/outputs/best_metrics.json` and `/history/research-notes/abi346-temporal-c4-connected-recall-ladder-late36.md` for ABI-346 comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
