# ABI-325 temporal five-frame positive-tail evidence reinjector late36

research-figures: []

## Scope

This note records ABI-325, Candidate `abi325_temporal_fiveframe_positive_tail_evidence_reinjector_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260916_212722_d66d93`.

ABI-325 was a close but mechanism-changing continuation of ABI-324's five-frame temporal C4 detail-consensus line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change was a `PositiveTailEvidenceReinjector` before the final detail-consensus head: decoder features, center-frame temporal-stem detail, and early C4 line-state evidence are projected into shared full-resolution memory and applied as a bounded feature residual where learned agreement and background guards support the pixel.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable to the full-validation ABI-202/249 frontier.

## Execution result

ABI-325 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324 (`run_20260916_184108_954ec7`), ABI-311 (`run_20260915_015552_1ac51f`), and ABI-306 (`run_20260914_124245_de843c`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,265,590, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 7,025,015,296 / 7,421,820,928 bytes.
- Training wall time: 5,715.8 s; validation wall time: 3,500.5 s; total Run wall time: 9,218.7 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-325 positive-tail reinjector | ABI-324 detail-consensus | Delta vs ABI-324 | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 0 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.427745 | 0.429430 | -0.001685 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.412855 | 0.408188 | +0.004667 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.466540 | 0.487231 | -0.020692 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.425680 | 0.470412 | -0.044732 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.429830 | 0.395017 | +0.034813 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.327452 | 0.397925 | -0.070474 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 552,142 | 459,172 | +92,970 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-325 is finite, non-collapsed, and source-informative, but it is not a balanced improvement over ABI-324. The intended positive-tail support is visible as higher selected fixed-threshold recall and higher MIT filtered Dice relative to ABI-324. However, this comes with a much broader footprint, lower precision, much lower connectivity, and a sharp Google-source regression. Aggregate filtered Dice falls slightly below ABI-324 despite the recall gain.

Relative to ABI-311, ABI-325 improves aggregate filtered Dice by +0.002745 and MIT Dice by +0.009024, but loses Google Dice, precision, and connectivity while adding 82,093 filtered predicted-positive pixels. Relative to ABI-306, it improves recall and MIT Dice but abandons the compact high-precision behavior. Relative to ABI-309, it is a less broad recall variant with better precision/connectivity, but it does not match ABI-324's cleaner balance. Relative to ABI-223, it improves aggregate and MIT Dice plus recall, but trails badly on precision and connectivity.

At the selected checkpoint, raw Dice was 0.444471 versus filtered Dice 0.427745, raw recall was 0.464644 versus filtered recall 0.429830, and raw predicted-positive pixels were 596,447 versus 552,142 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.225484 | 0.219921 | 0.238739 | 0.312170 | 0.176477 | 0.169414 | 0.002924 |
| 8 | 0.384290 | 0.367660 | 0.425977 | 0.439770 | 0.341240 | 0.284676 | 0.004014 |
| 16 | 0.399383 | 0.381321 | 0.444807 | 0.438154 | 0.366916 | 0.309989 | 0.004332 |
| 20 | 0.407266 | 0.389022 | 0.452710 | 0.440093 | 0.378997 | 0.331022 | 0.004455 |
| 25 | 0.412284 | 0.387297 | 0.477241 | 0.511352 | 0.345373 | 0.364087 | 0.003494 |
| 27 | 0.427745 | 0.412855 | 0.466540 | 0.425680 | 0.429830 | 0.327452 | 0.005220 |
| 30 | 0.399761 | 0.373065 | 0.468841 | 0.536242 | 0.318658 | 0.416388 | 0.003073 |
| 32 | 0.420234 | 0.399353 | 0.473647 | 0.483495 | 0.371612 | 0.346557 | 0.003975 |
| 36 | 0.410372 | 0.386890 | 0.469517 | 0.454868 | 0.373807 | 0.276081 | 0.004248 |

The trajectory remains late-budget-dependent and oscillatory. Epoch 27 is the only selected high-recall/MIT-positive operating point. Epoch 30 shows that the model can reach ABI-324-like or better connectivity, but only with lower Dice and recall. Epoch 32 recovers a cleaner precision/recall balance but still trails ABI-324 on aggregate Dice, Google Dice, and connectivity. The final epoch ends below the selected checkpoint and below ABI-324's final Dice.

This pattern suggests that feature-level reinjection increases true-positive evidence in some MIT/low-recall cases, but it does not stably preserve the line-continuity and source balance that made ABI-324 the better temporal C4 comparator.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3655, approximately 0.0000, 0.5310, and 0.4988. This confirms finite non-collapsed predictions but also includes one retained first-n complete miss, consistent with the need for per-sample positive-tail diagnostics before claiming tail repair.

## Interpretation

Classify ABI-325 as mixed but mostly negative capped temporal-family development evidence for the exact feature-level positive-tail reinjection branch. The mechanism did move the selected operating point toward higher recall and better MIT filtered Dice, which is the intended direction for ABI-324's diagnosed positive-tail/MIT undercoverage. The cost is too large for the branch to replace ABI-324: lower aggregate Dice, lower Google Dice, much lower precision, a much broader footprint, and a large connectivity regression.

Comparator roles after ABI-325:

- ABI-324 remains the local balanced temporal C4 aggregate/connectivity comparator.
- ABI-325 is a recall/MIT-tail diagnostic variant, not a new comparator or promotion candidate.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy broad-footprint temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.
- ABI-322 remains negative evidence for an unchanged ABI-311-style architecture trained with `bce_dice_cldice`.

ABI-325 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249, and it does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, or resource scheduling.

## Decision

Do not promote ABI-325 and do not submit another unchanged positive-tail reinjector continuation. ABI-324 remains the better temporal C4 balance point.

A future temporal-eligible failure-bucket Evaluation Request is scientifically reasonable if the next step is to verify whether ABI-325 truly reduces positive-patch zero-TP/low-recall tails or merely broadens predictions and shifts errors across sources. That diagnostic should compare ABI-325 against ABI-324, ABI-311, ABI-306, ABI-309, and ABI-223 on positive-patch tails, negative-patch clutter, source-stratified medians, threshold behavior, and Artifact Filter dependence. If diagnostics are not requested, the next Candidate should broaden away from this exact temporal C4 feature-reinjection branch toward a materially different temporal alignment/change or attention mechanism that raises connected true-positive evidence without sacrificing ABI-324's compactness.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260916_212722_d66d93/candidate/PROPOSAL.md`
- `run_20260916_212722_d66d93/candidate/README.md`
- `run_20260916_212722_d66d93/candidate/manifest.yaml`
- `run_20260916_212722_d66d93/candidate/budget_request.yaml`
- `run_20260916_212722_d66d93/resolved_manifest.yaml`
- `run_20260916_212722_d66d93/execution.json`
- `run_20260916_212722_d66d93/outputs/model_summary.json`
- `run_20260916_212722_d66d93/outputs/best_metrics.json`
- `run_20260916_212722_d66d93/outputs/final_metrics.json`
- `run_20260916_212722_d66d93/outputs/metrics.jsonl`
- `run_20260916_212722_d66d93/outputs/resource_profile.json`
- `run_20260916_212722_d66d93/outputs/validation_postprocessing/index.json`
- `run_20260916_212722_d66d93/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 diagnostic context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260915_191945_382cc4/outputs/best_metrics.json` and `/history/research-notes/abi322-temporal-fiveframe-c4-cldice-connectivity-line-state-late36.md` for ABI-322 trusted-loss comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
