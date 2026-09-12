# ABI-268 compact spectral-regime MoE line U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-268, Candidate `abi268_fullspectral_btd_sza_compact_spectral_moe_line_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_113911_7a5f94`.

ABI-268 was a resource-aware family-development continuation of the spectral/Solar Geometry Input mixture-of-experts direction. ABI-267 (`run_20260912_103414_825633`) attempted a fuller spectral MoE line U-Net but failed with a Harness-recorded `resource_failure` after exhausting the 3,600 s exploratory wall-clock budget. ABI-268 narrowed channels and restricted MoE blocks to downsampled encoder/bottleneck and one low-resolution decoder stage while preserving the hypothesis that learned gates from provider-approved ABI+SZA features can select local, dilated, and line-oriented transformations.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` inputs, used trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-268 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,755,175, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.97 / 6.44 GB.
- Training wall time: 757.8 s; validation wall time: 1,105.1 s; total Run wall time: 1,864.6 s, within the 3,600 s exploratory timeout.

This is valid finite capped-validation evidence for the compact spectral-regime MoE line U-Net. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 12, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-268 best epoch 12 | ABI-232 MoE late36 | ABI-265 axial line-memory late36 | ABI-249 C4 line-context | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.398540 | 0.400942 | 0.411977 | 0.416400 | 0.427570 |
| Raw Dice | 0.413801 | 0.414940 | 0.427098 | 0.432320 | 0.442746 |
| Filtered precision | 0.446572 | 0.405218 | 0.433940 | 0.480886 | 0.439467 |
| Filtered recall | 0.359837 | 0.396756 | 0.392130 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.360615 | 0.383636 | 0.433071 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.386144 | 0.386542 | 0.401437 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.429981 | 0.439983 | 0.438974 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.002920 | 0.003548 | 0.003275 | 0.002767 | 0.003433 |

ABI-268 solved the ABI-267 resource problem and produced a useful capped Result. Relative to the original ABI-231 12-epoch MoE scout, ABI-268 improves aggregate filtered Dice by about +0.0266, MIT filtered Dice by +0.0303, Google filtered Dice by +0.0162, precision by +0.0144, and recall by +0.0333, but loses connectivity by about -0.0379. Relative to ABI-232 late36, ABI-268 nearly ties aggregate/MIT Dice under only 12 epochs and is more precise and compact, but it has lower recall, connectivity, and Google Dice.

Relative to the stronger recent frontier, ABI-268 remains below ABI-265, ABI-249, and ABI-202 on aggregate filtered Dice and connectivity. It is therefore not a promotion candidate and does not justify immediate whole-validation diagnostics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.199266 | 0.216695 | 0.169829 | 0.159093 | 0.266579 | 0.102668 | 0.006072 |
| 2 | 0.277518 | 0.282847 | 0.266747 | 0.260412 | 0.297030 | 0.208533 | 0.004133 |
| 3 | 0.295547 | 0.304505 | 0.277951 | 0.271295 | 0.324561 | 0.210238 | 0.004335 |
| 4 | 0.320623 | 0.324292 | 0.312945 | 0.290924 | 0.357074 | 0.144519 | 0.004448 |
| 5 | 0.308255 | 0.291755 | 0.343263 | 0.351478 | 0.274499 | 0.216307 | 0.002830 |
| 6 | 0.345933 | 0.331805 | 0.377807 | 0.355725 | 0.336665 | 0.245597 | 0.003430 |
| 7 | 0.361414 | 0.348203 | 0.392832 | 0.372794 | 0.350708 | 0.253973 | 0.003409 |
| 8 | 0.367905 | 0.347645 | 0.417434 | 0.447693 | 0.312255 | 0.315846 | 0.002527 |
| 9 | 0.368216 | 0.354286 | 0.401332 | 0.404610 | 0.337829 | 0.232411 | 0.003026 |
| 10 | 0.349867 | 0.331824 | 0.389718 | 0.381632 | 0.322984 | 0.264815 | 0.003067 |
| 11 | 0.386736 | 0.373569 | 0.418197 | 0.417133 | 0.360468 | 0.259636 | 0.003131 |
| 12 | 0.398540 | 0.386144 | 0.429981 | 0.446572 | 0.359837 | 0.360615 | 0.002920 |

The trajectory is finite, non-collapsed, source-informative, and still improving at the exploratory epoch ceiling. Epoch 12 is the selected checkpoint and improves simultaneously on aggregate filtered Dice, MIT Dice, Google Dice, precision, connectivity, and compact positive fraction relative to epoch 11, with recall essentially held steady. The late trajectory therefore looks budget-truncated rather than exhausted.

The source pattern is also useful: Google filtered Dice reaches 0.4300 and MIT reaches 0.3861 without a large positive-area blow-up. The main remaining weakness is that connectivity lags ABI-231/232/249/265/202, so the compact MoE design gained resource feasibility and precision but did not yet preserve enough connected-line continuity.

## Interpretation

Classify ABI-268 as a positive resource-safe compact MoE continuation, but not a new campaign frontier. The result repairs the practical failure mode of ABI-267 and shows that spectral/SZA-regime gating can be made small enough to complete the exploratory budget while remaining competitive with the earlier MoE branch. Its selected checkpoint is nearly tied with ABI-232 late36 on aggregate capped Dice despite using only the exploratory budget, which suggests the compact architecture is more efficient than the older MoE formulation.

The scientific signal is mixed because ABI-268 trades away the high-connectivity signature that made ABI-231 distinctive and remains below the current whole-validation-tested ABI-202 frontier and recent ABI-249/ABI-265 capped comparators. Low score alone is not a hard stop for this branch because the trajectory is improving and non-degenerate, but any continuation should target a specific mechanism: recover connected-line evidence without turning the compact MoE into another expensive high-resolution branch.

## Decision

Do not promote ABI-268 and do not request whole-validation diagnostics from this capped Result. It is below the established ABI-202/ABI-249 frontier and below ABI-265 on capped aggregate Dice/connectivity.

Do not abandon compact spectral/SZA-regime MoE. ABI-268 is a resource-successful, improving final-epoch scout after ABI-267 timed out. A bounded next step could request the approved `late_improving` budget for the compact ABI-268 architecture, because it selected epoch 12, stayed finite and source-informative, and did not collapse. A more mechanism-changing alternative would keep the compact MoE blocks but add a lightweight connectivity-preserving line-consensus or orientation-memory component, while avoiding candidate-owned thresholds, postprocessing, losses, sampling, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_113911_7a5f94/candidate/PROPOSAL.md`
- `run_20260912_113911_7a5f94/candidate/README.md`
- `run_20260912_113911_7a5f94/candidate/manifest.yaml`
- `run_20260912_113911_7a5f94/resolved_manifest.yaml`
- `run_20260912_113911_7a5f94/outputs/model_summary.json`
- `run_20260912_113911_7a5f94/outputs/best_metrics.json`
- `run_20260912_113911_7a5f94/outputs/final_metrics.json`
- `run_20260912_113911_7a5f94/outputs/metrics.jsonl`
- `run_20260912_113911_7a5f94/outputs/resource_profile.json`
- `run_20260912_113911_7a5f94/outputs/validation_postprocessing/index.json`
- `run_20260912_113911_7a5f94/outputs/prediction_samples/samples.json`
- `run_20260912_103414_825633` for ABI-267 resource-failure context
- `run_20260910_155936_362435` for ABI-231 MoE exploratory context
- `run_20260910_163616_4f7416` for ABI-232 MoE late36 context
- `run_20260912_065321_ceab64` for ABI-265 selective axial line-memory context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
