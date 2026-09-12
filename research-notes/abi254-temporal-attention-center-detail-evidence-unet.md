# ABI-254 temporal attention center-detail evidence U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-254, Candidate `abi254_temporal_attention_center_detail_evidence_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_202724_fee837`.

ABI-254 was a mechanism-changing temporal continuation after ABI-223 diagnostics. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. The architectural change was a center-detail evidence bridge that fuses center-frame detail features, broad temporal support, horizontal/vertical line cues, and high-resolution encoder support before the mask head. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-254 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned temporal offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,192,772, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.79 / 4.13 GB.
- Training wall time: 1,096.4 s; validation wall time: 1,003.1 s; total Run wall time: 2,101.2 s.

This is valid finite/resource evidence for the center-detail bridge branch. Resource cost is higher than ABI-223 per epoch but remains well inside the exploratory timeout and memory limits.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 10. The final epoch 12 stayed finite but regressed materially on filtered Dice and recall.

| Metric | ABI-254 best epoch 10 | ABI-254 final epoch 12 | ABI-222 12ep attention | ABI-223 late36 attention |
| --- | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.393943 | 0.356952 | 0.374329 | 0.419776 |
| Raw Dice | 0.412509 | 0.375625 | 0.392066 | 0.438487 |
| Filtered precision | 0.486613 | 0.524723 | 0.466148 | 0.483764 |
| Filtered recall | 0.330922 | 0.270473 | 0.312729 | 0.370738 |
| Filtered connectivity | 0.365528 | 0.375960 | 0.281396 | 0.412427 |
| MIT filtered Dice | 0.377873 | 0.334517 | 0.357658 | 0.398498 |
| Google filtered Dice | 0.436096 | 0.416608 | 0.416510 | 0.476764 |
| Filtered predicted-positive fraction | 0.003516 | 0.002665 | 0.003468 | 0.003962 |

Relative to the earlier 12-epoch ABI-222 temporal-attention scout, ABI-254 improves filtered Dice by about +0.0196, raw Dice by +0.0204, precision by +0.0205, recall by +0.0182, connectivity by +0.0841, MIT filtered Dice by +0.0202, and Google filtered Dice by +0.0196 at its selected epoch. Thus the center-detail bridge is not a failed idea at the exploratory budget.

Relative to ABI-223, however, ABI-254 remains lower by about -0.0258 filtered Dice, -0.0398 recall, -0.0469 connectivity, -0.0206 MIT Dice, and -0.0407 Google Dice. The only near-tie is precision. ABI-254 therefore does not supersede the ABI-223 temporal-family comparator.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.190782 | 0.203211 | 0.167920 | 0.166907 | 0.222629 | 0.112112 | 0.006895 |
| 3 | 0.290047 | 0.282088 | 0.307222 | 0.313373 | 0.269954 | 0.177860 | 0.004453 |
| 6 | 0.315664 | 0.320283 | 0.305550 | 0.240393 | 0.459560 | 0.151748 | 0.009883 |
| 8 | 0.346179 | 0.328205 | 0.391798 | 0.452714 | 0.280233 | 0.181998 | 0.003200 |
| 10 | 0.393943 | 0.377873 | 0.436096 | 0.486613 | 0.330922 | 0.365528 | 0.003516 |
| 11 | 0.388195 | 0.373050 | 0.425542 | 0.406763 | 0.371248 | 0.173558 | 0.004718 |
| 12 | 0.356952 | 0.334517 | 0.416608 | 0.524723 | 0.270473 | 0.375960 | 0.002665 |

The trajectory is oscillatory. Epoch 10 is the best aggregate compromise, epoch 11 trades precision for recall, and epoch 12 becomes a conservative high-precision/low-recall endpoint. This is not strong late-improving evidence under the current late-budget policy because the selected checkpoint occurs before the exploratory ceiling and the final checkpoint is worse on the primary metric. The bridge appears to add useful evidence early but does not stabilize the temporal-attention branch by itself.

## Interpretation

Classify ABI-254 as a finite mixed temporal-family result. The center-detail evidence bridge improved over the original 12-epoch temporal-attention scout and preserved source-informative behavior, so the mechanism is not disproven. But it did not improve over ABI-223, did not create a new capped frontier, and did not show a trajectory that justifies an exact late36 continuation.

The main failure mode is recall/coverage instability rather than collapse. At its best epoch, ABI-254 has compact predicted-positive area and reasonable precision, but recall remains below ABI-223 and the final epoch prunes too aggressively. This matches ABI-223 diagnostics: temporal models have useful lower-confidence evidence, but candidate-side thresholding is not allowed; the architecture must raise true contrail logits without sacrificing MIT and positive-patch coverage.

## Decision

Do not promote ABI-254 and do not request a late-improving continuation of this exact center-detail bridge. Retain ABI-223 as the temporal-family comparator and ABI-202/ABI-249 as whole-validation reference points.

A future temporal step should be mechanism-changing rather than an epoch repeat: for example, a recall-preserving temporal detail/logit calibration head, a compact dual-head agreement design over temporal features, or a stronger motion/change stream that targets threshold-0.5 recall and connectivity while keeping provider-owned temporal inputs and Harness-owned metrics/Artifact Filters. If the next step broadens outside temporal modeling, use ABI-254 as evidence that simply adding a high-resolution detail bridge to temporal attention is insufficient without a more stable evidence-raising mechanism.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_202724_fee837/candidate/PROPOSAL.md`
- `run_20260911_202724_fee837/candidate/README.md`
- `run_20260911_202724_fee837/candidate/manifest.yaml`
- `run_20260911_202724_fee837/resolved_manifest.yaml`
- `run_20260911_202724_fee837/outputs/model_summary.json`
- `run_20260911_202724_fee837/outputs/best_metrics.json`
- `run_20260911_202724_fee837/outputs/final_metrics.json`
- `run_20260911_202724_fee837/outputs/metrics.jsonl`
- `run_20260911_202724_fee837/outputs/resource_profile.json`
- `run_20260911_202724_fee837/outputs/validation_postprocessing/index.json`
- `run_20260911_202724_fee837/outputs/prediction_samples/samples.json`
- `run_20260908_150315_9aea3f` for ABI-222 temporal-attention 12-epoch context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `run_20260911_111909_dd7ef7` for ABI-249 high-precision C4 comparator context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
