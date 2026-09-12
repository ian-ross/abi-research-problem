# ABI-232 spectral-regime MoE U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-232, Candidate `abi232_fullspectral_btd_sza_spectral_regime_moe_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260910_163616_4f7416`.

ABI-232 was a close family-development continuation of ABI-231. It preserved the compact single-frame spectral/Solar Geometry Input mixture-of-experts U-Net and requested the approved `late_improving` budget because ABI-231 completed finite, source-informative training and selected its best checkpoint at the exploratory epoch ceiling. The model consumed provider-owned `abi_16ch_plus_sza` tensors, derived approved-channel BTD and Solar Geometry Input features, learned soft gates over three convolutional experts, and used trusted Mask/Line/Centerline outputs.

Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-232 completed the approved 36-epoch late-improving budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; parent Run `run_20260910_155936_362435`.
- Effective budget: 36 epochs, constant learning rate, disabled early stopping, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 2,300,013, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.49 / 5.41 GB.
- Training wall time: 1,825.9 s; validation wall time: 3,296.3 s; total Run wall time: 5,123.9 s.

This is successful finite/resource evidence for the spectral/SZA-regime MoE family under the longer approved budget.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 32. The final epoch 36 regressed from that selected checkpoint, so selection matters for interpretation.

| Metric | ABI-232 best epoch 32 | ABI-232 final epoch 36 |
| --- | ---: | ---: |
| Filtered Dice | 0.400942 | 0.384597 |
| Raw Dice | 0.414940 | 0.399244 |
| Filtered IoU | 0.250737 | 0.238081 |
| Filtered precision | 0.405218 | 0.405980 |
| Filtered recall | 0.396756 | 0.365353 |
| Filtered contrail connectivity | 0.383636 | 0.346495 |
| Filtered predicted-positive fraction | 0.003548 | 0.003261 |
| MIT filtered Dice | 0.386542 | 0.374482 |
| Google filtered Dice | 0.439983 | 0.409506 |
| MIT filtered recall | 0.374978 | 0.339521 |
| Google filtered recall | 0.460448 | 0.440904 |
| Train loss | 0.825334 | 0.825151 |
| Validation loss | 0.883700 | 0.887472 |

The selected Result is finite, noncollapsed, and source-informative. It improves the parent ABI-231 on aggregate filtered Dice, recall, MIT Dice, and Google Dice, while giving back some of ABI-231's unusually high connectivity and compact-positive-area precision profile.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.224132 | 0.172638 | 0.319402 | 0.244470 | 0.186860 | 0.135612 | 0.006704 |
| 2 | 0.272640 | 0.270104 | 0.275225 | 0.277632 | 0.261516 | 0.166149 | 0.003692 |
| 3 | 0.260636 | 0.203076 | 0.363733 | 0.285506 | 0.216616 | 0.128040 | 0.006490 |
| 4 | 0.321207 | 0.316364 | 0.326199 | 0.318310 | 0.327717 | 0.214516 | 0.003736 |
| 5 | 0.338472 | 0.412616 | 0.286916 | 0.325793 | 0.369403 | 0.365450 | 0.002520 |
| 6 | 0.323490 | 0.363004 | 0.291733 | 0.307783 | 0.358631 | 0.266225 | 0.002912 |
| 7 | 0.363352 | 0.413907 | 0.323802 | 0.349202 | 0.397740 | 0.359146 | 0.002835 |
| 8 | 0.358826 | 0.454865 | 0.296271 | 0.340461 | 0.405020 | 0.427205 | 0.002360 |
| 9 | 0.357406 | 0.358653 | 0.356167 | 0.342732 | 0.393680 | 0.264556 | 0.003599 |
| 10 | 0.359608 | 0.426666 | 0.310766 | 0.345293 | 0.393948 | 0.344803 | 0.002639 |
| 11 | 0.333459 | 0.292433 | 0.387876 | 0.334164 | 0.331960 | 0.180572 | 0.004806 |
| 12 | 0.364219 | 0.418504 | 0.322400 | 0.346991 | 0.406560 | 0.332763 | 0.002792 |
| 16 | 0.373268 | 0.395115 | 0.353710 | 0.360215 | 0.404452 | 0.270660 | 0.003244 |
| 20 | 0.355269 | 0.323947 | 0.393298 | 0.346392 | 0.375093 | 0.254706 | 0.004399 |
| 24 | 0.376209 | 0.454400 | 0.320977 | 0.356213 | 0.426718 | 0.397728 | 0.002560 |
| 28 | 0.377936 | 0.480203 | 0.311581 | 0.354762 | 0.437706 | 0.389296 | 0.002351 |
| 32 | 0.400942 | 0.405218 | 0.396756 | 0.386542 | 0.439983 | 0.383636 | 0.003548 |
| 33 | 0.395177 | 0.424426 | 0.369700 | 0.381041 | 0.435237 | 0.421985 | 0.003156 |
| 34 | 0.395965 | 0.479366 | 0.337284 | 0.381976 | 0.434312 | 0.453086 | 0.002550 |
| 35 | 0.396385 | 0.400661 | 0.392200 | 0.386593 | 0.422051 | 0.283892 | 0.003547 |
| 36 | 0.384597 | 0.405980 | 0.365353 | 0.374482 | 0.409506 | 0.346495 | 0.003261 |

The late budget was useful: ABI-232 did not simply plateau at epoch 12, and the selected epoch 32 is materially above the parent. The last four epochs are mixed rather than monotonically improving: epoch 34 has the strongest connectivity/precision profile, epoch 35 ties the best MIT Dice but lower Google Dice, and epoch 36 declines. This supports the late-improving budget decision but does not argue for an even longer version of the same exact branch.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-231 parent | ABI-232 late36 |
| --- | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 12 | 32 |
| Filtered Dice | 0.427570 | 0.419776 | 0.371985 | 0.400942 |
| Raw Dice | 0.442746 | 0.438487 | 0.386649 | 0.414940 |
| Filtered precision | 0.439467 | 0.483764 | 0.432192 | 0.405218 |
| Filtered recall | 0.416301 | 0.370738 | 0.326502 | 0.396756 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.398515 | 0.383636 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.355799 | 0.386542 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.413787 | 0.439983 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.002738 | 0.003548 |

Relative to ABI-231, ABI-232 improves filtered Dice by +0.028957, filtered recall by +0.070254, MIT filtered Dice by +0.030743, and Google filtered Dice by +0.026196. The cost is lower precision (-0.026974), lower connectivity (-0.014879), and a higher predicted-positive fraction (+0.000810). This means the longer budget successfully recovered coverage/recall, but partly softened the conservative connected-line signature that made ABI-231 distinctive.

Relative to ABI-223, ABI-232 still trails aggregate filtered Dice by -0.018834, Google Dice by -0.036781, and connectivity by -0.028791, though it exceeds ABI-223 recall by +0.026018 and comes within -0.011956 MIT Dice. Relative to ABI-202, ABI-232 trails filtered Dice by -0.026628, MIT Dice by -0.025450, Google Dice by -0.028168, precision by -0.034249, recall by -0.019545, and connectivity by -0.074137. It is therefore not a frontier promotion candidate.

## Interpretation

Classify ABI-232 as a positive late-budget family-development Result for the spectral/SZA-regime MoE branch, but not as a new campaign frontier. The core scientific result is that ABI-231's final-epoch behavior was genuinely budget-limited: extending the same architecture improved source-balanced overlap and recall substantially. The branch remains noncollapsed and source-informative, with both MIT and Google filtered Dice well above 0.38 at the selected checkpoint.

The main weakness is that the MoE family still lags the best single-frame and temporal frontiers, especially on connectivity and Google overlap. Its selected checkpoint no longer preserves ABI-231's highest-connectivity/lowest-positive-fraction signature, and the late trajectory peaks before the final epoch. That pattern does not justify abandoning all spectral/illumination-gated experts, but it does argue against simply rerunning the same architecture longer.

## Decision

Do not promote ABI-232 and do not request whole-validation diagnostics from this capped Result. It is below ABI-202 and ABI-223, and whole-validation budget should remain focused on closer frontier candidates or diagnostically necessary comparisons.

Do not classify the MoE family as exhausted. The late-budget result validates that spectral/SZA-regime gating can recover recall under longer training. If this branch is continued, the next MoE hypothesis should be a bounded architecture change aimed at preserving epoch-34-style connectivity while retaining epoch-32 recall, for example a recall-preserving line-consensus head or a more explicit differentiable line-voting support path. If the campaign broadens instead, prefer a materially different differentiable Hough/Radon-style line-accumulation scout, because ABI-232 still leaves a clear connectivity gap to ABI-202/ABI-223.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_163616_4f7416/candidate/PROPOSAL.md`
- `run_20260910_163616_4f7416/candidate/README.md`
- `run_20260910_163616_4f7416/candidate/manifest.yaml`
- `run_20260910_163616_4f7416/candidate/budget_request.yaml`
- `run_20260910_163616_4f7416/resolved_manifest.yaml`
- `run_20260910_163616_4f7416/outputs/model_summary.json`
- `run_20260910_163616_4f7416/outputs/best_metrics.json`
- `run_20260910_163616_4f7416/outputs/final_metrics.json`
- `run_20260910_163616_4f7416/outputs/metrics.jsonl`
- `run_20260910_163616_4f7416/outputs/resource_profile.json`
- `run_20260910_163616_4f7416/outputs/validation_postprocessing/index.json`
- `run_20260910_163616_4f7416/outputs/prediction_samples/samples.json`
- `run_20260910_155936_362435` for ABI-231 parent context
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family late36 frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
