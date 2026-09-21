# ABI-277 temporal bidirectional-consistency line-state U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-277, Candidate `abi277_temporal_bidirectional_consistency_line_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_222529_d1a74a`.

ABI-277 was a mechanism-changing temporal-family continuation after ABI-274, ABI-275, and ABI-276. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. The architectural change was to add a bidirectional temporal-consistency state from before/after residual agreement, persistence, motion, and imbalance features, then inject that state with the temporal line state at encoder scales and final refinement.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Execution result

ABI-277 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,362,400, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.06 / 6.44 GB.
- Training wall time: 1,698.8 s; validation wall time: 1,132.2 s; total Run wall time: 2,832.9 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-277 best epoch 11 | ABI-274 temporal line-state late36 | ABI-276 center-detail scout | ABI-275 C4 bridge scout | ABI-223 temporal attention late36 | ABI-255 recurrent temporal late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.384239 | 0.419364 | 0.392168 | 0.385365 | 0.419776 | 0.417348 | 0.427570 |
| Raw Dice | 0.401624 | 0.436760 | 0.409195 | 0.401336 | 0.438487 | 0.433815 | 0.442746 |
| Filtered precision | 0.457624 | 0.454127 | 0.445297 | 0.413604 | 0.483764 | 0.468293 | 0.439467 |
| Filtered recall | 0.331138 | 0.389545 | 0.350365 | 0.360736 | 0.370738 | 0.376400 | 0.416301 |
| Filtered connectivity | 0.263442 | 0.282911 | 0.278531 | 0.266368 | 0.412427 | 0.281116 | 0.457773 |
| MIT filtered Dice | 0.364664 | 0.399386 | 0.375358 | 0.372421 | 0.398498 | 0.400833 | 0.411992 |
| Google filtered Dice | 0.436066 | 0.472606 | 0.434143 | 0.417764 | 0.476764 | 0.463143 | 0.468151 |
| Filtered predicted-positive fraction | 0.003741 | 0.004434 | 0.004067 | 0.004509 | 0.003962 | 0.004155 | 0.003433 |

ABI-277 did not meet its primary comparison targets. Relative to ABI-274, it is lower by about -0.0351 filtered Dice, -0.0584 recall, -0.0195 connectivity, -0.0347 MIT Dice, and -0.0365 Google Dice, with only a small precision gain (+0.0035) and a more compact predicted-positive fraction. Relative to ABI-276, it is lower by about -0.0079 filtered Dice, -0.0192 recall, -0.0151 connectivity, and -0.0107 MIT Dice, while precision rises modestly (+0.0123) and Google Dice is essentially similar to slightly higher (+0.0019). Relative to ABI-275, ABI-277 is more compact and higher precision, but not higher Dice, recall, connectivity, or MIT performance.

The bidirectional-consistency branch therefore acts mainly as a conservative evidence filter. It suppresses predicted-positive extent and improves precision versus the weakest ABI-275 branch, but it does not preserve enough true-positive coverage or connected thin-line continuity to repair ABI-274's main failure mode.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.231709 | 0.225784 | 0.246462 | 0.331339 | 0.178143 | 0.265582 | 0.002779 |
| 2 | 0.277531 | 0.283453 | 0.265470 | 0.247130 | 0.316462 | 0.163687 | 0.006620 |
| 3 | 0.267309 | 0.244465 | 0.325378 | 0.452742 | 0.189637 | 0.257223 | 0.002165 |
| 4 | 0.316381 | 0.299480 | 0.358026 | 0.382728 | 0.269639 | 0.240866 | 0.003642 |
| 5 | 0.319399 | 0.296845 | 0.378908 | 0.472358 | 0.241271 | 0.278941 | 0.002641 |
| 6 | 0.350682 | 0.338020 | 0.384535 | 0.468256 | 0.280301 | 0.361014 | 0.003095 |
| 7 | 0.307930 | 0.283240 | 0.375102 | 0.567274 | 0.211319 | 0.385288 | 0.001926 |
| 8 | 0.371871 | 0.356394 | 0.414300 | 0.493248 | 0.298433 | 0.375709 | 0.003128 |
| 9 | 0.366289 | 0.356641 | 0.389748 | 0.350523 | 0.383541 | 0.202123 | 0.005657 |
| 10 | 0.327666 | 0.312375 | 0.364256 | 0.399749 | 0.277607 | 0.169914 | 0.003590 |
| 11 | 0.384239 | 0.364664 | 0.436066 | 0.457624 | 0.331138 | 0.263442 | 0.003741 |
| 12 | 0.374676 | 0.356568 | 0.421036 | 0.460785 | 0.315683 | 0.222886 | 0.003542 |

The trajectory is finite, source-informative, and non-collapsed, but noisy. Best filtered Dice occurs at epoch 11, then the final epoch drops in filtered Dice, recall, connectivity, MIT Dice, and Google Dice. Epochs 6-8 show temporarily stronger connectivity, especially epoch 8 at 0.3757, but those checkpoints are lower-Dice and lower-recall conservative operating points. Epoch 9 briefly reaches high recall (0.3835) at a broad predicted-positive fraction, but precision and connectivity fall sharply. The branch does not show a stable late-improving trajectory that would justify an unchanged late36 continuation.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2680, 0.4380, 0.4885, and 0.4439. This is consistent with a finite non-collapsed model and substantial per-sample variability. This note does not reproduce raw samples, images, coordinates, scene identifiers, or patch identities.

At the selected checkpoint, Artifact Filters removed about 31,185 predicted-positive pixels (`426,859` raw predicted-positive pixels versus `395,674` filtered). Raw Dice was 0.4016 versus filtered Dice 0.3842, so filtering lowers rather than creates the Result.

## Interpretation

Classify ABI-277 as a finite negative mechanism test. The bidirectional before/after consistency state is resource-safe and does create conservative high-precision/high-connectivity episodes, but it does not improve selected-checkpoint connectivity over ABI-274, ABI-276, or even ABI-275, and it under-covers MIT validation more strongly than the recent temporal comparators. The mechanism appears to treat temporal inconsistency as a suppressor rather than as a continuity organizer: when it is compact, it misses true contrail extent; when it broadens, connectivity and precision degrade.

This does not eliminate temporal modeling or consistency features as families. It narrows the exact ABI-277 integration point: injecting residual-agreement consistency beside the line state at every encoder scale is insufficient to recover ABI-274's recall/source lift or ABI-223's connected-line behavior. ABI-274 remains the temporal recall/source-balance comparator, ABI-223 remains the cleaner temporal connectivity comparator, ABI-255 remains the compact recurrent temporal comparator, ABI-249 remains the high-precision C4 whole-validation comparator, and ABI-202 remains the aggregate whole-validation reference.

## Decision

Do not promote ABI-277, do not request temporal-eligible failure-bucket diagnostics, and do not request a late-improving budget for this exact bidirectional-consistency branch. The branch failed its stated success criteria: it did not improve ABI-276, did not approach ABI-274 filtered Dice/recall/source balance, and did not lift selected-checkpoint connectivity.

Do not repeat ABI-277 unchanged. Future work should be mechanism-changing and should broaden away from adding more temporal suppressor states to ABI-274. A better next hypothesis should either return to ABI-223/238-style temporal attention with architecture-level evidence sharpening, or switch to a recall-preserving calibration/dual-evidence or orientation-consensus mechanism that raises true contrail logits at threshold 0.5 without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_222529_d1a74a/candidate/PROPOSAL.md`
- `run_20260912_222529_d1a74a/candidate/README.md`
- `run_20260912_222529_d1a74a/candidate/manifest.yaml`
- `run_20260912_222529_d1a74a/resolved_manifest.yaml`
- `run_20260912_222529_d1a74a/outputs/model_summary.json`
- `run_20260912_222529_d1a74a/outputs/best_metrics.json`
- `run_20260912_222529_d1a74a/outputs/final_metrics.json`
- `run_20260912_222529_d1a74a/outputs/metrics.jsonl`
- `run_20260912_222529_d1a74a/outputs/resource_profile.json`
- `run_20260912_222529_d1a74a/outputs/validation_postprocessing/index.json`
- `run_20260912_222529_d1a74a/outputs/prediction_samples/samples.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260912_212900_56562e/outputs/best_metrics.json` for ABI-276 center-detail comparison context
- `run_20260912_203536_240ad8/outputs/best_metrics.json` for ABI-275 C4 bridge comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal comparator context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparator context
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
