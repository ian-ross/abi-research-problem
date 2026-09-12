# ABI-231 spectral-regime MoE U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-231, Candidate `abi231_fullspectral_btd_sza_spectral_regime_moe_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260910_155936_362435`.

ABI-231 was a single-frame spectral/Solar Geometry Input mixture-of-experts family scout after the recent temporal-window-attention branch. It consumed provider-owned `abi_16ch_plus_sza` tensors and used approved-channel ABI bands, candidate-derived BTD planes, Solar Geometry Input features, and learned soft gates over three compact convolutional experts before a GroupNorm U-Net/ASPP decoder with trusted Line and Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-231 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 2,300,013, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.49 / 5.41 GB.
- Training wall time: 611.4 s; validation wall time: 1,124.3 s; total Run wall time: 1,737.2 s.

This is successful finite/resource evidence for the spectral/SZA-regime MoE family.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 12, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-231 best epoch 12 |
| --- | ---: |
| Filtered Dice | 0.371985 |
| Raw Dice | 0.386649 |
| Filtered IoU | 0.228490 |
| Filtered precision | 0.432192 |
| Filtered recall | 0.326502 |
| Filtered contrail connectivity | 0.398515 |
| Filtered predicted-positive fraction | 0.002738 |
| Raw predicted-positive fraction | 0.002923 |
| MIT filtered Dice | 0.355799 |
| Google filtered Dice | 0.413787 |
| MIT filtered recall | 0.302099 |
| Google filtered recall | 0.397870 |
| Train loss | 0.862900 |
| Validation loss | 0.891715 |

The Result is finite, noncollapsed, and source-informative. Its aggregate overlap trails the ABI-202 whole-validation-tested frontier and the ABI-223 late36 temporal frontier, but its selected connectivity is unusually strong for a 12-epoch scout and its final/best epoch suggests the branch may still be budget-limited.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.224286 | 0.174721 | 0.313110 | 0.243488 | 0.188694 | 0.136555 | 0.006494 |
| 2 | 0.269663 | 0.315294 | 0.235569 | 0.268864 | 0.271564 | 0.213506 | 0.002707 |
| 3 | 0.264729 | 0.206907 | 0.367403 | 0.290586 | 0.218813 | 0.129127 | 0.006435 |
| 4 | 0.323172 | 0.317244 | 0.329327 | 0.318675 | 0.333738 | 0.208349 | 0.003762 |
| 5 | 0.323805 | 0.312824 | 0.335585 | 0.320579 | 0.330649 | 0.250789 | 0.003887 |
| 6 | 0.329698 | 0.356379 | 0.306734 | 0.315959 | 0.361304 | 0.294115 | 0.003119 |
| 7 | 0.359727 | 0.345510 | 0.375165 | 0.353374 | 0.374135 | 0.272009 | 0.003935 |
| 8 | 0.351487 | 0.436347 | 0.294260 | 0.328954 | 0.408187 | 0.407230 | 0.002444 |
| 9 | 0.370341 | 0.421863 | 0.330034 | 0.350732 | 0.421794 | 0.349384 | 0.002835 |
| 10 | 0.371263 | 0.418841 | 0.333392 | 0.355689 | 0.408637 | 0.318747 | 0.002884 |
| 11 | 0.362674 | 0.377348 | 0.349098 | 0.353764 | 0.385161 | 0.275175 | 0.003352 |
| 12 | 0.371985 | 0.432192 | 0.326502 | 0.355799 | 0.413787 | 0.398515 | 0.002738 |

The trajectory improves substantially through epoch 7, becomes oscillatory, and selects its best aggregate checkpoint at the final epoch. Epoch 8 and epoch 12 both show high precision/connectivity at low predicted-positive fraction, while epoch 11 temporarily trades precision/connectivity for recall. This is not a clear plateau or collapse.

## Comparison context

| Metric | ABI-202 frontier | ABI-222 temporal 12ep | ABI-223 temporal late36 | ABI-226 five-frame | ABI-229 window attention | ABI-230 five-frame window | ABI-231 spectral MoE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 12 | 36 | 10 | 8 | 8 | 12 |
| Filtered Dice | 0.427570 | 0.374329 | 0.419776 | 0.378604 | 0.376958 | 0.358285 | 0.371985 |
| Raw Dice | 0.442746 | 0.392066 | 0.438487 | 0.394881 | 0.393997 | 0.374020 | 0.386649 |
| Filtered precision | 0.439467 | 0.466148 | 0.483764 | 0.428061 | 0.434428 | 0.399750 | 0.432192 |
| Filtered recall | 0.416301 | 0.312729 | 0.370738 | 0.339391 | 0.332917 | 0.324614 | 0.326502 |
| Filtered connectivity | 0.457773 | 0.281396 | 0.412427 | 0.224851 | 0.313635 | 0.225921 | 0.398515 |
| MIT filtered Dice | 0.411992 | 0.357658 | 0.398498 | 0.366586 | 0.364086 | 0.349067 | 0.355799 |
| Google filtered Dice | 0.468151 | 0.416510 | 0.476764 | 0.409886 | 0.410445 | 0.381970 | 0.413787 |
| Filtered predicted-positive fraction | 0.003433 | 0.003468 | 0.003962 | 0.004099 | 0.003962 | 0.004198 | 0.002738 |

Relative to ABI-222, ABI-231 is nearly tied on same-budget aggregate filtered Dice (-0.002344) and has much stronger connectivity (+0.117119), but lower precision, recall, MIT Dice, and Google Dice. Relative to ABI-229, it is lower on filtered Dice (-0.004973) and source Dice, but higher on connectivity (+0.084880) with a lower predicted-positive fraction. Relative to ABI-230, it is stronger on aggregate Dice (+0.013700), precision, connectivity (+0.172594), source Dice, and positive-fraction compactness.

Relative to ABI-202, ABI-231 remains far behind on capped filtered Dice (-0.055585), recall (-0.089799), MIT Dice (-0.056193), Google Dice (-0.054364), and connectivity (-0.059259). It is therefore not a promotion candidate and does not warrant whole-validation diagnostics. Relative to ABI-223, it trails filtered Dice by -0.047791 but comes much closer on connectivity (-0.013912), which is the main family-specific positive signal.

## Interpretation

Classify ABI-231 as a completed, finite, modestly positive spectral/SZA-regime MoE scout. It does not beat the mature single-frame frontier or the late36 temporal frontier, but it is competitive with several recent 12-epoch scouts and produces a distinctive high-connectivity/low-positive-fraction profile without temporal input. The result is source-informative rather than collapsed: Google filtered Dice is above 0.41, MIT filtered Dice is above 0.35, and both Dataset Sources retain nonzero recall.

The main weakness is insufficient recall and MIT overlap. The MoE gate appears to make conservative, connected predictions rather than broadening coverage. Because the best checkpoint lands at epoch 12 and the late trajectory is oscillatory but not exhausted, low score alone is not enough to abandon this first MoE family scout.

## Decision

Do not promote ABI-231 and do not request whole-validation diagnostics from this capped result.

Do not classify the spectral/SZA-regime MoE family as exhausted. A reasonable next step is a close family-development continuation that preserves the ABI-231 MoE idea but uses the approved `late_improving` budget, because ABI-231 is finite, noncollapsed, source-informative, and selected its best checkpoint at the exploratory epoch ceiling. If continued, the follow-up should stay architecture-only and target recall/MIT recovery without adding candidate-owned thresholding, postprocessing, sampling, losses, or data access.

If the campaign instead broadens again, prefer a materially different differentiable Hough/Radon-style line-voting scout, using ABI-231's high-connectivity behavior as comparison context.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_155936_362435/candidate/PROPOSAL.md`
- `run_20260910_155936_362435/candidate/README.md`
- `run_20260910_155936_362435/candidate/manifest.yaml`
- `run_20260910_155936_362435/resolved_manifest.yaml`
- `run_20260910_155936_362435/outputs/model_summary.json`
- `run_20260910_155936_362435/outputs/best_metrics.json`
- `run_20260910_155936_362435/outputs/final_metrics.json`
- `run_20260910_155936_362435/outputs/metrics.jsonl`
- `run_20260910_155936_362435/outputs/resource_profile.json`
- `run_20260910_155936_362435/outputs/validation_postprocessing/index.json`
- `run_20260910_155936_362435/outputs/prediction_samples/samples.json`
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_120441_916a03` for ABI-226 five-frame temporal comparison context
- `run_20260910_141659_818da0` for ABI-229 three-frame window-attention comparison context
- `run_20260910_150603_7065ec` for ABI-230 five-frame window-attention comparison context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
