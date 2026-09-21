# ABI-308 temporal C4 selective agreement center-detail late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-308, Candidate `abi308_temporal_c4_selective_agreement_center_detail_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260914_175746_f48be2`.

ABI-308 was a mechanism-changing continuation of the temporal C4 line-state U-Net branch. It kept the provider-owned three-frame temporal input (`abi_16ch_plus_sza_temporal`, offsets `[-1, 0, 1]`, `temporal_eligible_center`), BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The intended mechanism was a selective agreement-gated center-detail bridge: reduce ABI-307's broad center-detail residuals by requiring decoder/detail/temporal-line-state agreement and orientation-detail consensus before injecting a lower-amplitude residual.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-308 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Direct parents/comparators: ABI-306, `run_20260914_124245_de843c`, and ABI-307, `run_20260914_151259_e64cba`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,306,448, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.76 / 7.12 GiB.
- Total Run wall time: 8,813.3 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 31.

## Best-validation metrics

| Metric | ABI-308 selective bridge | ABI-306 dual-evidence line-state | Delta vs ABI-306 | ABI-307 center-detail bridge | Delta vs ABI-307 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 31 | 36 | -5 | 36 | -5 |
| Filtered Dice | 0.410731 | 0.422548 | -0.011818 | 0.420526 | -0.009795 |
| Raw Dice | 0.429809 | 0.441449 | -0.011640 | 0.438888 | -0.009079 |
| MIT filtered Dice | 0.392983 | 0.402764 | -0.009781 | 0.404932 | -0.011949 |
| Google filtered Dice | 0.456340 | 0.476152 | -0.019812 | 0.460655 | -0.004314 |
| Filtered precision | 0.483193 | 0.493422 | -0.010229 | 0.470249 | +0.012944 |
| Filtered recall | 0.357168 | 0.369478 | -0.012310 | 0.380314 | -0.023145 |
| Filtered connectivity | 0.367013 | 0.299384 | +0.067629 | 0.325308 | +0.041706 |
| Filtered predicted-positive fraction | 0.003821 | 0.003871 | -0.000050 | 0.004181 | -0.000360 |
| Filtered predicted-positive pixels | 404,195 | 409,457 | -5,262 | 442,234 | -38,039 |

ABI-308 successfully made the center-detail bridge more compact than ABI-307: precision recovered by about +0.0129, the filtered footprint shrank by about 38k pixels, and Google filtered Dice lost only -0.0043 versus ABI-307 instead of reopening the full ABI-307 clutter/footprint behavior.

However, that selectivity overcorrected. Relative to ABI-306, ABI-308 is worse on aggregate filtered Dice (-0.0118), MIT filtered Dice (-0.0098), Google filtered Dice (-0.0198), precision (-0.0102), and recall (-0.0123). The main positive signal is connectivity: ABI-308's selected checkpoint reaches 0.3670, substantially above ABI-306 and ABI-307 and near ABI-238-style temporal directional context, but this comes without the required Dice/recall improvement.

At the selected checkpoint, raw Dice was 0.429809 versus filtered Dice 0.410731, raw recall was 0.386023 versus filtered recall 0.357168, and raw predicted-positive pixels were 435,401 versus 404,195 filtered. Artifact Filters reduce both footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.200196 | 0.211166 | 0.180125 | 0.172308 | 0.238854 | 0.094169 | 0.007166 |
| 3 | 0.301802 | 0.283703 | 0.345760 | 0.391117 | 0.245695 | 0.215412 | 0.003247 |
| 5 | 0.328813 | 0.307988 | 0.383180 | 0.511204 | 0.242347 | 0.355774 | 0.002451 |
| 8 | 0.360332 | 0.340134 | 0.413243 | 0.469579 | 0.292324 | 0.348256 | 0.003218 |
| 11 | 0.380402 | 0.364175 | 0.420268 | 0.403024 | 0.360184 | 0.292964 | 0.004620 |
| 15 | 0.371358 | 0.355409 | 0.413425 | 0.427578 | 0.328204 | 0.344351 | 0.003968 |
| 19 | 0.374489 | 0.352445 | 0.430806 | 0.466898 | 0.312616 | 0.312512 | 0.003461 |
| 23 | 0.347265 | 0.318138 | 0.425576 | 0.539054 | 0.256136 | 0.420624 | 0.002456 |
| 27 | 0.368193 | 0.340864 | 0.440800 | 0.528374 | 0.282540 | 0.379242 | 0.002764 |
| 31 | 0.410731 | 0.392983 | 0.456340 | 0.483193 | 0.357168 | 0.367013 | 0.003821 |
| 34 | 0.396772 | 0.373208 | 0.457864 | 0.496348 | 0.330474 | 0.369728 | 0.003442 |
| 36 | 0.398824 | 0.384396 | 0.436301 | 0.448819 | 0.358851 | 0.305240 | 0.004133 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent: the best epoch appears well after the 12-epoch exploratory ceiling. It is also oscillatory. Epoch 23 reaches very high connectivity (0.4206) and high precision (0.5391) but low recall and weak MIT Dice; epoch 31 recovers the best aggregate Dice by adding recall and MIT support while keeping connectivity above ABI-306/307; epochs 34-36 fail to improve the selected score.

This pattern suggests the selective agreement bridge can stabilize connected predictions in some states, but it suppresses too much true contrail evidence at threshold 0.5 and does not reliably maintain source balance.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4038, 0.4789, 0.6279, and 0.2918. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, but it does not establish promotion evidence.

## Interpretation

Classify ABI-308 as valid but negative/mixed temporal C4 family-development evidence. The selectivity mechanism partially addressed ABI-307's broad-footprint failure mode: the footprint is smaller than both parents, precision improves over ABI-307, and connectivity improves over ABI-306 and ABI-307. But the mechanism also removes too much recall and source-balanced evidence. It falls below ABI-306 on the primary aggregate/precision comparator role and below ABI-307 on the recall-support role.

The center-detail bridge branch now has a clear lesson: broad residual detail support can raise recall/connectivity but broadens positive-patch predictions (ABI-307), while a stricter decoder/detail/line-state agreement gate can recover compactness and connectivity but suppresses fixed-threshold true positives (ABI-308). Neither variant improves the capped temporal-eligible Dice/recall trade-off against ABI-306. ABI-306 remains the compact high-precision temporal C4 comparator; ABI-307 remains mixed evidence that center detail can add true-positive pixels; ABI-308 is not a replacement for either.

Because ABI-308 did not retain a recall gain over ABI-306 and regressed aggregate/source Dice, do not spend another Run on an unchanged ABI-308 late36 continuation. Any future temporal C4 continuation should be mechanism-changing, for example a different temporal line-state recurrence or evidence-sharpening head that raises true contrail logits to threshold 0.5 without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-308 and do not replace ABI-306 as the capped temporal-eligible aggregate/precision comparator. Do not request an unchanged continuation of ABI-306, ABI-307, or ABI-308.

The result does not require immediate operator review or a Capability Request. A future Autonomy Step may either request diagnostics only if the campaign specifically wants to understand ABI-308's high-connectivity/low-recall state, or more usefully broaden to a mechanism-changing temporal architecture that preserves ABI-306 compactness while adding less suppressive connected-recall support.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_175746_f48be2/candidate/PROPOSAL.md`
- `run_20260914_175746_f48be2/candidate/README.md`
- `run_20260914_175746_f48be2/candidate/manifest.yaml`
- `run_20260914_175746_f48be2/candidate/budget_request.yaml`
- `run_20260914_175746_f48be2/resolved_manifest.yaml`
- `run_20260914_175746_f48be2/execution.json`
- `run_20260914_175746_f48be2/outputs/model_summary.json`
- `run_20260914_175746_f48be2/outputs/best_metrics.json`
- `run_20260914_175746_f48be2/outputs/final_metrics.json`
- `run_20260914_175746_f48be2/outputs/metrics.jsonl`
- `run_20260914_175746_f48be2/outputs/resource_profile.json`
- `run_20260914_175746_f48be2/outputs/validation_postprocessing/index.json`
- `run_20260914_175746_f48be2/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 parent comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260914_151259_e64cba/outputs/best_metrics.json` and `/history/research-notes/abi307-temporal-c4-center-detail-recall-bridge-late36.md` for ABI-307 parent comparison context
- `/history/research-notes/abi307-temporal-eligible-failure-bucket-review.md` for ABI-307 diagnostic context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
