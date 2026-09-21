# ABI-295 compact early evidence-calibrated detail U-Net

research-figures: []

## Scope

This note records ABI-295, Candidate `abi295_fullspectral_btd_sza_compact_early_evidence_calibrated_detail_unet_syntax_repair_v1`, Run `run_20260914_000805_a73a22`.

ABI-295 was a repair of ABI-294 after `run_20260914_000407_7232d1` smoke-failed with a candidate-owned indentation bug. It preserved ABI-294's compact early evidence-calibration hypothesis, which itself was a resource-aware follow-up after ABI-293 timed out under the exploratory wall-clock budget. The mechanism was to share calibrated detail and line evidence through compact encoder skips and a calibrated evidence head, testing whether earlier feature-level evidence could recover fixed-threshold contrail support more cleanly than recent late C4/soft-band calibration heads.

The Candidate consumed only provider-approved `abi_16ch_plus_sza` tensors. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-295 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The repair therefore resolved the ABI-294 syntax defect and made the compact ABI-293/294 mechanism evaluable.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 7,020,320, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 12.41 / 13.15 GiB.
- Training wall time: 1,475.2 s; validation wall time: 1,302.5 s; total Run wall time: 2,779.7 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-295 best/final epoch 12 | ABI-292 C4 soft-band calibrator | ABI-283 compact C4 parent | ABI-249 compact C4 comparator | ABI-279 recall bridge | ABI-280 selective consensus | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.380175 | 0.384676 | 0.412957 | 0.416400 | 0.414518 | 0.415244 | 0.427570 |
| Raw Dice | 0.395205 | 0.398552 | 0.429271 | 0.432320 | 0.429448 | 0.430420 | 0.442746 |
| Filtered precision | 0.473625 | 0.404530 | 0.500379 | 0.480886 | 0.442551 | 0.425162 | 0.439467 |
| Filtered recall | 0.317525 | 0.366680 | 0.351539 | 0.367165 | 0.389825 | 0.405778 | 0.416301 |
| Filtered connectivity | 0.470984 | 0.249203 | 0.475887 | 0.392524 | 0.439185 | 0.316291 | 0.457773 |
| MIT filtered Dice | 0.360063 | 0.371401 | 0.393239 | 0.396436 | 0.398381 | 0.405113 | 0.411992 |
| Google filtered Dice | 0.432880 | 0.417038 | 0.464463 | 0.468855 | 0.457385 | 0.442121 | 0.468151 |
| Filtered predicted-positive fraction | 0.002429 | 0.003285 | 0.002546 | 0.002767 | 0.003192 | 0.003458 | 0.003433 |
| Filtered predicted-positive pixels | 326,064 | 440,855 | 341,691 | 371,346 | 428,416 | 464,188 | 460,724 |

ABI-295 is a mixed-to-negative result for the compact early evidence-calibration mechanism. It is resource-safe and produces a compact, high-precision, high-connectivity checkpoint. Relative to ABI-292, it repairs the main soft-band failure mode by raising precision by about +0.069 and connectivity by about +0.222 while shrinking the filtered footprint by 114,791 pixels. However, it does so by giving up about -0.049 recall and still lands slightly lower on aggregate filtered Dice.

Relative to ABI-283 and ABI-249, ABI-295 is lower on filtered Dice, recall, and both source Dice values. Its connectivity is nearly tied with ABI-283 and better than ABI-249, and its footprint is slightly smaller than ABI-283's, but this is primarily another compact underprediction state rather than a better recall/connectivity balance. Relative to ABI-279/280 and ABI-202, ABI-295 does not recover enough recall or aggregate/source Dice to justify promotion or diagnostics.

The Google source is less weak than MIT: ABI-295 beats ABI-292 on Google filtered Dice and has strong compactness there, but MIT filtered Dice falls to 0.3601. That source imbalance is an additional reason not to treat the compact high-connectivity state as a frontier result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212324 | 0.233189 | 0.175464 | 0.158791 | 0.320309 | 0.102835 | 0.007310 |
| 2 | 0.286627 | 0.281934 | 0.297178 | 0.303064 | 0.271882 | 0.192315 | 0.003251 |
| 3 | 0.317992 | 0.320863 | 0.311513 | 0.321582 | 0.314482 | 0.259513 | 0.003544 |
| 4 | 0.315983 | 0.320050 | 0.307309 | 0.259937 | 0.402842 | 0.181915 | 0.005616 |
| 5 | 0.337594 | 0.317250 | 0.386732 | 0.429309 | 0.278167 | 0.390950 | 0.002348 |
| 6 | 0.355176 | 0.335881 | 0.403674 | 0.442761 | 0.296520 | 0.399702 | 0.002427 |
| 7 | 0.312285 | 0.324231 | 0.290043 | 0.286603 | 0.343022 | 0.202837 | 0.004337 |
| 8 | 0.365799 | 0.355377 | 0.390897 | 0.433241 | 0.316526 | 0.381590 | 0.002647 |
| 9 | 0.365038 | 0.342261 | 0.421930 | 0.411457 | 0.328031 | 0.342638 | 0.002889 |
| 10 | 0.369051 | 0.352110 | 0.409548 | 0.415041 | 0.332236 | 0.347638 | 0.002901 |
| 11 | 0.341516 | 0.331291 | 0.364215 | 0.309624 | 0.380733 | 0.206438 | 0.004456 |
| 12 | 0.380175 | 0.360063 | 0.432880 | 0.473625 | 0.317525 | 0.470984 | 0.002429 |

The trajectory is finite and non-collapsed, but it oscillates between broader recall states and compact precision/connectivity states. Epoch 11 raises recall to 0.3807, but only by expanding the footprint, dropping precision to 0.3096, and lowering connectivity to 0.2064. Epoch 12 then becomes the selected compact state with high precision/connectivity and lower recall. The best epoch at the final epoch is not enough to request late36 because the scientific trade-off is not competitive with ABI-283/249, ABI-279/280, or ABI-202, and the late behavior is a swing along the known precision/recall curve rather than stable improvement.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3952 versus filtered Dice 0.3802, and the filtered predicted-positive fraction is 0.002429. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were near zero, 1.0000, near zero, and 1.0000. This does not indicate aggregate collapse because the validation metrics are finite and source-informative, but it also does not provide a qualitative reason to override the weak aggregate trade-off.

## Interpretation

Classify ABI-295 as a successful repair and resource-feasible but scientifically non-frontier family-development result. The compact early evidence-calibrated U-Net avoids ABI-293's resource infeasibility and ABI-294's smoke defect, and it produces a clean high-connectivity compact checkpoint. But it does not solve the campaign's fixed-threshold recall problem: the selected Result underpredicts relative to the current C4 and recall-bridge comparators, and the only high-recall epoch has poor precision/connectivity.

This result supports stopping the exact ABI-293/294/295 early evidence-calibration branch under the exploratory policy. It does not eliminate all calibration or dual-evidence heads, but it argues that this specific compact skip-calibration mechanism has joined the same recurring single-frame pattern: compact connected predictions suppress recall, while recall-support states broaden predictions and lose continuity. Future work should be mechanism-changing, for example a lighter dual-evidence head that explicitly protects recall without sacrificing MIT balance, or a broadened architecture family outside the recent C4/soft-band/early-calibration lineage.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-295. Do not request whole-validation failure-bucket diagnostics for this capped result. Do not request a late-improving continuation of this exact compact early evidence-calibration design; despite best epoch at epoch 12, the trade-off is not competitive and the trajectory is oscillatory rather than convincingly improving.

Treat ABI-295 as closing the ABI-293/294 repair chain: the resource-safe version was evaluated, but the mechanism did not provide the intended recall/connectivity improvement. Prefer a mechanism-changing pivot rather than another unchanged continuation of the branch.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_000805_a73a22/candidate/PROPOSAL.md`
- `run_20260914_000805_a73a22/candidate/README.md`
- `run_20260914_000805_a73a22/candidate/manifest.yaml`
- `run_20260914_000805_a73a22/resolved_manifest.yaml`
- `run_20260914_000805_a73a22/execution.json`
- `run_20260914_000805_a73a22/outputs/model_summary.json`
- `run_20260914_000805_a73a22/outputs/best_metrics.json`
- `run_20260914_000805_a73a22/outputs/final_metrics.json`
- `run_20260914_000805_a73a22/outputs/metrics.jsonl`
- `run_20260914_000805_a73a22/outputs/resource_profile.json`
- `run_20260914_000805_a73a22/outputs/validation_postprocessing/index.json`
- `run_20260914_000805_a73a22/outputs/prediction_samples/samples.json`
- `run_20260913_230004_0c9a9b` for ABI-293 resource-failure context
- `run_20260914_000407_7232d1` for ABI-294 syntax-repair context
- `run_20260913_215909_27c6e3/outputs/best_metrics.json` and `/history/research-notes/abi292-c4-softband-recall-calibrator-unet.md` for ABI-292 comparison context
- `run_20260913_063411_d8a862/outputs/best_metrics.json` and `/history/research-notes/abi283-c4-crossscale-consensus-recall-bridge-late36.md` for ABI-283 compact C4 comparison context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 comparison context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-whole-validation-failure-bucket-review.md` for ABI-279 recall-bridge comparison context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` and `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md` for ABI-280 selective-consensus comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
