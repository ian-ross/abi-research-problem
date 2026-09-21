# ABI-346 temporal C4 connected-recall ladder late36

research-figures: []

## Scope

This note records ABI-346, Candidate `abi346_temporal_c4_connected_recall_ladder_late36_bce_dice_line_centerline_aux_v1`, and Run `run_20260918_152331_c80150`.

ABI-346 was a close, mechanism-changing continuation of ABI-306. It kept the provider-owned three-frame `abi_16ch_plus_sza_temporal` input with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was a connected-recall ladder head intended to recover ABI-306's fixed-threshold under-recall reserve by adding bounded recall support only where base mask, Line, Centerline, and local continuity evidence agreed.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-346 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-306, ABI-285, and ABI-223 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,246,376, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,592,263,168 / 5,905,580,032 bytes.
- Training wall time: 4,724.0 s; validation wall time: 3,374.9 s; total Run wall time: 8,101.0 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 23.

## Best-validation metrics

| Metric | ABI-346 connected-recall ladder | ABI-306 compact dual-evidence C4 | ABI-285 recall-heavy C4 | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-324 five-frame balanced C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 23 | 36 | 32 | 36 | 29 | 27 |
| Filtered Dice | 0.427835 | 0.422548 | 0.422195 | 0.419776 | 0.420235 | 0.429430 |
| MIT filtered Dice | 0.407956 | 0.402764 | 0.400831 | 0.398498 | 0.405383 | 0.408188 |
| Google filtered Dice | 0.480484 | 0.476152 | 0.477410 | 0.476764 | 0.460838 | 0.487231 |
| Filtered precision | 0.461087 | 0.493422 | 0.448400 | 0.483764 | 0.488730 | 0.470412 |
| Filtered recall | 0.399057 | 0.369478 | 0.398883 | 0.370738 | 0.368578 | 0.395017 |
| Filtered connectivity | 0.299258 | 0.299384 | 0.243387 | 0.412427 | 0.352239 | 0.397925 |
| Filtered predicted-positive pixels | 473,249 | 409,457 | 486,427 | 419,056 | 412,381 | 459,172 |

ABI-346 improves the immediate ABI-306 target on aggregate Dice (+0.0053), MIT Dice (+0.0052), Google Dice (+0.0043), and recall (+0.0296). The cost is lower precision (-0.0323) and a larger filtered footprint (+63,792 pixels), while connectivity is essentially unchanged and remains low (-0.0001). This means the connected-recall ladder did recover fixed-threshold area evidence, but it did not deliver the intended connected-line improvement.

Relative to ABI-285, ABI-346 is a cleaner version of the recall-heavy temporal C4 operating point: similar recall (+0.0002), higher precision (+0.0127), higher connectivity (+0.0559), higher source-stratified Dice, and 13,178 fewer filtered predicted-positive pixels. That is useful family-development evidence. However, ABI-346 still does not reach ABI-223/238 connectivity, and it remains below the best five-frame temporal C4/detail-consensus comparators on connected-line continuity.

Relative to ABI-324, ABI-346 is close on aggregate filtered Dice (-0.0016) and MIT Dice (-0.0002), with slightly higher recall (+0.0040), but lower Google Dice (-0.0067), lower precision (-0.0093), and much lower connectivity (-0.0987). ABI-324 therefore remains the better balanced temporal C4/detail-consensus comparator.

At the selected checkpoint, raw Dice was 0.445587 versus filtered Dice 0.427835, raw recall was 0.430987 versus filtered recall 0.399057, and raw predicted-positive pixels were 510,978 versus 473,249 filtered. Artifact Filters removed 37,729 predicted-positive pixels and lowered the score; they did not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.201670 | 0.195716 | 0.217809 | 0.426935 | 0.132014 | 0.372420 | 0.001599 |
| 5 | 0.291552 | 0.266283 | 0.359017 | 0.559598 | 0.197128 | 0.358787 | 0.001821 |
| 10 | 0.380958 | 0.360520 | 0.432836 | 0.475827 | 0.317630 | 0.252905 | 0.003451 |
| 15 | 0.397178 | 0.375714 | 0.452144 | 0.493233 | 0.332438 | 0.291289 | 0.003484 |
| 20 | 0.358161 | 0.328601 | 0.436309 | 0.549982 | 0.265545 | 0.310592 | 0.002496 |
| 23 | 0.427835 | 0.407956 | 0.480484 | 0.461087 | 0.399057 | 0.299258 | 0.004474 |
| 25 | 0.399051 | 0.375515 | 0.461834 | 0.522769 | 0.322685 | 0.299614 | 0.003191 |
| 30 | 0.420755 | 0.401412 | 0.469862 | 0.433770 | 0.408499 | 0.318543 | 0.004868 |
| 32 | 0.403201 | 0.384243 | 0.449709 | 0.413371 | 0.393519 | 0.247266 | 0.004921 |
| 34 | 0.404100 | 0.382981 | 0.458435 | 0.455123 | 0.363364 | 0.236842 | 0.004127 |
| 36 | 0.421834 | 0.401143 | 0.478819 | 0.482352 | 0.374809 | 0.296170 | 0.004017 |

The trajectory was finite, non-collapsed, source-informative, and late-budget-dependent, but oscillatory. The selected epoch 23 is the best aggregate/source-balanced checkpoint. Epochs 25 and 36 show more compact, higher-precision states but with lower recall and Dice; epoch 30 raises recall slightly above the selected checkpoint but broadens the footprint and loses precision. The final epoch remains strong relative to ABI-306/285 but is below the selected checkpoint on filtered Dice, MIT Dice, Google Dice, recall, and connectivity.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2970, 0.2437, 0.5308, and 0.3832. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-346 as mixed-positive temporal C4 family-development evidence for this exact connected-recall ladder head. It succeeds at the narrow ABI-306 under-recall objective: fixed-threshold recall and aggregate/source filtered Dice improve while predictions remain less broad than ABI-285. It also slightly surpasses ABI-285's recall-heavy aggregate trade-off without returning all the way to ABI-285's cluttered footprint.

The result is not a connectivity solution. The proposed connected-recall ladder did not improve aggregate connectivity over ABI-306 and remains far below ABI-223, ABI-238, and ABI-324 on connected-line continuity. Its gain appears to be a better recall/precision trade-off in the temporal C4 line-state branch, not a solved thin-line continuity mechanism.

Comparator roles after ABI-346:

- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-306 remains the compact high-precision three-frame temporal C4 comparator and has a completed temporal-eligible failure-bucket diagnostic.
- ABI-346 becomes useful positive evidence for a better three-frame temporal C4 recall/aggregate trade-off, but not a connectivity comparator until bounded diagnostics show where the additional positives land.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-238 remains a strong directional temporal-attention precision/connectivity comparator.

ABI-346 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-346 on capped temporal-eligible evidence alone. Do not submit an unchanged late36 continuation of this exact connected-recall ladder head. The late-budget question has been answered: the head can lift ABI-306-style recall and aggregate Dice, but it does not stabilize connected-line continuity.

A future Autonomy Step could reasonably request temporal-eligible failure-bucket diagnostics for ABI-346, because it is a near-frontier three-frame temporal C4 line-state result and the campaign needs to know whether its extra 63,792 filtered-positive pixels over ABI-306 are mainly recovered positive-tail contrails or negative-patch clutter. That Evaluation Request is not created here because this Research Note is the single primary handoff.

If architecture work proceeds instead of diagnostics, the next Candidate should be mechanism-changing and explicitly protect ABI-306 compactness while adding connected-line support; another simple uncertainty-band recall residual or unchanged connected-recall ladder gain tweak is not justified.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_152331_c80150/candidate/PROPOSAL.md`
- `run_20260918_152331_c80150/candidate/README.md`
- `run_20260918_152331_c80150/candidate/manifest.yaml`
- `run_20260918_152331_c80150/candidate/budget_request.yaml`
- `run_20260918_152331_c80150/resolved_manifest.yaml`
- `run_20260918_152331_c80150/execution.json`
- `run_20260918_152331_c80150/run_metadata.json`
- `run_20260918_152331_c80150/outputs/model_summary.json`
- `run_20260918_152331_c80150/outputs/best_metrics.json`
- `run_20260918_152331_c80150/outputs/final_metrics.json`
- `run_20260918_152331_c80150/outputs/metrics.jsonl`
- `run_20260918_152331_c80150/outputs/resource_profile.json`
- `run_20260918_152331_c80150/outputs/validation_postprocessing/index.json`
- `run_20260918_152331_c80150/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-c4-orientation-line-state-late36.md` for ABI-285 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
