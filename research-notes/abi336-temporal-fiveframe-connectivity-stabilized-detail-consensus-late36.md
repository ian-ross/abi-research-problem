# ABI-336 temporal five-frame connectivity-stabilized detail consensus late36

research-figures: []

## Scope

This note records ABI-336, Candidate `abi336_temporal_fiveframe_connectivity_stabilized_detail_consensus_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_173355_dfeb18`.

ABI-336 was a close but mechanism-changing continuation of ABI-324's provider-owned five-frame temporal C4 line-state branch. It consumed only `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change was a `ConnectivityStabilizedDetailConsensusHead` intended to add a bounded recall residual only where decoder, center-frame detail, Line, Centerline, temporal line-state, and learned directional-continuity evidence agree, plus a small learned isolation veto against line-discontinuous clutter.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-336 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324 (`run_20260916_184108_954ec7`), ABI-325 (`run_20260916_212722_d66d93`), and ABI-328 (`run_20260917_055012_ba7890`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,264,463, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,882,662,912 / 7,321,157,632 bytes.
- Training wall time: 5,706.2 s; validation wall time: 3,561.4 s; total Run wall time: 9,269.9 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-336 connectivity-stabilized | ABI-324 detail-consensus | Delta vs ABI-324 | ABI-325 positive-tail | ABI-328 soft-shift align | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 0 | 27 | 36 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.417195 | 0.429430 | -0.012236 | 0.427745 | 0.423805 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.396476 | 0.408188 | -0.011712 | 0.412855 | 0.403841 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.473730 | 0.487231 | -0.013502 | 0.466540 | 0.476913 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.415053 | 0.470412 | -0.055358 | 0.425680 | 0.444466 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.419358 | 0.395017 | +0.024341 | 0.429830 | 0.404980 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.330825 | 0.397925 | -0.067100 | 0.327452 | 0.322966 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 552,483 | 459,172 | +93,311 | 552,142 | 498,234 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-336 is finite, source-informative, and non-collapsed, but it is not a positive result for the proposed connectivity-stabilized final-head mechanism. Relative to ABI-324, the intended recall increase appears (+0.024), but it comes with a much broader filtered footprint (+93k pixels), lower precision, lower aggregate/source Dice, and a large connectivity regression. The mechanism therefore moved the operating point toward ABI-325-like positive-tail broadening rather than preserving ABI-324's compact connected balance.

Relative to ABI-325, ABI-336 has essentially the same filtered footprint and only a tiny connectivity edge, but lower aggregate Dice, lower MIT Dice, lower precision, and lower recall. Relative to ABI-328, ABI-336 gains recall and slight connectivity but gives up aggregate/source Dice, precision, and compactness. Relative to ABI-223, ABI-336 has higher recall but remains lower on aggregate/source Dice, precision, connectivity, and footprint compactness.

At the selected checkpoint, raw Dice was 0.433262 versus filtered Dice 0.417195, raw recall was 0.453309 versus filtered recall 0.419358, and raw predicted-positive pixels were 597,414 versus 552,483 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212518 | 0.219043 | 0.198513 | 0.201141 | 0.225260 | 0.135720 | 0.005789 |
| 5 | 0.310720 | 0.291275 | 0.359873 | 0.441005 | 0.239859 | 0.279380 | 0.002812 |
| 10 | 0.360484 | 0.334497 | 0.425962 | 0.462580 | 0.295306 | 0.312724 | 0.003300 |
| 15 | 0.385204 | 0.363007 | 0.441762 | 0.440883 | 0.342012 | 0.297329 | 0.004010 |
| 20 | 0.380820 | 0.353521 | 0.453266 | 0.502737 | 0.306493 | 0.399129 | 0.003152 |
| 25 | 0.381349 | 0.357378 | 0.440945 | 0.468185 | 0.321685 | 0.207646 | 0.003552 |
| 27 | 0.417195 | 0.396476 | 0.473730 | 0.415053 | 0.419358 | 0.330825 | 0.005223 |
| 28 | 0.384172 | 0.360011 | 0.446106 | 0.505847 | 0.309682 | 0.304729 | 0.003165 |
| 30 | 0.393773 | 0.370812 | 0.453718 | 0.525698 | 0.314779 | 0.368960 | 0.003095 |
| 32 | 0.383438 | 0.355853 | 0.450468 | 0.467925 | 0.324794 | 0.235518 | 0.003588 |
| 34 | 0.411622 | 0.392502 | 0.462761 | 0.437341 | 0.388761 | 0.261374 | 0.004595 |
| 36 | 0.384336 | 0.361538 | 0.445466 | 0.508290 | 0.308986 | 0.267154 | 0.003143 |

The trajectory is late-budget-dependent but oscillatory. Epoch 20 shows that the architecture can find a compact high-precision/high-connectivity state, but only with weak recall and lower Dice. The selected epoch 27 raises recall and aggregate/source Dice, but connectivity remains below ABI-324/311/223 and the footprint broadens to ABI-325 scale. The final epoch returns to high precision and compactness but loses recall, Dice, and connectivity. This repeats the branch's core failure mode: high-connectivity compact states and higher-recall states remain decoupled.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2236, 0.2941, 0.3421, and 0.3201. These confirm finite non-collapsed predictions, but retained-sample quality is weaker than ABI-324/325/328 notes and does not overturn the aggregate evidence.

## Interpretation

Classify ABI-336 as negative-to-mixed capped temporal-family development evidence for the exact connectivity-stabilized final-head branch. The final-head continuity agreement and isolation veto did not preserve ABI-324's connected compactness while raising recall. Instead, ABI-336 mostly reproduces the ABI-325-style broad recall operating point with lower Dice and without meaningful connectivity recovery.

Comparator roles after ABI-336:

- ABI-324 remains the strongest local balanced recent temporal C4 aggregate/source/connectivity comparator.
- ABI-325 remains the positive-tail recall diagnostic, not a balanced comparator.
- ABI-328 remains negative-to-mixed evidence for local soft-shift alignment alone.
- ABI-336 is negative-to-mixed evidence that a final-head connectivity residual/veto does not solve the temporal C4 recall/connectivity coupling problem.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the broad recall-heavy temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-336 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249, and it does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-336 and do not submit another close continuation of this exact final-head connectivity-stabilized temporal C4 branch. The ABI-324/325/328/336 sequence now gives enough bounded evidence that head-local residuals, vetoes, reinjection, and soft-shift C4 alignment variants have not reliably unified connected-line continuity with fixed-threshold recall and source balance.

No immediate Evaluation Request is justified from ABI-336 because capped aggregate/source/connectivity metrics are below ABI-324 and do not reveal a favorable hidden trade-off. If the campaign continues from this area, broaden to a materially different temporal attention/alignment/change mechanism, a modern lightweight temporal backbone, a trusted policy direction, or a failure-bucket-driven diagnostic focused on ABI-324 rather than another ABI-336-style head continuation.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_173355_dfeb18/candidate/PROPOSAL.md`
- `run_20260917_173355_dfeb18/candidate/README.md`
- `run_20260917_173355_dfeb18/candidate/manifest.yaml`
- `run_20260917_173355_dfeb18/candidate/budget_request.yaml`
- `run_20260917_173355_dfeb18/resolved_manifest.yaml`
- `run_20260917_173355_dfeb18/execution.json`
- `run_20260917_173355_dfeb18/outputs/model_summary.json`
- `run_20260917_173355_dfeb18/outputs/best_metrics.json`
- `run_20260917_173355_dfeb18/outputs/final_metrics.json`
- `run_20260917_173355_dfeb18/outputs/metrics.jsonl`
- `run_20260917_173355_dfeb18/outputs/resource_profile.json`
- `run_20260917_173355_dfeb18/outputs/validation_postprocessing/index.json`
- `run_20260917_173355_dfeb18/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
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
