# ABI-304 temporal five-frame additive recall line-consensus U-Net

research-figures: []

## Scope

This note records ABI-304, Candidate `abi304_temporal_fiveframe_additive_recall_line_consensus_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_110002_f591b9`.

ABI-304 was a bounded temporal family-development continuation after ABI-291 and ABI-300. It used the provider-owned five-frame temporal window `[-2, -1, 0, 1, 2]` to test additive recall support from learned temporal attention, short/long temporal differences, and line/detail/scale consensus. The intended mechanism was to raise true contrail evidence at the fixed Harness threshold without repeating ABI-291's compact hard-persistence under-recall or ABI-296/299's broader local-correlation clutter.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Execution result

ABI-304 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-2, -1, 0, 1, 2]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 3,243,445, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,836,509,696 / 6,094,323,712 bytes.
- Training wall time: 1,518.8 s; validation wall time: 1,126.7 s; total Run wall time: 2,647.2 s, within the exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-304 five-frame additive recall | ABI-291 five-frame persistence | ABI-300 evidence-sharpened attention | ABI-299 correlation line-continuity | ABI-296 local correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 10 | 10 | 9 | 9 | 36 | 29 | 32 |
| Filtered Dice | 0.380635 | 0.358719 | 0.370607 | 0.396406 | 0.395208 | 0.419776 | 0.420235 | 0.422195 |
| MIT filtered Dice | 0.364758 | 0.336776 | 0.357208 | 0.383650 | 0.379768 | 0.398498 | 0.405383 | 0.400831 |
| Google filtered Dice | 0.420799 | 0.414922 | 0.403910 | 0.428424 | 0.433397 | 0.476764 | 0.460838 | 0.477410 |
| Filtered precision | 0.432089 | 0.495053 | 0.420466 | 0.408439 | 0.389486 | 0.483764 | 0.488730 | 0.448400 |
| Filtered recall | 0.340132 | 0.281261 | 0.331319 | 0.385063 | 0.401101 | 0.370738 | 0.368578 | 0.398883 |
| Filtered connectivity | 0.265446 | 0.295736 | 0.242191 | 0.268913 | 0.331894 | 0.412427 | 0.352239 | 0.243387 |
| Filtered predicted-positive fraction | 0.004069 | 0.002937 | 0.004074 | 0.004874 | 0.005324 | 0.003962 | 0.003899 | 0.004599 |
| Filtered predicted-positive pixels | 430,439 | 310,668 | 430,877 | 515,517 | 563,119 | 419,056 | 412,381 | 486,427 |

ABI-304 is a completed mixed-to-negative temporal result. It improves over the immediate conservative baselines ABI-291 and ABI-300, but it does not recover the ABI-223/238/285 temporal frontier and does not match the stronger ABI-296/299 local-correlation branch.

Relative to ABI-300, ABI-304 improves filtered Dice by about +0.0100, MIT Dice by +0.0076, Google Dice by +0.0169, precision by +0.0116, recall by +0.0088, and connectivity by +0.0233 at essentially the same filtered footprint. This means the five-frame additive design is a better operating point than the three-frame evidence-sharpening head it followed.

Relative to ABI-291, ABI-304 raises filtered Dice by about +0.0219 and recall by +0.0589 while expanding the filtered footprint from 310,668 to 430,439 pixels. That is directionally consistent with the proposal's goal of escaping hard-persistence under-recall. However, it loses precision by about -0.0630 and connectivity by about -0.0303, so the added recall support is not organized into a stronger connected-line result.

Relative to ABI-296/299, ABI-304 remains below by about -0.0146 to -0.0158 filtered Dice and by -0.0449 to -0.0610 recall. Its footprint is smaller and precision is higher than both, but connectivity only slightly trails ABI-299 and remains well below ABI-296. Relative to ABI-223/238/285, ABI-304 is still far from the temporal frontier: it trails by about -0.0391 to -0.0416 filtered Dice, -0.0306 to -0.0588 recall, and, except against ABI-285, materially worse connectivity. The result does not establish five-frame additive support as a frontier-improving mechanism.

At the selected checkpoint, raw Dice was 0.397588 versus filtered Dice 0.380635, raw recall was 0.367377 versus filtered recall 0.340132, and raw predicted-positive fraction was 0.004384 versus filtered predicted-positive fraction 0.004069. Artifact Filters reduce some footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212622 | 0.220615 | 0.197196 | 0.194151 | 0.234978 | 0.127940 | 0.006257 |
| 2 | 0.234483 | 0.218638 | 0.272173 | 0.349892 | 0.176324 | 0.237851 | 0.002605 |
| 3 | 0.291186 | 0.275734 | 0.329464 | 0.379810 | 0.236096 | 0.222795 | 0.003213 |
| 4 | 0.264671 | 0.243130 | 0.319990 | 0.442654 | 0.188771 | 0.230031 | 0.002205 |
| 5 | 0.286969 | 0.261701 | 0.348977 | 0.422154 | 0.217364 | 0.287475 | 0.002662 |
| 6 | 0.355918 | 0.355654 | 0.356528 | 0.343694 | 0.369043 | 0.184688 | 0.005551 |
| 7 | 0.293147 | 0.267420 | 0.358211 | 0.449846 | 0.217413 | 0.229424 | 0.002498 |
| 8 | 0.360752 | 0.351450 | 0.383706 | 0.372882 | 0.349387 | 0.187441 | 0.004844 |
| 9 | 0.367806 | 0.353135 | 0.403365 | 0.370914 | 0.364749 | 0.256348 | 0.005084 |
| 10 | 0.342633 | 0.317126 | 0.408293 | 0.457307 | 0.273941 | 0.323453 | 0.003097 |
| 11 | 0.363368 | 0.340193 | 0.421083 | 0.417199 | 0.321840 | 0.253465 | 0.003988 |
| 12 | 0.380635 | 0.364758 | 0.420799 | 0.432089 | 0.340132 | 0.265446 | 0.004069 |

The trajectory is finite, non-collapsed, and source-informative. The best checkpoint occurs at the final exploratory epoch, and epochs 11-12 recover from the epoch-10 precision-heavy dip. That is weak evidence that the branch had not fully plateaued at the 12-epoch budget.

However, the trajectory is also oscillatory: epoch 6 and epoch 9 have higher recall with wider footprints and weaker precision, epoch 10 has the best connectivity but low recall, and epoch 12 selects a moderate compromise. This looks more like another temporal precision/recall/connectivity trade-off surface than a clean, monotonic emergence of connected recall. The late final-epoch improvement is therefore not by itself enough to treat ABI-304 as a promotion candidate or to request diagnostics.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4290, 0.2967, 0.5359, and 0.4069. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-304 as a finite, resource-safe, scientifically useful mixed result for five-frame additive temporal recall support. It shows that additive five-frame evidence can improve on ABI-291's compact persistence and ABI-300's conservative evidence-sharpening head, but it still fails to deliver the intended combination of temporal recall and connected-line organization. The model remains below ABI-296/299 on recall and filtered Dice, and far below ABI-223/238 on temporal-attention precision/connectivity balance.

This does not eliminate temporal modeling as a family. ABI-223/238/285 remain useful temporal comparators, and ABI-304's final-epoch best checkpoint means the exact branch is not a collapsed dead end. But the scientific signal is not strong enough to justify promotion, whole-validation diagnostics, or a claim that five-frame additive support solved the campaign's fixed-threshold recall/connectivity failure mode.

A future follow-up, if chosen, should be framed as bounded family development rather than promotion. It should either materially change the continuity mechanism that organizes the recovered recall, or explicitly justify a late-improving budget from ABI-304's final-epoch best checkpoint while acknowledging the current connectivity and frontier gap. Avoid another minor additive-head tweak that merely slides along the same precision/recall footprint trade-off.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-304. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not treat it as a frontier result relative to ABI-223/238/285.

Record ABI-304 as bounded mixed evidence: better than ABI-291/300 conservative temporal heads, but still behind the temporal and local-correlation comparators on the intended recall/connectivity trade-off. A later close-continuation would need an explicit late-improving or mechanism-changing rationale; no such Candidate is created in this Autonomy Step.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_110002_f591b9/candidate/PROPOSAL.md`
- `run_20260914_110002_f591b9/candidate/README.md`
- `run_20260914_110002_f591b9/candidate/manifest.yaml`
- `run_20260914_110002_f591b9/resolved_manifest.yaml`
- `run_20260914_110002_f591b9/execution.json`
- `run_20260914_110002_f591b9/outputs/model_summary.json`
- `run_20260914_110002_f591b9/outputs/best_metrics.json`
- `run_20260914_110002_f591b9/outputs/final_metrics.json`
- `run_20260914_110002_f591b9/outputs/metrics.jsonl`
- `run_20260914_110002_f591b9/outputs/resource_profile.json`
- `run_20260914_110002_f591b9/outputs/validation_postprocessing/index.json`
- `run_20260914_110002_f591b9/outputs/prediction_samples/samples.json`
- `run_20260913_211453_8c6c4e/outputs/best_metrics.json` and `/history/research-notes/abi291-temporal-fiveframe-persistence-attention-directional-unet.md` for ABI-291 five-frame persistence context
- `run_20260914_050146_4e9b36/outputs/best_metrics.json` and `/history/research-notes/abi300-temporal-attention-evidence-sharpened-recall-unet.md` for ABI-300 evidence-sharpening context
- `run_20260914_040326_98380c/outputs/best_metrics.json` and `/history/research-notes/abi299-temporal-correlation-line-continuity-decoder-unet.md` for ABI-299 temporal-correlation comparison context
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 temporal C4 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
