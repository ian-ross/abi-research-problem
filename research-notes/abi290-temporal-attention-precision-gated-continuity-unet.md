# ABI-290 temporal attention precision-gated continuity U-Net

research-figures: []

## Scope

This note records ABI-290, Candidate `abi290_temporal_attention_precision_gated_continuity_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_202938_44793e`.

ABI-290 was a mechanism-changing temporal-family continuation after ABI-289. ABI-289 showed that a late center-detail plus directional-continuity lift can raise fixed-threshold recall, but at the cost of broad predicted-positive footprint, low precision, source imbalance, and weak connected-line organization. ABI-290 kept the same provider-owned temporal-attention U-Net family and replaced the permissive non-negative lift with a learned precision-gated continuity lift plus a small learned clutter-veto residual initialized conservatively.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-290 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal` with 51 input channels.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,180,945, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.77 / 4.03 GiB.
- Training wall time: 1,175.5 s; validation wall time: 1,014.9 s; total Run wall time: 2,192.1 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-290 best epoch 9 | ABI-290 final epoch 12 | ABI-289 dual-evidence parent | ABI-238 temporal directional-context late36 | ABI-223 temporal attention late36 | ABI-285 temporal C4 late36 | ABI-286 continuity bridge | ABI-287 recall-protected bridge | ABI-288 clDice loss scout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.379803 | 0.343244 | 0.380244 | 0.420235 | 0.419776 | 0.422195 | 0.393183 | 0.386937 | 0.376321 |
| Raw Dice | 0.394762 | 0.361381 | 0.394687 | 0.438718 | 0.438487 | 0.439439 | 0.409514 | 0.403084 | 0.390671 |
| Filtered precision | 0.384437 | 0.519917 | 0.361568 | 0.488730 | 0.483764 | 0.448400 | 0.419944 | 0.425221 | 0.381459 |
| Filtered recall | 0.375279 | 0.256189 | 0.400955 | 0.368578 | 0.370738 | 0.398883 | 0.369628 | 0.354978 | 0.371320 |
| Filtered connectivity | 0.245732 | 0.311644 | 0.249988 | 0.352239 | 0.412427 | 0.243387 | 0.280479 | 0.222259 | 0.237941 |
| MIT filtered Dice | 0.368809 | 0.319498 | 0.372684 | 0.405383 | 0.398498 | 0.400831 | 0.381112 | 0.372922 | 0.369607 |
| Google filtered Dice | 0.406267 | 0.406466 | 0.398412 | 0.460838 | 0.476764 | 0.477410 | 0.424115 | 0.422601 | 0.392678 |
| Filtered predicted-positive fraction | 0.005046 | 0.002547 | 0.005733 | 0.003899 | 0.003962 | 0.004599 | 0.004550 | 0.004316 | 0.005032 |
| Filtered predicted-positive pixels | 533,786 | 269,441 | 606,379 | 412,381 | 419,056 | 486,427 | 481,295 | 456,483 | 532,277 |

ABI-290 partially achieved the intended cleanliness shift relative to ABI-289: at the selected checkpoint it improved filtered precision by about +0.0229 and reduced filtered predicted-positive pixels by 72,593 while retaining non-collapsed source-informative predictions. However, it paid for that precision gate with lower recall (-0.0257), slightly lower aggregate filtered Dice (-0.0004), slightly lower MIT Dice (-0.0039), and essentially unchanged weak connectivity (-0.0043). Google filtered Dice improved over ABI-289 by about +0.0079, but remained far below ABI-238/223/285.

Relative to the mature temporal comparators, ABI-290 remains below the ABI-238/223/285 band on aggregate filtered Dice by about 0.040 to 0.042. It also remains below ABI-238/223 on precision, source Dice, and connected-line continuity. ABI-290 has similar selected-checkpoint recall to ABI-238/223 but reaches it with a larger filtered predicted-positive footprint and weaker connectivity, so the precision gate did not turn the ABI-289 recall mechanism into a competitive connected-line solution.

Against recent local temporal mechanism tests, ABI-290 is mixed. It is slightly better than ABI-288 in aggregate filtered Dice and Google Dice, but similar in footprint and lower on MIT Dice. It is below ABI-286 and ABI-287 on aggregate/source Dice, and below ABI-286 on connectivity. The final epoch becomes much more compact and high-precision, with filtered precision 0.5199 and predicted-positive fraction 0.00255, but recall collapses to 0.2562 and filtered Dice drops to 0.3432.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.207069 | 0.210511 | 0.199906 | 0.217132 | 0.197898 | 0.145802 | 0.004712 |
| 2 | 0.244222 | 0.252567 | 0.227361 | 0.237374 | 0.251478 | 0.149999 | 0.005477 |
| 3 | 0.262240 | 0.248609 | 0.292592 | 0.345331 | 0.211380 | 0.196187 | 0.003164 |
| 4 | 0.289053 | 0.270709 | 0.334918 | 0.438528 | 0.215573 | 0.235172 | 0.002541 |
| 5 | 0.321182 | 0.304088 | 0.363493 | 0.432368 | 0.255483 | 0.271710 | 0.003055 |
| 6 | 0.351053 | 0.339528 | 0.377483 | 0.352917 | 0.349208 | 0.236591 | 0.005115 |
| 7 | 0.350445 | 0.324173 | 0.420955 | 0.503562 | 0.268732 | 0.426454 | 0.002759 |
| 8 | 0.378638 | 0.363191 | 0.417104 | 0.417439 | 0.346437 | 0.260598 | 0.004290 |
| 9 | 0.379803 | 0.368809 | 0.406267 | 0.384437 | 0.375279 | 0.245732 | 0.005046 |
| 10 | 0.329812 | 0.312060 | 0.371374 | 0.399283 | 0.280932 | 0.196740 | 0.003637 |
| 11 | 0.375648 | 0.355933 | 0.426568 | 0.469432 | 0.313097 | 0.371464 | 0.003448 |
| 12 | 0.343244 | 0.319498 | 0.406466 | 0.519917 | 0.256189 | 0.311644 | 0.002547 |

The trajectory is finite, non-collapsed, and source-informative, but unstable rather than convincingly late-improving. The model alternates between compact high-precision/low-recall states and broader recall states. Epoch 7 is scientifically interesting because it briefly reaches high precision and the strongest connectivity seen in the Run, but aggregate Dice and recall are low. Epochs 8-9 raise recall and aggregate Dice, but lose much of the compactness and connectivity. Epochs 11-12 recover precision and connectivity partly, especially on Google, but recall and aggregate Dice fall.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3948 versus filtered Dice 0.3798, and raw predicted-positive pixels 574,820 versus filtered predicted-positive pixels 533,786. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2561, 0.1603, 0.5806, and 0.3898. They are consistent with finite non-collapsed predictions, but the weak first two retained samples and the below-comparator aggregate metrics do not support promotion or a diagnostic request by themselves.

## Interpretation

Classify ABI-290 as a finite, resource-safe, scientifically mixed-to-negative temporal mechanism test. The precision gate did reduce the ABI-289 footprint and improved selected-checkpoint precision, and the Run exposed a potentially useful compact high-connectivity operating mode around epoch 7. However, the selected checkpoint did not materially improve aggregate Dice or connected-line continuity over ABI-289, remained weaker than ABI-286/287 on aggregate Dice, and stayed far below ABI-238/223/285 temporal comparators.

The architectural lesson is that making the late continuity lift conditional on learned agreement can constrain clutter, but in this implementation the constraint trades away recall rather than producing clean connected evidence at the fixed 0.5 threshold. The model appears to move along a precision/recall operating curve across epochs rather than learning a stable high-Dice, high-connectivity temporal representation. This does not justify whole-validation promotion, temporal-eligible failure-bucket diagnostics, or an unchanged late36 continuation.

A future follow-up, if any, should be mechanism-changing rather than a longer run of the same precision-gated head. Useful next hypotheses would need to preserve the compact high-precision/high-connectivity state while maintaining the epoch-8/9 recall level, for example through a better-calibrated dual-operating-point architecture head, earlier continuity-aware feature sharing, or a different temporal evidence family. Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-290. Do not request temporal-eligible or whole-validation failure-bucket diagnostics for this capped temporal-eligible result. Do not request an unchanged late-improving continuation of the ABI-290 precision-gated continuity head. Treat ABI-290 as evidence that agreement gating can reduce the ABI-289 clutter footprint, but that this tested gate does not solve the recall/connectivity trade-off.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_202938_44793e/candidate/PROPOSAL.md`
- `run_20260913_202938_44793e/candidate/README.md`
- `run_20260913_202938_44793e/candidate/manifest.yaml`
- `run_20260913_202938_44793e/resolved_manifest.yaml`
- `run_20260913_202938_44793e/execution.json`
- `run_20260913_202938_44793e/outputs/model_summary.json`
- `run_20260913_202938_44793e/outputs/best_metrics.json`
- `run_20260913_202938_44793e/outputs/final_metrics.json`
- `run_20260913_202938_44793e/outputs/metrics.jsonl`
- `run_20260913_202938_44793e/outputs/resource_profile.json`
- `run_20260913_202938_44793e/outputs/validation_postprocessing/index.json`
- `run_20260913_202938_44793e/outputs/prediction_samples/samples.json`
- `run_20260913_194511_b462e0/outputs/best_metrics.json` for ABI-289 parent comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260913_123056_4152f3/outputs/best_metrics.json` for ABI-286 continuity-bridge comparison context
- `run_20260913_133037_6bd482/outputs/best_metrics.json` for ABI-287 recall-protected bridge comparison context
- `run_20260913_143121_ebfc60/outputs/best_metrics.json` for ABI-288 clDice loss comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi289-temporal-attention-dual-evidence-recall-continuity-unet.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
