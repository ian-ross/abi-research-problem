# ABI-296 temporal local-correlation center-detail U-Net

research-figures: []

## Scope

This note records ABI-296, Candidate `abi296_temporal_local_correlation_center_detail_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_010510_9ea033`.

ABI-296 was a bounded temporal family-development scout. It tested a mechanism-changing pivot away from recent temporal-attention and persistence variants by computing differentiable 3x3 local-correlation volumes between projected center-frame features and previous/next-frame features. The intended mechanism was to allow small neighbor-frame displacement while preserving center-frame spectral/BTD/Solar Geometry Input detail and directional line evidence.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-296 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 5,742,791, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.99 / 6.30 GiB.
- Training wall time: 1,537.1 s; validation wall time: 1,178.5 s; total Run wall time: 2,717.5 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-296 local correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-274 line-state attention late36 | ABI-285 temporal C4 line-state late36 | ABI-289 dual-evidence temporal | ABI-290 precision-gated temporal | ABI-291 five-frame persistence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 36 | 29 | 36 | 32 | 8 | 9 | 10 |
| Filtered Dice | 0.395208 | 0.419776 | 0.420235 | 0.419364 | 0.422195 | 0.380244 | 0.379803 | 0.358719 |
| MIT filtered Dice | 0.379768 | 0.398498 | 0.405383 | 0.399386 | 0.400831 | 0.372684 | 0.368809 | 0.336776 |
| Google filtered Dice | 0.433397 | 0.476764 | 0.460838 | 0.472606 | 0.477410 | 0.398412 | 0.406267 | 0.414922 |
| Filtered precision | 0.389486 | 0.483764 | 0.488730 | 0.454127 | 0.448400 | 0.361568 | 0.384437 | 0.495053 |
| Filtered recall | 0.401101 | 0.370738 | 0.368578 | 0.389545 | 0.398883 | 0.400955 | 0.375279 | 0.281261 |
| Filtered connectivity | 0.331894 | 0.412427 | 0.352239 | 0.282911 | 0.243387 | 0.249988 | 0.245732 | 0.295736 |
| Filtered predicted-positive fraction | 0.005324 | 0.003962 | 0.003899 | 0.004434 | 0.004599 | 0.005733 | 0.005046 | 0.002937 |

ABI-296 is a useful but non-frontier temporal result. It succeeds at one stated target: relative to ABI-289/290/291, local correlation recovers a stronger recall/continuity balance. Its selected recall is close to ABI-289 while connectivity is materially higher, and it avoids ABI-291's compact underprediction. It also has better connectivity than the late36 ABI-274/285 temporal line-state/C4 variants, which were high-Dice but weak on continuity.

The improvement is not enough to displace the temporal frontier. ABI-296 trails ABI-223/238/285 by about 0.025 to 0.027 filtered Dice and is lower on both MIT and Google filtered Dice. Its recall is slightly higher than ABI-223/238 and near ABI-285, but the gain comes with lower precision and a broader filtered footprint. Google remains substantially stronger than MIT, and the MIT filtered Dice of 0.3798 is below the stronger temporal comparators.

Against the hypothesis, the local 3x3 correlation mechanism appears to raise fixed-threshold support better than the most recent temporal negative controls, but it does not provide the clean evidence sharpening needed to match ABI-223/238/285. The selected state is recall-positive and finite, not collapsed, but not promotion-level.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.220652 | 0.214665 | 0.236036 | 0.288891 | 0.178491 | 0.181802 | 0.003194 |
| 2 | 0.324396 | 0.311024 | 0.357684 | 0.416171 | 0.265784 | 0.263208 | 0.003302 |
| 3 | 0.337792 | 0.329074 | 0.356906 | 0.347180 | 0.328897 | 0.217972 | 0.004897 |
| 4 | 0.337941 | 0.312652 | 0.403625 | 0.497645 | 0.255837 | 0.381242 | 0.002658 |
| 5 | 0.364412 | 0.341440 | 0.422021 | 0.502101 | 0.285987 | 0.387842 | 0.002944 |
| 6 | 0.388545 | 0.368633 | 0.439049 | 0.454256 | 0.339442 | 0.373884 | 0.003863 |
| 7 | 0.377793 | 0.353877 | 0.440036 | 0.506950 | 0.301085 | 0.430131 | 0.003070 |
| 8 | 0.364855 | 0.344371 | 0.415241 | 0.433030 | 0.315227 | 0.298900 | 0.003763 |
| 9 | 0.395208 | 0.379768 | 0.433397 | 0.389486 | 0.401101 | 0.331894 | 0.005324 |
| 10 | 0.382859 | 0.360975 | 0.439955 | 0.501280 | 0.309697 | 0.393094 | 0.003194 |
| 11 | 0.390829 | 0.368608 | 0.448369 | 0.513237 | 0.315565 | 0.436968 | 0.003179 |
| 12 | 0.378368 | 0.354548 | 0.438457 | 0.506969 | 0.301809 | 0.402327 | 0.003078 |

The trajectory is finite and source-informative, but it oscillates between broader high-recall states and compact high-precision/connectivity states. Epoch 9 is selected because it reaches the best aggregate filtered Dice with the strongest recall. Epochs 10-12 improve precision and connectivity but lose enough recall and MIT Dice to reduce the primary metric. This is not convincing late-improving evidence for an unchanged late36 continuation; the selected best occurs before the final quarter, and later behavior moves along the familiar temporal precision/recall curve rather than steadily improving.

Raw-to-filtered differences are modest at the selected checkpoint: raw Dice 0.4103 versus filtered Dice 0.3952, raw recall 0.4333 versus filtered recall 0.4011, and filtered predicted-positive fraction 0.005324. Artifact Filters remove some footprint, but they do not create the result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3155, 0.8000, 0.6239, and 0.4846. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-296 as a completed, resource-safe, scientifically useful temporal family-development scout, but not a frontier or promotion candidate. The local-correlation mechanism is better than recent failed temporal dual-evidence, precision-gated, and five-frame persistence variants at balancing recall and continuity. It therefore provides positive evidence that explicit small-displacement neighbor matching is a more promising temporal support primitive than those exact recent branches.

However, the mechanism still falls short of the stronger temporal comparators. Its recall gain does not overcome lower precision, broader predictions, weaker Google Dice than ABI-223/285, and weaker MIT Dice than ABI-238/285. The result does not justify whole-validation diagnostics or an unchanged late36 request.

Future temporal work should be mechanism-changing rather than a direct late36 continuation of ABI-296. A reasonable next temporal hypothesis would keep the useful center-detail protection but constrain local-correlation support with orientation-aware or agreement-gated evidence so that the recall lift does not require the wider footprint seen at epoch 9. Alternatively, broaden outside temporal local matching if the next proposal cannot state a specific precision-preserving recall or connectivity mechanism.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-296. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not request an unchanged late36 continuation of this exact local-correlation design; the exploratory run completed, peaked at epoch 9, and then oscillated toward compact lower-recall checkpoints.

Keep temporal local correlation as a partially useful mechanism: it improved over ABI-289/290/291 and raised continuity over ABI-274/285, but it needs a new precision-preserving or orientation-aware constraint before another Run is worth spending. Prefer a mechanism-changing temporal continuation or a broadened architecture family for the next handoff.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_010510_9ea033/candidate/PROPOSAL.md`
- `run_20260914_010510_9ea033/candidate/README.md`
- `run_20260914_010510_9ea033/candidate/manifest.yaml`
- `run_20260914_010510_9ea033/resolved_manifest.yaml`
- `run_20260914_010510_9ea033/execution.json`
- `run_20260914_010510_9ea033/outputs/model_summary.json`
- `run_20260914_010510_9ea033/outputs/best_metrics.json`
- `run_20260914_010510_9ea033/outputs/final_metrics.json`
- `run_20260914_010510_9ea033/outputs/metrics.jsonl`
- `run_20260914_010510_9ea033/outputs/resource_profile.json`
- `run_20260914_010510_9ea033/outputs/validation_postprocessing/index.json`
- `run_20260914_010510_9ea033/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 temporal C4 comparison context
- `run_20260913_194511_b462e0/outputs/best_metrics.json` and `/history/research-notes/abi289-temporal-attention-dual-evidence-recall-continuity-unet.md` for ABI-289 comparison context
- `run_20260913_202938_44793e/outputs/best_metrics.json` and `/history/research-notes/abi290-temporal-attention-precision-gated-continuity-unet.md` for ABI-290 comparison context
- `run_20260913_211453_8c6c4e/outputs/best_metrics.json` and `/history/research-notes/abi291-temporal-fiveframe-persistence-attention-directional-unet.md` for ABI-291 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
