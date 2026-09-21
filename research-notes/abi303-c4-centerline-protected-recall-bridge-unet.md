# ABI-303 C4 centerline-protected recall bridge U-Net

research-figures: []

## Scope

This note records ABI-303, Candidate `abi303_fullspectral_btd_sza_c4_centerline_protected_recall_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_095802_a2f059`.

ABI-303 was a bounded C4/orientation-prior family-development continuation after ABI-283 and ABI-292. ABI-283 found a compact high-precision/high-connectivity C4 operating point that under-recalled true contrails. ABI-292 loosened that behavior with a soft-band recall calibrator, but recovered too little recall while losing precision and connectivity. ABI-303 tested a different head mechanism: keep the C4 steerable line-context U-Net body, but add a centerline/detail stream and bounded residual recall bridge protected by precision and disagreement gates.

The Candidate consumed only provider-approved `abi_16ch_plus_sza` tensors. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-303 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,175,059, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 11,495,410,176 / 12,322,865,152 bytes.
- Training wall time: 1,609.5 s; validation wall time: 1,499.6 s; total Run wall time: 3,111.1 s, within the exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-303 centerline-protected bridge | ABI-292 soft-band C4 | ABI-283 compact C4 consensus | ABI-279 C4 recall bridge | ABI-280 selective C4 bridge | ABI-249 compact C4 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 11 | 31 | 22 | 22 | 31 | 34 |
| Filtered Dice | 0.377921 | 0.384676 | 0.412957 | 0.414518 | 0.415244 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.361436 | 0.371401 | 0.393239 | 0.398381 | 0.405113 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.419321 | 0.417038 | 0.464463 | 0.457385 | 0.442121 | 0.468855 | 0.468151 |
| Filtered precision | 0.446396 | 0.404530 | 0.500379 | 0.442551 | 0.425162 | 0.480886 | 0.439467 |
| Filtered recall | 0.327659 | 0.366680 | 0.351539 | 0.389825 | 0.405778 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.322926 | 0.249203 | 0.475887 | 0.439185 | 0.316291 | 0.392524 | 0.457773 |
| Filtered predicted-positive fraction | 0.002660 | 0.003285 | 0.002546 | 0.003192 | 0.003458 | 0.002767 | 0.003433 |
| Filtered predicted-positive pixels | 356,995 | 440,855 | 341,691 | 428,416 | 464,188 | 371,346 | 460,724 |

ABI-303 is a completed but negative centerline-protected C4 result. Relative to ABI-292, the new head improves precision by about +0.0419 and connectivity by about +0.0737 while shrinking the filtered footprint by 83,860 pixels, but it loses about -0.0068 filtered Dice, -0.0390 recall, and -0.0100 MIT Dice. It therefore corrects part of ABI-292's broad low-connectivity behavior, but does so mainly by returning toward compact underprediction.

Relative to ABI-283, ABI-303 is lower by about -0.0350 filtered Dice, -0.0318 MIT Dice, -0.0451 Google Dice, -0.0540 precision, -0.0239 recall, and -0.1530 connectivity. The selected footprint is only 15,304 pixels broader than ABI-283, so the added centerline/detail recall bridge did not materially recover true positives from the compact consensus parent. Relative to ABI-279/280/249, ABI-303 is likewise below on aggregate/source Dice and recall, and it only matches or exceeds ABI-280 connectivity while remaining much lower than ABI-279/249 on the main trade-off.

Relative to ABI-202, ABI-303 remains far below the aggregate reference: about -0.0496 filtered Dice, -0.0506 MIT Dice, -0.0488 Google Dice, -0.0886 recall, and -0.1348 connectivity. Precision is slightly higher than ABI-202, but the positive footprint is much more compact. This is not a frontier-improving operating point.

At the selected checkpoint, raw Dice was 0.392934 versus filtered Dice 0.377921, raw recall was 0.350260 versus filtered recall 0.327659, and raw predicted-positive fraction was 0.002837 versus filtered predicted-positive fraction 0.002660. Artifact Filters reduce the footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.185305 | 0.216172 | 0.140277 | 0.131206 | 0.315315 | 0.105319 | 0.008708 |
| 2 | 0.282318 | 0.274873 | 0.301423 | 0.383073 | 0.223527 | 0.320755 | 0.002114 |
| 3 | 0.301665 | 0.306801 | 0.291271 | 0.289171 | 0.315288 | 0.189669 | 0.003951 |
| 4 | 0.332161 | 0.333768 | 0.328534 | 0.339710 | 0.324941 | 0.165647 | 0.003466 |
| 5 | 0.340904 | 0.323921 | 0.381621 | 0.435949 | 0.279884 | 0.364615 | 0.002326 |
| 6 | 0.371887 | 0.358878 | 0.401754 | 0.376080 | 0.367786 | 0.319928 | 0.003544 |
| 7 | 0.370337 | 0.356525 | 0.403917 | 0.428537 | 0.326055 | 0.331562 | 0.002757 |
| 8 | 0.332037 | 0.317760 | 0.363672 | 0.373026 | 0.299164 | 0.187198 | 0.002906 |
| 9 | 0.377921 | 0.361436 | 0.419321 | 0.446396 | 0.327659 | 0.322926 | 0.002660 |
| 10 | 0.315747 | 0.312535 | 0.322283 | 0.318598 | 0.312946 | 0.140438 | 0.003559 |
| 11 | 0.374137 | 0.365606 | 0.394353 | 0.392130 | 0.357723 | 0.234556 | 0.003306 |
| 12 | 0.374073 | 0.363152 | 0.400381 | 0.415482 | 0.340170 | 0.254987 | 0.002967 |

The trajectory is finite, non-collapsed, and source-informative, but it is not good evidence for an unchanged late-improving continuation. The best checkpoint occurs at epoch 9. Epoch 11 and epoch 12 nearly recover the selected filtered Dice, but they do not improve the proposal's trade-off: epoch 11 gains recall relative to epoch 9 while losing precision, Google Dice, and connectivity; epoch 12 recovers some precision but remains lower on filtered Dice, recall, connectivity, and Google Dice. This resembles the same oscillatory compact-versus-recall behavior seen in ABI-283/292, not a branch cleanly improving toward the current comparators.

The retained fixed `first_n` prediction samples all have near-zero per-sample Dice. They are traceability artifacts selected by the Harness retention policy, not representative diagnostics. Population metrics and predicted-positive fractions show the model is not an all-negative collapse, but the retained samples do not supply qualitative support for promotion.

## Interpretation

Classify ABI-303 as a finite, resource-safe, scientifically useful negative result for the centerline-protected recall bridge mechanism. The architecture completed and produced a compact non-degenerate C4 operating point, but the new centerline/detail stream did not solve the intended fixed-threshold recall problem. It mainly shifted ABI-292 back toward compactness while remaining much weaker than ABI-283/249/279 on aggregate/source Dice, recall, and connected-line evidence.

This narrows the C4 recall-bridge branch. The campaign has now tested broad dual-evidence support, selective consensus, cross-scale consensus, soft-band calibration, and centerline-protected detail support. These mechanisms repeatedly expose the same trade-off: compact high-precision C4 states suppress recall, while recall-support states broaden predictions and often lose precision, source balance, or connectivity. ABI-303 does not eliminate all orientation-prior ideas, but it argues against another unchanged C4 head run in this exact family.

Future work should broaden or materially change mechanism rather than extend ABI-303 unchanged. Higher-value hypotheses are likely in temporal evidence sharpening, non-C4 line-continuity mechanisms, or recall-preserving calibration that raises true contrail logits without relying on another late C4 residual/veto head. Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-303. Do not request whole-validation diagnostics for this capped Result. Do not request an unchanged late-improving continuation of ABI-303; the best checkpoint is mid-run, the final checkpoint is lower, and the result is far below ABI-283/249/279 and ABI-202 on the proposed recall/connectivity trade-off.

Record ABI-303 as bounded negative evidence for centerline-protected C4 recall bridging. Stop this exact C4 head design unless a future proposal changes the mechanism substantially.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_095802_a2f059/candidate/PROPOSAL.md`
- `run_20260914_095802_a2f059/candidate/README.md`
- `run_20260914_095802_a2f059/candidate/manifest.yaml`
- `run_20260914_095802_a2f059/resolved_manifest.yaml`
- `run_20260914_095802_a2f059/execution.json`
- `run_20260914_095802_a2f059/outputs/model_summary.json`
- `run_20260914_095802_a2f059/outputs/best_metrics.json`
- `run_20260914_095802_a2f059/outputs/final_metrics.json`
- `run_20260914_095802_a2f059/outputs/metrics.jsonl`
- `run_20260914_095802_a2f059/outputs/resource_profile.json`
- `run_20260914_095802_a2f059/outputs/validation_postprocessing/index.json`
- `run_20260914_095802_a2f059/outputs/prediction_samples/samples.json`
- `run_20260913_215909_27c6e3/outputs/best_metrics.json` and `/history/research-notes/abi292-c4-softband-recall-calibrator-unet.md` for ABI-292 soft-band C4 context
- `run_20260913_063411_d8a862/outputs/best_metrics.json` and `/history/research-notes/abi283-c4-crossscale-consensus-recall-bridge-late36.md` for ABI-283 compact C4 consensus context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-c4-dual-evidence-recall-bridge-late36.md` for ABI-279 recall-bridge context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` and `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md` for ABI-280 selective-consensus context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
