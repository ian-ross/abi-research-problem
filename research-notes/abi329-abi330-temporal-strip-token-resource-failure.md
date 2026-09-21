# ABI-329/ABI-330 temporal strip-token line-mixer resource failure

research-figures: []

## Scope

This note records failure classification and next-step guidance for two related temporal strip-token line-mixer Candidates:

- ABI-329, Candidate `abi329_temporal_attention_strip_token_line_mixer_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260917_084054_9439c2`.
- ABI-330, Candidate `abi330_temporal_attention_compact_strip_token_line_mixer_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260917_094525_ca3a59`.

Both Candidates used provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-1, 0, 1]`, combined source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. Candidate code owned only model architecture over provider-supplied tensors.

This is capped temporal-eligible feasibility and resource evidence only. Neither Run produced a terminal Result suitable for ranking against completed capped or whole-validation comparators.

## Execution result

Both Runs failed under Harness-owned lifecycle control with `failure_classification: resource_failure` after exhausting the 3,600-second exploratory Docker wall-clock budget and 30-second grace period.

| Run | Candidate | Parameters | Terminal status | Last completed validation epoch | Best observed epoch | Best observed filtered Dice | Last observed filtered Dice |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| `run_20260917_084054_9439c2` | ABI-329 strip-token line mixer | 7,053,871 | failed / resource_failure | 10 | 10 | 0.369888 | 0.369888 |
| `run_20260917_094525_ca3a59` | ABI-330 compact strip-token line mixer | 4,901,427 | failed / resource_failure | 10 | 8 | 0.390537 | 0.353109 |

ABI-330 successfully reduced parameter count by about 30% relative to ABI-329 and improved the best partial validation score, but it still failed to finish the exploratory budget. That makes this an architecture/resource feasibility stop for the exact strip-token hierarchy under the current policy, not a reason to request Candidate-owned scheduling or reinterpret partial metrics as terminal Results.

## Partial metric evidence

The partial metrics are useful only for diagnosing whether the resource-failed branch was finite and source-informative before timeout.

| Metric at best observed epoch | ABI-329 epoch 10 | ABI-330 epoch 8 |
| --- | ---: | ---: |
| Filtered Dice | 0.369888 | 0.390537 |
| MIT filtered Dice | 0.350164 | 0.370234 |
| Google filtered Dice | 0.416892 | 0.443476 |
| Filtered precision | 0.403433 | 0.467951 |
| Filtered recall | 0.341494 | 0.335101 |
| Filtered connectivity | 0.225061 | 0.385993 |
| Filtered predicted-positive fraction | 0.004376 | 0.003702 |
| Train loss | 0.805270 | 0.815178 |

ABI-330's partial epoch-8 operating point is the most interesting observation: it was finite, compact, more precise than ABI-329, and had much higher connectivity. However, the same Run degraded by epoch 10 and still timed out. Because the Run failed, this is not a completed Result and should not trigger a late-improving request or promotion-style comparison.

## Failure classification

Use the Harness-recorded classification: `resource_failure` for both Runs.

This is not a candidate bug, contract violation, non-finite state, metric collapse, or Harness failure. A narrow Repair Candidate is not appropriate under the usual candidate-bug/contract-repair meaning. ABI-330 already tested the obvious resource-narrowing continuation of ABI-329 and still exhausted the wall-clock budget.

The exact mechanism should therefore be considered resource-infeasible for the current exploratory policy:

- three-frame temporal attention is acceptable in other Candidates, but
- multi-scale full-resolution horizontal/vertical strip-token mixing throughout the stem, encoder, decoder, refinement, and consensus head is too expensive in this form,
- further small width reductions would likely change capacity while preserving the expensive hierarchy and would risk another timeout.

## Comparator context

Completed temporal-family context remains stronger and terminal:

- ABI-324 (`run_20260916_184108_954ec7`) remains the strongest recent balanced temporal C4 aggregate/connectivity comparator, with best capped temporal-eligible filtered Dice 0.429430 at epoch 27.
- ABI-325 (`run_20260916_212722_d66d93`) remains the positive-tail recall diagnostic, not a balanced comparator.
- ABI-326 (`run_20260917_002229_d43b7a`) and ABI-328 (`run_20260917_055012_ba7890`) are finite late36 alternatives around the same temporal C4 family but do not solve the connected-line trade-off.
- ABI-223 remains the older temporal-attention diagnostic comparator with strong temporal-eligible connectivity.

ABI-329/330 should not displace these completed comparators. Their contribution is showing that a materially different strip-token line-mixer path can be finite and partly promising, but not resource-fit under the current ceiling.

## Decision

Do not spend another Run on an unchanged or merely narrower ABI-329/330 strip-token U-Net hierarchy. Do not request Candidate-owned scheduling, lower-level timeout changes, custom batching, custom validation cadence, or any candidate-side lifecycle workaround.

The next safe hypothesis should broaden away from this exact resource-heavy branch while preserving the scientific target: connected true-positive temporal line evidence at threshold 0.5 with source balance and compact predicted-positive footprint. Viable next directions include:

1. a materially cheaper temporal model that uses local temporal-difference/detail features with depthwise-separable or residual blocks rather than multi-scale strip-token mixers;
2. a single-frame or temporal dual-evidence/calibration head that raises fixed-threshold recall without adding full-resolution long-kernel feature mixing;
3. a focused Research Note or Candidate Proposal comparing whether the ABI-324/325 failure-bucket diagnostics point to data/loss/calibration mechanisms rather than heavier architecture.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_084054_9439c2/candidate/PROPOSAL.md`
- `run_20260917_084054_9439c2/candidate/README.md`
- `run_20260917_084054_9439c2/candidate/manifest.yaml`
- `run_20260917_084054_9439c2/outputs/model_summary.json`
- `run_20260917_084054_9439c2/outputs/metrics.jsonl`
- `run_20260917_084054_9439c2/outputs/logs/harness_timeout.log`
- `run_20260917_084054_9439c2/outputs/validation_postprocessing/index.json`
- `run_20260917_094525_ca3a59/candidate/PROPOSAL.md`
- `run_20260917_094525_ca3a59/candidate/README.md`
- `run_20260917_094525_ca3a59/candidate/manifest.yaml`
- `run_20260917_094525_ca3a59/outputs/model_summary.json`
- `run_20260917_094525_ca3a59/outputs/metrics.jsonl`
- `run_20260917_094525_ca3a59/outputs/logs/harness_timeout.log`
- `run_20260917_094525_ca3a59/outputs/validation_postprocessing/index.json`
- `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
