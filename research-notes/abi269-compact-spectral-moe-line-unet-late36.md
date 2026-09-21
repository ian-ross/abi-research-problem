# ABI-269 compact spectral-regime MoE line U-Net late36

research-figures: []

## Scope

This note records ABI-269, Candidate `abi269_fullspectral_btd_sza_compact_spectral_moe_line_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260912_121857_19f67d`.

ABI-269 was a late-improving close continuation of ABI-268. It preserved the compact full-spectral ABI plus Solar Geometry Input spectral-regime MoE line U-Net architecture and requested the approved 36-epoch `late_improving` budget because ABI-268 completed finitely, selected epoch 12 as its best checkpoint, and remained source-informative under the exploratory ceiling.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` tensors and returned `mask_logits`, `line_logits`, and `centerline_logits`. It used trusted combined source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, provider-derived Line and Centerline auxiliary targets, AdamW with constant learning rate, batch size 4, and the provider-owned 1,024-record-per-Dataset-Source/split cap. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling implementation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle control.

## Execution result

ABI-269 completed the approved 36-epoch late-improving budget without contract, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; parent Run `run_20260912_113911_7a5f94`.
- Effective budget: 36 epochs, constant learning rate, disabled early stopping, late-improving timeout.
- Input mode: `abi_16ch_plus_sza`; forbidden longitude and latitude source channels excluded in `outputs/model_summary.json`.
- Effective frame-selection policy: `all_target_frames`.
- Provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,755,175, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.97 / 6.44 GB.
- Training wall time: 2,295.9 s; validation wall time: 3,358.6 s; total Run wall time: 5,656.4 s.

This is successful finite/resource evidence for the compact spectral/Solar Geometry Input MoE branch under the longer approved budget.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 34. Final epoch 36 regressed from the selected checkpoint, so checkpoint selection matters.

| Metric | ABI-269 best epoch 34 | ABI-269 final epoch 36 |
| --- | ---: | ---: |
| Filtered Dice | 0.410444 | 0.398290 |
| Raw Dice | 0.424777 | 0.413241 |
| Filtered IoU | 0.258213 | 0.248665 |
| Filtered precision | 0.427505 | 0.448145 |
| Filtered recall | 0.394692 | 0.358416 |
| Filtered contrail connectivity | 0.318646 | 0.249918 |
| Filtered predicted-positive fraction | 0.003346 | 0.002898 |
| MIT filtered Dice | 0.394541 | 0.383196 |
| Google filtered Dice | 0.450109 | 0.435739 |
| MIT filtered recall | 0.363423 | 0.329812 |
| Google filtered recall | 0.486141 | 0.442074 |
| Train loss | 0.823579 | 0.827811 |
| Validation loss | 0.876959 | 0.877274 |

At the selected checkpoint, raw Dice was 0.424777 versus filtered Dice 0.410444, and raw recall was 0.422009 versus filtered recall 0.394692. The raw-to-filtered gap is noticeable but not evidence that the branch is primarily Artifact-Filter-dependent.

The fixed `first_n` retained prediction samples all have near-zero per-sample Dice. They are traceability samples from the Harness retention policy, not representative qualitative evidence for the full validation population.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.199212 | 0.219683 | 0.164576 | 0.159824 | 0.264363 | 0.113443 | 0.005994 |
| 4 | 0.314259 | 0.321600 | 0.299696 | 0.274027 | 0.368337 | 0.136596 | 0.004871 |
| 8 | 0.375835 | 0.365450 | 0.400302 | 0.416738 | 0.342243 | 0.288808 | 0.002976 |
| 12 | 0.350443 | 0.333395 | 0.394668 | 0.495318 | 0.271138 | 0.324405 | 0.001984 |
| 15 | 0.391755 | 0.382720 | 0.414126 | 0.393349 | 0.390174 | 0.215169 | 0.003594 |
| 22 | 0.396459 | 0.379268 | 0.439454 | 0.431389 | 0.366762 | 0.258807 | 0.003081 |
| 26 | 0.400548 | 0.383995 | 0.441077 | 0.443859 | 0.364938 | 0.300432 | 0.002979 |
| 28 | 0.402954 | 0.382265 | 0.453439 | 0.446787 | 0.366953 | 0.298861 | 0.002976 |
| 30 | 0.390021 | 0.372526 | 0.434726 | 0.469089 | 0.333764 | 0.438844 | 0.002578 |
| 32 | 0.390804 | 0.386871 | 0.400304 | 0.325085 | 0.489829 | 0.258481 | 0.005460 |
| 33 | 0.400687 | 0.385125 | 0.438702 | 0.413033 | 0.389058 | 0.261630 | 0.003413 |
| 34 | 0.410444 | 0.394541 | 0.450109 | 0.427505 | 0.394692 | 0.318646 | 0.003346 |
| 35 | 0.399396 | 0.380716 | 0.446308 | 0.442933 | 0.363651 | 0.280442 | 0.002975 |
| 36 | 0.398290 | 0.383196 | 0.435739 | 0.448145 | 0.358416 | 0.249918 | 0.002898 |

The longer budget was useful relative to ABI-268: the selected checkpoint improved after the exploratory ceiling rather than merely repeating the parent result. However, the trajectory remained oscillatory. Epoch 30 reached much stronger connectivity with lower recall, epoch 32 reached much higher recall with weak precision and larger predicted-positive fraction, and epoch 34 was the best aggregate balance. The final two epochs declined on aggregate Dice and connectivity.

## Comparison context

| Run | Candidate/context | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_043143_ee0005` | ABI-202 aggregate reference | 34 | 0.427570 | 0.411992 | 0.468151 | 0.439467 | 0.416301 | 0.457773 | 0.003433 |
| `run_20260911_111909_dd7ef7` | ABI-249 C4/rotation-aware comparator | 31 | 0.416400 | 0.396436 | 0.468855 | 0.480886 | 0.367165 | 0.392524 | 0.002767 |
| `run_20260912_065321_ceab64` | ABI-265 selective axial line-memory comparator | 34 | 0.411977 | 0.401437 | 0.438974 | 0.433940 | 0.392130 | 0.433071 | 0.003275 |
| `run_20260910_163616_4f7416` | ABI-232 earlier MoE late36 | 32 | 0.400942 | 0.386542 | 0.439983 | 0.405218 | 0.396756 | 0.383636 | 0.003548 |
| `run_20260912_113911_7a5f94` | ABI-268 compact MoE exploratory parent | 12 | 0.398540 | 0.386144 | 0.429981 | 0.446572 | 0.359837 | 0.360615 | 0.002920 |
| `run_20260912_121857_19f67d` | ABI-269 compact MoE late36 | 34 | 0.410444 | 0.394541 | 0.450109 | 0.427505 | 0.394692 | 0.318646 | 0.003346 |

Relative to ABI-268, ABI-269 improved filtered Dice by +0.011904, MIT Dice by +0.008397, Google Dice by +0.020127, and recall by +0.034855. The cost was lower precision (-0.019067), lower connectivity (-0.041969), and a larger predicted-positive fraction (+0.000426). This supports the late-improving budget request as scientifically useful, but the extension mainly recovered recall/source overlap rather than connected-line strength.

Relative to ABI-232, ABI-269 improved aggregate filtered Dice (+0.009502), MIT Dice (+0.007999), Google Dice (+0.010126), and precision (+0.022287), with a slightly lower predicted-positive fraction. It did not improve recall (-0.002064) and lost substantial connectivity (-0.064990). The compact MoE formulation therefore became the better aggregate MoE result, but not a better line-continuity mechanism.

Relative to ABI-265 and ABI-249, ABI-269 is close on aggregate but behind on the stated line-continuity and precision comparators. It trails ABI-265 by -0.001533 filtered Dice and -0.114425 connectivity, and it trails ABI-249 by -0.005957 filtered Dice, -0.053381 precision, and -0.073878 connectivity. Relative to ABI-202, it remains below the aggregate frontier across filtered Dice, source strata, recall, and connectivity.

## Interpretation

Classify ABI-269 as a positive late-budget family-development result for the compact spectral/Solar Geometry Input MoE branch, but not as a new campaign frontier or promotion candidate. The approved longer budget answered the ABI-268 truncation question: the same compact architecture did improve meaningfully after epoch 12 and surpassed the earlier ABI-232 MoE aggregate/source scores. The Run was finite, resource-safe, non-collapsed, and source-informative.

The weakness is also clear. The best checkpoint improved overlap by sacrificing the parent and ABI-232 connectivity profile. ABI-269 did not become a better connected-line comparator than ABI-265, ABI-249, ABI-223, or ABI-202. The late trajectory shows that high-connectivity and high-recall operating points appeared at different epochs rather than being jointly stabilized by the architecture. That pattern argues against another unchanged late36 continuation of ABI-269 and against treating generic spectral/Solar Geometry Input gating as sufficient for the campaign's remaining thin-line continuity problem.

## Decision

Do not promote ABI-269 and do not request whole-validation diagnostics from this capped Result alone. Retain ABI-269 as the compact spectral/Solar Geometry Input MoE aggregate comparator and evidence that compact MoE gating can improve under the approved late budget, but stop unchanged late36 repeats of ABI-269.

Future MoE work should be mechanism-changing and explicitly tied to connected-line continuity: for example, add an architecture-level line-consensus or orientation-support path that attempts to preserve epoch-30/ABI-265-style connectivity while retaining epoch-34 recall/source balance. If the next step is not such a mechanism change, broaden to another frontier such as C4/orientation prior plus recall support, temporal attention evidence sharpening, or a bounded line-accumulation mechanism.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

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
- `run_20260912_113911_7a5f94/outputs/best_metrics.json` for ABI-268 parent context
- `run_20260910_163616_4f7416/outputs/best_metrics.json` for ABI-232 MoE late36 context
- `run_20260912_065321_ceab64/outputs/best_metrics.json` for ABI-265 selective axial line-memory comparator context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 C4/rotation-aware comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate reference context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
