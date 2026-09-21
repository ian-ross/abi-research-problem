# ABI-283 C4 cross-scale consensus recall bridge late36

research-figures: []

## Scope

This note records capped Run `run_20260913_063411_d8a862` for Candidate `abi283_fullspectral_btd_sza_c4_crossscale_consensus_recall_bridge_late36_bce_dice_line_centerline_aux_v1`.

ABI-283 was a close C4/orientation-prior family-development continuation after ABI-249, ABI-279, and ABI-280. The hypothesis was that a cross-scale consensus bridge could keep ABI-279-style recall/connectivity support only where full-resolution C4 line evidence agreed with coarser decoder/context support, thereby reducing clutter while preserving connected thin-line evidence.

The Candidate used provider-approved `abi_16ch_plus_sza` inputs, trusted source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. It remained architecture/manifest-only and did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-283 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, approved from parent Runs `run_20260911_111909_dd7ef7`, `run_20260913_000141_3344db`, and `run_20260913_023629_7902f3`.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,078,698, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 10.57 / 11.87 GiB.
- Training wall time: 4,583.4 s; validation wall time: 4,343.3 s; total Run wall time: 8,929.2 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 31.

## Capped best-validation metrics

| Metric | ABI-283 best epoch 31 | ABI-249 compact C4 | ABI-279 recall bridge | ABI-280 selective consensus | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.412957 | 0.416400 | 0.414518 | 0.415244 | 0.427570 |
| Raw Dice | 0.429271 | 0.432320 | 0.429448 | 0.430420 | 0.442746 |
| Filtered precision | 0.500379 | 0.480886 | 0.442551 | 0.425162 | 0.439467 |
| Filtered recall | 0.351539 | 0.367165 | 0.389825 | 0.405778 | 0.416301 |
| Filtered connectivity | 0.475887 | 0.392524 | 0.439185 | 0.316291 | 0.457773 |
| MIT filtered Dice | 0.393239 | 0.396436 | 0.398381 | 0.405113 | 0.411992 |
| Google filtered Dice | 0.464463 | 0.468855 | 0.457385 | 0.442121 | 0.468151 |
| Filtered predicted-positive fraction | 0.002546 | 0.002767 | 0.003192 | 0.003458 | 0.003433 |
| Filtered predicted-positive pixels | 341,691 | 371,346 | 428,416 | 464,188 | 460,724 |

Relative to ABI-249, ABI-283 did not improve aggregate or source Dice: filtered Dice was lower by about -0.0034, MIT Dice by -0.0032, and Google Dice by -0.0044. It did, however, move the operating point in the intended compact/high-evidence direction: precision improved by +0.0195, connectivity by +0.0834, and the filtered footprint shrank by 29,655 pixels. The cost was lower recall (-0.0156).

Relative to ABI-279, ABI-283 recovered a much more compact prediction footprint and higher precision: +0.0578 precision, +0.0367 connectivity, and 86,725 fewer filtered predicted-positive pixels. Google Dice also improved by +0.0071. But recall dropped by -0.0383, MIT Dice by -0.0051, and aggregate filtered Dice by -0.0016. This means the cross-scale consensus solved part of ABI-279's clutter/precision problem, but did not preserve enough recall.

Relative to ABI-280, ABI-283 is a clearer correction of the selective-consensus failure mode: precision is higher by +0.0752, connectivity by +0.1596, Google Dice by +0.0223, and filtered predicted-positive pixels are lower by 122,497. The tradeoff is again recall and MIT performance: recall is lower by -0.0542 and MIT Dice by -0.0119.

Relative to ABI-202, ABI-283 remains below the aggregate reference by about -0.0146 filtered Dice and is much lower recall (-0.0648), although it is higher precision (+0.0609), slightly higher connectivity (+0.0181), and more compact by 119,033 filtered positive pixels.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.209875 | 0.231785 | 0.174239 | 0.168485 | 0.278225 | 0.138703 | 0.005984 |
| 4 | 0.337663 | 0.327539 | 0.362970 | 0.375666 | 0.306642 | 0.297015 | 0.002958 |
| 8 | 0.377310 | 0.356626 | 0.429868 | 0.456742 | 0.321413 | 0.419908 | 0.002550 |
| 14 | 0.388013 | 0.367029 | 0.440080 | 0.464975 | 0.332910 | 0.443139 | 0.002594 |
| 15 | 0.397232 | 0.386773 | 0.422568 | 0.376288 | 0.420643 | 0.335647 | 0.004051 |
| 21 | 0.402303 | 0.387777 | 0.440401 | 0.371943 | 0.438058 | 0.236465 | 0.004268 |
| 22 | 0.406869 | 0.392686 | 0.442505 | 0.412707 | 0.401193 | 0.340721 | 0.003523 |
| 23 | 0.387400 | 0.359395 | 0.461259 | 0.529197 | 0.305534 | 0.575383 | 0.002092 |
| 28 | 0.401901 | 0.379162 | 0.458946 | 0.476599 | 0.347445 | 0.347928 | 0.002642 |
| 31 | 0.412957 | 0.393239 | 0.464463 | 0.500379 | 0.351539 | 0.475887 | 0.002546 |
| 32 | 0.410393 | 0.390906 | 0.459170 | 0.432766 | 0.390220 | 0.368262 | 0.003267 |
| 35 | 0.392244 | 0.368190 | 0.452864 | 0.506068 | 0.320220 | 0.345333 | 0.002293 |
| 36 | 0.396212 | 0.374850 | 0.446961 | 0.454683 | 0.351066 | 0.291240 | 0.002798 |

The longer budget was useful for characterizing this branch: the best checkpoint arrived at epoch 31, well after the exploratory ceiling. The trajectory is finite and non-collapsed, but still oscillatory. ABI-283 repeatedly alternates between compact high-precision/high-connectivity states and broader higher-recall states. Epoch 23 demonstrates the most extreme compact/connectivity mode, with precision 0.5292 and connectivity 0.5754, but recall falls to 0.3055. Epoch 21 and epoch 32 show higher recall states, but precision/connectivity drop.

The selected epoch 31 is the best compromise this branch found: compact footprint, high precision, strong connectivity, and decent Google Dice. The final epoch does not collapse, but it falls back to lower filtered Dice (0.3962) and much lower connectivity (0.2912), so the branch did not settle into a stable superior late endpoint.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were near zero: `7.1e-09`, `1.1e-08`, `1.3e-09`, and `1.7e-09`. This likely reflects the retained first samples rather than aggregate collapse, because aggregate validation metrics are finite, source-informative, and non-degenerate.

At the selected checkpoint, raw Dice was 0.4293 versus filtered Dice 0.4130, with 365,119 raw predicted-positive pixels versus 341,691 filtered predicted-positive pixels. Artifact Filters therefore lower rather than create the Result.

## Interpretation

Classify ABI-283 as a finite, resource-safe, scientifically useful but not frontier-improving C4 mechanism test. The cross-scale consensus bridge achieved one intended local effect: it made the C4 recall-bridge lineage more compact and more precise while restoring strong connected-line evidence. It is the strongest recent C4 branch on capped precision/connectivity compactness and is cleaner than ABI-279/280 in that narrow sense.

However, the mechanism over-corrected toward conservative evidence. It did not preserve enough true-positive recall to improve aggregate filtered Dice, MIT Dice, or the ABI-249 compact C4 comparator. The filtered Dice deficit is small, but the recall deficit is material and keeps ABI-283 below ABI-202/249 as a promotion target. The high connectivity is real but partially coupled to underprediction, as shown by high-connectivity epochs with depressed recall.

This result narrows the C4/orientation-prior branch. Cross-scale consensus is better than ABI-280's selective consensus for precision, connectivity, and compactness, but it is not enough by itself to solve the fixed-threshold recall problem. Further unchanged C4 bridge work is unlikely to be the best use of Runs unless the next mechanism explicitly raises recall without giving back ABI-283's compactness/connectivity.

## Decision

Do not promote ABI-283. Do not repeat this exact cross-scale consensus head unchanged and do not request another late-improving budget for it.

A whole-validation failure-bucket evaluation is not the highest-priority immediate handoff from this capped Result because ABI-283 remains below ABI-249 and ABI-202 on capped aggregate filtered Dice and recall. It could be considered later only if the campaign specifically needs a compact high-connectivity C4 diagnostic, but the current next-step value is stronger in a mechanism-changing hypothesis that preserves ABI-283's precision/connectivity while adding recall support.

Future work should broaden or materially change mechanism: earlier evidence calibration, dual-evidence heads with explicit recall preservation, temporal evidence sharpening, or another source-balanced architecture-level support path that raises true contrail logits at threshold 0.5 without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, sample selection, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_063411_d8a862/candidate/PROPOSAL.md`
- `run_20260913_063411_d8a862/candidate/README.md`
- `run_20260913_063411_d8a862/candidate/manifest.yaml`
- `run_20260913_063411_d8a862/candidate/budget_request.yaml`
- `run_20260913_063411_d8a862/resolved_manifest.yaml`
- `run_20260913_063411_d8a862/outputs/model_summary.json`
- `run_20260913_063411_d8a862/outputs/best_metrics.json`
- `run_20260913_063411_d8a862/outputs/final_metrics.json`
- `run_20260913_063411_d8a862/outputs/metrics.jsonl`
- `run_20260913_063411_d8a862/outputs/resource_profile.json`
- `run_20260913_063411_d8a862/outputs/validation_postprocessing/index.json`
- `run_20260913_063411_d8a862/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 comparison context
- `run_20260913_000141_3344db/outputs/best_metrics.json` for ABI-279 recall-bridge comparison context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` for ABI-280 selective-consensus comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference comparison context
- `/history/research-notes/abi279-whole-validation-failure-bucket-review.md`
- `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
