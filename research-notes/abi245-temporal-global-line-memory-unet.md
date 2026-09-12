# ABI-245 temporal global line-memory U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-245, Candidate `abi245_temporal_global_line_memory_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_081827_1c0932`.

ABI-245 tested whether a differentiable full-resolution row/column/coarse line-memory module could improve thin-contrail continuity in the provider-owned temporal attention branch. The Candidate consumed trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, cache reads, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-245 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,178,540, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.68 / 3.97 GiB.
- Training wall time: 1,133.2 s; validation wall time: 1,020.3 s; total Run wall time: 2,155.3 s.

This is successful finite/resource evidence for the global line-memory block. Resource use stayed well inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 10, not the final epoch 12.

| Metric | ABI-245 best epoch 10 | ABI-245 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.380155 | 0.345960 |
| Raw Dice | 0.395704 | 0.363357 |
| Filtered IoU | 0.234686 | 0.209160 |
| Filtered precision | 0.390156 | 0.464806 |
| Filtered recall | 0.370654 | 0.275513 |
| Filtered contrail connectivity | 0.239968 | 0.277905 |
| Filtered predicted-positive fraction | 0.004911 | 0.003064 |
| Raw predicted-positive fraction | 0.005287 | 0.003298 |
| MIT filtered Dice | 0.363006 | 0.328405 |
| Google filtered Dice | 0.422177 | 0.390401 |
| MIT filtered recall | 0.335838 | 0.250491 |
| Google filtered recall | 0.474239 | 0.349962 |
| Train loss | 0.805444 | 0.797699 |
| Validation loss | 0.858152 | 0.864775 |

The selected checkpoint is finite, noncollapsed, and source-informative. The final epoch trades lower positive fraction and higher precision for a substantial recall and Dice regression; it is not evidence for a clean late-improving continuation.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.204030 | 0.213358 | 0.213667 | 0.195224 | 0.208959 | 0.193892 | 0.153339 | 0.004723 |
| 2 | 0.233437 | 0.244043 | 0.302266 | 0.190140 | 0.224106 | 0.254677 | 0.196537 | 0.003252 |
| 3 | 0.276851 | 0.286963 | 0.472293 | 0.195819 | 0.259624 | 0.322601 | 0.393508 | 0.002143 |
| 4 | 0.302364 | 0.315730 | 0.444860 | 0.229009 | 0.280239 | 0.357573 | 0.326388 | 0.002661 |
| 5 | 0.319972 | 0.332788 | 0.295599 | 0.348725 | 0.317064 | 0.326360 | 0.150881 | 0.006099 |
| 6 | 0.367801 | 0.383775 | 0.375753 | 0.360179 | 0.351550 | 0.408893 | 0.325859 | 0.004955 |
| 7 | 0.322683 | 0.336525 | 0.514691 | 0.235011 | 0.301137 | 0.378778 | 0.346846 | 0.002360 |
| 8 | 0.370687 | 0.385494 | 0.409458 | 0.338623 | 0.363606 | 0.388492 | 0.218976 | 0.004275 |
| 9 | 0.343371 | 0.357686 | 0.316814 | 0.374787 | 0.328575 | 0.379637 | 0.170963 | 0.006116 |
| 10 | 0.380155 | 0.395704 | 0.390156 | 0.370654 | 0.363006 | 0.422177 | 0.239968 | 0.004911 |
| 11 | 0.340890 | 0.357160 | 0.465787 | 0.268811 | 0.321089 | 0.390760 | 0.280449 | 0.002983 |
| 12 | 0.345960 | 0.363357 | 0.464806 | 0.275513 | 0.328405 | 0.390401 | 0.277905 | 0.003064 |

The trajectory is noisy and peaks before the end of the exploratory budget. Filtered Dice improves from early epochs to epoch 10, then regresses at epochs 11 and 12 as precision rises and recall falls. Connectivity is decoupled from the selected primary metric: its highest value occurs at epoch 3 with low Dice and very low positive fraction, while the selected epoch 10 connectivity is only 0.239968.

## Comparison context

| Metric | ABI-245 global line memory | ABI-244 shifted-window U-NetFormer | ABI-238 temporal directional late36 | ABI-240 temporal line-accum late36 | ABI-223 temporal attention late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_081827_1c0932` | `run_20260911_072719_ade068` | `run_20260911_004137_f54c45` | `run_20260911_031326_43ed12` | `run_20260908_154531_8c7e2b` | `run_20260904_043143_ee0005` |
| Budget | exploratory | exploratory | late36 | late36 | late36 | late36 |
| Best epoch | 10 | 11 | 29 | 29 | 36 | 34 |
| Filtered Dice | 0.380155 | 0.392808 | 0.420235 | 0.414892 | 0.419776 | 0.427570 |
| Raw Dice | 0.395704 | 0.408130 | 0.438718 | 0.431959 | 0.438487 | 0.442746 |
| Filtered precision | 0.390156 | 0.397628 | 0.488730 | 0.436241 | 0.483764 | 0.439467 |
| Filtered recall | 0.370654 | 0.388104 | 0.368578 | 0.395534 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.239968 | 0.290859 | 0.352239 | 0.264863 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.363006 | 0.380020 | 0.405383 | 0.397067 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.422177 | 0.426225 | 0.460838 | 0.460659 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004911 | 0.005046 | 0.003899 | 0.004687 | 0.003962 | 0.003433 |

Relative to ABI-244, ABI-245 lowers selected filtered Dice by -0.012653, MIT filtered Dice by -0.017014, Google filtered Dice by -0.004048, precision by -0.007472, recall by -0.017450, and connectivity by -0.050891. Its filtered predicted-positive fraction is slightly smaller (-0.000135), so the regression is not simply a controlled reduction in overprediction; it loses both overlap and continuity.

Relative to the late36 temporal frontier, ABI-245 remains materially behind ABI-238/223 on filtered Dice and connectivity. It has ABI-238-like recall at the selected checkpoint, but ABI-238 achieves that recall with much higher precision, lower positive fraction, and substantially better connectivity. Relative to ABI-202, ABI-245 is behind by -0.047415 filtered Dice and -0.217805 connectivity.

## Interpretation

Classify ABI-245 as a finite but negative/mixed family-development Result. It supports that full-resolution global line-memory can be trained within the provider-owned temporal tensor and resource limits, but it does not support the hypothesis that this row/column/coarse memory mechanism improves thin-line continuity. The central success criterion was improved connectivity without a predicted-positive blow-up; the selected checkpoint instead has lower connectivity than ABI-244 and ABI-240 and much lower connectivity than ABI-238, ABI-223, or ABI-202.

The exact global line-memory branch should not be extended with a late36 budget: the best checkpoint is not the final epoch, final validation regresses in Dice/recall, and the mechanism misses the stated continuity target. The broader temporal line-continuity family is not eliminated; other mechanisms such as explicitly line-conditioned recurrence, five-frame change modeling, or calibrated temporal confidence may still be worth bounded sequential testing.

## Decision

Do not promote ABI-245 and do not request whole-validation diagnostics from this capped Result alone. Do not request a late36 continuation of the exact ABI-245 global line-memory branch.

Stop this exact row/column/coarse global-memory continuation as a continuity mechanism. A future Candidate should change the mechanism rather than only resize or prolong this block. Plausible next directions include a five-frame temporal change model, a smaller state-space/attention block that operates on line features rather than generic decoder features, or a calibration-oriented temporal architecture that preserves recall without damaging precision and connectivity.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_081827_1c0932/candidate/PROPOSAL.md`
- `run_20260911_081827_1c0932/candidate/README.md`
- `run_20260911_081827_1c0932/candidate/manifest.yaml`
- `run_20260911_081827_1c0932/resolved_manifest.yaml`
- `run_20260911_081827_1c0932/outputs/model_summary.json`
- `run_20260911_081827_1c0932/outputs/best_metrics.json`
- `run_20260911_081827_1c0932/outputs/final_metrics.json`
- `run_20260911_081827_1c0932/outputs/metrics.jsonl`
- `run_20260911_081827_1c0932/outputs/resource_profile.json`
- `run_20260911_081827_1c0932/outputs/validation_postprocessing/index.json`
- `run_20260911_081827_1c0932/outputs/prediction_samples/samples.json`
- `run_20260911_072719_ade068` for ABI-244 shifted-window temporal U-NetFormer context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
