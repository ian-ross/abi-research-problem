# ABI-307 temporal C4 center-detail recall bridge late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-307, Candidate `abi307_temporal_c4_center_detail_recall_bridge_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260914_151259_e64cba`.

ABI-307 was a mechanism-changing family-development continuation of ABI-306. It kept the provider-owned three-frame temporal input (`abi_16ch_plus_sza_temporal`, offsets `[-1, 0, 1]`, `temporal_eligible_center`), the temporal C4 line-state U-Net backbone, BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The added mechanism was a compact center-frame detail recall bridge before the logit head, intended to raise fixed-threshold recall and connectivity while preserving ABI-306's compact high-precision behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-307 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Direct parent/comparator: ABI-306, `run_20260914_124245_de843c`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,301,119, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.45 / 6.88 GiB.
- Total Run wall time: 8,648.8 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-307 center-detail bridge | ABI-306 dual-evidence line-state | Delta |
| --- | ---: | ---: | ---: |
| Best epoch | 36 | 36 | 0 |
| Filtered Dice | 0.420526 | 0.422548 | -0.002022 |
| Raw Dice | 0.438888 | 0.441449 | -0.002561 |
| MIT filtered Dice | 0.404932 | 0.402764 | +0.002168 |
| Google filtered Dice | 0.460655 | 0.476152 | -0.015497 |
| Filtered precision | 0.470249 | 0.493422 | -0.023173 |
| Filtered recall | 0.380314 | 0.369478 | +0.010836 |
| Filtered connectivity | 0.325308 | 0.299384 | +0.025923 |
| Filtered predicted-positive fraction | 0.004181 | 0.003871 | +0.000310 |
| Filtered predicted-positive pixels | 442,252 | 409,457 | +32,795 |

ABI-307 delivers the intended direction on two of the proposal's failure modes: fixed-threshold recall rises by about +0.0108 and aggregate connectivity rises by about +0.0259 versus ABI-306. MIT filtered Dice also improves slightly (+0.0022), consistent with the hypothesis that center-frame detail support could help the harder MIT undercoverage tail.

The trade-off is not free. Aggregate filtered Dice regresses modestly (-0.0020), precision drops by about -0.0232, the filtered footprint expands by 32,795 pixels, and Google filtered Dice falls materially (-0.0155). ABI-307 therefore does not replace ABI-306 as the capped temporal-eligible aggregate/precision comparator. It is mixed-positive mechanism evidence for recall/connectivity support, not a frontier promotion candidate.

Relative to broader temporal comparators, ABI-307 remains near the high end of capped temporal-eligible aggregate Dice but still trails ABI-223's connectivity (0.4124) and ABI-238's connectivity (0.3522). Its recall is better than ABI-306/223/238 but remains below ABI-285's 0.3989 recall-heavy operating point.

At the selected checkpoint, raw Dice was 0.438888 versus filtered Dice 0.420526, raw recall was 0.410854 versus filtered recall 0.380314, and raw predicted-positive pixels were 475,138 versus 442,252 filtered. Artifact Filters reduce both footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.222846 | 0.229749 | 0.208126 | 0.217764 | 0.228172 | 0.152469 | 0.005417 |
| 3 | 0.264671 | 0.244275 | 0.316438 | 0.465081 | 0.184967 | 0.265900 | 0.002056 |
| 5 | 0.352862 | 0.337605 | 0.391318 | 0.429549 | 0.299408 | 0.308151 | 0.003603 |
| 8 | 0.374459 | 0.357398 | 0.417589 | 0.436306 | 0.327968 | 0.300314 | 0.003886 |
| 11 | 0.375356 | 0.352734 | 0.434447 | 0.486173 | 0.305681 | 0.376198 | 0.003250 |
| 15 | 0.384874 | 0.366719 | 0.432429 | 0.456068 | 0.332906 | 0.362861 | 0.003774 |
| 19 | 0.383475 | 0.356933 | 0.453495 | 0.506678 | 0.308468 | 0.394019 | 0.003147 |
| 23 | 0.402916 | 0.379710 | 0.463656 | 0.454973 | 0.361548 | 0.325178 | 0.004108 |
| 27 | 0.399796 | 0.378583 | 0.458287 | 0.530328 | 0.320829 | 0.414536 | 0.003127 |
| 31 | 0.391173 | 0.372375 | 0.438994 | 0.469027 | 0.335486 | 0.300374 | 0.003698 |
| 34 | 0.408914 | 0.392868 | 0.453014 | 0.475094 | 0.358917 | 0.332455 | 0.003905 |
| 36 | 0.420526 | 0.404932 | 0.460655 | 0.470249 | 0.380314 | 0.325308 | 0.004181 |

The trajectory is finite, non-collapsed, source-informative, and late-improving. Like ABI-306, it is oscillatory. Epoch 27 reaches the strongest connectivity state (0.4145, approximately ABI-223-level) but with only 0.3208 recall; epoch 36 selects the best aggregate filtered Dice by recovering recall and MIT Dice while sacrificing some precision/connectivity. This suggests the center-detail bridge can access more connected states, but the selected operating point still cannot stabilize ABI-223-like continuity together with higher recall and high precision.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4335, 0.1993, 0.6225, and 0.3513. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, but it does not establish promotion evidence.

## Interpretation

Classify ABI-307 as a mixed temporal C4 family-development result. The center-frame detail recall bridge did what it was designed to do in aggregate direction: it raised fixed-threshold recall, raised connectivity, and slightly improved MIT filtered Dice relative to ABI-306. However, the added detail support also expanded the predicted-positive footprint, lowered precision, and caused enough Google regression that aggregate filtered Dice fell below ABI-306.

The mechanism is therefore useful but not sufficient. A center-detail bypass can recover some missed true positives and connected structure, but when applied as this gated residual it partially reopens the compactness/precision trade-off that ABI-306 had repaired. ABI-306 remains the compact high-precision temporal C4 comparator; ABI-307 is evidence that a recall/connectivity bridge is promising enough to diagnose, not strong enough to continue unchanged.

Because the proposal's useful-mixed criterion was met, a future Autonomy Step should consider temporal-eligible failure-bucket diagnostics for ABI-307 before deciding whether to keep this mechanism. The diagnostic question should be whether the recall/connectivity gain actually reduces ABI-306's MIT positive-patch under-recall and fragmentation tails, or whether the added positives are mostly broad Google/negative-patch clutter. Do not submit an unchanged ABI-307 late36 continuation.

## Decision

Do not promote ABI-307 and do not replace ABI-306 as the capped temporal-eligible aggregate/precision comparator. Record ABI-307 as mixed-positive mechanism evidence: better recall/connectivity and slightly better MIT Dice, offset by lower precision, larger footprint, and Google regression.

Recommended next handoff is an Evaluation Request for temporal-eligible failure-bucket review of ABI-307 against ABI-306/285/223/238, if the campaign next chooses diagnostics. If submitting a new Candidate instead, it should be mechanism-changing: preserve ABI-306's compact precision while adding more selective connected-recall support, rather than another unchanged center-detail residual.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_151259_e64cba/candidate/PROPOSAL.md`
- `run_20260914_151259_e64cba/candidate/README.md`
- `run_20260914_151259_e64cba/candidate/manifest.yaml`
- `run_20260914_151259_e64cba/candidate/budget_request.yaml`
- `run_20260914_151259_e64cba/resolved_manifest.yaml`
- `run_20260914_151259_e64cba/execution.json`
- `run_20260914_151259_e64cba/outputs/model_summary.json`
- `run_20260914_151259_e64cba/outputs/best_metrics.json`
- `run_20260914_151259_e64cba/outputs/final_metrics.json`
- `run_20260914_151259_e64cba/outputs/metrics.jsonl`
- `run_20260914_151259_e64cba/outputs/resource_profile.json`
- `run_20260914_151259_e64cba/outputs/validation_postprocessing/index.json`
- `run_20260914_151259_e64cba/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 parent comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` for ABI-285 recall-heavy temporal C4 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
