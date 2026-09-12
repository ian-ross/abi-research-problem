# ABI-234 long-range Radon ASPP decoder

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-234, Candidate `abi234_fullspectral_btd_sza_longrange_radon_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260910_185443_f88be8`.

ABI-234 was a single-frame differentiable long-line accumulation family scout. It consumed provider-owned `abi_16ch_plus_sza` tensors, derived approved-channel BTD features, used a signed-detail ASPP U-Net scaffold, and added a low-resolution differentiable Radon-style bridge over horizontal, vertical, diagonal, anti-diagonal, shallow, and steep oriented support. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-234 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,094,749, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 9.32 / 11.09 GiB.
- Training wall time: 1,656.9 s; validation wall time: 1,395.4 s; total Run wall time: 3,054.6 s.

This is successful finite/resource evidence for the explicit long-range Radon-style support module. It is resource-heavier than the recent temporal and MoE scouts but still safely in contract.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final epoch 12.

| Metric | ABI-234 best/final epoch 12 |
| --- | ---: |
| Filtered Dice | 0.381342 |
| Raw Dice | 0.396685 |
| Filtered IoU | 0.235592 |
| Filtered precision | 0.451640 |
| Filtered recall | 0.329981 |
| Filtered contrail connectivity | 0.386193 |
| Filtered predicted-positive fraction | 0.002648 |
| Raw predicted-positive fraction | 0.002818 |
| MIT filtered Dice | 0.363530 |
| Google filtered Dice | 0.425620 |
| MIT filtered recall | 0.301029 |
| Google filtered recall | 0.414654 |
| Train loss | 0.851480 |
| Validation loss | 0.885987 |

The selected checkpoint is finite, noncollapsed, and source-informative. Its signature is precision/connectivity-heavy with compact predicted-positive area, but recall and MIT overlap lag the stronger frontier branches.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.178460 | 0.127887 | 0.295194 | 0.207161 | 0.136106 | 0.086793 | 0.008364 |
| 2 | 0.240540 | 0.203170 | 0.294758 | 0.259471 | 0.206008 | 0.124449 | 0.005257 |
| 3 | 0.272981 | 0.262729 | 0.284066 | 0.283123 | 0.252639 | 0.179438 | 0.003918 |
| 4 | 0.316266 | 0.272009 | 0.377723 | 0.328614 | 0.291644 | 0.177807 | 0.005032 |
| 5 | 0.335653 | 0.422399 | 0.278465 | 0.317665 | 0.378464 | 0.375288 | 0.002389 |
| 6 | 0.345332 | 0.383941 | 0.313779 | 0.337824 | 0.362724 | 0.259800 | 0.002961 |
| 7 | 0.348358 | 0.325319 | 0.374910 | 0.348803 | 0.347398 | 0.187520 | 0.004176 |
| 8 | 0.352186 | 0.401857 | 0.313443 | 0.341061 | 0.377757 | 0.281775 | 0.002826 |
| 9 | 0.355562 | 0.456082 | 0.291349 | 0.334042 | 0.407551 | 0.354846 | 0.002315 |
| 10 | 0.366300 | 0.420286 | 0.324604 | 0.354802 | 0.392093 | 0.322047 | 0.002799 |
| 11 | 0.361371 | 0.379059 | 0.345259 | 0.356235 | 0.372809 | 0.250878 | 0.003301 |
| 12 | 0.381342 | 0.451640 | 0.329981 | 0.363530 | 0.425620 | 0.386193 | 0.002648 |

The trajectory is broadly improving and selected its best checkpoint at the exploratory epoch ceiling. Epoch 12 is the best aggregate filtered Dice, best Google filtered Dice, best connectivity, and near-best precision. This is the strongest argument for continued bounded development: the branch was not clearly plateaued at 12 epochs.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-228 temporal line-accum | ABI-232 MoE late36 | ABI-233 MoE line-voting | ABI-234 Radon scout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 8 | 32 | 9 | 12 |
| Filtered Dice | 0.427570 | 0.419776 | 0.368554 | 0.400942 | 0.379025 | 0.381342 |
| Raw Dice | 0.442746 | 0.438487 | 0.383662 | 0.414940 | 0.392046 | 0.396685 |
| Filtered precision | 0.439467 | 0.483764 | 0.381951 | 0.405218 | 0.364180 | 0.451640 |
| Filtered recall | 0.416301 | 0.370738 | 0.356064 | 0.396756 | 0.395132 | 0.329981 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.202312 | 0.383636 | 0.291487 | 0.386193 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.358973 | 0.386542 | 0.373808 | 0.363530 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.391801 | 0.439983 | 0.391121 | 0.425620 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.004819 | 0.003548 | 0.003932 | 0.002648 |

Relative to ABI-233, ABI-234 is slightly higher on filtered Dice (+0.002317), raw Dice (+0.004639), precision (+0.087460), connectivity (+0.094706), and Google filtered Dice (+0.034499), but lower on recall (-0.065151) and MIT filtered Dice (-0.010278). Relative to ABI-228, it is a much stronger line-accumulation result on selected-checkpoint connectivity (+0.183881) and filtered Dice (+0.012788), although the data/input setting differs because ABI-228 was temporal-eligible and ABI-234 is single-frame/all-target.

Relative to ABI-232, ABI-234 trails filtered Dice (-0.019600), recall (-0.066775), MIT Dice (-0.023012), and Google Dice (-0.014363), while narrowly improving connectivity (+0.002557) and precision (+0.046422). Relative to the campaign frontiers, ABI-234 remains below ABI-202 and ABI-223 on aggregate filtered Dice, recall, source-stratified Dice, and connectivity. It is therefore not a promotion candidate and does not justify whole-validation diagnostics from this capped Result.

## Interpretation

Classify ABI-234 as a finite, resource-safe, scientifically mixed-to-positive family scout. The exact long-range Radon bridge did not beat the best single-frame or temporal frontiers, but it produced the intended kind of signal better than the recent local line-voting attempts: compact positives, high precision, and selected-checkpoint connectivity comparable to ABI-232 and well above ABI-228/ABI-233.

The main failure mode is recall, especially on MIT. The Radon support appears to regularize predictions toward fewer, more connected positives, but the current fusion likely suppresses faint or fragmented contrails. Because the best checkpoint occurred at epoch 12 with a late jump in filtered Dice, Google Dice, and connectivity, low score alone should not eliminate this new family. The result satisfies the evidence pattern for at least one bounded continuation or late-improving follow-up, provided the next hypothesis directly addresses recall preservation rather than merely adding more line support.

## Decision

Do not promote ABI-234 and do not request whole-validation diagnostics now. Do not classify the differentiable Radon/Hough-style family as exhausted.

A reasonable next step is a close continuation of ABI-234 under the approved `late_improving` budget, because the exploratory Run is finite, noncollapsed, source-informative, and selected its best checkpoint at the final epoch. The continuation should preserve the contract and either (a) rerun the same architecture under the approved longer budget to test whether the late trajectory continues, or (b) make one controlled recall-preserving fusion change, such as reducing the Radon residual gate strength or adding a center-detail bypass, while keeping the same provider-owned input/loss/sampling boundaries. If the campaign instead broadens, prefer a different modern lightweight backbone or calibration/agreement family rather than another local orientation-voting tweak.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_185443_f88be8/candidate/PROPOSAL.md`
- `run_20260910_185443_f88be8/candidate/README.md`
- `run_20260910_185443_f88be8/candidate/manifest.yaml`
- `run_20260910_185443_f88be8/resolved_manifest.yaml`
- `run_20260910_185443_f88be8/outputs/model_summary.json`
- `run_20260910_185443_f88be8/outputs/best_metrics.json`
- `run_20260910_185443_f88be8/outputs/final_metrics.json`
- `run_20260910_185443_f88be8/outputs/metrics.jsonl`
- `run_20260910_185443_f88be8/outputs/resource_profile.json`
- `run_20260910_185443_f88be8/outputs/validation_postprocessing/index.json`
- `run_20260910_185443_f88be8/outputs/prediction_samples/samples.json`
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_133212_0380e1` for ABI-228 temporal line-accumulation context
- `run_20260910_163616_4f7416` for ABI-232 MoE late36 context
- `run_20260910_181015_afea31` for ABI-233 MoE line-voting context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
