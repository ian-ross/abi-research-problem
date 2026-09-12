# ABI-228 temporal center-anchored rotation-aware line accumulation U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-228, Candidate `abi228_temporal_centeranchored_rotation_lineaccum_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260910_133212_0380e1`.

ABI-228 was a temporal/line family scout after ABI-223, ABI-226, and ABI-227. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. The hypothesis was that center-anchored temporal residual support plus differentiable multi-orientation line accumulation would align thin-line continuity with filtered Dice better than ABI-227's temporal-line consistency gate. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-228 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,130,112, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.58 / 3.84 GB.
- Training wall time: 1,071.7 s; validation wall time: 1,047.8 s; total Run wall time: 2,121.2 s.

This is successful finite/resource evidence for the center-anchored rotation-aware line-accumulation formulation, but it is not a primary-metric improvement over the prior temporal scouts.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8.

| Metric | ABI-228 best epoch 8 |
| --- | ---: |
| Filtered Dice | 0.368554 |
| Raw Dice | 0.383662 |
| Filtered IoU | 0.225906 |
| Filtered precision | 0.381951 |
| Filtered recall | 0.356064 |
| Filtered contrail connectivity | 0.202312 |
| Filtered predicted-positive fraction | 0.004819 |
| Raw predicted-positive fraction | 0.005195 |
| MIT filtered Dice | 0.358973 |
| Google filtered Dice | 0.391801 |
| MIT filtered recall | 0.328148 |
| Google filtered recall | 0.439119 |
| Train loss | 0.822319 |
| Validation loss | 0.864079 |

The Result is finite, noncollapsed, and source-informative. It is still below the same-budget temporal-attention and five-frame scouts on filtered Dice, and the line-accumulation mechanism did not produce a connectivity advantage.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218017 | 0.229145 | 0.297999 | 0.171884 | 0.211826 | 0.232296 | 0.183603 | 0.002982 |
| 2 | 0.240827 | 0.251222 | 0.265785 | 0.220154 | 0.237060 | 0.248854 | 0.131890 | 0.004282 |
| 3 | 0.290873 | 0.305467 | 0.450538 | 0.214763 | 0.270955 | 0.342158 | 0.290884 | 0.002464 |
| 4 | 0.314533 | 0.329657 | 0.418717 | 0.251865 | 0.301377 | 0.347786 | 0.252394 | 0.003110 |
| 5 | 0.339243 | 0.353957 | 0.396911 | 0.296206 | 0.318596 | 0.389802 | 0.230567 | 0.003858 |
| 6 | 0.281040 | 0.296056 | 0.416657 | 0.212027 | 0.265639 | 0.319735 | 0.173563 | 0.002631 |
| 7 | 0.310211 | 0.325852 | 0.449031 | 0.236955 | 0.291493 | 0.358226 | 0.254614 | 0.002728 |
| 8 | 0.368554 | 0.383662 | 0.381951 | 0.356064 | 0.358973 | 0.391801 | 0.202312 | 0.004819 |
| 9 | 0.364469 | 0.378615 | 0.349109 | 0.381243 | 0.352560 | 0.391956 | 0.196836 | 0.005645 |
| 10 | 0.366779 | 0.381803 | 0.387440 | 0.348209 | 0.350066 | 0.406943 | 0.220767 | 0.004646 |
| 11 | 0.364499 | 0.381039 | 0.429139 | 0.316783 | 0.347881 | 0.404902 | 0.212342 | 0.003816 |
| 12 | 0.345295 | 0.360913 | 0.397036 | 0.305485 | 0.327480 | 0.389218 | 0.233111 | 0.003978 |

The trajectory improved materially through epoch 8 and stayed near the same primary-metric band through epochs 9-11, but final filtered Dice regressed. The best checkpoint is not late enough to justify a late-improving continuation, and the final checkpoint's modest connectivity increase does not recover primary Dice.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-222 attention 12ep | ABI-223 attention late36 | ABI-226 five-frame scout | ABI-227 line-consistency | ABI-228 rotation line-accum |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 36 | 10 | 9 | 8 |
| Filtered Dice | 0.345570 | 0.374329 | 0.419776 | 0.378604 | 0.370657 | 0.368554 |
| Raw Dice | 0.361077 | 0.392066 | 0.438487 | 0.394881 | 0.383841 | 0.383662 |
| Filtered precision | 0.407234 | 0.466148 | 0.483764 | 0.428061 | 0.341621 | 0.381951 |
| Filtered recall | 0.300125 | 0.312729 | 0.370738 | 0.339391 | 0.405088 | 0.356064 |
| Filtered connectivity | 0.231399 | 0.281396 | 0.412427 | 0.224851 | 0.190346 | 0.202312 |
| MIT filtered Dice | 0.330415 | 0.357658 | 0.398498 | 0.366586 | 0.360838 | 0.358973 |
| Google filtered Dice | 0.385184 | 0.416510 | 0.476764 | 0.409886 | 0.394514 | 0.391801 |
| Filtered predicted-positive fraction | 0.003810 | 0.003468 | 0.003962 | 0.004099 | 0.006130 | 0.004819 |
| Parameter count | 3,050,475 | 3,095,836 | 3,095,836 | 3,098,332 | 3,133,588 | 3,130,112 |

ABI-228 improves over the matched single-frame control ABI-218 by +0.022984 filtered Dice and +0.055939 recall, so the temporal branch remains useful relative to no temporal input. However, it trails the same-budget ABI-222 attention scout by -0.005775 filtered Dice, -0.084197 precision, -0.079084 connectivity, and -0.024709 Google filtered Dice, with recall as the only substantial positive delta. It also trails ABI-226 by -0.010050 filtered Dice and ABI-227 by -0.002104 filtered Dice.

The intended line-continuity effect is not visible at the selected checkpoint: ABI-228 connectivity is below ABI-222, ABI-226, and far below ABI-227's final-epoch connectivity of 0.378301. ABI-228's best epoch is a balanced recall/precision checkpoint, not a line-continuity breakthrough.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result, with whole-validation filtered Dice 0.4312. ABI-223 remains the capped temporal-family frontier, with filtered Dice 0.419776 at epoch 36 and strong MIT/Google source behavior. ABI-228 is useful as a completed temporal/rotation-aware line-accumulation scout, but it is not a promotion candidate and does not justify whole-validation diagnostics.

## Interpretation

Classify ABI-228 as a finite but negative temporal/rotation-aware line-accumulation scout. The center-anchored stem and differentiable orientation accumulator are resource-safe and nondegenerate, but the exact formulation does not beat the temporal-attention baselines on filtered Dice and does not deliver the hypothesized connectivity gain. The final decline and best epoch at 8 argue against spending the approved late-improving budget on this exact branch.

The result does not disprove all rotation-aware or differentiable Hough/Radon-style ideas. It specifically weakens this compact per-pixel orientation-mixture accumulator when paired with the current ABI-223-like temporal U-Net stem. A future line-voting attempt would need a more materially different mechanism, such as explicit long-range differentiable voting/strip aggregation, or should broaden away from temporal-line modules toward another underexplored family.

## Decision

Do not promote ABI-228, do not request whole-validation diagnostics, and do not request a `late_improving` continuation of this exact center-anchored rotation-aware line-accumulation branch.

For the next research step, prefer broadening rather than another small temporal stem tweak. In-contract options include a compact window-attention/UNetFormer-style temporal scout, spectral/SZA-gated mixture-of-experts, or a more explicit differentiable Hough/Radon-style long-line voting module that is materially different from ABI-228's local orientation mixture.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_133212_0380e1/candidate/PROPOSAL.md`
- `run_20260910_133212_0380e1/candidate/README.md`
- `run_20260910_133212_0380e1/candidate/manifest.yaml`
- `run_20260910_133212_0380e1/resolved_manifest.yaml`
- `run_20260910_133212_0380e1/outputs/model_summary.json`
- `run_20260910_133212_0380e1/outputs/best_metrics.json`
- `run_20260910_133212_0380e1/outputs/final_metrics.json`
- `run_20260910_133212_0380e1/outputs/metrics.jsonl`
- `run_20260910_133212_0380e1/outputs/resource_profile.json`
- `run_20260910_133212_0380e1/outputs/validation_postprocessing/index.json`
- `run_20260910_133212_0380e1/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_124920_f1b455` for ABI-227 temporal-line consistency context
- `run_20260910_120441_916a03` for ABI-226 five-frame comparison context
- `run_20260908_150315_9aea3f` for ABI-222 same-budget temporal-attention context
- `run_20260908_123030_05ad37` for ABI-218 matched temporal-eligible single-frame control
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
