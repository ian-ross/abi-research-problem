# ABI-320 temporal shift-bank C4 center-detail recall-gate U-Net

research-figures: []

## Scope

This note records ABI-320, Candidate `abi320_temporal_shiftbank_c4_center_detail_recall_gate_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260915_172705_4d6463`.

ABI-320 was a bounded exploratory family-development continuation after ABI-319. It kept provider-owned three-frame temporal input with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, ABI-319-style local shift-bank alignment, and alignment-confidence-gated C4 line-state. It changed the evidence head to add a bounded center-detail recall gate intended to lift uncertain true-contrail logits only when center-frame detail, aligned temporal support, and C4 line-state evidence agreed, while suppressing disagreement/clutter.

The candidate did not implement Candidate-owned data loading, temporal lookup, target construction, losses, metrics, thresholds, postprocessing, Artifact Filters, longitude/latitude features, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior. This is capped temporal-eligible feasibility evidence only, not full Working Validation Split promotion evidence.

## Execution result

ABI-320 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,897,867, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 8,798,162,944 / 9,489,612,800 bytes.
- Training wall time: 2,095.3 s; validation wall time: 1,277.6 s; total Run wall time: 3,374.9 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-320 center-detail recall gate | ABI-319 shift-bank C4 confidence | ABI-315 shift-bank scout | ABI-311 five-frame C4 | ABI-309 recall-heavy C4 | ABI-306 compact C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 10 | 12 | 27 | 29 | 36 |
| Filtered Dice | 0.382100 | 0.405847 | 0.389886 | 0.425000 | 0.423544 | 0.422548 |
| MIT filtered Dice | 0.366449 | 0.387897 | 0.377376 | 0.403831 | 0.402446 | 0.402764 |
| Google filtered Dice | 0.420464 | 0.451369 | 0.420154 | 0.482615 | 0.478510 | 0.476152 |
| Filtered precision | 0.415251 | 0.463906 | 0.412308 | 0.459703 | 0.401806 | 0.493422 |
| Filtered recall | 0.353851 | 0.360703 | 0.369776 | 0.395169 | 0.447768 | 0.369478 |
| Filtered connectivity | 0.365299 | 0.360704 | 0.266017 | 0.366735 | 0.316074 | 0.299384 |
| Filtered predicted-positive fraction | 0.004405 | 0.004020 | 0.004636 | 0.004444 | 0.005761 | 0.003871 |

ABI-320 did not achieve the intended recall-protected improvement over ABI-319. Relative to ABI-319, ABI-320 loses about -0.0237 filtered Dice, -0.0214 MIT Dice, -0.0309 Google Dice, -0.0487 precision, and -0.0069 recall. Connectivity is essentially tied/slightly higher (+0.0046), but this small continuity gain does not compensate for weaker source-stratified Dice and precision.

Relative to ABI-315, ABI-320 preserves the shift-bank branch's later connectivity repair (+0.0993 connectivity) and similar Google Dice, but it is lower on aggregate Dice, MIT Dice, and recall. This indicates that the added center-detail recall gate did not recover true-positive evidence; it mainly retained connected-line behavior while still under-recalling.

Against the stronger temporal C4 comparators, ABI-320 remains materially below the frontier. ABI-311 is higher by about +0.0429 filtered Dice with better source balance and recall at nearly the same footprint. ABI-309 remains the recall-heavy comparator, with much higher recall despite broader predictions. ABI-306 remains the compact high-precision comparator; ABI-320's connectivity is higher, but Dice, precision, recall, MIT Dice, and Google Dice are all lower.

At the selected checkpoint, raw Dice was 0.398155 versus filtered Dice 0.382100, raw recall was 0.382014 versus filtered recall 0.353851, and raw predicted-positive fraction was 0.004750 versus filtered predicted-positive fraction 0.004405. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.219183 | 0.230837 | 0.198063 | 0.185840 | 0.267106 | 0.137096 | 0.007430 |
| 2 | 0.292172 | 0.282220 | 0.317919 | 0.427107 | 0.222027 | 0.340281 | 0.002687 |
| 3 | 0.314987 | 0.315995 | 0.312919 | 0.290412 | 0.344105 | 0.163023 | 0.006125 |
| 4 | 0.307807 | 0.287731 | 0.359626 | 0.497088 | 0.222923 | 0.399187 | 0.002318 |
| 5 | 0.344772 | 0.333732 | 0.371146 | 0.439590 | 0.283600 | 0.285238 | 0.003335 |
| 6 | 0.373898 | 0.366955 | 0.390690 | 0.390522 | 0.358631 | 0.272429 | 0.004747 |
| 7 | 0.336477 | 0.313253 | 0.397739 | 0.534524 | 0.245512 | 0.439372 | 0.002374 |
| 8 | 0.380741 | 0.361526 | 0.431325 | 0.488652 | 0.311870 | 0.382657 | 0.003299 |
| 9 | 0.382100 | 0.366449 | 0.420464 | 0.415251 | 0.353851 | 0.365299 | 0.004405 |
| 10 | 0.360201 | 0.340594 | 0.410700 | 0.519953 | 0.275543 | 0.389520 | 0.002740 |
| 11 | 0.367912 | 0.345345 | 0.423932 | 0.436729 | 0.317830 | 0.324129 | 0.003762 |
| 12 | 0.379810 | 0.360807 | 0.426884 | 0.452114 | 0.327443 | 0.301654 | 0.003744 |

The trajectory is finite and source-informative, but it does not support a late-improving continuation. The best checkpoint occurs at epoch 9, not at the final epoch. Epochs 10-12 partially recover aggregate Dice after the epoch-10 drop, but final filtered Dice remains below the selected checkpoint and below ABI-319. The run alternates among high-precision/low-recall states, recall-balanced but lower-precision states, and connected but sub-frontier states. This is an oscillating calibration surface rather than clear evidence of truncation.

The source behavior is also unfavorable. At the selected checkpoint, the MIT/Google filtered-Dice gap is about 0.0540, wider than ABI-319's gap and lower on both sources. The center-detail recall gate therefore did not repair the shift-bank branch's source-balanced fixed-threshold recall weakness.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3333, 0.4217, 0.5916, and 0.4875. This confirms finite non-collapsed predictions with mixed retained-sample behavior, but it is not promotion evidence.

## Interpretation

Classify ABI-320 as a valid, resource-feasible, scientifically useful but negative temporal shift-bank/C4 continuation. The mechanism was well bounded and contract-compliant, but the intended center-detail recall gate did not raise enough true contrail evidence at the fixed 0.5 threshold. It preserved some connected-line behavior, yet it reduced precision and did not improve recall relative to ABI-319.

The main lesson is that adding another gated head to the local shift-bank/C4 stack is not enough to recover the temporal branch's missing recall. The stronger ABI-311/309/306 comparators suggest that the next useful temporal proposal should materially change the evidence path rather than further refine this same shift-bank head: for example a different temporal attention/evidence-sharpening mechanism, a line-continuity module that does not depend on local shift agreement alone, or a trusted calibration/loss/data-policy change if made available through the contract.

## Decision

Do not promote ABI-320. Do not request temporal-eligible failure-bucket diagnostics for this capped exploratory Result. Do not request an unchanged late36 continuation: the best epoch was not final, final metrics remained below ABI-319, wall time was already close to the exploratory timeout, and the trajectory shows oscillating precision/recall/connectivity rather than under-training.

Record ABI-320 as bounded negative evidence for this exact center-detail recall-gated shift-bank/C4 branch. Future work should avoid another direct shift-bank/C4 head refinement and should be mechanism-changing if it continues the temporal recall/connectivity theme.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_172705_4d6463/candidate/PROPOSAL.md`
- `run_20260915_172705_4d6463/candidate/README.md`
- `run_20260915_172705_4d6463/candidate/manifest.yaml`
- `run_20260915_172705_4d6463/resolved_manifest.yaml`
- `run_20260915_172705_4d6463/execution.json`
- `run_20260915_172705_4d6463/outputs/model_summary.json`
- `run_20260915_172705_4d6463/outputs/best_metrics.json`
- `run_20260915_172705_4d6463/outputs/final_metrics.json`
- `run_20260915_172705_4d6463/outputs/metrics.jsonl`
- `run_20260915_172705_4d6463/outputs/resource_profile.json`
- `run_20260915_172705_4d6463/outputs/validation_postprocessing/index.json`
- `run_20260915_172705_4d6463/outputs/prediction_samples/samples.json`
- `run_20260915_162050_163586/outputs/best_metrics.json` and `/history/research-notes/abi319-temporal-shiftbank-c4-alignment-confidence-line-unet.md` for ABI-319 comparison context
- `run_20260915_100642_28e66d/outputs/best_metrics.json` and `/history/research-notes/abi315-temporal-shiftbank-alignment-detail-unet-syntax-repair.md` for ABI-315 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
