# ABI-280 C4 selective-consensus recall bridge late36

research-figures: []

## Scope

This note records capped Run `run_20260913_023629_7902f3` for Candidate `abi280_fullspectral_btd_sza_c4_selective_consensus_recall_bridge_late36_bce_dice_line_centerline_aux_v1`.

ABI-280 was a close C4/orientation-prior family-development continuation after ABI-249 and ABI-279. The hypothesis was that replacing ABI-279's broad dual-evidence recall bridge with a learned selective consensus gate and bounded low-consensus clutter veto would retain part of ABI-279's recall/connectivity lift while moving precision and compact-prediction behavior closer to ABI-249.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Capped best-validation metrics

The Harness approved the `late_improving` budget and completed 36 epochs. The selected checkpoint was epoch 22 by `val/filtered_dice`.

| Metric | ABI-280 best epoch 22 |
| --- | ---: |
| Filtered Dice | 0.4152 |
| MIT filtered Dice | 0.4051 |
| Google filtered Dice | 0.4421 |
| Filtered precision | 0.4252 |
| Filtered recall | 0.4058 |
| Filtered contrail connectivity | 0.3163 |
| Filtered predicted-positive fraction | 0.00346 |
| Filtered predicted-positive pixels | 464,188 |
| Raw Dice | 0.4304 |

Relative to ABI-249's capped best epoch, ABI-280 was slightly lower in aggregate filtered Dice (-0.0012), higher on MIT Dice (+0.0087), lower on Google Dice (-0.0267), much lower in precision (-0.0557), higher in recall (+0.0386), lower in connectivity (-0.0762), and broader in predicted-positive footprint (+92,842 filtered positive pixels).

Relative to ABI-279's capped best epoch, ABI-280 was only marginally higher in aggregate filtered Dice (+0.0007) and improved MIT Dice (+0.0067) and recall (+0.0160), but it reduced precision (-0.0174), reduced Google Dice (-0.0153), reduced connectivity sharply (-0.1229), and broadened the predicted-positive footprint (+35,772 filtered positive pixels).

## Trajectory observations

ABI-280 was finite and non-collapsed, but the late trajectory was not a clean monotonic improvement. Filtered Dice rose from 0.2036 at epoch 1 to 0.3809 at epoch 12, then oscillated through the late budget. The best filtered Dice occurred at epoch 22. Later epochs repeatedly shifted between recall-heavy and precision-heavy operating points rather than stabilizing a superior tradeoff.

The final epoch reached filtered Dice 0.4029, precision 0.4893, recall 0.3424, connectivity 0.4363, and filtered predicted-positive fraction 0.00254. That final state shows the selective head can produce a compact high-precision/high-connectivity endpoint, but the selected best-Dice checkpoint did not preserve that compactness; it achieved its score through higher recall with lower precision and a broader footprint.

## Interpretation

ABI-280 partially answered the mechanism question. The selective consensus head did not simply collapse; it found a viable capped Dice point near ABI-249/ABI-279 and improved MIT capped Dice. However, it did not deliver the intended combined tradeoff. At the selected checkpoint it behaved more like an even broader recall bridge than a selective precision-preserving bridge: recall improved, but precision, Google Dice, connectivity, and compactness all moved in the wrong direction relative to the stated target.

The final epoch's high precision and connectivity suggest the architecture has internal capacity for compact line evidence, but this capacity is unstable under the approved fixed-threshold selection objective. Because the best checkpoint fails the main precision/compactness goal and the late36 trajectory is oscillatory, ABI-280 is not a stronger C4 comparator than ABI-249 and is not a clear whole-validation diagnostic priority over already evaluated ABI-279.

## Decision

Do not promote ABI-280. Do not repeat the exact selective-consensus head unchanged and do not request another late budget for this branch. A whole-validation failure-bucket evaluation is not the highest-priority next handoff from this capped result because the selected checkpoint did not improve the intended precision/recall/connectivity tradeoff versus ABI-249/279.

Future C4 work should be mechanism-changing if pursued: preserve the compact high-precision behavior of ABI-249 while adding recall support that does not broaden negative-patch clutter or destabilize connectivity. More promising next hypotheses may broaden away from this exact C4 head toward temporal evidence sharpening with orientation consensus, source-balanced architecture-level calibration, or another compact mechanism that raises true contrail logits at threshold 0.5 without Candidate-owned thresholds, postprocessing, losses, metrics, data loading, sampling, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_023629_7902f3/outputs/best_metrics.json`
- `run_20260913_023629_7902f3/outputs/final_metrics.json`
- `run_20260913_023629_7902f3/outputs/metrics.jsonl`
- `run_20260913_023629_7902f3/outputs/model_summary.json`
- `run_20260913_023629_7902f3/outputs/resource_profile.json`
- `run_20260913_023629_7902f3/outputs/prediction_samples/samples.json`
- `run_20260913_023629_7902f3/resolved_manifest.yaml`
- `run_20260913_023629_7902f3/candidate/PROPOSAL.md`
- `run_20260913_023629_7902f3/candidate/budget_request.yaml`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json`
- `run_20260913_000141_3344db/outputs/best_metrics.json`
- `/history/research-notes/abi279-whole-validation-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
