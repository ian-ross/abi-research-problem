# ABI-341 temporal five-frame compact continuity recall router late36

research-figures: []

## Scope

This note records ABI-341, Candidate `abi341_temporal_fiveframe_compact_continuity_recall_router_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260918_031022_a8f552`, and Post-Run Evaluation `eval_evalreq_abi341_temporal_eligible_failure_buckets_v1`.

ABI-341 was a mechanism-changing continuation of the five-frame temporal C4/detail-consensus branch. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The architectural change was `CompactContinuityRecallRouterHead`: a small signed compact continuity anchor plus a bounded non-negative recall lift in the soft uncertainty band, gated by mask/Line/Centerline/detail/temporal line-state evidence agreement.

This is capped temporal-eligible diagnostic evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-341 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324, ABI-337, and ABI-338 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,255,210, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,598,057,472 / 6,987,710,464 bytes.
- Training wall time: 5,343.4 s; validation wall time: 3,489.3 s; total Run wall time: 8,834.9 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation and evaluation metrics

| Metric | ABI-341 recall router | ABI-324 balanced parent | ABI-337 no mirroring | ABI-338 soft-band reinjector | ABI-325 positive-tail | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 27 | 36 | 27 | 36 |
| Filtered Dice | 0.417101 | 0.429430 | 0.428894 | 0.414875 | 0.427745 | 0.419776 |
| MIT filtered Dice | 0.397921 | 0.408188 | 0.411838 | 0.393182 | 0.412855 | 0.398498 |
| Google filtered Dice | 0.465708 | 0.487231 | 0.476340 | 0.473735 | 0.466540 | 0.476764 |
| Filtered precision | 0.418916 | 0.470412 | 0.466489 | 0.477241 | 0.425680 | 0.483764 |
| Filtered recall | 0.415302 | 0.395017 | 0.396906 | 0.366925 | 0.429830 | 0.370738 |
| Filtered connectivity | 0.279162 | 0.397925 | 0.365326 | 0.352106 | 0.327452 | 0.412427 |
| Filtered predicted-positive pixels | 542,094 | 459,172 | 465,248 | 420,414 | 552,142 | 419,056 |

ABI-341 did recover some fixed-threshold recall over ABI-324 and ABI-337, but the recall was too expensive. Relative to ABI-324 it lost -0.0123 filtered Dice, -0.0103 MIT Dice, -0.0215 Google Dice, -0.0515 precision, and -0.1188 connectivity while adding 82,922 filtered predicted-positive pixels. It also underperformed the ABI-325 positive-tail diagnostic on aggregate Dice, MIT Dice, precision, recall, and connectivity while retaining a similarly broad footprint.

At the selected checkpoint, raw Dice was 0.433209 versus filtered Dice 0.417101, raw recall was 0.448695 versus filtered recall 0.415302, and raw predicted-positive pixels were 585,907 versus 542,094 filtered. Artifact Filters removed 43,813 predicted-positive pixels and lowered the score; they did not create the Result.

## Failure-bucket diagnostic observations

The Post-Run Evaluation completed on the same 1,614 temporal-eligible validation ABI Patches. It confirms a real positive-tail recall effect, but also shows that the effect is not clean enough to continue this exact router branch.

| Bucket metric | ABI-341 MIT | ABI-341 Google |
| --- | ---: | ---: |
| Positive samples | 423 | 296 |
| Positive mean filtered recall | 0.4371 | 0.5200 |
| Positive mean filtered Dice | 0.3760 | 0.4517 |
| Positive mean connectivity | 0.3710 | 0.4548 |
| Positive median filtered Dice | 0.4006 | 0.4973 |
| Positive median filtered recall | 0.4478 | 0.5439 |
| Complete positive misses | 32 | 25 |
| Positive samples with recall < 0.25 | 95 | 49 |
| Positive samples with recall < 0.50 | 247 | 121 |
| Negative samples | 492 | 403 |
| Negative samples with any filtered prediction | 386 | 350 |
| Negative samples with >128 filtered predicted pixels | 121 | 49 |
| Negative samples with >512 filtered predicted pixels | 10 | 0 |
| Negative total filtered false-positive pixels | 46,378 | 25,399 |

Across both Dataset Sources, ABI-341 had 57 complete positive misses, 82 positive patches with filtered Dice below 0.1, 126 below 0.2, and 144 with filtered recall below 0.25. These are better positive-tail counts than ABI-324's 72 complete misses, 100 Dice-below-0.1 patches, 150 Dice-below-0.2 patches, and 207 recall-below-0.25 patches. The recall router therefore did what it was designed to do in one narrow sense: it found more true contrail pixels on hard positive patches.

The negative-patch clutter cost is the hard stop. ABI-341 touched 736 of 895 negative temporal-eligible validation patches and accumulated 71,777 negative-patch false-positive pixels. ABI-324 touched 533 negatives with 40,097 negative-patch false-positive pixels; ABI-337 touched 591 negatives with 49,852 negative-patch false-positive pixels. ABI-341 also had 231 negative patches above 100 filtered predicted pixels and 13 above 500. This is not a compact-state-protected recall lift; it is much closer to the broad-footprint recall mode that the branch was supposed to avoid.

The source pattern remains a Google-over-MIT quality gap rather than source collapse. ABI-341's Google filtered Dice is about +0.0678 above MIT at the selected checkpoint, and positive-patch median recall is substantially higher on Google. The MIT tail improves relative to ABI-324 on recall counts, but the improvement arrives with MIT negative clutter rising to 46,378 false-positive pixels.

## Threshold behavior

The threshold sweep does not reveal a useful hidden calibration reserve:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low-threshold high-recall reference | 0.10 | 0.413560 | 0.355185 | 0.494898 | 761,902 |
| Best filtered Dice | 0.30 | 0.418729 | 0.396953 | 0.443032 | 610,286 |
| Primary evaluation | 0.50 | 0.417101 | 0.418916 | 0.415302 | 542,094 |
| High-precision reference | 0.70 | 0.411824 | 0.440846 | 0.386387 | 479,263 |
| Very high threshold reference | 0.90 | 0.379771 | 0.477463 | 0.315266 | 361,056 |

The best diagnostic filtered Dice is only +0.0016 above the fixed 0.50 threshold and occurs with an even larger footprint. This confirms that ABI-341 is not failing because the trusted threshold happens to miss a much better operating point. It also does not authorize Candidate-owned thresholding, postprocessing, calibration, metrics, losses, Artifact Filters, or validation selection.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232169 | 0.231932 | 0.232732 | 0.273808 | 0.201523 | 0.180557 | 0.003805 |
| 5 | 0.335032 | 0.316976 | 0.381247 | 0.475019 | 0.258773 | 0.376822 | 0.002816 |
| 10 | 0.376362 | 0.357497 | 0.423013 | 0.419334 | 0.341379 | 0.279836 | 0.004209 |
| 15 | 0.393251 | 0.369981 | 0.453566 | 0.505870 | 0.321644 | 0.450954 | 0.003287 |
| 20 | 0.379408 | 0.352297 | 0.449743 | 0.517739 | 0.299410 | 0.366708 | 0.002990 |
| 25 | 0.358424 | 0.329805 | 0.435373 | 0.582602 | 0.258829 | 0.456482 | 0.002297 |
| 27 | 0.417101 | 0.397921 | 0.465708 | 0.418916 | 0.415302 | 0.279162 | 0.005125 |
| 28 | 0.395888 | 0.369178 | 0.463532 | 0.491591 | 0.331375 | 0.366990 | 0.003485 |
| 30 | 0.368871 | 0.337418 | 0.448398 | 0.517777 | 0.286482 | 0.364027 | 0.002860 |
| 32 | 0.400012 | 0.376107 | 0.460260 | 0.499166 | 0.333722 | 0.326362 | 0.003456 |
| 34 | 0.375591 | 0.350718 | 0.439048 | 0.468633 | 0.313375 | 0.290557 | 0.003457 |
| 36 | 0.399122 | 0.375738 | 0.460585 | 0.518506 | 0.324424 | 0.334774 | 0.003235 |

The trajectory was finite, non-collapsed, source-informative, and late-budget-dependent, but it was unstable. Epochs 15 and 25 show high-connectivity/high-precision compact states with insufficient recall and weak aggregate Dice. Epoch 27 is the only strong aggregate/recall state, but it has poor connectivity and a broad footprint. The final epoch regressed to a high-precision/lower-recall state without recovering ABI-324-level connectivity. This repeats the temporal C4 family's persistent decoupling between connected compact states and recall-heavy states.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.5317, 0.4553, 0.5121, and 0.5693. These samples look stronger than many recent retained first-four sets, but the evaluation population shows that the positive-tail improvement comes with broad negative-patch clutter and weak aggregate connectivity.

The diagnostic GeoTIFF samples and per-sample rows are bounded Evaluation artifacts. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-341 as mixed but ultimately negative capped temporal-family evidence for this exact compact-continuity recall-router head. The head provides useful evidence that architecture-internal uncertainty-band recall routing can reduce positive-patch complete misses and low-recall tails. However, the compact-continuity guard did not prevent broad false positives, and the selected checkpoint's connectivity is worse than ABI-324, ABI-337, ABI-338, ABI-325, and ABI-223.

Comparator roles after ABI-341:

- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 remains a useful no-mirroring diagnostic control, not a new comparator.
- ABI-325 remains the positive-tail/broad-footprint recall diagnostic and is stronger than ABI-341 as a recall-mode comparator.
- ABI-338 remains negative evidence for soft-band continuity reinjection.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-341 is evidence that positive-tail repair is possible in this family, but not with this router's current clutter/connectivity trade-off.

ABI-341 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-341 and do not submit another unchanged late36 compact-continuity recall-router continuation. The success criteria were only partially met: positive-tail recall improved, but aggregate/source Dice, precision, negative-patch clutter, and connectivity are not competitive with ABI-324 or ABI-223.

If this temporal C4/detail-consensus family is revisited, the next Candidate must be mechanism-changing and should explicitly constrain clutter and preserve connected-line evidence while keeping the positive-tail benefit. A simple increase/decrease of the recall lift, another soft-band residual, or another unchanged late36 head variant is not justified. Broader temporal attention/evidence-sharpening or a non-temporal C4/orientation-recall mechanism may be a better frontier move.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_031022_a8f552/candidate/PROPOSAL.md`
- `run_20260918_031022_a8f552/candidate/README.md`
- `run_20260918_031022_a8f552/candidate/manifest.yaml`
- `run_20260918_031022_a8f552/candidate/budget_request.yaml`
- `run_20260918_031022_a8f552/resolved_manifest.yaml`
- `run_20260918_031022_a8f552/execution.json`
- `run_20260918_031022_a8f552/outputs/model_summary.json`
- `run_20260918_031022_a8f552/outputs/best_metrics.json`
- `run_20260918_031022_a8f552/outputs/final_metrics.json`
- `run_20260918_031022_a8f552/outputs/metrics.jsonl`
- `run_20260918_031022_a8f552/outputs/resource_profile.json`
- `run_20260918_031022_a8f552/outputs/validation_postprocessing/index.json`
- `run_20260918_031022_a8f552/outputs/prediction_samples/samples.json`
- `run_20260918_031022_a8f552/outputs/evaluations/eval_evalreq_abi341_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260918_031022_a8f552/outputs/evaluations/eval_evalreq_abi341_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_031022_a8f552/outputs/evaluations/eval_evalreq_abi341_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260918_031022_a8f552/outputs/evaluations/eval_evalreq_abi341_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260918_031022_a8f552/outputs/evaluations/eval_evalreq_abi341_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparison context
- `run_20260917_201833_57b081/outputs/best_metrics.json` and `/history/research-notes/abi337-temporal-fiveframe-detail-consensus-no-mirroring-late36.md` for ABI-337 comparison context
- `run_20260917_230319_ed1362/outputs/best_metrics.json` and `/history/research-notes/abi338-temporal-softband-continuity-reinjector-late36.md` for ABI-338 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
