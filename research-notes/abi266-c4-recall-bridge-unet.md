# ABI-266 C4 recall-bridge U-Net

research-figures: []

## Scope

This note records the exploratory capped-validation Result for ABI-266, Candidate `abi266_fullspectral_btd_sza_c4_recall_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_093630_4550c9`.

ABI-266 was a mechanism-changing continuation of the C4 steerable line-context branch. It kept provider-owned `abi_16ch_plus_sza` inputs, trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary outputs. Relative to ABI-249, it added a lightweight gated recall bridge intended to raise under-confident contrail evidence when high-resolution detail and C4 line context agree.

Candidate code remained architecture-only. It did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-266 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,067,334, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 10.15 / 11.65 GB.
- Training wall time: 1,531.5 s; validation wall time: 1,403.7 s; total Run wall time: 2,937.1 s, within the 3,600 s exploratory timeout.

This is valid finite capped-validation evidence for the C4 recall-bridge design. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 9. The final epoch 12 was lower on aggregate filtered Dice, so the exploratory trajectory did not justify an unchanged late-improving budget request.

| Metric | ABI-266 best epoch 9 | ABI-266 final epoch 12 | ABI-248 C4 exploratory | ABI-249 C4 late36 | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.374081 | 0.368003 | 0.383829 | 0.416400 | 0.427570 |
| Raw Dice | 0.386801 | 0.381460 | 0.399160 | 0.432320 | 0.442746 |
| Filtered precision | 0.363731 | 0.391182 | 0.454139 | 0.480886 | 0.439467 |
| Filtered recall | 0.385036 | 0.347418 | 0.332372 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.172858 | 0.183509 | 0.327777 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.367395 | 0.358973 | 0.373157 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.389347 | 0.388688 | 0.411614 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003836 | 0.003218 | 0.002652 | 0.002767 | 0.003433 |

ABI-266 partially achieved the intended recall-raising effect versus ABI-248 at its selected checkpoint: filtered recall increased from 0.3324 to 0.3850. However, this came with a much larger loss of precision and line continuity. Aggregate filtered Dice fell by about -0.0097 versus ABI-248, precision fell by about -0.0904, connectivity fell by about -0.1549, MIT Dice fell by about -0.0058, and Google Dice fell by about -0.0223. Relative to ABI-249, ABI-266 is clearly weaker on aggregate Dice, precision, connectivity, and both Dataset Sources.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.193624 | 0.199146 | 0.183396 | 0.176410 | 0.214560 | 0.076842 | 0.004407 |
| 2 | 0.268262 | 0.259887 | 0.286828 | 0.321463 | 0.230170 | 0.160556 | 0.002595 |
| 3 | 0.275822 | 0.271197 | 0.284638 | 0.262354 | 0.290746 | 0.122980 | 0.004016 |
| 4 | 0.308634 | 0.304507 | 0.317285 | 0.284385 | 0.337403 | 0.138485 | 0.004299 |
| 5 | 0.305808 | 0.283734 | 0.356784 | 0.398750 | 0.248003 | 0.215470 | 0.002254 |
| 6 | 0.308630 | 0.298254 | 0.329980 | 0.319628 | 0.298364 | 0.167926 | 0.003383 |
| 7 | 0.364029 | 0.359562 | 0.374404 | 0.355738 | 0.372716 | 0.212926 | 0.003797 |
| 8 | 0.352309 | 0.333257 | 0.396359 | 0.406177 | 0.311056 | 0.214634 | 0.002775 |
| 9 | 0.374081 | 0.367395 | 0.389347 | 0.363731 | 0.385036 | 0.172858 | 0.003836 |
| 10 | 0.357864 | 0.346233 | 0.383389 | 0.387342 | 0.332555 | 0.214604 | 0.003111 |
| 11 | 0.363023 | 0.368366 | 0.351326 | 0.304876 | 0.448579 | 0.173877 | 0.005332 |
| 12 | 0.368003 | 0.358973 | 0.388688 | 0.391182 | 0.347418 | 0.183509 | 0.003218 |

The trajectory is finite and non-collapsed, but it is not frontier-competitive. Epoch 11 shows that the recall bridge can push recall as high as 0.4486, but the corresponding precision drop to 0.3049, positive fraction increase to 0.00533, and Google filtered Dice drop to 0.3513 indicate that the bridge raises false positives faster than useful fixed-threshold contrail evidence. The selected epoch 9 is a better aggregate compromise, but connectivity remains low throughout.

## Interpretation

Classify ABI-266 as a negative but informative mechanism-changing C4 continuation. The bridge did what it was designed to do in the narrow sense of raising recall above the ABI-248 exploratory parent, but it damaged the C4 family's most valuable property: compact, high-precision, line-continuous predictions. The bounded residual/gating design did not preserve enough orientation-prior selectivity to convert additional positive area into higher filtered Dice or connectivity.

The result does not eliminate C4 steerable line context as a family; ABI-249 remains a strong whole-validation-tested high-precision comparator. It does eliminate this exact recall-bridge design as the next C4 development path. Future C4 work should avoid broad logit boosting and instead preserve the conservative orientation prior while improving coverage through better high-resolution evidence alignment, source-balanced calibration, or a diagnostic-motivated threshold-shaping architecture that does not implement candidate-owned thresholding or postprocessing.

## Decision

Do not promote ABI-266, do not request whole-validation diagnostics, and do not request a late-improving continuation of this exact recall bridge. The run is valid finite evidence, but it regressed ABI-248 exploratory C4 aggregate Dice and connectivity and remains far below ABI-249/ABI-202.

Stop the exact gated recall-bridge branch. Retain the observation that recall can be raised, but only as a warning that naive architecture-level logit support erodes C4 precision and continuity. A reasonable future handoff would broaden to a different underexplored mechanism or propose a C4 variant that improves evidence alignment without adding a general recall boost.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_093630_4550c9/candidate/PROPOSAL.md`
- `run_20260912_093630_4550c9/candidate/README.md`
- `run_20260912_093630_4550c9/candidate/manifest.yaml`
- `run_20260912_093630_4550c9/resolved_manifest.yaml`
- `run_20260912_093630_4550c9/outputs/model_summary.json`
- `run_20260912_093630_4550c9/outputs/best_metrics.json`
- `run_20260912_093630_4550c9/outputs/final_metrics.json`
- `run_20260912_093630_4550c9/outputs/metrics.jsonl`
- `run_20260912_093630_4550c9/outputs/resource_profile.json`
- `run_20260912_093630_4550c9/outputs/validation_postprocessing/index.json`
- `run_20260912_093630_4550c9/outputs/prediction_samples/samples.json`
- `run_20260911_102833_5db7f8` for ABI-248 C4 exploratory parent context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 late36 and whole-validation comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
