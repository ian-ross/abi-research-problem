# ABI-337 temporal five-frame detail-consensus no-mirroring late36

research-figures: []

## Scope

This note records ABI-337, Candidate `abi337_temporal_fiveframe_detail_consensus_no_mirroring_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_201833_57b081`, and Post-Run Evaluation `eval_evalreq_abi337_temporal_eligible_failure_buckets_v1`.

ABI-337 was a controlled data-policy continuation of ABI-324. It kept the five-frame temporal C4/detail-consensus architecture, provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The controlled change was disabling trusted `random_mirroring` by setting the allowlisted augmentation policy to `none`, testing whether preserving physical GOES scan/illumination orientation would improve MIT-positive undercoverage or connected-line continuity.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a promotion comparison against ABI-202 or ABI-249.

## Execution result

ABI-337 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324 (`run_20260916_184108_954ec7`) and ABI-311 (`run_20260915_015552_1ac51f`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `none`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,254,908, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,557,149,696 / 6,920,601,600 bytes.
- Training wall time: 5,262.9 s; validation wall time: 3,469.4 s; total Run wall time: 8,734.4 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation and evaluation metrics

| Metric | ABI-337 no mirroring | ABI-324 mirrored parent | Delta vs ABI-324 | ABI-325 positive-tail | ABI-328 soft-shift align | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 0 | 27 | 36 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.428894 | 0.429430 | -0.000537 | 0.427745 | 0.423805 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.411838 | 0.408188 | +0.003651 | 0.412855 | 0.403841 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.476340 | 0.487231 | -0.010892 | 0.466540 | 0.476913 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.466489 | 0.470412 | -0.003923 | 0.425680 | 0.444466 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.396906 | 0.395017 | +0.001889 | 0.429830 | 0.404980 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.365326 | 0.397925 | -0.032600 | 0.327452 | 0.322966 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 465,248 | 459,172 | +6,076 | 552,142 | 498,234 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-337 nearly tied ABI-324 on aggregate filtered Dice while modestly improving MIT filtered Dice and fixed-threshold recall. However, the gains are small and do not come with the hoped-for connected-line improvement. The same checkpoint loses about 0.033 filtered connectivity and about 0.011 Google filtered Dice versus ABI-324, while slightly expanding the filtered footprint. The result is therefore a mixed but not positive no-mirroring control: it suggests a small MIT/recall shift, not a broadly better operating point.

At the selected checkpoint, raw Dice was 0.446983 versus filtered Dice 0.428894, raw recall was 0.428476 versus filtered recall 0.396906, and raw predicted-positive pixels were 501,531 versus 465,248 filtered. Artifact Filters reduced footprint and score; they did not create the Result.

## Failure-bucket diagnostic observations

The evaluation request completed as `eval_evalreq_abi337_temporal_eligible_failure_buckets_v1` on the same 1,614-sample temporal-eligible validation population. Its aggregate metrics match the best-checkpoint validation metrics, and the retained `per_sample_metrics.jsonl` and `threshold_sweep.json` were used for bounded diagnostics.

Source/positive/negative buckets from the evaluation artifacts show the trade-off more clearly:

| Bucket metric | ABI-337 MIT | ABI-324 MIT | ABI-337 Google | ABI-324 Google |
| --- | ---: | ---: | ---: | ---: |
| Positive samples | 423 | 423 | 296 | 296 |
| Positive mean filtered recall | 0.4015 | 0.3975 | 0.4420 | 0.4452 |
| Positive mean filtered Dice | 0.3699 | 0.3709 | 0.4396 | 0.4289 |
| Positive mean connectivity | 0.3668 | 0.3638 | 0.4408 | 0.4269 |
| Complete positive misses | 49 | 39 | 30 | 33 |
| Positive samples with recall < 0.25 | 124 | 131 | 72 | 76 |
| Positive samples with recall < 0.50 | 259 | 273 | 169 | 157 |
| Negative samples | 492 | 492 | 403 | 403 |
| Negative samples with any filtered prediction | 301 | 294 | 290 | 239 |
| Negative samples with >128 filtered predicted pixels | 82 | 62 | 27 | 16 |
| Negative samples with >512 filtered predicted pixels | 10 | 6 | 0 | 0 |
| Negative mean filtered predicted pixels | 68.2 | 54.8 | 40.4 | 32.6 |
| Negative total filtered false-positive pixels | 33,575 | 26,974 | 16,277 | 13,123 |

The MIT-positive bucket is genuinely ambiguous: mean recall improves slightly and low-recall counts improve, but complete misses increase. Google positive samples improve in mean per-sample Dice/connectivity but lose mean recall and show worse recall<0.50 count. Negative-patch clutter worsens for both sources, especially Google any-prediction frequency and MIT >128-pixel clutter. This does not support a clean physical-orientation stability win.

Threshold diagnostics also argue against treating the no-mirroring branch as a new fixed-threshold comparator. ABI-337's best diagnostic filtered Dice was 0.434109 at threshold 0.20, versus 0.428894 at the fixed 0.50 threshold. ABI-324's best diagnostic filtered Dice was 0.433856 at threshold 0.25, versus 0.429430 at fixed 0.50. The diagnostic optima are close and below the level needed to justify Candidate-owned thresholding; fixed-threshold selection remains the trusted comparison surface.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232648 | 0.236480 | 0.224233 | 0.253491 | 0.214972 | 0.150837 | 0.004384 |
| 5 | 0.343866 | 0.324144 | 0.394559 | 0.462958 | 0.273509 | 0.333272 | 0.003054 |
| 10 | 0.379298 | 0.358688 | 0.432442 | 0.475803 | 0.315339 | 0.363726 | 0.003426 |
| 15 | 0.356783 | 0.339639 | 0.405968 | 0.611593 | 0.251853 | 0.508529 | 0.002129 |
| 20 | 0.402538 | 0.382394 | 0.456158 | 0.464479 | 0.355173 | 0.306391 | 0.003953 |
| 25 | 0.386275 | 0.362198 | 0.452178 | 0.564318 | 0.293633 | 0.400094 | 0.002690 |
| 27 | 0.428894 | 0.411838 | 0.476340 | 0.466489 | 0.396906 | 0.365326 | 0.004398 |
| 28 | 0.411278 | 0.393586 | 0.455533 | 0.463298 | 0.369761 | 0.317809 | 0.004126 |
| 30 | 0.415409 | 0.396103 | 0.467846 | 0.514628 | 0.348264 | 0.383165 | 0.003498 |
| 32 | 0.428673 | 0.409213 | 0.480076 | 0.449739 | 0.409492 | 0.309856 | 0.004707 |
| 34 | 0.406175 | 0.387173 | 0.456443 | 0.496788 | 0.343518 | 0.334478 | 0.003575 |
| 36 | 0.420566 | 0.404516 | 0.465129 | 0.424628 | 0.416580 | 0.275891 | 0.005072 |

The trajectory remains finite, source-informative, and late-budget-dependent. It also remains oscillatory. Epoch 15 found a very high-precision/high-connectivity compact state with weak recall and low Dice; epoch 27 selected the best aggregate Dice; epoch 32 nearly tied that Dice with higher recall but much lower connectivity; and the final epoch pushed recall higher with another connectivity loss. This repeats the temporal C4 family's core decoupling between compact connected states and higher-recall fixed-threshold states.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3160, 0.0756, 0.5776, and 0.3185. These confirm finite non-collapsed predictions, but the second retained example is weak and the sample set does not overturn the aggregate and bucket evidence.

## Interpretation

Classify ABI-337 as mixed capped temporal-family data-policy evidence, not a new temporal comparator. Disabling mirroring produced a small MIT/recall shift and preserved aggregate Dice close to ABI-324, but it did not improve the main targeted connected-line metric and it worsened negative-patch clutter. The strongest safe interpretation is that random mirroring is not clearly harmful for this branch; if anything, it appears to regularize source balance and clutter while preserving better aggregate connectivity.

Comparator roles after ABI-337:

- ABI-324 remains the strongest local balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 is a useful no-mirroring diagnostic control, showing small MIT/recall changes but lower connectivity and more negative clutter.
- ABI-325 remains the positive-tail recall diagnostic, not a balanced comparator.
- ABI-328 remains negative-to-mixed evidence for local soft-shift alignment alone.
- ABI-311 remains the earlier five-frame C4 parent; ABI-306 remains the compact high-precision temporal C4 comparator; ABI-309 remains the broad recall-heavy temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-337 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-337 and do not submit another unchanged no-mirroring late36 continuation of the ABI-324 branch. Keep ABI-324 as the balanced temporal C4/detail-consensus comparator. If this family is revisited, the next Run should be mechanism-changing and explicitly address the persistent decoupling between high-connectivity compact states and higher-recall states; simply preserving physical orientation by disabling trusted mirroring is not sufficient.

No additional Evaluation Request is needed from ABI-337 because the temporal-eligible failure-bucket review has already completed and shows a mixed source/clutter trade-off rather than a hidden favorable failure mode. No Candidate Submission, Experiment Batch Submission, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_201833_57b081/candidate/PROPOSAL.md`
- `run_20260917_201833_57b081/candidate/README.md`
- `run_20260917_201833_57b081/candidate/manifest.yaml`
- `run_20260917_201833_57b081/candidate/budget_request.yaml`
- `run_20260917_201833_57b081/resolved_manifest.yaml`
- `run_20260917_201833_57b081/execution.json`
- `run_20260917_201833_57b081/outputs/model_summary.json`
- `run_20260917_201833_57b081/outputs/best_metrics.json`
- `run_20260917_201833_57b081/outputs/final_metrics.json`
- `run_20260917_201833_57b081/outputs/metrics.jsonl`
- `run_20260917_201833_57b081/outputs/resource_profile.json`
- `run_20260917_201833_57b081/outputs/validation_postprocessing/index.json`
- `run_20260917_201833_57b081/outputs/prediction_samples/samples.json`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/` for ABI-324 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
