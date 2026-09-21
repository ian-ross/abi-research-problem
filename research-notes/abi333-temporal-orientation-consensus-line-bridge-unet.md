# ABI-333 temporal orientation-consensus line bridge U-Net

research-figures: []

## Scope

This note records ABI-333, Candidate `abi333_temporal_orientation_consensus_line_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260917_142841_02a028`.

ABI-333 was a mechanism-changing exploratory continuation of the compact three-frame ABI-331/332 temporal persistence/detail line-gate branch. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The mechanism added a differentiable orientation-consensus line bridge intended to raise connected thin-line evidence without candidate-owned thresholding or postprocessing.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-333 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped temporal-eligible sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 2,691,249, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,384,455,680 / 4,781,506,560 bytes.
- Training wall time: 1,624.1 s; validation wall time: 1,313.7 s; total Run wall time: 2,939.6 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-333 orientation consensus | ABI-331 exploratory parent | ABI-332 late parent | ABI-319 shift-bank C4 | ABI-324 five-frame detail consensus | ABI-328 soft-shift align | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 12 | 36 | 10 | 27 | 36 | 36 |
| Filtered Dice | 0.389367 | 0.391024 | 0.413321 | 0.405847 | 0.429430 | 0.423805 | 0.419776 |
| MIT filtered Dice | 0.374039 | 0.373811 | 0.394660 | 0.387897 | 0.408188 | 0.403841 | 0.398498 |
| Google filtered Dice | 0.428703 | 0.436055 | 0.460548 | 0.451369 | 0.487231 | 0.476913 | 0.476764 |
| Filtered precision | 0.446187 | 0.481788 | 0.466793 | 0.463906 | 0.470412 | 0.444466 | 0.483764 |
| Filtered recall | 0.345384 | 0.329036 | 0.370840 | 0.360703 | 0.395017 | 0.404980 | 0.370738 |
| Filtered connectivity | 0.345629 | 0.361417 | 0.365588 | 0.360704 | 0.397925 | 0.322966 | 0.412427 |
| Filtered predicted-positive pixels | 423,275 | 373,444 | 434,411 | 425,166 | 459,172 | 498,234 | 419,056 |

ABI-333 is finite and non-collapsed, but it is not positive evidence for the specific orientation-consensus line bridge. Relative to ABI-331, it raises recall by about +0.016 and nearly ties MIT Dice, but it lowers aggregate filtered Dice by about -0.0017, Google Dice by about -0.0074, precision by about -0.0356, and connectivity by about -0.0158 while expanding the filtered footprint by about 49.8k pixels. This is the opposite of the intended signature: the bridge did not improve connected-line support while preserving compactness.

Relative to ABI-332, the orientation-consensus scout is clearly behind on aggregate/source Dice, precision, recall, and connectivity. It is only slightly more compact than ABI-332, and the compactness does not offset the lower true-positive evidence. Relative to stronger temporal comparators, ABI-333 remains below ABI-319/324/223 on connected-line continuity and below ABI-324/328 on aggregate/source Dice and recall.

At the selected checkpoint, raw Dice was 0.406524 versus filtered Dice 0.389367, raw recall was 0.372927 versus filtered recall 0.345384, and raw predicted-positive pixels were 456,430 versus 423,275 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.221054 | 0.225301 | 0.212178 | 0.218432 | 0.223739 | 0.153923 | 0.005295 |
| 2 | 0.219631 | 0.203108 | 0.264959 | 0.491747 | 0.141390 | 0.401062 | 0.001486 |
| 3 | 0.315935 | 0.298560 | 0.357561 | 0.393733 | 0.263809 | 0.283399 | 0.003464 |
| 4 | 0.323578 | 0.303227 | 0.376227 | 0.472528 | 0.246026 | 0.363509 | 0.002692 |
| 5 | 0.347537 | 0.338362 | 0.368246 | 0.360860 | 0.335163 | 0.251755 | 0.004801 |
| 6 | 0.334708 | 0.314818 | 0.384854 | 0.452991 | 0.265406 | 0.369720 | 0.003029 |
| 7 | 0.362714 | 0.342195 | 0.418224 | 0.506029 | 0.282660 | 0.450851 | 0.002888 |
| 8 | 0.383907 | 0.368831 | 0.424346 | 0.462487 | 0.328151 | 0.372091 | 0.003668 |
| 9 | 0.374894 | 0.363838 | 0.401827 | 0.370229 | 0.379679 | 0.297556 | 0.005302 |
| 10 | 0.362254 | 0.339668 | 0.421459 | 0.512834 | 0.280030 | 0.429198 | 0.002823 |
| 11 | 0.359682 | 0.343040 | 0.401555 | 0.447201 | 0.300813 | 0.300140 | 0.003477 |
| 12 | 0.389367 | 0.374039 | 0.428703 | 0.446187 | 0.345384 | 0.345629 | 0.004002 |

The trajectory is finite, source-informative, and selected the final exploratory epoch. However, the connectivity behavior is unstable and decoupled from aggregate Dice. Epochs 7 and 10 briefly reach higher connectivity under compact, high-precision, low-recall states, while the final selected checkpoint improves aggregate/source Dice by accepting more recall and a broader footprint with weaker connectivity. This pattern suggests that the orientation-consensus bridge can find oriented support, but it is not converting that support into the balanced connected true-positive evidence targeted by the proposal.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4225, 0.3780, 0.5887, and 0.3592. This confirms finite non-collapsed predictions on retained examples, but it does not overturn the aggregate evidence that the orientation-consensus bridge did not improve the compact three-frame branch.

## Interpretation

Classify ABI-333 as negative-to-mixed capped temporal-family development evidence for the exact orientation-consensus line bridge. The run is resource-safe and scientifically useful as a mechanism test, but its effect is mainly a recall/footprint shift from ABI-331 rather than the desired connectivity gain. It neither improves on ABI-331's aggregate Dice nor approaches ABI-332's late-budget balance, and it remains below the stronger temporal C4 and temporal-attention comparators.

The result does not eliminate the broader compact three-frame persistence/detail family, but it argues against an unchanged late36 continuation of this exact orientation-consensus head. ABI-332 already showed that the parent branch benefits from longer training; ABI-333 shows that adding this particular orientation bridge at exploratory budget does not solve the branch's key failure mode. Future work should be mechanism-changing if it reuses the compact branch: for example, a different temporal attention/alignment path, calibrated evidence sharpening, or a connectivity-preserving bridge that explicitly avoids the high-connectivity/low-recall oscillation observed here.

Comparator roles after ABI-333:

- ABI-324 remains the strongest local balanced temporal C4 aggregate/source/connectivity comparator.
- ABI-332 remains the best compact three-frame persistence/detail line-gate comparator.
- ABI-331 remains useful as the exploratory compact three-frame parent; ABI-333 does not supersede it except as negative evidence for this orientation-consensus modification.
- ABI-319 remains a stronger three-frame shift-bank/C4 comparator than ABI-333.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-333 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-333 and do not request whole-validation-style evaluation from this capped temporal-eligible Result. A temporal-eligible failure-bucket Evaluation Request is not immediately necessary because the capped aggregate/source/precision/recall/connectivity metrics already show the central failure mode: a modest recall gain over ABI-331 at the cost of precision, compactness, Google Dice, and connected-line continuity.

Do not spend another Run on an unchanged late36 continuation of ABI-333. If this area is revisited, make the next hypothesis mechanism-changing and explicitly targeted at preserving the high-connectivity compact states while recovering recall, or broaden away from the compact orientation-consensus branch toward a materially different temporal attention/alignment, calibration, trusted loss, or data-policy direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_142841_02a028/candidate/PROPOSAL.md`
- `run_20260917_142841_02a028/candidate/README.md`
- `run_20260917_142841_02a028/candidate/manifest.yaml`
- `run_20260917_142841_02a028/resolved_manifest.yaml`
- `run_20260917_142841_02a028/execution.json`
- `run_20260917_142841_02a028/outputs/model_summary.json`
- `run_20260917_142841_02a028/outputs/best_metrics.json`
- `run_20260917_142841_02a028/outputs/final_metrics.json`
- `run_20260917_142841_02a028/outputs/metrics.jsonl`
- `run_20260917_142841_02a028/outputs/resource_profile.json`
- `run_20260917_142841_02a028/outputs/validation_postprocessing/index.json`
- `run_20260917_142841_02a028/outputs/prediction_samples/samples.json`
- `run_20260917_105650_6a68cc/outputs/best_metrics.json` and `/history/research-notes/abi331-temporal-persistence-detail-line-gate-unet.md` for ABI-331 comparison context
- `run_20260917_115326_f1e460/outputs/best_metrics.json` and `/history/research-notes/abi332-temporal-persistence-detail-line-gate-late36.md` for ABI-332 comparison context
- `run_20260915_162050_163586/outputs/best_metrics.json` and `/history/research-notes/abi319-temporal-shiftbank-c4-alignment-confidence-line-unet.md` for ABI-319 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
