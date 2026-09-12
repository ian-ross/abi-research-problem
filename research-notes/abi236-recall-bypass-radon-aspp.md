# ABI-236 recall-bypass Radon ASPP decoder

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-236, Candidate `abi236_fullspectral_btd_sza_recall_bypass_radon_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260910_223916_575307`.

ABI-236 was a controlled Radon-family continuation after ABI-235. It kept the provider-owned `abi_16ch_plus_sza` input, ABI-channel-derived BTD/Solar Geometry Input front end, signed-detail ASPP U-Net scaffold, full-scale skip fusion, trusted BCE-Dice loss, and Line/Centerline auxiliary outputs. The architectural change weakened the long-range differentiable Radon residual and added a learned high-resolution detail bypass so faint local contrail evidence could survive alongside line-integral support. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-236 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,127,473, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 9.38 / 11.03 GiB.
- Training wall time: 1,729.3 s; validation wall time: 1,452.0 s; total Run wall time: 3,183.4 s.

This is successful finite/resource evidence for the recall-bypass Radon variant, with resource behavior similar to ABI-234/235 and safe only as a sequential architecture-profiled branch.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final epoch 12.

| Metric | ABI-236 best/final epoch 12 |
| --- | ---: |
| Filtered Dice | 0.384218 |
| Raw Dice | 0.399448 |
| Filtered IoU | 0.237791 |
| Filtered precision | 0.450097 |
| Filtered recall | 0.335162 |
| Filtered contrail connectivity | 0.356652 |
| Filtered predicted-positive fraction | 0.002698 |
| Raw predicted-positive fraction | 0.002890 |
| MIT filtered Dice | 0.374075 |
| Google filtered Dice | 0.411495 |
| MIT filtered recall | 0.319192 |
| Google filtered recall | 0.381868 |
| Train loss | 0.852136 |
| Validation loss | 0.889163 |

The selected checkpoint is finite, noncollapsed, and source-informative. It is compact-positive and precision-heavy, but the intended recall-preserving connectivity recovery was only partially expressed.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.203312 | 0.151335 | 0.309671 | 0.228904 | 0.162149 | 0.109955 | 0.007415 |
| 2 | 0.227201 | 0.185471 | 0.293160 | 0.254390 | 0.184725 | 0.142627 | 0.005728 |
| 3 | 0.279621 | 0.244355 | 0.326783 | 0.295724 | 0.249237 | 0.140380 | 0.004846 |
| 4 | 0.332570 | 0.347811 | 0.318608 | 0.330383 | 0.337823 | 0.243275 | 0.003319 |
| 5 | 0.306402 | 0.277561 | 0.341933 | 0.320358 | 0.280435 | 0.217300 | 0.004464 |
| 6 | 0.348775 | 0.350849 | 0.346725 | 0.349078 | 0.348130 | 0.190202 | 0.003581 |
| 7 | 0.272718 | 0.215912 | 0.370086 | 0.298730 | 0.227350 | 0.129923 | 0.006211 |
| 8 | 0.306020 | 0.273124 | 0.347926 | 0.320830 | 0.279068 | 0.138178 | 0.004616 |
| 9 | 0.374584 | 0.393117 | 0.357719 | 0.367057 | 0.392527 | 0.236345 | 0.003297 |
| 10 | 0.350535 | 0.435926 | 0.293117 | 0.334137 | 0.387476 | 0.273690 | 0.002437 |
| 11 | 0.371003 | 0.349094 | 0.395845 | 0.366819 | 0.380780 | 0.211720 | 0.004109 |
| 12 | 0.384218 | 0.450097 | 0.335162 | 0.374075 | 0.411495 | 0.356652 | 0.002698 |

The trajectory is noisy but not collapsed. Epoch 12 is the best aggregate filtered Dice, best MIT filtered Dice, best connectivity, and best precision; epoch 11 briefly achieved the best recall. The final-epoch selection means the exploratory budget may still truncate this variant, but the family-level tradeoff is weaker than ABI-235's late36 behavior.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-234 Radon scout | ABI-235 Radon late36 | ABI-236 recall-bypass Radon |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 12 | 36 | 12 |
| Filtered Dice | 0.427570 | 0.419776 | 0.381342 | 0.407900 | 0.384218 |
| Raw Dice | 0.442746 | 0.438487 | 0.396685 | 0.423244 | 0.399448 |
| Filtered precision | 0.439467 | 0.483764 | 0.451640 | 0.432065 | 0.450097 |
| Filtered recall | 0.416301 | 0.370738 | 0.329981 | 0.386295 | 0.335162 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.386193 | 0.343190 | 0.356652 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.363530 | 0.393464 | 0.374075 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.425620 | 0.443533 | 0.411495 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.002648 | 0.003240 | 0.002698 |

Relative to ABI-234, ABI-236 improves filtered Dice by +0.002876, raw Dice by +0.002763, filtered recall by +0.005181, MIT filtered Dice by +0.010545, and filtered positive fraction by +0.000051, while losing connectivity by -0.029541, precision by -0.001543, and Google filtered Dice by -0.014125. This is a small overlap/recall gain rather than the intended connectivity recovery.

Relative to ABI-235, ABI-236 is lower on filtered Dice (-0.023681), raw Dice (-0.023796), filtered recall (-0.051133), MIT filtered Dice (-0.019389), Google filtered Dice (-0.032038), and filtered positive fraction (-0.000541). It recovers only a small amount of selected-checkpoint connectivity (+0.013462) and precision (+0.018033). It remains well below ABI-202 and ABI-223 on aggregate filtered Dice and source-stratified frontier metrics.

## Interpretation

Classify ABI-236 as a finite but mixed-to-negative Radon-family continuation. The high-resolution detail bypass did not catastrophically destabilize training and produced a final-epoch best checkpoint, but it did not solve the ABI-235 question. It recovered only a small amount of connectivity versus the late36 Radon parent while giving up substantially more recall and overlap; compared with the original ABI-234 scout, it modestly improves Dice/MIT/recall but loses the connectivity signature that made the Radon branch distinctive.

The result does not eliminate differentiable Radon/Hough-style support as a family, because ABI-235 remains a positive late-budget family-development result. It does weaken the specific weaker-residual plus local-detail-bypass hypothesis. Further small Radon gate or bypass tweaks are unlikely to be the best next use of capped runs unless tied to a materially different calibration/agreement or temporal motion hypothesis.

## Decision

Do not promote ABI-236 and do not request whole-validation diagnostics from this capped Result. Do not request a late-improving continuation for this exact recall-bypass variant despite its final-epoch selection, because the controlled architectural change failed its intended tradeoff against ABI-235 and only marginally improved ABI-234.

Treat ABI-235 as the stronger Radon-family reference. The next useful step should broaden rather than continue local Radon gate tuning: prefer a modern lightweight backbone, a calibration/agreement architecture, or a materially different temporal/Radon hybrid if it remains fully in contract and consumes only provider-advertised tensors. If the campaign revisits Radon, use ABI-235 as the parent comparison and require a clearer one-factor mechanism for preserving late36 recall while improving line continuity.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_223916_575307/candidate/PROPOSAL.md`
- `run_20260910_223916_575307/candidate/README.md`
- `run_20260910_223916_575307/candidate/manifest.yaml`
- `run_20260910_223916_575307/resolved_manifest.yaml`
- `run_20260910_223916_575307/outputs/model_summary.json`
- `run_20260910_223916_575307/outputs/best_metrics.json`
- `run_20260910_223916_575307/outputs/final_metrics.json`
- `run_20260910_223916_575307/outputs/metrics.jsonl`
- `run_20260910_223916_575307/outputs/resource_profile.json`
- `run_20260910_223916_575307/outputs/validation_postprocessing/index.json`
- `run_20260910_223916_575307/outputs/prediction_samples/samples.json`
- `run_20260910_185443_f88be8` for ABI-234 Radon scout context
- `run_20260910_195407_469d7c` for ABI-235 Radon late36 parent context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
