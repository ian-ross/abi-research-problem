# ABI-237 dual-head agreement ASPP scout

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-237, Candidate `abi237_fullspectral_btd_sza_dual_head_agreement_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260910_234350_c70d56`.

ABI-237 was a single-frame calibration/agreement scout after recent Radon and MoE work. It used provider-owned `abi_16ch_plus_sza` input, ABI-channel-derived BTD/Solar Geometry Input features, a signed-detail ASPP U-Net scaffold, and two internal recall/precision feature branches fused by a learned agreement gate. It emitted the required single `mask_logits` output plus trusted Line and Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-237 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,093,629, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 8.86 / 10.66 GiB.
- Training wall time: 1,597.6 s; validation wall time: 1,362.2 s; total Run wall time: 2,961.8 s.

This is successful finite/resource evidence for the dual-head agreement branch, with resource behavior similar to the recent Radon ASPP variants and still appropriate for sequential use.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 10. The final epoch 12 regressed slightly, so checkpoint selection matters.

| Metric | ABI-237 best epoch 10 | ABI-237 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.376006 | 0.367194 |
| Raw Dice | 0.388371 | 0.379908 |
| Filtered IoU | 0.231532 | 0.224885 |
| Filtered precision | 0.404292 | 0.362268 |
| Filtered recall | 0.351419 | 0.372256 |
| Filtered contrail connectivity | 0.344898 | 0.243594 |
| Filtered predicted-positive fraction | 0.003150 | 0.003724 |
| Raw predicted-positive fraction | 0.003397 | 0.003971 |
| MIT filtered Dice | 0.361753 | 0.355949 |
| Google filtered Dice | 0.411253 | 0.393744 |
| MIT filtered recall | 0.323063 | 0.340169 |
| Google filtered recall | 0.434351 | 0.466096 |
| Train loss | 0.858512 | 0.853080 |
| Validation loss | 0.887644 | 0.889152 |

The selected checkpoint is finite, noncollapsed, and source-informative. It is not an all-negative or all-positive degenerate solution, but its primary score is below the recent scout neighborhood that motivated the branch.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.184919 | 0.133239 | 0.302094 | 0.212434 | 0.144569 | 0.085321 | 0.008216 |
| 2 | 0.273372 | 0.275816 | 0.270971 | 0.274568 | 0.270749 | 0.175091 | 0.003560 |
| 3 | 0.278016 | 0.242153 | 0.326347 | 0.288068 | 0.259211 | 0.149165 | 0.004884 |
| 4 | 0.262184 | 0.196451 | 0.394025 | 0.288529 | 0.218450 | 0.139331 | 0.007268 |
| 5 | 0.349030 | 0.348925 | 0.349135 | 0.344185 | 0.360451 | 0.246336 | 0.003626 |
| 6 | 0.353043 | 0.347113 | 0.359179 | 0.343593 | 0.375392 | 0.238546 | 0.003750 |
| 7 | 0.364106 | 0.384905 | 0.345440 | 0.355477 | 0.384535 | 0.318957 | 0.003252 |
| 8 | 0.346388 | 0.335982 | 0.357458 | 0.339127 | 0.361555 | 0.238060 | 0.003855 |
| 9 | 0.370569 | 0.443390 | 0.318294 | 0.347552 | 0.430678 | 0.424339 | 0.002601 |
| 10 | 0.376006 | 0.404292 | 0.351419 | 0.361753 | 0.411253 | 0.344898 | 0.003150 |
| 11 | 0.366000 | 0.349928 | 0.383620 | 0.358706 | 0.382753 | 0.241204 | 0.003973 |
| 12 | 0.367194 | 0.362268 | 0.372256 | 0.355949 | 0.393744 | 0.243594 | 0.003724 |

The trajectory improves rapidly through epoch 7 and reaches its selected primary checkpoint at epoch 10. Epoch 9 is diagnostically interesting because it has the best Google Dice, precision, and connectivity, but it is low-recall and compact-positive. Epochs 11-12 shift toward higher recall and positive area while losing precision, Google overlap, and especially connectivity. The branch is oscillatory rather than late-upward at the exploratory ceiling.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-232 MoE late36 | ABI-235 Radon late36 | ABI-236 recall-bypass Radon | ABI-237 agreement scout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 32 | 36 | 12 | 10 |
| Filtered Dice | 0.427570 | 0.419776 | 0.400942 | 0.407900 | 0.384218 | 0.376006 |
| Raw Dice | 0.442746 | 0.438487 | 0.414940 | 0.423244 | 0.399448 | 0.388371 |
| Filtered precision | 0.439467 | 0.483764 | 0.405218 | 0.432065 | 0.450097 | 0.404292 |
| Filtered recall | 0.416301 | 0.370738 | 0.396756 | 0.386295 | 0.335162 | 0.351419 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.383636 | 0.343190 | 0.356652 | 0.344898 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.386542 | 0.393464 | 0.374075 | 0.361753 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.439983 | 0.443533 | 0.411495 | 0.411253 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.003548 | 0.003240 | 0.002698 | 0.003150 |

Relative to ABI-236, ABI-237 is lower on filtered Dice (-0.008212), raw Dice (-0.011077), precision (-0.045805), connectivity (-0.011754), MIT Dice (-0.012322), and essentially tied on Google Dice (-0.000242), while improving recall by +0.016257 and predicted-positive fraction by +0.000452. Relative to ABI-235, ABI-237 gives up -0.031894 filtered Dice and -0.034876 recall. Relative to ABI-232, it gives up -0.024936 filtered Dice, -0.045337 recall, and -0.038738 connectivity. It is well below ABI-202 and ABI-223 on the primary capped metric.

## Interpretation

Classify ABI-237 as a finite but negative-to-mixed agreement/calibration scout. The internal dual-head fusion did not cause collapse, and the branch can trade between compact high-precision/high-connectivity checkpoints and higher-recall checkpoints. However, it did not produce a superior precision/recall balance: the selected checkpoint trails ABI-236 despite a higher recall, and the late epochs show recall recovery coupled to precision and connectivity loss.

The result does not eliminate all calibration/agreement architectures, but it weakens this exact fused feature-gate formulation. The most promising signal is the epoch-9 connectivity/Google/precision spike, not the selected epoch-10 primary score. That signal suggests agreement features can identify coherent line evidence, but this implementation suppresses too much recall or loses continuity when recall expands.

## Decision

Do not promote ABI-237 and do not request whole-validation diagnostics. Do not request a late-improving continuation for this exact branch because the best checkpoint occurred at epoch 10 and the last two epochs were mixed/regressive rather than clearly budget-truncated.

Do not classify matched calibration/uncertainty ideas as exhausted. If revisited, the next hypothesis should be materially different, such as a dual-logit consensus head that preserves a recall path more explicitly, or it should be combined with a stronger parent architecture rather than used as a standalone ASPP scout. For the next autonomous step, prefer broadening toward a modern lightweight backbone or a temporal/Radon hybrid rather than another local agreement-gate tweak.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_234350_c70d56/candidate/PROPOSAL.md`
- `run_20260910_234350_c70d56/candidate/README.md`
- `run_20260910_234350_c70d56/candidate/manifest.yaml`
- `run_20260910_234350_c70d56/resolved_manifest.yaml`
- `run_20260910_234350_c70d56/outputs/model_summary.json`
- `run_20260910_234350_c70d56/outputs/best_metrics.json`
- `run_20260910_234350_c70d56/outputs/final_metrics.json`
- `run_20260910_234350_c70d56/outputs/metrics.jsonl`
- `run_20260910_234350_c70d56/outputs/resource_profile.json`
- `run_20260910_234350_c70d56/outputs/validation_postprocessing/index.json`
- `run_20260910_234350_c70d56/outputs/prediction_samples/samples.json`
- `run_20260910_223916_575307` for ABI-236 recall-bypass Radon context
- `run_20260910_195407_469d7c` for ABI-235 Radon late36 context
- `run_20260910_163616_4f7416` for ABI-232 spectral-regime MoE late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
