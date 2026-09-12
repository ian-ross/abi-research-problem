# ABI-229 temporal window-attention U-NetFormer

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-229, Candidate `abi229_temporal_window_attention_unetformer_bce_dice_line_centerline_aux_v1`, Run `run_20260910_141659_818da0`.

ABI-229 was a temporal/modern-backbone family scout after ABI-223, ABI-226, ABI-227, and ABI-228. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. The hypothesis was that compact Swin/UNetFormer-style local window attention could improve temporal contrail segmentation by letting the encoder/bottleneck/decoder use local self-attention over temporally fused thin-line evidence, without Candidate-owned temporal lookup or postprocessing. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-229 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,880,780, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.21 / 4.45 GB.
- Training wall time: 1,359.1 s; validation wall time: 1,066.6 s; total Run wall time: 2,427.5 s.

This is successful finite/resource evidence for a compact temporal window-attention/U-NetFormer formulation.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8.

| Metric | ABI-229 best epoch 8 |
| --- | ---: |
| Filtered Dice | 0.376958 |
| Raw Dice | 0.393997 |
| Filtered IoU | 0.232254 |
| Filtered precision | 0.434428 |
| Filtered recall | 0.332917 |
| Filtered contrail connectivity | 0.313635 |
| Filtered predicted-positive fraction | 0.003962 |
| Raw predicted-positive fraction | 0.004282 |
| MIT filtered Dice | 0.364086 |
| Google filtered Dice | 0.410445 |
| MIT filtered recall | 0.310336 |
| Google filtered recall | 0.400102 |
| Train loss | 0.825286 |
| Validation loss | 0.866218 |

The selected Result is finite, noncollapsed, source-informative, and has a balanced precision/recall profile. It is a small same-budget improvement over the earlier three-frame temporal-attention scout ABI-222, with a stronger connectivity value, but it does not exceed the five-frame ABI-226 primary metric and remains far below the late36 temporal frontier ABI-223.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.195534 | 0.205172 | 0.186761 | 0.199830 | 0.186822 | 0.147983 | 0.004706 |
| 2 | 0.242228 | 0.248747 | 0.236041 | 0.247618 | 0.230929 | 0.152978 | 0.004906 |
| 3 | 0.275998 | 0.319954 | 0.242661 | 0.268500 | 0.292653 | 0.166465 | 0.003921 |
| 4 | 0.298842 | 0.326866 | 0.275243 | 0.294101 | 0.309593 | 0.187716 | 0.004353 |
| 5 | 0.328356 | 0.488564 | 0.247271 | 0.312795 | 0.368812 | 0.325944 | 0.002616 |
| 6 | 0.353746 | 0.343289 | 0.364860 | 0.351682 | 0.358547 | 0.232251 | 0.005494 |
| 7 | 0.338965 | 0.365918 | 0.315710 | 0.326587 | 0.368504 | 0.269006 | 0.004460 |
| 8 | 0.376958 | 0.434428 | 0.332917 | 0.364086 | 0.410445 | 0.313635 | 0.003962 |
| 9 | 0.366613 | 0.344612 | 0.391615 | 0.360621 | 0.381004 | 0.225268 | 0.005875 |
| 10 | 0.342330 | 0.419506 | 0.289138 | 0.325580 | 0.384180 | 0.265332 | 0.003563 |
| 11 | 0.366072 | 0.462338 | 0.302985 | 0.344352 | 0.422155 | 0.302832 | 0.003388 |
| 12 | 0.355316 | 0.392749 | 0.324397 | 0.346021 | 0.379166 | 0.189218 | 0.004270 |

The trajectory rises steadily through epoch 6, peaks at epoch 8, then oscillates without setting a new primary-metric high. Epoch 11 shows the best Google filtered Dice (0.422155) and strong precision/connectivity, but it does not recover the aggregate best Dice because MIT Dice falls. The final epoch regresses on aggregate filtered Dice and connectivity.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-222 attention 12ep | ABI-223 attention late36 | ABI-226 five-frame scout | ABI-227 line-consistency | ABI-228 rotation line-accum | ABI-229 window attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 36 | 10 | 9 | 8 | 8 |
| Filtered Dice | 0.345570 | 0.374329 | 0.419776 | 0.378604 | 0.370657 | 0.368554 | 0.376958 |
| Raw Dice | 0.361077 | 0.392066 | 0.438487 | 0.394881 | 0.383841 | 0.383662 | 0.393997 |
| Filtered precision | 0.407234 | 0.466148 | 0.483764 | 0.428061 | 0.341621 | 0.381951 | 0.434428 |
| Filtered recall | 0.300125 | 0.312729 | 0.370738 | 0.339391 | 0.405088 | 0.356064 | 0.332917 |
| Filtered connectivity | 0.231399 | 0.281396 | 0.412427 | 0.224851 | 0.190346 | 0.202312 | 0.313635 |
| MIT filtered Dice | 0.330415 | 0.357658 | 0.398498 | 0.366586 | 0.360838 | 0.358973 | 0.364086 |
| Google filtered Dice | 0.385184 | 0.416510 | 0.476764 | 0.409886 | 0.394514 | 0.391801 | 0.410445 |
| Filtered predicted-positive fraction | 0.003810 | 0.003468 | 0.003962 | 0.004099 | 0.006130 | 0.004819 | 0.003962 |
| Parameter count | 3,050,475 | 3,095,836 | 3,095,836 | 3,098,332 | 3,133,588 | 3,130,112 | 3,880,780 |

Relative to ABI-222 at the same 12-epoch three-frame temporal-attention budget, ABI-229 is +0.002629 filtered Dice, +0.012239 raw Dice, +0.020188 filtered recall, +0.006428 MIT filtered Dice, and +0.032239 connectivity, while sacrificing -0.031720 precision and -0.006065 Google filtered Dice. Relative to the matched single-frame control ABI-218, ABI-229 is +0.031388 filtered Dice and +0.082236 connectivity, so temporal attention remains useful relative to no temporal input.

Relative to ABI-226, the current best 12-epoch temporal scout, ABI-229 is slightly lower on aggregate filtered Dice (-0.001646) and MIT Dice (-0.002500), but slightly higher on Google Dice (+0.000559), precision (+0.006367), and connectivity (+0.088784). That makes ABI-229 scientifically positive for the window-attention idea even though it is not a new capped frontier.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result, with whole-validation filtered Dice 0.4312. ABI-223 remains the capped temporal-family frontier, with filtered Dice 0.419776 at epoch 36 and strong MIT/Google source behavior. ABI-229 is the strongest same-budget three-frame temporal-attention Result observed so far, but its capped score remains below ABI-226 and far below ABI-223.

ABI-229 is therefore not a promotion candidate and does not justify immediate whole-validation diagnostics. It does, however, strengthen the evidence that modern local attention can help temporal contrail segmentation when used in a compact resource-safe backbone.

## Interpretation

Classify ABI-229 as a finite, resource-safe, modestly positive temporal/modern-backbone scout. The window-attention U-NetFormer mechanism improves the three-frame same-budget temporal-attention baseline and shows better selected-checkpoint connectivity than ABI-222, ABI-226, ABI-227, or ABI-228. The improvement is small and the best checkpoint occurs at epoch 8, followed by oscillation and final regression, so the exact ABI-229 branch does not meet the approved `late_improving` budget rationale.

The useful signal is not that this exact model should be extended unchanged; it is that compact local attention appears compatible with the ABI temporal tensor and may align thin-line continuity with overlap better than several convolutional temporal-line modules. A future candidate should make a more controlled change, such as combining the window-attention backbone with the now-cache-ready five-frame temporal window, or broadening to a spectral/SZA-gated mixture-of-experts if the campaign wants to leave the temporal branch.

## Decision

Do not promote ABI-229, do not request whole-validation diagnostics, and do not request a `late_improving` continuation of this exact 12-epoch three-frame window-attention branch.

For the next research step, prefer one bounded follow-up rather than another small post-decoder tweak: either a five-frame window-attention temporal scout that tests whether ABI-226's wider temporal context and ABI-229's connectivity-positive local attention combine, or a broader non-temporal scout such as spectral/SZA-gated experts if the campaign decides the temporal branch has enough representative evidence for now.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_141659_818da0/candidate/PROPOSAL.md`
- `run_20260910_141659_818da0/candidate/README.md`
- `run_20260910_141659_818da0/candidate/manifest.yaml`
- `run_20260910_141659_818da0/resolved_manifest.yaml`
- `run_20260910_141659_818da0/outputs/model_summary.json`
- `run_20260910_141659_818da0/outputs/best_metrics.json`
- `run_20260910_141659_818da0/outputs/final_metrics.json`
- `run_20260910_141659_818da0/outputs/metrics.jsonl`
- `run_20260910_141659_818da0/outputs/resource_profile.json`
- `run_20260910_141659_818da0/outputs/validation_postprocessing/index.json`
- `run_20260910_141659_818da0/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_120441_916a03` for ABI-226 five-frame comparison context
- `run_20260910_124920_f1b455` for ABI-227 temporal-line consistency context
- `run_20260910_133212_0380e1` for ABI-228 rotation-aware line-accumulation context
- `run_20260908_150315_9aea3f` for ABI-222 same-budget temporal-attention context
- `run_20260908_123030_05ad37` for ABI-218 matched temporal-eligible single-frame control
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
