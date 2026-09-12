# ABI-249 C4 steerable line-context U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-249, Candidate `abi249_fullspectral_btd_sza_c4_steerable_line_context_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260911_111909_dd7ef7`.

ABI-249 is the exact late36 close-continuation of ABI-248. It keeps the provider-approved `abi_16ch_plus_sza` input, derived approved-channel thermal BTD planes inside the architecture, C4 rotation-shared anisotropic line-context block, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-249 completed the approved late-improving 36-epoch budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; parent Run `run_20260911_102833_5db7f8`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,802,052, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 7.70 / 8.99 GiB.
- Training wall time: 3,747.4 s; validation wall time: 3,892.5 s; total Run wall time: 7,642.3 s.

This is successful finite/resource evidence for the C4 steerable line-context family under the late-improving budget. Resource use stayed inside the trusted memory and late36 timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 31. The final epoch 36 remained essentially tied on aggregate filtered Dice and improved MIT filtered Dice and recall, so the late36 trajectory did not collapse after the selected checkpoint.

| Metric | ABI-249 best epoch 31 | ABI-249 final epoch 36 | ABI-248 parent epoch 12 |
| --- | ---: | ---: | ---: |
| Filtered Dice | 0.416400 | 0.415810 | 0.383829 |
| Raw Dice | 0.432320 | 0.431141 | 0.399160 |
| Filtered IoU | 0.262946 | 0.262475 | 0.237493 |
| Filtered precision | 0.480886 | 0.448622 | 0.454139 |
| Filtered recall | 0.367165 | 0.387471 | 0.332372 |
| Filtered contrail connectivity | 0.392524 | 0.340016 | 0.327777 |
| Filtered predicted-positive fraction | 0.002767 | 0.003130 | 0.002652 |
| Raw predicted-positive fraction | 0.002955 | 0.003346 | 0.002830 |
| MIT filtered Dice | 0.396436 | 0.398843 | 0.373157 |
| Google filtered Dice | 0.468855 | 0.460079 | 0.411614 |
| MIT filtered recall | 0.339764 | 0.360545 | 0.313282 |
| Google filtered recall | 0.447303 | 0.466217 | 0.388203 |
| Train loss | 0.811498 | 0.805566 | 0.847672 |
| Validation loss | 0.873648 | 0.872833 | 0.882328 |

Relative to ABI-248, the selected ABI-249 checkpoint improves aggregate filtered Dice by about +0.0326, MIT filtered Dice by +0.0233, Google filtered Dice by +0.0572, filtered recall by +0.0348, and connectivity by +0.0647, while also improving precision by +0.0267 and only slightly increasing the filtered predicted-positive fraction. This validates the late-improving budget request: ABI-248 was materially truncated by the 12-epoch scout ceiling.

The best checkpoint is finite, noncollapsed, source-informative, and not obviously Artifact Filter-dependent from the capped metrics: raw Dice is only about 0.0159 above filtered Dice, and raw/filtered predicted-positive fractions remain compact.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.227396 | 0.243557 | 0.195247 | 0.189524 | 0.284181 | 0.131827 | 0.005434 |
| 6 | 0.346147 | 0.337523 | 0.366039 | 0.352684 | 0.339848 | 0.265365 | 0.003886 |
| 12 | 0.370438 | 0.363795 | 0.385599 | 0.387683 | 0.354662 | 0.157726 | 0.003312 |
| 18 | 0.373173 | 0.374718 | 0.369593 | 0.338861 | 0.415217 | 0.167143 | 0.004431 |
| 24 | 0.371900 | 0.356941 | 0.404745 | 0.362463 | 0.381841 | 0.190764 | 0.003817 |
| 30 | 0.388955 | 0.365406 | 0.448156 | 0.515957 | 0.312126 | 0.416510 | 0.002192 |
| 31 | 0.416400 | 0.396436 | 0.468855 | 0.480886 | 0.367165 | 0.392524 | 0.002767 |
| 36 | 0.415810 | 0.398843 | 0.460079 | 0.448622 | 0.387471 | 0.340016 | 0.003130 |

The trajectory is noisy but clearly late-improving. Epochs 30-36 show the branch finding a much stronger precision/connectivity operating region than the exploratory endpoint, while the final epoch keeps the aggregate score within 0.0006 of the best checkpoint and improves recall versus epoch 31. The source split remains informative: Google is stronger than MIT, but both sources improve materially over ABI-248 and neither collapses.

## Comparison context

| Metric | ABI-249 C4 late36 | ABI-248 C4 scout | ABI-202 current whole-validation frontier context |
| --- | ---: | ---: | ---: |
| Run | `run_20260911_111909_dd7ef7` | `run_20260911_102833_5db7f8` | `run_20260904_043143_ee0005` |
| Best epoch | 31 | 12 | 34 |
| Filtered Dice | 0.416400 | 0.383829 | 0.427570 |
| Raw Dice | 0.432320 | 0.399160 | 0.442746 |
| Filtered precision | 0.480886 | 0.454139 | 0.439467 |
| Filtered recall | 0.367165 | 0.332372 | 0.416301 |
| Filtered connectivity | 0.392524 | 0.327777 | 0.457773 |
| MIT filtered Dice | 0.396436 | 0.373157 | 0.411992 |
| Google filtered Dice | 0.468855 | 0.411614 | 0.468151 |
| Filtered predicted-positive fraction | 0.002767 | 0.002652 | 0.003433 |

ABI-249 becomes a strong capped single-frame Result: it is well above ABI-248 and appears competitive with the mature capped frontier on precision and Google filtered Dice. It remains below ABI-202 on aggregate filtered Dice by about -0.0112, MIT filtered Dice by about -0.0156, recall by about -0.0491, and connectivity by about -0.0652. Thus ABI-249 is not a promotion claim, but it is strong enough to justify trusted whole-validation diagnostics if the next Autonomy Step chooses an Evaluation Request.

## Interpretation

Classify ABI-249 as a successful late-budget family-development result. The exact C4 rotation-sharing branch should not be dismissed as merely a low-scoring scout: the late budget converted ABI-248 from a mid-0.38 capped scout into a >0.416 capped Result with improved source balance, precision, recall, and connectivity. The main remaining weakness is recall/connectivity versus ABI-202, especially on MIT. The C4 block appears to be a precision-preserving orientation prior that benefits substantially from longer optimization, but it still does not recover as many filtered contrail pixels as the best crossscale directional-consensus ASPP branch.

The result is capped representative feasibility evidence only. It should not be compared as a full-data promotion result until trusted whole-validation diagnostics are requested and observed.

## Decision

Do not promote ABI-249 from capped evidence alone. Do treat it as a high-priority diagnostic candidate: a future step should consider a whole-validation failure-bucket Evaluation Request for `run_20260911_111909_dd7ef7` to test whether the capped precision and Google strength transfer, whether MIT recall/connectivity remain the limiting failure mode, and whether Artifact Filter effects stay modest on the canonical Working Validation Split.

Do not run another exact C4 late-budget repetition. If diagnostics are favorable, a next architecture branch should target recall/connectivity explicitly, for example by adding a recall-preserving high-resolution detail bypass or crossscale support bridge before C4 orientation fusion. If diagnostics expose source-specific MIT failures or clutter modes, use those buckets to design a mechanism-changing branch rather than auxiliary-head or epoch tweaks.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_111909_dd7ef7/candidate/PROPOSAL.md`
- `run_20260911_111909_dd7ef7/candidate/README.md`
- `run_20260911_111909_dd7ef7/candidate/manifest.yaml`
- `run_20260911_111909_dd7ef7/candidate/budget_request.yaml`
- `run_20260911_111909_dd7ef7/resolved_manifest.yaml`
- `run_20260911_111909_dd7ef7/outputs/model_summary.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/final_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/metrics.jsonl`
- `run_20260911_111909_dd7ef7/outputs/resource_profile.json`
- `run_20260911_111909_dd7ef7/outputs/validation_postprocessing/index.json`
- `run_20260911_111909_dd7ef7/outputs/prediction_samples/samples.json`
- `run_20260911_102833_5db7f8` for ABI-248 parent context
- `run_20260904_043143_ee0005` for ABI-202 current single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
