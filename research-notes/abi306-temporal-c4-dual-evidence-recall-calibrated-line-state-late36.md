# ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 U-Net

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-306, Candidate `abi306_temporal_c4_dual_evidence_recall_calibrated_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260914_124245_de843c`.

ABI-306 was a mechanism-changing continuation of the ABI-285 temporal C4 orientation line-state branch. ABI-285 was the strongest capped temporal-eligible aggregate filtered-Dice comparator but achieved that by favoring recall over connected-line continuity. ABI-306 kept the provider-owned three-frame temporal C4 line-state backbone and replaced the simple segmentation head with an internal dual-evidence recall-calibrated head: base mask logits plus a bounded residual gated by decoder features and internal mask/Line/Centerline evidence.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection. It used trusted `combined_source_balanced` sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-306 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Direct parent/comparator: ABI-285, `run_20260913_100333_a250df`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,245,655, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.50 / 5.83 GiB.
- Training wall time: 4,565.9 s; validation wall time: 3,303.6 s; total Run wall time: 7,871.6 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-306 dual-evidence temporal C4 | ABI-285 temporal C4 line-state | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-255 recurrent temporal | ABI-305 calibrated temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 32 | 36 | 29 | 36 | 11 |
| Filtered Dice | 0.422548 | 0.422195 | 0.419776 | 0.420235 | 0.417348 | 0.386468 |
| Raw Dice | 0.441449 | 0.439439 | 0.438487 | 0.438718 | 0.435656 | 0.402748 |
| MIT filtered Dice | 0.402764 | 0.400831 | 0.398498 | 0.405383 | 0.400833 | 0.366658 |
| Google filtered Dice | 0.476152 | 0.477410 | 0.476764 | 0.460838 | 0.463143 | 0.436547 |
| Filtered precision | 0.493422 | 0.448400 | 0.483764 | 0.488730 | 0.468293 | 0.432442 |
| Filtered recall | 0.369478 | 0.398883 | 0.370738 | 0.368578 | 0.376400 | 0.349330 |
| Filtered connectivity | 0.299384 | 0.243387 | 0.412427 | 0.352239 | 0.281116 | 0.226195 |
| Filtered predicted-positive fraction | 0.003871 | 0.004599 | 0.003962 | 0.003899 | 0.004155 | 0.004176 |
| Filtered predicted-positive pixels | 409,457 | 486,427 | 419,056 | 412,381 | 439,511 | 441,719 |

ABI-306 narrowly edges ABI-285 on the temporal-eligible primary metric (+0.00035 filtered Dice) and improves the exact weakness targeted by the proposal: precision rises by about +0.0450, connectivity by about +0.0560, and the filtered footprint shrinks by about 76,970 pixels. MIT filtered Dice also improves slightly (+0.0019). The cost is lower recall (-0.0294) and slightly lower Google filtered Dice (-0.0013). This makes ABI-306 a better compact/connected operating point than ABI-285 rather than a decisive aggregate breakthrough.

Relative to ABI-223, ABI-306 is slightly higher on aggregate filtered Dice (+0.0028), MIT Dice (+0.0043), and precision (+0.0097), with nearly identical recall (-0.0013) but much lower connectivity (-0.1130). Relative to ABI-238, ABI-306 improves aggregate filtered Dice (+0.0023), Google Dice (+0.0153), precision (+0.0047), and recall (+0.0009), but trails MIT Dice (-0.0026) and connectivity (-0.0529). The dual-evidence head therefore moves the temporal C4 branch closer to ABI-223/238 compactness and precision, but it still does not recover their connected-line organization.

Relative to the recent ABI-305 temporal-attention calibration head, ABI-306 is clearly stronger: +0.0361 filtered Dice, +0.0361 MIT Dice, +0.0396 Google Dice, +0.0610 precision, +0.0201 recall, and +0.0732 connectivity, with a smaller filtered footprint. The temporal C4 family remains more promising than the current calibrated temporal-attention head variants.

At the selected checkpoint, raw Dice was 0.441449 versus filtered Dice 0.422548, raw recall was 0.399146 versus filtered recall 0.369478, and raw predicted-positive pixels were 442,013 versus 409,457 filtered. Artifact Filters reduce both footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.239743 | 0.237613 | 0.244863 | 0.316403 | 0.192986 | 0.236173 | 0.003153 |
| 3 | 0.329171 | 0.307517 | 0.380730 | 0.409555 | 0.275164 | 0.278803 | 0.003473 |
| 5 | 0.373359 | 0.357603 | 0.411176 | 0.389883 | 0.358178 | 0.283003 | 0.004749 |
| 6 | 0.382288 | 0.370559 | 0.410574 | 0.373366 | 0.391646 | 0.259872 | 0.005423 |
| 8 | 0.391537 | 0.369564 | 0.446363 | 0.455807 | 0.343151 | 0.324079 | 0.003892 |
| 13 | 0.358418 | 0.328207 | 0.435174 | 0.515117 | 0.274818 | 0.343658 | 0.002758 |
| 15 | 0.393586 | 0.372139 | 0.449825 | 0.486733 | 0.330364 | 0.342995 | 0.003509 |
| 17 | 0.400455 | 0.376700 | 0.461776 | 0.487977 | 0.339554 | 0.331294 | 0.003597 |
| 19 | 0.412927 | 0.392241 | 0.468189 | 0.492917 | 0.355274 | 0.393490 | 0.003726 |
| 22 | 0.400584 | 0.378550 | 0.460197 | 0.539498 | 0.318559 | 0.447506 | 0.003052 |
| 27 | 0.417780 | 0.392881 | 0.486617 | 0.500149 | 0.358705 | 0.442703 | 0.003708 |
| 32 | 0.404320 | 0.381841 | 0.458884 | 0.422041 | 0.388027 | 0.245738 | 0.004753 |
| 34 | 0.416541 | 0.399042 | 0.463368 | 0.470572 | 0.373640 | 0.284831 | 0.004105 |
| 35 | 0.357353 | 0.331549 | 0.426913 | 0.524086 | 0.271104 | 0.290656 | 0.002674 |
| 36 | 0.422548 | 0.402764 | 0.476152 | 0.493422 | 0.369478 | 0.299384 | 0.003871 |

The trajectory is finite, non-collapsed, source-informative, and late-improving, but still oscillatory. ABI-306 enters the 0.40 filtered-Dice band at epoch 17, reaches a high-connectivity/high-precision state at epochs 19/22/27, drops sharply at epoch 35, and then selects its best primary checkpoint at the final epoch. Unlike ABI-285, whose selected epoch was a recall-heavy/low-connectivity compromise, ABI-306's selected epoch combines strong precision and compact footprint with moderate recall and moderate connectivity.

The best evidence for the proposed mechanism is not the tiny aggregate-Dice gain over ABI-285; it is the shift in the trade-off surface. Epoch 27 reaches 0.4178 filtered Dice with 0.5001 precision and 0.4427 connectivity, close to ABI-223 connectivity, but recall is only 0.3587. Epoch 36 gives up some of that connectivity to recover the highest aggregate/source balance. This suggests the dual-evidence head can access compact connected states, but it does not yet stabilize ABI-223-like connectivity at ABI-285-like recall.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3750, 0.2039, 0.5947, and 0.3780. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, but it does not establish aggregate promotion evidence.

## Interpretation

Classify ABI-306 as a useful positive-but-limited temporal C4 family-development result. It becomes the highest observed capped temporal-eligible filtered-Dice checkpoint in the indexed temporal branch, but only by a negligible margin over ABI-285. Its more important contribution is that the dual-evidence recall-calibrated head partially repairs ABI-285's compactness/connectivity problem while preserving about the same aggregate temporal-eligible Dice.

The mechanism question is therefore answered as mixed-positive. Internal mask/Line/Centerline-gated residual logits can shift the temporal C4 branch away from ABI-285's broad recall-heavy footprint and toward a higher-precision, more connected operating point. However, the branch still trails ABI-223 and ABI-238 on connected-line continuity, and it sacrifices ABI-285's strongest recall. It has not solved the temporal frontier's central problem of combining high recall, high precision, and continuous thin-line structure at the fixed Harness threshold.

Because ABI-306 selected its best checkpoint at epoch 36 after multiple late oscillations, an unchanged longer continuation is not available under the current trusted budget and should not be requested. The result is strong enough to justify bounded temporal-eligible failure-bucket diagnostics in a future Autonomy Step, especially to compare ABI-306 against ABI-285/223/238 on negative-patch clutter, positive-patch miss tails, and connected-line fragmentation. That Evaluation Request is not created here because this Research Note is the single primary handoff.

ABI-306 is not whole-validation promotion evidence. Keep ABI-202 as the whole-validation aggregate reference, ABI-249 as the high-precision C4/rotation-aware whole-validation comparator, ABI-223 as the temporal connectivity comparator, and ABI-285/306 as closely related temporal C4 aggregate/compact trade-off comparators on the temporal-eligible validation population.

## Decision

Do not promote ABI-306 on this capped temporal-eligible evidence alone. Do not submit an unchanged ABI-306 late36 continuation. Record ABI-306 as the current marginal aggregate temporal-eligible best and a useful compact/precision/connectivity repair of ABI-285, but not as a solved temporal frontier.

Future work should first request temporal-eligible failure-bucket diagnostics for ABI-306 or, if submitting a new Candidate instead, make a mechanism-changing move that preserves ABI-306's compact precision while explicitly raising connected recall. Candidate code must continue to avoid thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, training loops, or prediction retention.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_124245_de843c/candidate/PROPOSAL.md`
- `run_20260914_124245_de843c/candidate/README.md`
- `run_20260914_124245_de843c/candidate/manifest.yaml`
- `run_20260914_124245_de843c/candidate/budget_request.yaml`
- `run_20260914_124245_de843c/resolved_manifest.yaml`
- `run_20260914_124245_de843c/execution.json`
- `run_20260914_124245_de843c/outputs/model_summary.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json`
- `run_20260914_124245_de843c/outputs/final_metrics.json`
- `run_20260914_124245_de843c/outputs/metrics.jsonl`
- `run_20260914_124245_de843c/outputs/resource_profile.json`
- `run_20260914_124245_de843c/outputs/validation_postprocessing/index.json`
- `run_20260914_124245_de843c/outputs/prediction_samples/samples.json`
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-c4-orientation-line-state-late36.md` for ABI-285 parent comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 diagnostic context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal comparison context
- `run_20260914_115424_977db1/outputs/best_metrics.json` and `/history/research-notes/abi305-temporal-attention-line-memory-calibrated-unet.md` for ABI-305 calibrated temporal-attention comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
