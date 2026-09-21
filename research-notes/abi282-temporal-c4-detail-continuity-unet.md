# ABI-282 temporal C4 detail-continuity U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-282, Candidate `abi282_temporal_c4_detail_continuity_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_054610_22cd27`.

ABI-282 was a temporal-family development Candidate after ABI-274, ABI-275, ABI-278, and ABI-281. It kept the provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection, then added a C4 rotation-shared detail-continuity head over final temporal/detail features. The hypothesis was that organizing center-frame detail with rotation-shared anisotropic line context could recover connected thin-line evidence while preserving temporal recall.

The Candidate used source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. It remained architecture/manifest-only and did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Execution result

ABI-282 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,220,687, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.62 / 5.08 GiB.
- Training wall time: 1,230.0 s; validation wall time: 1,102.9 s; total Run wall time: 2,334.7 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-282 best epoch 12 | ABI-281 detail agreement | ABI-275 temporal C4 bridge | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.371561 | 0.375376 | 0.385365 | 0.419364 | 0.419776 |
| Raw Dice | 0.387573 | 0.392039 | 0.401336 | 0.436760 | 0.438487 |
| Filtered precision | 0.437707 | 0.418431 | 0.413604 | 0.454127 | 0.483764 |
| Filtered recall | 0.322782 | 0.340355 | 0.360736 | 0.389545 | 0.370738 |
| Filtered connectivity | 0.230765 | 0.251147 | 0.266368 | 0.282911 | 0.412427 |
| MIT filtered Dice | 0.354712 | 0.365315 | 0.372421 | 0.399386 | 0.398498 |
| Google filtered Dice | 0.412957 | 0.400773 | 0.417764 | 0.472606 | 0.476764 |
| Filtered predicted-positive fraction | 0.003812 | 0.004205 | 0.004509 | 0.004434 | 0.003962 |
| Filtered predicted-positive pixels | 403,240 | 444,781 | — | 469,049 | 419,056 |

ABI-282 did not meet its primary target. Relative to ABI-281, the C4 detail-continuity head traded to a more compact and slightly higher-precision operating point, with +0.0193 precision, -41,541 filtered positive pixels, and a modest Google Dice gain. But it lost filtered Dice (-0.0038), recall (-0.0176), connectivity (-0.0204), and MIT Dice (-0.0106). That is the wrong direction for a mechanism intended to recover connected line evidence.

Relative to ABI-275's earlier temporal C4 bridge, ABI-282 is also lower on filtered Dice (-0.0138), recall (-0.0380), connectivity (-0.0356), MIT Dice (-0.0177), and Google Dice (-0.0048), despite somewhat higher precision. Relative to the stronger temporal comparators ABI-274 and ABI-223, ABI-282 remains far behind: about -0.048 filtered Dice versus both, -0.0668 recall versus ABI-274, and -0.1817 connectivity versus ABI-223.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.195929 | 0.195380 | 0.197135 | 0.245852 | 0.162859 | 0.172693 | 0.003424 |
| 2 | 0.216232 | 0.205516 | 0.240773 | 0.289907 | 0.172416 | 0.187338 | 0.003074 |
| 3 | 0.263476 | 0.248673 | 0.298166 | 0.386594 | 0.199835 | 0.233355 | 0.002672 |
| 4 | 0.288455 | 0.272693 | 0.324563 | 0.363456 | 0.239113 | 0.170485 | 0.003401 |
| 5 | 0.331685 | 0.327601 | 0.340656 | 0.335394 | 0.328056 | 0.174759 | 0.005056 |
| 6 | 0.342873 | 0.325551 | 0.384118 | 0.407862 | 0.295749 | 0.244792 | 0.003749 |
| 7 | 0.328644 | 0.307183 | 0.382043 | 0.436693 | 0.263458 | 0.252814 | 0.003119 |
| 8 | 0.366608 | 0.352865 | 0.400277 | 0.399472 | 0.338740 | 0.204571 | 0.004384 |
| 9 | 0.360404 | 0.349726 | 0.385214 | 0.339308 | 0.384298 | 0.163975 | 0.005855 |
| 10 | 0.370970 | 0.353994 | 0.412801 | 0.446680 | 0.317206 | 0.272002 | 0.003671 |
| 11 | 0.341599 | 0.315512 | 0.409393 | 0.521381 | 0.254011 | 0.404984 | 0.002519 |
| 12 | 0.371561 | 0.354712 | 0.412957 | 0.437707 | 0.322782 | 0.230765 | 0.003812 |

The trajectory is finite and non-collapsed, but it is not a clean late-improving case. The final epoch is the selected best, yet it improves only +0.00059 filtered Dice over epoch 10 and remains much lower than ABI-223/274. Epoch 11 demonstrates that the head can produce very compact, high-precision, high-connectivity predictions, but only by dropping recall to 0.2540 and MIT Dice to 0.3155. Epoch 12 recovers some recall and MIT Dice, but connectivity falls back to 0.2308.

This oscillation indicates an operating-point tradeoff rather than a maturing line-continuity mechanism: when the C4 head is compact, recall/source coverage collapses; when recall recovers, connectivity does not remain high.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2513, 0.4217, 0.5999, and 0.3259. This is consistent with finite non-collapsed predictions and substantial per-sample variability, but it does not establish promotion evidence.

At the selected checkpoint, raw Dice was 0.3876 and filtered Dice was 0.3716, with 434,243 raw predicted-positive pixels versus 403,240 filtered predicted-positive pixels. Artifact Filters therefore lowered rather than created the selected Result.

## Interpretation

Classify ABI-282 as a finite negative mechanism test. It is resource-safe and executable, but the C4 detail-continuity head did not deliver the intended effect. It made ABI-281 more compact and slightly more precise, yet reduced the recall, MIT performance, and connected-line continuity that the mechanism was meant to repair. It also underperformed the earlier ABI-275 C4 bridge and remains far below ABI-223/274 on temporal-eligible filtered Dice.

The result narrows the post-decoder C4/detail-continuity integration point. Adding rotation-shared line context after temporal-attention/detail fusion is not enough to preserve temporal recall while improving connected thin-line evidence. The high-connectivity epoch 11 looks like conservative underprediction rather than useful continuity repair.

This does not eliminate temporal attention, C4/orientation priors, or center-frame detail preservation as broad families. It does argue against repeating an unchanged ABI-282-style final C4 detail-continuity head. ABI-223 remains the temporal-attention connectivity comparator, ABI-274 remains the temporal recall/source-balance comparator, ABI-255 remains the compact recurrent temporal comparator, ABI-249 remains the high-precision C4 whole-validation comparator, and ABI-202 remains the aggregate whole-validation reference.

## Decision

Do not promote ABI-282, do not request temporal-eligible failure-bucket diagnostics, and do not request a late-improving budget for this exact branch. Although the best checkpoint lands at the exploratory ceiling, the improvement over epoch 10 is negligible, the trajectory is oscillatory, and the selected checkpoint is too far below ABI-223/274 while failing the connectivity target.

Do not repeat ABI-282 unchanged. Future temporal work should be mechanism-changing: move continuity support earlier in the temporal encoder/state path, use a different recall-preserving calibration/dual-evidence mechanism, or broaden away from post-decoder C4 heads toward architectures that raise true contrail logits at threshold 0.5 without broad negative-patch clutter. Such work must still keep data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, and resource scheduling provider/Harness-owned.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_054610_22cd27/candidate/PROPOSAL.md`
- `run_20260913_054610_22cd27/candidate/README.md`
- `run_20260913_054610_22cd27/candidate/manifest.yaml`
- `run_20260913_054610_22cd27/resolved_manifest.yaml`
- `run_20260913_054610_22cd27/outputs/model_summary.json`
- `run_20260913_054610_22cd27/outputs/best_metrics.json`
- `run_20260913_054610_22cd27/outputs/final_metrics.json`
- `run_20260913_054610_22cd27/outputs/metrics.jsonl`
- `run_20260913_054610_22cd27/outputs/resource_profile.json`
- `run_20260913_054610_22cd27/outputs/validation_postprocessing/index.json`
- `run_20260913_054610_22cd27/outputs/prediction_samples/samples.json`
- `run_20260913_050456_f4352b/outputs/best_metrics.json` for ABI-281 center-detail agreement comparison context
- `run_20260912_203536_240ad8/outputs/best_metrics.json` for ABI-275 temporal C4 bridge comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `/history/research-notes/abi281-temporal-attention-center-detail-agreement-unet.md`
- `/history/research-notes/abi275-temporal-c4-continuity-bridge-unet.md`
- `/history/research-notes/abi274-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
