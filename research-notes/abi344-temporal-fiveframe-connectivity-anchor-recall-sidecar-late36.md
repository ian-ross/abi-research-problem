# ABI-344 temporal five-frame connectivity-anchor recall-sidecar late36

research-figures: []

## Scope

This note records ABI-344, Candidate `abi344_temporal_fiveframe_connectivity_anchor_recall_sidecar_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260918_105020_e806bb`, and Post-Run Evaluation `eval_evalreq_abi344_temporal_eligible_failure_buckets_v1`.

ABI-344 was a mechanism-changing continuation of the five-frame temporal C4/detail-consensus branch. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The architectural change was an explicit compact connectivity anchor plus a bounded agreement-gated recall sidecar intended to recover true positives without broadening ABI-324-style predictions.

This is capped temporal-eligible diagnostic evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-344 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324, ABI-337, and ABI-341 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,258,040, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,665,729,536 / 7,061,110,784 bytes.
- Training wall time: 5,371.8 s; validation wall time: 3,456.2 s; total Run wall time: 8,830.1 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 29.

## Best-validation and evaluation metrics

| Metric | ABI-344 anchor sidecar | ABI-324 balanced parent | ABI-337 no mirroring | ABI-341 recall router | ABI-325 positive-tail | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 29 | 27 | 27 | 27 | 27 | 36 |
| Filtered Dice | 0.426448 | 0.429430 | 0.428894 | 0.417101 | 0.427745 | 0.419776 |
| MIT filtered Dice | 0.412208 | 0.408188 | 0.411838 | 0.397921 | 0.412855 | 0.398498 |
| Google filtered Dice | 0.462585 | 0.487231 | 0.476340 | 0.465708 | 0.466540 | 0.476764 |
| Filtered precision | 0.426700 | 0.470412 | 0.466489 | 0.418916 | 0.425680 | 0.483764 |
| Filtered recall | 0.426196 | 0.395017 | 0.396906 | 0.415302 | 0.429830 | 0.370738 |
| Filtered connectivity | 0.315733 | 0.397925 | 0.365326 | 0.279162 | 0.327452 | 0.412427 |
| Filtered predicted-positive pixels | 546,166 | 459,172 | 465,248 | 542,094 | 552,142 | 419,056 |

ABI-344 produced the targeted fixed-threshold recall lift over ABI-324 and ABI-337, and it is the strongest MIT Dice point among the local ABI-324/337/341 comparison set. The cost is too high for a new comparator: versus ABI-324 it loses -0.0030 aggregate filtered Dice, -0.0246 Google Dice, -0.0437 precision, and -0.0822 connectivity while adding 86,994 filtered predicted-positive pixels. Compared with ABI-325, the older positive-tail diagnostic, ABI-344 has slightly lower Dice, recall, connectivity, and similar broad footprint; compared with ABI-341 it repairs aggregate Dice and connectivity but still does not restore ABI-324/337 connected compactness.

At the selected checkpoint, raw Dice was 0.442863 versus filtered Dice 0.426448, raw recall was 0.460189 versus filtered recall 0.426196, and raw predicted-positive pixels were 589,598 versus 546,166 filtered. Artifact Filters removed 43,432 predicted-positive pixels and lowered the score; they did not create the Result.

## Failure-bucket diagnostic observations

The Post-Run Evaluation completed on the same 1,614 temporal-eligible validation ABI Patches. Source/positive/negative buckets from `per_sample_metrics.jsonl` show that ABI-344 partially fixes positive-tail recall but repeats the branch's broad-footprint and weak-connectivity failure mode.

| Bucket metric | ABI-344 MIT | ABI-344 Google |
| --- | ---: | ---: |
| Positive samples | 423 | 296 |
| Positive mean filtered recall | 0.4468 | 0.5131 |
| Positive mean filtered Dice | 0.3803 | 0.4322 |
| Positive mean connectivity | 0.3727 | 0.4322 |
| Positive median filtered Dice | 0.4116 | 0.4753 |
| Positive median filtered recall | 0.4578 | 0.5599 |
| Complete positive misses | 34 | 25 |
| Positive samples with recall < 0.25 | 94 | 49 |
| Positive samples with recall < 0.50 | 239 | 131 |
| Negative samples | 492 | 403 |
| Negative samples with any filtered prediction | 360 | 311 |
| Negative samples with >128 filtered predicted pixels | 99 | 61 |
| Negative samples with >512 filtered predicted pixels | 13 | 0 |
| Negative total filtered false-positive pixels | 41,481 | 25,206 |

Across both Dataset Sources, ABI-344 had 59 complete positive misses, 88 positive patches with filtered Dice below 0.1, 133 below 0.2, and 143 with filtered recall below 0.25. This is better than ABI-324's 72 complete misses, 100 Dice-below-0.1 patches, 150 Dice-below-0.2 patches, and 207 recall-below-0.25 patches, and slightly better than ABI-341's 57 complete misses / 82 Dice-below-0.1 / 126 Dice-below-0.2 / 144 recall-below-0.25 in the low-recall-tail bucket mix. So the sidecar did recover hard positive-patch evidence.

The negative-patch clutter cost remains a hard limitation. ABI-344 touched 671 of 895 negative temporal-eligible validation patches and accumulated 66,687 negative-patch false-positive pixels, with 222 negative patches above 100 filtered predicted pixels, 14 above 500, and 1 above 1,000. This is much broader than ABI-324's 533 touched negatives and 40,097 negative-patch false-positive pixels, and also worse than ABI-337's 591 touched negatives and 49,852 negative-patch false-positive pixels. It is cleaner than ABI-341's 736 touched negatives and 71,777 negative-patch false-positive pixels, but not clean enough to count as a compact-state-protected recall lift.

The source pattern is mixed. MIT filtered Dice improves over ABI-324 by about +0.0040 and nearly ties ABI-325, suggesting the sidecar does address part of the MIT-positive undercoverage problem. Google filtered Dice, however, falls substantially behind ABI-324, ABI-337, ABI-223, and ABI-325. The source gap narrows because Google regresses, not because both Dataset Sources improve.

## Threshold behavior

The threshold sweep shows only a small low-threshold diagnostic gain and does not reveal a hidden fixed-threshold failure that would justify Candidate-owned thresholding:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low-threshold high-recall reference | 0.10 | 0.425230 | 0.367684 | 0.504133 | 749,737 |
| Best filtered Dice | 0.25 | 0.428591 | 0.399929 | 0.461678 | 631,240 |
| Primary evaluation | 0.50 | 0.426448 | 0.426700 | 0.426196 | 546,166 |
| High-precision reference | 0.70 | 0.420906 | 0.447844 | 0.397025 | 484,763 |
| Very high threshold reference | 0.90 | 0.398109 | 0.482692 | 0.338749 | 383,748 |

The best diagnostic threshold is only +0.0021 filtered Dice above the trusted 0.50 threshold, but requires another 85,074 filtered predicted-positive pixels. The primary fixed-threshold operating point is therefore not an obvious calibration accident. This does not authorize Candidate-owned thresholds, postprocessing, calibration, metrics, losses, Artifact Filters, or validation selection.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.216190 | 0.216341 | 0.215845 | 0.254252 | 0.188041 | 0.151288 | 0.003823 |
| 5 | 0.326216 | 0.310229 | 0.366683 | 0.446440 | 0.257006 | 0.302973 | 0.002976 |
| 10 | 0.354351 | 0.334021 | 0.405409 | 0.455102 | 0.290123 | 0.256592 | 0.003296 |
| 15 | 0.379917 | 0.357641 | 0.440206 | 0.527083 | 0.296994 | 0.381956 | 0.002913 |
| 20 | 0.390124 | 0.365387 | 0.455771 | 0.531051 | 0.308307 | 0.396123 | 0.003001 |
| 25 | 0.354927 | 0.325946 | 0.433576 | 0.592526 | 0.253339 | 0.451310 | 0.002210 |
| 29 | 0.426448 | 0.412208 | 0.462585 | 0.426700 | 0.426196 | 0.315733 | 0.005163 |
| 30 | 0.372254 | 0.342370 | 0.446774 | 0.464344 | 0.310646 | 0.336466 | 0.003458 |
| 32 | 0.413553 | 0.390653 | 0.473297 | 0.496754 | 0.354224 | 0.367270 | 0.003686 |
| 34 | 0.414271 | 0.389388 | 0.479950 | 0.489381 | 0.359149 | 0.401255 | 0.003794 |
| 36 | 0.405661 | 0.382794 | 0.467271 | 0.470221 | 0.356689 | 0.349165 | 0.003921 |

The trajectory was finite, non-collapsed, source-informative, and late-budget-dependent, but still oscillatory. Epochs 20, 25, and 34 recover compact high-connectivity/high-precision states with insufficient recall; epoch 29 is the selected broad-recall state with weak connectivity; the final epoch regresses from the selected aggregate. This repeats the temporal C4 family's recurring decoupling between connected compact states and fixed-threshold recall-heavy states.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2325, 0.3402, 0.4913, and 0.4255. These confirm finite non-collapsed predictions, but the evaluation population is the evidence for branch decisions.

The diagnostic GeoTIFF samples and per-sample rows are bounded Evaluation artifacts. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-344 as mixed but ultimately negative capped temporal-family evidence for this exact connectivity-anchor/recall-sidecar head. The positive signal is real: ABI-344 improves MIT Dice and low-recall positive-tail counts over ABI-324/337 while repairing much of ABI-341's aggregate Dice regression. The negative signal is decisive for comparator status: connectivity remains well below ABI-324, ABI-337, ABI-223, and ABI-325, the footprint remains broad, and negative-patch clutter is much higher than ABI-324/337.

Comparator roles after ABI-344:

- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 remains a useful no-mirroring diagnostic control, not a new comparator.
- ABI-325 remains the positive-tail/broad-footprint recall diagnostic and is at least as good as ABI-344 for recall-mode comparison.
- ABI-341 remains negative evidence for the compact-continuity recall-router because of clutter/connectivity cost.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-344 is evidence that explicit anchor/sidecar separation can improve MIT and positive-tail recall, but not with adequate compactness or connected-line continuity in this implementation.

ABI-344 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-344 and do not submit another unchanged late36 connectivity-anchor/recall-sidecar continuation. The mechanism partially meets the recall/MIT objective, but the compactness and connectivity guard is not strong enough and the result does not replace ABI-324 or ABI-223 as a comparator.

If this temporal C4/detail-consensus family is revisited, the next Candidate must be mechanism-changing and should explicitly preserve ABI-324-style negative-patch compactness and connectivity before adding recall. A simple sidecar gain change, another soft-band residual, or another unchanged late36 temporal C4 residual-head variant is not justified. Broader temporal attention/evidence-sharpening, a materially different alignment/change mechanism, or a non-temporal C4/orientation-recall mechanism may be a better frontier move.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_105020_e806bb/candidate/PROPOSAL.md`
- `run_20260918_105020_e806bb/candidate/README.md`
- `run_20260918_105020_e806bb/candidate/manifest.yaml`
- `run_20260918_105020_e806bb/candidate/budget_request.yaml`
- `run_20260918_105020_e806bb/resolved_manifest.yaml`
- `run_20260918_105020_e806bb/execution.json`
- `run_20260918_105020_e806bb/outputs/model_summary.json`
- `run_20260918_105020_e806bb/outputs/best_metrics.json`
- `run_20260918_105020_e806bb/outputs/final_metrics.json`
- `run_20260918_105020_e806bb/outputs/metrics.jsonl`
- `run_20260918_105020_e806bb/outputs/resource_profile.json`
- `run_20260918_105020_e806bb/outputs/validation_postprocessing/index.json`
- `run_20260918_105020_e806bb/outputs/prediction_samples/samples.json`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparison context
- `run_20260917_201833_57b081/outputs/best_metrics.json` and `/history/research-notes/abi337-temporal-fiveframe-detail-consensus-no-mirroring-late36.md` for ABI-337 comparison context
- `run_20260918_031022_a8f552/outputs/best_metrics.json` and `/history/research-notes/abi341-temporal-fiveframe-compact-continuity-recall-router-late36.md` for ABI-341 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
