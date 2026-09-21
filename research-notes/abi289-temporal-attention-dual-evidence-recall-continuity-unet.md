# ABI-289 temporal attention dual-evidence recall/continuity U-Net

research-figures: []

## Scope

This note records ABI-289, Candidate `abi289_temporal_attention_dual_evidence_recall_continuity_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_194511_b462e0`.

ABI-289 was a mechanism-changing temporal-family continuation after ABI-288 and the recent temporal C4 continuity branches. It returned to the resource-profiled ABI-238 temporal-attention directional-context U-Net backbone, but changed the late evidence geometry rather than the trusted loss: center-frame detail/recall evidence and directional continuity evidence stayed in separate full-resolution paths until final logits, with a small bounded non-negative agreement lift intended to raise weak connected contrail evidence at the fixed 0.5 threshold.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-289 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal` with 51 input channels.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,180,894, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.76 / 4.03 GiB.
- Training wall time: 1,150.6 s; validation wall time: 999.4 s; total Run wall time: 2,151.6 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 8.

## Best-validation metrics

| Metric | ABI-289 best epoch 8 | ABI-289 final epoch 12 | ABI-238 temporal directional-context late36 | ABI-223 temporal attention late36 | ABI-285 temporal C4 late36 | ABI-286 continuity bridge | ABI-287 recall-protected bridge | ABI-288 clDice loss scout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.380244 | 0.364914 | 0.420235 | 0.419776 | 0.422195 | 0.393183 | 0.386937 | 0.376321 |
| Raw Dice | 0.394687 | 0.378712 | 0.438718 | 0.438487 | 0.439439 | 0.409514 | 0.403084 | 0.390671 |
| Filtered precision | 0.361568 | 0.362879 | 0.488730 | 0.483764 | 0.448400 | 0.419944 | 0.425221 | 0.381459 |
| Filtered recall | 0.400955 | 0.366973 | 0.368578 | 0.370738 | 0.398883 | 0.369628 | 0.354978 | 0.371320 |
| Filtered connectivity | 0.249988 | 0.188124 | 0.352239 | 0.412427 | 0.243387 | 0.280479 | 0.222259 | 0.237941 |
| MIT filtered Dice | 0.372684 | 0.356206 | 0.405383 | 0.398498 | 0.400831 | 0.381112 | 0.372922 | 0.369607 |
| Google filtered Dice | 0.398412 | 0.385240 | 0.460838 | 0.476764 | 0.477410 | 0.424115 | 0.422601 | 0.392678 |
| Filtered predicted-positive fraction | 0.005733 | 0.005228 | 0.003899 | 0.003962 | 0.004599 | 0.004550 | 0.004316 | 0.005032 |
| Filtered predicted-positive pixels | 606,379 | 552,980 | 412,381 | 419,056 | 486,427 | 481,295 | 456,483 | 532,277 |

ABI-289 produced the intended recall lift but did not preserve precision, source balance, or connected-line organization. Relative to ABI-238, the same-backbone temporal directional-context comparator, ABI-289 is higher on recall by about +0.0324 but lower on filtered Dice by about -0.0400, precision by -0.1272, connectivity by -0.1023, MIT Dice by -0.0327, and Google Dice by -0.0624. Relative to ABI-223, it is similarly recall-positive but much weaker on precision, aggregate/source Dice, and connectivity. Relative to ABI-285, it matches or slightly exceeds recall but falls far below aggregate/source Dice and only marginally exceeds ABI-285's already weak connectivity.

Against the recent negative mechanism tests, ABI-289 is mixed. It improves on ABI-288's selected checkpoint in filtered Dice, recall, and connectivity, so separating recall and continuity evidence is better than the clDice loss-only ABI-238 variant. It remains below ABI-286 and ABI-287 on aggregate filtered Dice, below ABI-286 on connectivity and MIT/Google Dice, and below the temporal comparator band overall. The higher recall came with the broadest filtered predicted-positive footprint in this comparison set, indicating a low-precision, clutter-prone operating point rather than a clean continuity improvement.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.202721 | 0.204845 | 0.198244 | 0.208962 | 0.196843 | 0.147698 | 0.004870 |
| 2 | 0.233762 | 0.231471 | 0.238512 | 0.255103 | 0.215716 | 0.147685 | 0.004371 |
| 3 | 0.270123 | 0.266048 | 0.278902 | 0.309326 | 0.239739 | 0.201658 | 0.004007 |
| 4 | 0.279387 | 0.265470 | 0.311187 | 0.339469 | 0.237374 | 0.204456 | 0.003615 |
| 5 | 0.305399 | 0.289737 | 0.341989 | 0.386918 | 0.252253 | 0.192117 | 0.003370 |
| 6 | 0.334606 | 0.321673 | 0.368260 | 0.441094 | 0.269535 | 0.323055 | 0.003159 |
| 7 | 0.254503 | 0.239958 | 0.292307 | 0.437344 | 0.179471 | 0.259691 | 0.002121 |
| 8 | 0.380244 | 0.372684 | 0.398412 | 0.361568 | 0.400955 | 0.249988 | 0.005733 |
| 9 | 0.375832 | 0.362569 | 0.408435 | 0.366415 | 0.385745 | 0.238766 | 0.005442 |
| 10 | 0.363107 | 0.349635 | 0.394407 | 0.368463 | 0.357904 | 0.220552 | 0.005021 |
| 11 | 0.376417 | 0.363645 | 0.408624 | 0.412944 | 0.345826 | 0.262610 | 0.004329 |
| 12 | 0.364914 | 0.356206 | 0.385240 | 0.362879 | 0.366973 | 0.188124 | 0.005228 |

The trajectory is finite, non-collapsed, and source-informative, but unstable and not convincingly late-improving. Epoch 6 briefly finds the highest connectivity and precision at a compact predicted-positive fraction, but recall and Dice remain low. Epoch 8 is the selected checkpoint and the Run's recall maximum, but it expands the footprint to a filtered predicted-positive fraction of 0.005733 and gives up precision. Epoch 11 partially recovers precision and Google Dice, but with lower recall and still modest connectivity. Epoch 12 regresses in aggregate Dice, source Dice, and connectivity.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3947 versus filtered Dice 0.3802, and raw predicted-positive pixels 653,116 versus filtered predicted-positive pixels 606,379. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3997, 0.2273, 0.5138, and 0.3555. They are consistent with finite non-collapsed predictions, but the weak second retained sample and middling aggregate metrics do not support promotion or a diagnostic request by themselves.

## Interpretation

Classify ABI-289 as a finite, resource-safe, scientifically mixed-to-negative temporal mechanism test. The dual-evidence head did what it was biased to do in one respect: it raised fixed-threshold recall to the ABI-285 range and above ABI-238/223/286/287/288. However, the added evidence was not clean. It materially broadened predicted positives, reduced precision, remained weak on connected-line continuity, and failed to recover the source-stratified Dice of the mature temporal comparators.

The architectural lesson is that late non-negative agreement lifts can recover recall more effectively than ABI-288's loss-only change, but this implementation behaves like a clutter/recall trade-off rather than a continuity solution. It does not justify whole-validation promotion, temporal-eligible failure-bucket diagnostics, or an unchanged late36 continuation. A future follow-up, if any, should be mechanism-changing: constrain the agreement lift with stronger learned cleanliness/center-detail evidence, decouple continuity support from broad mask expansion, or switch away from temporal-attention head variants toward another architecture family or calibration-style evidence head. Any follow-up must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-289. Do not request temporal-eligible or whole-validation failure-bucket diagnostics for this capped temporal-eligible result. Do not request an unchanged late-improving continuation of the ABI-289 dual-evidence head. Treat ABI-289 as evidence that recall can be raised at fixed threshold, but that the tested late agreement lift does not solve precision or connected thin-line continuity.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_194511_b462e0/candidate/PROPOSAL.md`
- `run_20260913_194511_b462e0/candidate/README.md`
- `run_20260913_194511_b462e0/candidate/manifest.yaml`
- `run_20260913_194511_b462e0/resolved_manifest.yaml`
- `run_20260913_194511_b462e0/execution.json`
- `run_20260913_194511_b462e0/outputs/model_summary.json`
- `run_20260913_194511_b462e0/outputs/best_metrics.json`
- `run_20260913_194511_b462e0/outputs/final_metrics.json`
- `run_20260913_194511_b462e0/outputs/metrics.jsonl`
- `run_20260913_194511_b462e0/outputs/resource_profile.json`
- `run_20260913_194511_b462e0/outputs/validation_postprocessing/index.json`
- `run_20260913_194511_b462e0/outputs/prediction_samples/samples.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260913_123056_4152f3/outputs/best_metrics.json` for ABI-286 continuity-bridge comparison context
- `run_20260913_133037_6bd482/outputs/best_metrics.json` for ABI-287 recall-protected bridge comparison context
- `run_20260913_143121_ebfc60/outputs/best_metrics.json` for ABI-288 clDice loss comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi286-temporal-c4-continuity-evidence-bridge-unet.md`
- `/history/research-notes/abi287-temporal-c4-recall-protected-continuity-bridge-unet.md`
- `/history/research-notes/abi288-temporal-attention-directional-context-cldice.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
