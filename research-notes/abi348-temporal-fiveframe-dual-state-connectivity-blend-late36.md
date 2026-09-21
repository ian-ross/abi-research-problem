# ABI-348 temporal five-frame dual-state connectivity blend late36

research-figures: []

## Scope

This note records ABI-348, Candidate `abi348_temporal_fiveframe_dual_state_connectivity_blend_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260918_215534_a35ab9`, and Harness-owned Post-Run Evaluation `eval_evalreq_abi348_temporal_eligible_failure_buckets_v1`.

ABI-348 was a close but mechanism-changing five-frame temporal C4/detail-consensus continuation. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change replaced ABI-324/337-style final evidence construction with a dual-state connectivity blend: a compact connected anchor and bounded recall candidate are mixed only through learned decoder/detail/temporal-line agreement, Line/Centerline evidence, and a disagreement guard.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-348 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested `late_improving` budget was approved from ABI-324, ABI-337, and ABI-344 parent evidence.

Key Harness-owned execution facts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,258,328, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,697,189,888 / 7,107,248,128 bytes.
- Training wall time: 5,364.0 s; validation wall time: 3,495.0 s; total Run wall time: 8,861.2 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Temporal-eligible aggregate metrics

| Metric | ABI-348 dual-state blend | ABI-324 balanced five-frame C4 | ABI-337 no-mirroring five-frame C4 | ABI-344 broad recall sidecar | ABI-325 positive-tail reinjector | ABI-306 compact temporal C4 | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 27 | 27 | 29 | 26 | 36 | 36 |
| Filtered Dice | 0.427829 | 0.429430 | 0.428894 | 0.426448 | 0.427745 | 0.422548 | 0.419776 |
| MIT filtered Dice | 0.410244 | 0.408188 | 0.411838 | 0.412208 | 0.412855 | 0.402764 | 0.398498 |
| Google filtered Dice | 0.478363 | 0.487231 | 0.476340 | 0.462585 | 0.466540 | 0.476152 | 0.476764 |
| Filtered precision | 0.477546 | 0.470412 | 0.466489 | 0.426700 | 0.425680 | 0.493422 | 0.483764 |
| Filtered recall | 0.387488 | 0.395017 | 0.396906 | 0.426196 | 0.429830 | 0.369478 | 0.370738 |
| Filtered connectivity | 0.300904 | 0.397925 | 0.365326 | 0.315733 | 0.327452 | 0.299384 | 0.412427 |
| Filtered predicted-positive pixels | 443,691 | 459,172 | 465,248 | 546,166 | 552,142 | 409,457 | 419,056 |

ABI-348 landed in a compact high-precision state rather than the desired balanced compact/recall/connectivity state. Relative to ABI-324, it is slightly smaller and more precise (+0.0071 precision, -15,481 predicted-positive pixels), but loses aggregate Dice (-0.0016), Google Dice (-0.0089), recall (-0.0075), and especially connectivity (-0.0970). Relative to ABI-337, it improves precision (+0.0111) and compactness (-21,557 predicted-positive pixels) but loses MIT Dice (-0.0016), recall (-0.0094), and connectivity (-0.0644). Relative to ABI-344/325, it is much more compact and precise, but gives back most of their recall gains and does not match their connectivity.

Relative to ABI-306, ABI-348 improves aggregate Dice (+0.0053), MIT Dice (+0.0075), Google Dice (+0.0022), recall (+0.0180), and true-positive pixels (+9,848), while retaining almost identical connectivity (+0.0015). The cost is lower precision (-0.0159), +24,234 false-positive pixels, and +34,234 predicted-positive pixels. This makes ABI-348 a useful five-frame compact/precision operating point, but not a new connected-line comparator.

At the selected checkpoint, raw Dice was 0.445918 versus filtered Dice 0.427829, raw recall was 0.418530 versus filtered recall 0.387488, and raw predicted-positive pixels were 479,641 versus 443,691 filtered. Artifact Filters removed 35,950 predicted-positive pixels and lowered the score; they did not create the Result.

## Failure-bucket observations

The completed temporal-eligible diagnostic shows that ABI-348 reduces negative-patch heavy-tail clutter, but it does so by selecting a conservative low-recall state rather than a better connected-line state.

| Bucket metric | ABI-348 | ABI-324 | ABI-337 | ABI-344 | ABI-325 | ABI-306 | ABI-223 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Positive samples | 719 | 719 | 719 | 719 | 719 | 719 | 719 |
| Complete positive misses | 73 | 72 | 79 | 59 | 70 | 65 | 77 |
| Positive recall < 0.20 | 157 | 165 | 162 | 114 | 131 | 164 | 167 |
| Positive recall < 0.50 | 452 | 430 | 428 | 370 | 377 | 440 | 433 |
| Positive median recall | 0.4082 | 0.4231 | 0.4379 | 0.4887 | 0.4839 | 0.4111 | 0.4227 |
| Positive median Dice | 0.4286 | 0.4265 | 0.4308 | 0.4345 | 0.4419 | 0.4348 | 0.4357 |
| Positive median connectivity | 0.4230 | 0.4099 | 0.4229 | 0.4224 | 0.4277 | 0.4190 | 0.4226 |
| Positive connectivity < 0.20 | 143 | 162 | 148 | 135 | 142 | 139 | 154 |
| Negative samples with any prediction | 700 | 533 | 591 | 671 | 651 | 703 | 515 |
| Negative samples >50 predicted pixels | 258 | 244 | 298 | 372 | 358 | 371 | 332 |
| Negative samples >200 predicted pixels | 28 | 44 | 51 | 80 | 66 | 33 | 53 |
| Total negative-patch predicted pixels | 39,663 | 40,097 | 49,852 | 66,687 | 59,887 | 49,513 | 51,290 |

The positive-tail result is mixed-negative. ABI-348 reduces positive recall <0.20 relative to ABI-324 and ABI-337, but complete misses remain ABI-324-like and positive recall <0.50 worsens substantially. Median positive recall falls to 0.4082, lower than ABI-324, ABI-337, ABI-344, ABI-325, and ABI-223, and essentially similar to compact ABI-306. The diagnostic therefore does not support the hypothesis that the dual-state blend recovers positive-tail recall at ABI-324-like connectivity.

The negative-patch clutter result is the main positive signal. ABI-348 keeps total negative-patch predicted pixels slightly below ABI-324, far below ABI-344/325, and below ABI-306/337/223. It also has only 28 negative samples above 200 predicted pixels, the smallest count among these comparators. However, it still predicts something on 700 negative patches, similar to ABI-306 and ABI-346, so the gain is in high-tail clutter suppression rather than broad negative-patch silence.

Source buckets keep the usual MIT difficulty pattern:

| Source bucket | MIT | Google |
| --- | ---: | ---: |
| Positive samples | 423 | 296 |
| Positive median recall | 0.3816 | 0.4444 |
| Positive median Dice | 0.3973 | 0.4897 |
| Positive median connectivity | 0.3706 | 0.4866 |
| Complete positive misses | 42 | 31 |
| Positive recall < 0.25 | 131 | 77 |
| Negative samples | 492 | 403 |
| Negative samples with any prediction | 364 | 336 |
| Negative samples >128 predicted pixels | 59 | 12 |
| Negative samples >512 predicted pixels | 3 | 0 |
| Total negative-patch predicted pixels | 25,470 | 14,193 |

ABI-348's aggregate MIT Dice is competitive, but MIT positive median recall and connectivity remain materially weaker than Google. The branch did not solve the source-balanced connected-line weakness.

## Threshold behavior

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low threshold | 0.10 | 0.429591 | 0.403945 | 0.458713 | 620,951 |
| Best filtered Dice | 0.20 | 0.432793 | 0.436172 | 0.429466 | 538,404 |
| Primary evaluation | 0.50 | 0.427829 | 0.477546 | 0.387488 | 443,691 |
| High-precision reference | 0.70 | 0.420284 | 0.501637 | 0.361636 | 394,203 |
| Very high threshold reference | 0.90 | 0.387702 | 0.545643 | 0.300670 | 301,314 |

The best diagnostic threshold improves filtered Dice by +0.0050 over the trusted fixed 0.5 threshold. This is moderate low-threshold headroom: less than ABI-346/306/223 and only slightly above ABI-324's small headroom. Architecturally, ABI-348 has some sub-threshold recall reserve, but the fixed-threshold score is not merely a calibration accident. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, Artifact Filters, or validation selection.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.206515 | 0.219243 | 0.183177 | 0.171674 | 0.259100 | 0.107412 | 0.007802 |
| 5 | 0.283847 | 0.269075 | 0.316489 | 0.346337 | 0.240461 | 0.238025 | 0.003589 |
| 8 | 0.375533 | 0.357944 | 0.420257 | 0.445602 | 0.324506 | 0.334416 | 0.003765 |
| 12 | 0.325234 | 0.302627 | 0.376533 | 0.345999 | 0.306820 | 0.195543 | 0.004584 |
| 17 | 0.376711 | 0.349129 | 0.444536 | 0.437146 | 0.330957 | 0.241500 | 0.003914 |
| 24 | 0.368199 | 0.335151 | 0.451180 | 0.483124 | 0.297444 | 0.278771 | 0.003183 |
| 27 | 0.422206 | 0.401621 | 0.478261 | 0.437765 | 0.407716 | 0.365451 | 0.004815 |
| 29 | 0.412978 | 0.397926 | 0.453128 | 0.390795 | 0.437831 | 0.233081 | 0.005792 |
| 31 | 0.402551 | 0.379180 | 0.462014 | 0.476717 | 0.348356 | 0.200751 | 0.003778 |
| 34 | 0.389726 | 0.371100 | 0.436068 | 0.438022 | 0.351022 | 0.244598 | 0.004143 |
| 36 | 0.427829 | 0.410244 | 0.478363 | 0.477546 | 0.387488 | 0.300904 | 0.004195 |

The trajectory was finite, non-collapsed, source-informative, and late-budget-dependent, but unstable. Epoch 27 is closer to the intended balanced state: higher recall (0.4077) and connectivity (0.3655) than the selected epoch, with only a small aggregate Dice deficit. Epoch 29 found high recall but collapsed connectivity and precision. Epoch 36 maximized filtered Dice by moving back toward a compact, high-precision, lower-recall state with weak connectivity. The final selected checkpoint therefore does not demonstrate stable dual-state connectivity blending.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4034, 0.3022, 0.5933, and 0.4189. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-348 as mixed evidence for the five-frame temporal C4 final-head branch and negative evidence for this exact dual-state connectivity-blend head as a new comparator.

The positive result is compactness: ABI-348 achieves near-ABI-324 aggregate Dice while reducing high-tail negative-patch clutter and preserving a decent precision/footprint trade-off. It is a cleaner fixed-threshold footprint than ABI-344/325 broad recall sidecars.

The negative result is that the mechanism did not preserve connected-line continuity or positive-tail recall. It selected an ABI-306-like connectivity state, underperformed ABI-324/337 on recall/connectivity, and did not approach ABI-223's connectivity. Its apparent cleanliness comes mainly from conservative footprint control, not from better line continuity.

Comparator roles after ABI-348:

- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 remains useful no-mirroring/data-policy evidence but is not displaced.
- ABI-344 and ABI-325 remain broad recall-sidecar diagnostics, not comparators.
- ABI-306 remains the compact high-precision temporal C4 comparator; ABI-348 is a five-frame compact variant with slightly better Dice/recall but similar connectivity weakness.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-348 is not a new frontier comparator and is not a promotion candidate.

ABI-348 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-348 and do not submit another unchanged late36 temporal C4 final-head continuation of this dual-state blend. The diagnostic question is answered: guarded blending can suppress high-tail negative clutter, but this implementation does not recover positive-tail recall or connected-line continuity at ABI-324-like quality.

Future work should be mechanism-changing. If the temporal C4 branch is revisited, the next hypothesis should add a stronger temporal alignment/change or line-continuity mechanism before final logits, rather than another final-head blend, residual, or uncertainty-band gate. A reasonable broadening direction would move back toward temporal attention/alignment or a different lightweight backbone that raises true contrail logits at threshold 0.5 while explicitly protecting source balance and continuity.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_215534_a35ab9/candidate/PROPOSAL.md`
- `run_20260918_215534_a35ab9/candidate/README.md`
- `run_20260918_215534_a35ab9/candidate/manifest.yaml`
- `run_20260918_215534_a35ab9/candidate/budget_request.yaml`
- `run_20260918_215534_a35ab9/resolved_manifest.yaml`
- `run_20260918_215534_a35ab9/execution.json`
- `run_20260918_215534_a35ab9/run_metadata.json`
- `run_20260918_215534_a35ab9/outputs/model_summary.json`
- `run_20260918_215534_a35ab9/outputs/best_metrics.json`
- `run_20260918_215534_a35ab9/outputs/final_metrics.json`
- `run_20260918_215534_a35ab9/outputs/metrics.jsonl`
- `run_20260918_215534_a35ab9/outputs/resource_profile.json`
- `run_20260918_215534_a35ab9/outputs/validation_postprocessing/index.json`
- `run_20260918_215534_a35ab9/outputs/prediction_samples/samples.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260917_201833_57b081/outputs/evaluations/eval_evalreq_abi337_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `/history/research-notes/abi347-temporal-c4-orientation-bridge-compact-recall-late36.md`
- `/history/research-notes/abi346-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi337-temporal-fiveframe-detail-consensus-no-mirroring-late36.md`
- `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
