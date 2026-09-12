# ABI-248 C4 steerable line-context U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-248, Candidate `abi248_fullspectral_btd_sza_c4_steerable_line_context_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_102833_5db7f8`.

ABI-248 tested an underexplored rotation-aware line-network direction: a C4 rotation-shared anisotropic line-context block over approved full-spectral ABI+Solar Geometry Input features. The Candidate used trusted `abi_16ch_plus_sza` input, derived only approved-channel thermal BTD planes inside the architecture, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-248 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,802,052, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 7.70 / 8.99 GiB.
- Training wall time: 1,248.5 s; validation wall time: 1,336.7 s; total Run wall time: 2,587.4 s.

This is successful finite/resource evidence for the C4 steerable line-context family. Resource use stayed inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 12, which is also the final epoch.

| Metric | ABI-248 best/final epoch 12 |
| --- | ---: |
| Filtered Dice | 0.383829 |
| Raw Dice | 0.399160 |
| Filtered IoU | 0.237493 |
| Filtered precision | 0.454139 |
| Filtered recall | 0.332372 |
| Filtered contrail connectivity | 0.327777 |
| Filtered predicted-positive fraction | 0.002652 |
| Raw predicted-positive fraction | 0.002830 |
| MIT filtered Dice | 0.373157 |
| Google filtered Dice | 0.411614 |
| MIT filtered recall | 0.313282 |
| Google filtered recall | 0.388203 |
| Train loss | 0.847672 |
| Validation loss | 0.882328 |

The selected checkpoint is finite, noncollapsed, source-informative, and moderately precision-weighted. The Dataset Source split is acceptable for a scout: Google filtered Dice is stronger than MIT by about 0.0385, but both sources remain well above collapse. The low predicted-positive fraction and recall show that the C4 block did not create an over-generous line detector.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.227699 | 0.234800 | 0.190787 | 0.282321 | 0.243564 | 0.196012 | 0.132262 | 0.005362 |
| 2 | 0.246830 | 0.255598 | 0.255954 | 0.238335 | 0.247615 | 0.245244 | 0.142051 | 0.003374 |
| 3 | 0.280546 | 0.289948 | 0.279237 | 0.281866 | 0.286630 | 0.268020 | 0.176947 | 0.003658 |
| 4 | 0.310339 | 0.321025 | 0.317953 | 0.303081 | 0.305778 | 0.320883 | 0.176679 | 0.003454 |
| 5 | 0.337527 | 0.348930 | 0.326286 | 0.349571 | 0.330836 | 0.352256 | 0.221186 | 0.003882 |
| 6 | 0.330491 | 0.340176 | 0.274168 | 0.415939 | 0.336175 | 0.319073 | 0.161851 | 0.005497 |
| 7 | 0.351154 | 0.362846 | 0.328583 | 0.377055 | 0.348935 | 0.356232 | 0.174112 | 0.004158 |
| 8 | 0.353737 | 0.367714 | 0.412110 | 0.309849 | 0.345083 | 0.374328 | 0.211186 | 0.002725 |
| 9 | 0.361425 | 0.374842 | 0.405307 | 0.326117 | 0.341857 | 0.408708 | 0.271717 | 0.002916 |
| 10 | 0.365818 | 0.379898 | 0.424230 | 0.321544 | 0.360010 | 0.379217 | 0.273806 | 0.002747 |
| 11 | 0.367883 | 0.380665 | 0.377008 | 0.359189 | 0.356739 | 0.394052 | 0.194820 | 0.003452 |
| 12 | 0.383829 | 0.399160 | 0.454139 | 0.332372 | 0.373157 | 0.411614 | 0.327777 | 0.002652 |

The trajectory is broadly improving and ends at its best aggregate filtered Dice, best Google Dice, best MIT Dice, highest precision, and highest connectivity. Train and validation loss also decline into the final epoch. The final-epoch best is evidence that the exploratory budget may be truncating this exact family, although the absolute score remains below the mature single-frame frontier.

## Comparison context

| Metric | ABI-248 C4 steerable scout | ABI-142 multiscale ridge attention | ABI-143 soft ridge gate | ABI-207 directional message passing | ABI-208 orientation consensus | ABI-202 best single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_102833_5db7f8` | `run_20260831_215104_d4c318` | `run_20260831_224534_27b73d` | `run_20260904_120216_3ffbda` | `run_20260904_130809_8896f4` | `run_20260904_043143_ee0005` |
| Best epoch | 12 | 12 | 12 | 12 | 9 | 34 |
| Filtered Dice | 0.383829 | 0.393539 | 0.394748 | 0.388483 | 0.373853 | 0.427570 |
| Raw Dice | 0.399160 | 0.407899 | 0.408323 | 0.402044 | 0.388248 | 0.442746 |
| Filtered precision | 0.454139 | 0.439764 | 0.410547 | 0.392288 | 0.443703 | 0.439467 |
| Filtered recall | 0.332372 | 0.356107 | 0.380120 | 0.384753 | 0.323004 | 0.416301 |
| Filtered connectivity | 0.327777 | 0.381901 | 0.300971 | 0.291149 | 0.371139 | 0.457773 |
| MIT filtered Dice | 0.373157 | 0.376194 | 0.381519 | 0.375244 | 0.355710 | 0.411992 |
| Google filtered Dice | 0.411614 | 0.437319 | 0.428749 | 0.421213 | 0.420607 | 0.468151 |
| Filtered predicted-positive fraction | 0.002652 | 0.002934 | 0.003355 | 0.003554 | 0.002638 | 0.003433 |

Relative to ABI-142, ABI-248 is lower on filtered Dice by about -0.0097 and connectivity by about -0.0541, but slightly higher precision with a smaller predicted-positive fraction. Relative to ABI-143, ABI-248 is lower on filtered Dice by about -0.0109 and recall by about -0.0477, but higher precision and higher connectivity. Relative to ABI-207, ABI-248 is only -0.0047 filtered Dice, with higher precision and higher connectivity but lower recall. Relative to ABI-208, ABI-248 improves filtered Dice by about +0.0100 and both source Dice values, but ABI-208 has stronger connectivity.

ABI-248 remains far below the current single-frame ABI-202 late36 frontier: about -0.0437 filtered Dice, -0.0839 recall, and -0.1300 connectivity. It should not be interpreted as promotion evidence.

## Interpretation

Classify ABI-248 as a finite and moderately promising rotation-aware scout, not a frontier Result. It meets the preregistered scout success criterion of reaching the broad single-frame scout range around 0.38 filtered Dice and provides noncollapsed source-informative evidence. The C4 rotation-sharing idea appears useful enough to retain in the search space: it improved over ABI-208 on overlap and gave better connectivity than ABI-143 and ABI-207 at a conservative operating point.

The main weakness is that the current formulation is recall-limited and does not match the strongest ridge/ASPP/detail or temporal-frontier connectivity. The C4 block may be acting as a precision-preserving orientation prior rather than as a recall-expanding continuity mechanism. Because best Dice, precision, source Dice, and connectivity all occur at epoch 12, low score alone is not sufficient to eliminate the family under the architecture-scout policy.

## Decision

Do not promote ABI-248 and do not request whole-validation diagnostics from this capped Result alone. Keep the C4 steerable line-context family eligible for one bounded close-continuation: either a late36 continuation of the exact scout, justified by the final-epoch best and finite noncollapsed trajectory, or a mechanism-changing follow-up that adds recall-preserving high-resolution detail bypass/context before the C4 fusion. A continuation should explicitly protect recall while preserving the precision and source balance seen here.

Do not spend further effort on simple local tweaks unless they target the observed recall bottleneck or test whether the final-epoch best was budget-truncated. If the next branch cannot improve overlap/recall while maintaining connectivity, broaden again to another underexplored architecture family.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_102833_5db7f8/candidate/PROPOSAL.md`
- `run_20260911_102833_5db7f8/candidate/README.md`
- `run_20260911_102833_5db7f8/candidate/manifest.yaml`
- `run_20260911_102833_5db7f8/resolved_manifest.yaml`
- `run_20260911_102833_5db7f8/outputs/model_summary.json`
- `run_20260911_102833_5db7f8/outputs/best_metrics.json`
- `run_20260911_102833_5db7f8/outputs/final_metrics.json`
- `run_20260911_102833_5db7f8/outputs/metrics.jsonl`
- `run_20260911_102833_5db7f8/outputs/resource_profile.json`
- `run_20260911_102833_5db7f8/outputs/validation_postprocessing/index.json`
- `run_20260911_102833_5db7f8/outputs/prediction_samples/samples.json`
- `run_20260831_215104_d4c318` for ABI-142 multiscale ridge-attention context
- `run_20260831_224534_27b73d` for ABI-143 soft-ridge-gate context
- `run_20260904_120216_3ffbda` for ABI-207 directional-message-passing context
- `run_20260904_130809_8896f4` for ABI-208 orientation-consensus context
- `run_20260904_043143_ee0005` for ABI-202 current single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
