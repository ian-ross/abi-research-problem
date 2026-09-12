# ABI-235 long-range Radon ASPP late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-235, Candidate `abi235_fullspectral_btd_sza_longrange_radon_aspp_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260910_195407_469d7c`.

ABI-235 was a close family-development continuation of ABI-234. It kept the same single-frame full-spectral BTD+Solar Geometry Input signed-detail ASPP U-Net scaffold and differentiable low-resolution Radon-style long-line accumulation branch, and requested the approved `late_improving` budget because ABI-234 selected its best checkpoint at epoch 12. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-235 completed the approved 36-epoch late-improving budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget requested/effective: `late_improving`; request approved from parent Run `run_20260910_185443_f88be8`.
- Training policy: 36 effective epochs, constant learning rate, disabled early stopping, best checkpoint selected by `val/filtered_dice`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,094,749, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 9.32 / 11.09 GiB.
- Training wall time: 4,959.6 s; validation wall time: 4,217.8 s; total Run wall time: 9,179.8 s.

This is successful finite/resource evidence for late training of the Radon-style line-accumulation branch, though the runtime is high enough that further variants should stay sequential.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final epoch 36.

| Metric | ABI-235 best/final epoch 36 |
| --- | ---: |
| Filtered Dice | 0.407900 |
| Raw Dice | 0.423244 |
| Filtered IoU | 0.256202 |
| Filtered precision | 0.432065 |
| Filtered recall | 0.386295 |
| Filtered contrail connectivity | 0.343190 |
| Filtered predicted-positive fraction | 0.003240 |
| Raw predicted-positive fraction | 0.003457 |
| MIT filtered Dice | 0.393464 |
| Google filtered Dice | 0.443533 |
| MIT filtered recall | 0.355863 |
| Google filtered recall | 0.475296 |
| Train loss | 0.811716 |
| Validation loss | 0.876115 |

The selected checkpoint is finite, noncollapsed, and source-informative. Relative to ABI-234, the late budget primarily improved recall and source-stratified overlap while giving up some precision and selected-checkpoint connectivity.

## Learning trajectory

Selected trajectory points:

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.178142 | 0.133098 | 0.269269 | 0.203811 | 0.139994 | 0.100687 | 0.007331 |
| 5 | 0.346232 | 0.408804 | 0.300272 | 0.332323 | 0.378968 | 0.341637 | 0.002662 |
| 12 | 0.391342 | 0.459758 | 0.340650 | 0.376618 | 0.429082 | 0.386610 | 0.002685 |
| 15 | 0.393904 | 0.385641 | 0.402529 | 0.390531 | 0.401936 | 0.312433 | 0.003782 |
| 21 | 0.384983 | 0.323742 | 0.474799 | 0.381527 | 0.393913 | 0.231895 | 0.005314 |
| 22 | 0.396405 | 0.406914 | 0.386424 | 0.391002 | 0.410088 | 0.326192 | 0.003441 |
| 25 | 0.406246 | 0.452544 | 0.368542 | 0.391485 | 0.443495 | 0.399102 | 0.002951 |
| 31 | 0.397137 | 0.477155 | 0.340103 | 0.379106 | 0.441909 | 0.371814 | 0.002583 |
| 36 | 0.407900 | 0.432065 | 0.386295 | 0.393464 | 0.443533 | 0.343190 | 0.003240 |

The trajectory is noisy but productive under the longer budget. It reached new local highs after epoch 12 and selected the final epoch 36, so the exploratory budget had been truncating this branch. The late trajectory did not collapse or diverge, but the gains after epoch 25 were small and variable rather than a clean monotonic climb.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-232 MoE late36 | ABI-234 Radon scout | ABI-235 Radon late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 32 | 12 | 36 |
| Filtered Dice | 0.427570 | 0.419776 | 0.400942 | 0.381342 | 0.407900 |
| Raw Dice | 0.442746 | 0.438487 | 0.414940 | 0.396685 | 0.423244 |
| Filtered precision | 0.439467 | 0.483764 | 0.405218 | 0.451640 | 0.432065 |
| Filtered recall | 0.416301 | 0.370738 | 0.396756 | 0.329981 | 0.386295 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.383636 | 0.386193 | 0.343190 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.386542 | 0.363530 | 0.393464 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.439983 | 0.425620 | 0.443533 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.003548 | 0.002648 | 0.003240 |

Relative to ABI-234, ABI-235 improves filtered Dice by +0.026557, raw Dice by +0.026559, filtered recall by +0.056314, MIT filtered Dice by +0.029933, Google filtered Dice by +0.017913, and filtered positive fraction by +0.000592. It loses filtered precision by -0.019576 and connectivity by -0.043003.

Relative to ABI-232, ABI-235 is ahead on aggregate filtered Dice by about +0.00696 and improves Google filtered Dice, but is slightly lower on recall and connectivity. Relative to ABI-223 and ABI-202, ABI-235 still trails aggregate filtered Dice by about -0.01188 and -0.01967 respectively, and it does not match their stronger Google/frontier behavior. This is therefore not a promotion candidate from capped evidence and does not yet justify whole-validation diagnostics solely on rank.

## Interpretation

Classify ABI-235 as a positive late-budget family-development result for the differentiable Radon/Hough-style line-accumulation direction. The approved longer budget materially improved the parent scout and moved this branch into the stronger capped frontier neighborhood. The most important change is not just aggregate Dice: MIT Dice and recall both improved, addressing the parent note's suspected recall suppression.

The remaining weakness is that the late-trained Radon fusion no longer preserves ABI-234's selected-checkpoint connectivity advantage, and it remains below the best single-frame and temporal frontiers. The branch appears to trade some long-line compactness for recall once trained longer. That makes the family useful but not solved: the next meaningful question is whether the architecture can keep the late36 recall gains while restoring stronger line continuity, not whether it can simply train longer again.

## Decision

Do not promote ABI-235 and do not request whole-validation diagnostics from this capped Result alone. Do not classify the Radon/Hough-style family as exhausted.

The exact unchanged ABI-234-to-ABI-235 late36 question is answered positively: longer training helped. A reasonable next step is one controlled Radon-family continuation aimed at recall-preserving connectivity recovery, such as a weaker late Radon residual gate, a center-detail bypass around the line accumulator, or a dual-logit agreement head that lets local detail recover faint segments without moving thresholding or morphology into Candidate code. Because ABI-235 is resource-heavy, submit any such continuation sequentially under the default exploratory budget unless late-improving criteria are again met by its own parent Run. If broadening instead, prefer a modern lightweight backbone or calibration/agreement scout rather than another pure line-voting support tweak.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_195407_469d7c/candidate/PROPOSAL.md`
- `run_20260910_195407_469d7c/candidate/README.md`
- `run_20260910_195407_469d7c/candidate/manifest.yaml`
- `run_20260910_195407_469d7c/candidate/budget_request.yaml`
- `run_20260910_195407_469d7c/resolved_manifest.yaml`
- `run_20260910_195407_469d7c/outputs/model_summary.json`
- `run_20260910_195407_469d7c/outputs/best_metrics.json`
- `run_20260910_195407_469d7c/outputs/final_metrics.json`
- `run_20260910_195407_469d7c/outputs/metrics.jsonl`
- `run_20260910_195407_469d7c/outputs/resource_profile.json`
- `run_20260910_195407_469d7c/outputs/validation_postprocessing/index.json`
- `run_20260910_195407_469d7c/outputs/prediction_samples/samples.json`
- `run_20260910_185443_f88be8` for ABI-234 parent context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_163616_4f7416` for ABI-232 MoE late36 context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
