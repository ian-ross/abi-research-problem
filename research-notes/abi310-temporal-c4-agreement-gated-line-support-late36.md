# ABI-310 temporal C4 agreement-gated line-support late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-310, Candidate `abi310_temporal_c4_agreement_gated_line_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260914_232554_0320e8`.

ABI-310 was a mechanism-changing continuation of the profiled temporal C4 line-state U-Net branch. It kept the provider-owned three-frame temporal input (`abi_16ch_plus_sza_temporal`, offsets `[-1, 0, 1]`, `temporal_eligible_center`), BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The changed mechanism was an agreement-gated line-support head intended to retain part of ABI-309's recall recovery while suppressing unsupported line-state evidence and moving prediction compactness back toward ABI-306.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-310 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs; request approved as `late_improving_parent_completed`.
- Direct parents/comparators: ABI-306, `run_20260914_124245_de843c`, and ABI-309, `run_20260914_205014_1794f8`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,252,835, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.85 / 6.22 GB.
- Total Run wall time: 8,261.0 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-310 agreement-gated support | ABI-306 compact C4 dual-evidence | Delta vs ABI-306 | ABI-309 late line-support recall | Delta vs ABI-309 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 36 | +0 | 29 | +7 |
| Filtered Dice | 0.417524 | 0.422548 | -0.005024 | 0.423544 | -0.006019 |
| Raw Dice | 0.434711 | 0.441449 | -0.006739 | 0.439038 | -0.004327 |
| MIT filtered Dice | 0.403431 | 0.402764 | +0.000668 | 0.402446 | +0.000985 |
| Google filtered Dice | 0.453585 | 0.476152 | -0.022567 | 0.478510 | -0.024925 |
| Filtered precision | 0.438475 | 0.493422 | -0.054946 | 0.401806 | +0.036669 |
| Filtered recall | 0.398484 | 0.369478 | +0.029006 | 0.447768 | -0.049284 |
| Filtered connectivity | 0.284845 | 0.299384 | -0.014540 | 0.316074 | -0.031229 |
| Filtered predicted-positive fraction | 0.004698 | 0.003871 | +0.000827 | 0.005761 | -0.001063 |
| Filtered predicted-positive pixels | 496,940 | 409,457 | +87,483 | 609,361 | -112,421 |

ABI-310 partially achieved the intended precision/recall interpolation but did not improve the temporal C4 frontier. Relative to ABI-309, the agreement gate recovered compactness: precision improved by about +0.0367 and the filtered footprint shrank by about 112k pixels. Relative to ABI-306, recall improved by about +0.0290, so the head did retain some of ABI-309's recall-support behavior.

The costs are material. ABI-310 loses aggregate filtered Dice to both parents, primarily through a Google filtered Dice regression of about -0.0226 versus ABI-306 and -0.0249 versus ABI-309. It also fails to preserve connectivity, landing below both parents. MIT filtered Dice is slightly better than both parents, but this does not offset the Google and connectivity losses.

At the selected checkpoint, raw Dice was 0.434711 versus filtered Dice 0.417524, raw recall was 0.430653 versus filtered recall 0.398484, and raw predicted-positive pixels were 536,603 versus 496,940 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.192803 | 0.183222 | 0.217148 | 0.388477 | 0.128220 | 0.288559 | 0.001706 |
| 3 | 0.318560 | 0.301282 | 0.358983 | 0.354133 | 0.289482 | 0.204404 | 0.004226 |
| 5 | 0.344936 | 0.325157 | 0.391780 | 0.367961 | 0.324623 | 0.259539 | 0.004561 |
| 8 | 0.383655 | 0.361215 | 0.442693 | 0.484548 | 0.317537 | 0.322360 | 0.003388 |
| 11 | 0.380538 | 0.358370 | 0.435567 | 0.442479 | 0.333809 | 0.268198 | 0.003900 |
| 15 | 0.408579 | 0.387875 | 0.463190 | 0.454269 | 0.371239 | 0.384909 | 0.004225 |
| 19 | 0.396979 | 0.372624 | 0.461484 | 0.491446 | 0.332974 | 0.348159 | 0.003503 |
| 23 | 0.402127 | 0.376961 | 0.467557 | 0.486446 | 0.342721 | 0.325275 | 0.003642 |
| 27 | 0.411209 | 0.387815 | 0.475417 | 0.535647 | 0.333689 | 0.455282 | 0.003220 |
| 31 | 0.397134 | 0.375759 | 0.452211 | 0.485027 | 0.336209 | 0.297925 | 0.003583 |
| 34 | 0.406675 | 0.382366 | 0.469906 | 0.486684 | 0.349259 | 0.323810 | 0.003710 |
| 36 | 0.417524 | 0.403431 | 0.453585 | 0.438475 | 0.398484 | 0.284845 | 0.004698 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The best aggregate filtered Dice appears at the final epoch, well beyond the 12-epoch exploratory ceiling. However, the late improvement is a trade-off rather than a clean convergence pattern: epoch 27 showed the most compact/high-connectivity state, while epoch 36 improved aggregate Dice by raising recall and MIT support but degraded Google Dice, precision, and connectivity.

This pattern suggests the agreement gate can control ABI-309's broad footprint, but it does not stably combine ABI-306 precision, ABI-309 recall, and connected-line continuity in one checkpoint.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4138, 0.3645, 0.5652, and 0.3050. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, but it does not establish promotion evidence.

## Interpretation

Classify ABI-310 as valid mixed/negative temporal C4 family-development evidence. The mechanism answered the immediate ABI-309 question: learned agreement gating can reduce the recall head's footprint and recover some precision. But the resulting middle operating point is inferior on the primary aggregate filtered Dice to both ABI-306 and ABI-309, loses Google source performance, and weakens connectivity.

The temporal C4 line-support branch now has a sharper trade-off map:

- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy variant, with a small selected Dice gain and a large footprint/precision cost.
- ABI-310 is an interpolation: more compact than ABI-309 and more recall-oriented than ABI-306, but not better than either parent on aggregate/source/connectivity evidence.

Because ABI-310 selected its best checkpoint at epoch 36, the late-improving budget was scientifically useful. That does not justify another unchanged ABI-310 continuation. The exact agreement-gated line-support head has not solved the compact-recall-connectivity triad. Future work should broaden to a mechanism-changing temporal calibration or line-continuity design rather than repeating ABI-306/309/310 late36 variants.

## Decision

Do not promote ABI-310. Do not replace ABI-306 as the compact temporal C4 comparator or ABI-309 as the recall-support temporal C4 diagnostic variant. Do not spend another Run on an unchanged ABI-310 late36 continuation.

A future Autonomy Step may request temporal-eligible failure-bucket diagnostics only if the campaign specifically needs to understand whether ABI-310's improved MIT Dice and reduced footprint correspond to fewer negative-patch false positives. Otherwise, the more useful next move is to broaden away from agreement-gated line-support heads toward a different temporal attention/calibration or connected-line mechanism that preserves ABI-306 precision while raising true contrail logits at the fixed threshold.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_232554_0320e8/candidate/PROPOSAL.md`
- `run_20260914_232554_0320e8/candidate/README.md`
- `run_20260914_232554_0320e8/candidate/manifest.yaml`
- `run_20260914_232554_0320e8/candidate/budget_request.yaml`
- `run_20260914_232554_0320e8/resolved_manifest.yaml`
- `run_20260914_232554_0320e8/execution.json`
- `run_20260914_232554_0320e8/outputs/model_summary.json`
- `run_20260914_232554_0320e8/outputs/best_metrics.json`
- `run_20260914_232554_0320e8/outputs/final_metrics.json`
- `run_20260914_232554_0320e8/outputs/metrics.jsonl`
- `run_20260914_232554_0320e8/outputs/resource_profile.json`
- `run_20260914_232554_0320e8/outputs/validation_postprocessing/index.json`
- `run_20260914_232554_0320e8/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 parent comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 parent comparison context
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md` for ABI-309 diagnostic context
- `run_20260914_151259_e64cba/outputs/best_metrics.json` and `/history/research-notes/abi307-temporal-c4-center-detail-recall-bridge-late36.md` for ABI-307 comparison context
- `run_20260914_175746_f48be2/outputs/best_metrics.json` and `/history/research-notes/abi308-temporal-c4-selective-agreement-center-detail-late36.md` for ABI-308 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-attention-fusion-unet-late36.md` for temporal-attention comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
