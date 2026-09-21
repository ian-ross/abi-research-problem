# ABI-269 compact spectral-regime MoE line U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-269, Candidate `abi269_fullspectral_btd_sza_compact_spectral_moe_line_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260912_121857_19f67d`.

ABI-269 was a close continuation of ABI-268. It reused the same resource-safe compact spectral/Solar Geometry Input mixture-of-experts line U-Net and changed only the Harness-owned budget class, requesting the approved `late_improving` 36-epoch budget because ABI-268 selected its final exploratory epoch and had finite, source-informative, non-collapsed predictions.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` inputs, used trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-269 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,755,175, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.97 / 6.44 GB.
- Training wall time: 2,295.9 s; validation wall time: 3,358.6 s; total Run wall time: 5,656.4 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 34.

This is valid finite capped-validation evidence for the compact spectral-regime MoE line U-Net branch. It is not whole-validation promotion evidence.

## Best-validation metrics

| Metric | ABI-269 best epoch 34 | ABI-268 parent | ABI-232 MoE late36 | ABI-265 axial line-memory late36 | ABI-249 C4 line-context | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.410444 | 0.398540 | 0.400942 | 0.411977 | 0.416400 | 0.427570 |
| Raw Dice | 0.424777 | 0.413801 | 0.414940 | 0.427098 | 0.432320 | 0.442746 |
| Filtered precision | 0.427505 | 0.446572 | 0.405218 | 0.433940 | 0.480886 | 0.439467 |
| Filtered recall | 0.394692 | 0.359837 | 0.396756 | 0.392130 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.318646 | 0.360615 | 0.383636 | 0.433071 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.394541 | 0.386144 | 0.386542 | 0.401437 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.450109 | 0.429981 | 0.439983 | 0.438974 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003346 | 0.002920 | 0.003548 | 0.003275 | 0.002767 | 0.003433 |

ABI-269 improved over ABI-268 by about +0.0119 filtered Dice, +0.0349 recall, +0.0084 MIT filtered Dice, and +0.0201 Google filtered Dice, while reducing precision by about -0.0191 and connectivity by about -0.0420. The late budget therefore converted the ABI-268 final-epoch signal into better aggregate/source Dice and recall, but it did not recover connected-line continuity.

Relative to ABI-232, ABI-269 is stronger on aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, and precision, approximately tied on recall, and weaker on connectivity. Relative to ABI-265, ABI-269 is nearly tied on aggregate filtered Dice and has slightly higher recall and Google Dice, but it loses MIT Dice, precision, and especially connectivity. It remains below ABI-249 and ABI-202 on aggregate filtered Dice and below the main line-continuity comparators on connectivity.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.199212 | 0.219683 | 0.164576 | 0.159824 | 0.264363 | 0.113443 | 0.005994 |
| 2 | 0.274340 | 0.269522 | 0.285361 | 0.309092 | 0.246613 | 0.231980 | 0.002891 |
| 3 | 0.299878 | 0.297886 | 0.304075 | 0.304673 | 0.295231 | 0.184690 | 0.003511 |
| 4 | 0.314259 | 0.321600 | 0.299696 | 0.274027 | 0.368337 | 0.136596 | 0.004871 |
| 5 | 0.340240 | 0.324660 | 0.375375 | 0.356001 | 0.325815 | 0.216589 | 0.003316 |
| 6 | 0.328440 | 0.336568 | 0.312372 | 0.275497 | 0.406572 | 0.148069 | 0.005348 |
| 7 | 0.362259 | 0.347418 | 0.398316 | 0.407291 | 0.326193 | 0.330114 | 0.002902 |
| 8 | 0.375835 | 0.365450 | 0.400302 | 0.416738 | 0.342243 | 0.288808 | 0.002976 |
| 9 | 0.367905 | 0.348335 | 0.415645 | 0.436596 | 0.317891 | 0.301564 | 0.002638 |
| 10 | 0.350755 | 0.327778 | 0.404409 | 0.444708 | 0.289576 | 0.277570 | 0.002360 |
| 11 | 0.386065 | 0.376247 | 0.409616 | 0.401996 | 0.371349 | 0.280330 | 0.003347 |
| 12 | 0.350443 | 0.333395 | 0.394668 | 0.495318 | 0.271138 | 0.324405 | 0.001984 |
| 15 | 0.391755 | 0.382720 | 0.414126 | 0.393349 | 0.390174 | 0.215169 | 0.003594 |
| 18 | 0.388035 | 0.374545 | 0.422193 | 0.469885 | 0.330470 | 0.328926 | 0.002549 |
| 22 | 0.396459 | 0.379268 | 0.439454 | 0.431389 | 0.366762 | 0.258807 | 0.003081 |
| 26 | 0.400548 | 0.383995 | 0.441077 | 0.443859 | 0.364938 | 0.300432 | 0.002979 |
| 28 | 0.402954 | 0.382265 | 0.453439 | 0.446787 | 0.366953 | 0.298861 | 0.002976 |
| 30 | 0.390021 | 0.372526 | 0.434726 | 0.469089 | 0.333764 | 0.438844 | 0.002578 |
| 32 | 0.390804 | 0.386871 | 0.400304 | 0.325085 | 0.489829 | 0.258481 | 0.005460 |
| 33 | 0.400687 | 0.385125 | 0.438702 | 0.413033 | 0.389058 | 0.261630 | 0.003413 |
| 34 | 0.410444 | 0.394541 | 0.450109 | 0.427505 | 0.394692 | 0.318646 | 0.003346 |
| 35 | 0.399396 | 0.380716 | 0.446308 | 0.442933 | 0.363651 | 0.280442 | 0.002975 |
| 36 | 0.398290 | 0.383196 | 0.435739 | 0.448145 | 0.358416 | 0.249918 | 0.002898 |

The trajectory is finite and non-collapsed. It is also noisy rather than monotonically improving: aggregate Dice reaches new highs after epoch 26, selects epoch 34, and then falls back at epochs 35-36. Epoch 30 briefly gives the best connectivity signature (0.438844) but not the best Dice, while epoch 32 gives the highest recall (0.489829) with too much positive area and lower precision. The selected epoch 34 balances Dice, source metrics, recall, and bounded positive fraction, but the branch does not stabilize high connectivity.

## Interpretation

Classify ABI-269 as a useful positive late-budget continuation for compact spectral/SZA-regime MoE, but not a promotion candidate. It validates that ABI-268 was budget-sensitive: the same architecture trained longer moves into the capped top tier and overtakes the older ABI-232 MoE branch on aggregate/source Dice. It also stays resource-safe and compact in parameter count.

The main negative signal is mechanism-specific. The compact MoE gates raise recall and Google performance, but the selected checkpoint loses connected-line evidence versus the ABI-268 parent and remains far below ABI-265/ABI-202 on connectivity. The branch therefore did not satisfy the hoped-for recall-plus-connectivity recovery; it mainly became a compact recall/source-balance comparator.

Resource evidence is also mixed. ABI-269 has fewer parameters than ABI-232, ABI-265, ABI-249, and ABI-202, but its 36-epoch wall time and memory are not clearly cheaper than ABI-232. It is safe under the current late-improving limits, yet not compelling enough to justify unchanged late-budget repetition.

## Decision

Do not promote ABI-269 and do not request whole-validation diagnostics from this capped Result. It is below ABI-202 and ABI-249 on aggregate capped Dice, below ABI-202/ABI-249/ABI-265/ABI-232 on selected-checkpoint connectivity, and did not produce a stable high-connectivity late trajectory.

Stop unchanged late36 continuations of this exact compact spectral/Solar Geometry Input MoE branch. Future MoE work should be mechanism-changing and explicitly target connected-line continuity, for example by adding a lightweight orientation-consensus or line-memory component to the compact gates without candidate-owned thresholds, postprocessing, losses, sampling, or resource scheduling. Alternatively, broaden to ABI-249-style C4/orientation recall support, ABI-223-style temporal evidence sharpening, or another underexplored resource-aware architecture family.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_121857_19f67d/candidate/PROPOSAL.md`
- `run_20260912_121857_19f67d/candidate/README.md`
- `run_20260912_121857_19f67d/candidate/manifest.yaml`
- `run_20260912_121857_19f67d/candidate/budget_request.yaml`
- `run_20260912_121857_19f67d/resolved_manifest.yaml`
- `run_20260912_121857_19f67d/outputs/model_summary.json`
- `run_20260912_121857_19f67d/outputs/best_metrics.json`
- `run_20260912_121857_19f67d/outputs/final_metrics.json`
- `run_20260912_121857_19f67d/outputs/metrics.jsonl`
- `run_20260912_121857_19f67d/outputs/resource_profile.json`
- `run_20260912_121857_19f67d/outputs/validation_postprocessing/index.json`
- `run_20260912_121857_19f67d/outputs/prediction_samples/samples.json`
- `run_20260912_113911_7a5f94` for ABI-268 parent context
- `run_20260910_163616_4f7416` for ABI-232 MoE late36 context
- `run_20260912_065321_ceab64` for ABI-265 selective axial line-memory context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
