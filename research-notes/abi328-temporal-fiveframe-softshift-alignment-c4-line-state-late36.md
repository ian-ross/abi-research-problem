# ABI-328 temporal five-frame soft-shift alignment C4 line-state late36

research-figures: []

## Scope

This note records ABI-328, Candidate `abi328_temporal_fiveframe_softshift_alignment_c4_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_055012_ba7890`.

ABI-328 was a mechanism-changing continuation of the ABI-324/325/326/327 five-frame temporal C4 line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change replaced ABI-327's early change-salience gate with architecture-internal soft local alignment of non-center frames over a small shift bank before C4 line-state fusion.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-328 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324 (`run_20260916_184108_954ec7`), ABI-327 (`run_20260917_031010_2dd7e6`), and ABI-326 (`run_20260917_002229_d43b7a`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,267,125, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 7,952,223,744 / 8,304,721,920 bytes.
- Training wall time: 5,882.9 s; validation wall time: 3,577.1 s; total Run wall time: 9,462.2 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-328 soft-shift align | ABI-324 detail-consensus | Delta vs ABI-324 | ABI-327 change-salience | ABI-326 selective guard | ABI-325 positive-tail | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 27 | +9 | 22 | 36 | 27 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.423805 | 0.429430 | -0.005625 | 0.408640 | 0.424161 | 0.427745 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.403841 | 0.408188 | -0.004347 | 0.386226 | 0.406687 | 0.412855 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.476913 | 0.487231 | -0.010318 | 0.468667 | 0.471630 | 0.466540 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.444466 | 0.470412 | -0.025946 | 0.502123 | 0.447015 | 0.425680 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.404980 | 0.395017 | +0.009963 | 0.344502 | 0.403530 | 0.429830 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.322966 | 0.397925 | -0.074959 | 0.325101 | 0.268164 | 0.327452 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 498,234 | 459,172 | +39,062 | 375,163 | 493,619 | 552,142 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-328 is finite, non-collapsed, and source-informative, but it is not a positive result for the proposed soft-shift temporal alignment mechanism. It recovers recall relative to ABI-324 by about +0.010 and improves substantially over ABI-327's under-recall salience gate, but the gain is not clean: aggregate Dice remains -0.005625 below ABI-324, Google Dice is -0.010318 below ABI-324, precision drops by -0.025946, the filtered footprint grows by 39,062 pixels, and connectivity falls sharply by -0.074959.

Relative to ABI-326, ABI-328 is nearly tied on aggregate Dice (-0.000356), has slightly higher Google Dice and connectivity, and is slightly broader, but it does not restore ABI-324/311/223-level connected-line continuity. Relative to ABI-325, ABI-328 is more precise and less broad, but gives back much of ABI-325's recall and MIT-positive-tail benefit. Relative to ABI-306 and ABI-223, ABI-328 trades away precision/connectivity for only modest recall. The soft-shift aligner therefore moves the branch toward a middle operating point rather than solving the recall/connectivity/source-balance trade-off.

At the selected checkpoint, raw Dice was 0.440713 versus filtered Dice 0.423805, raw recall was 0.437150 versus filtered recall 0.404980, and raw predicted-positive pixels were 537,970 versus 498,234 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.210321 | 0.216909 | 0.197316 | 0.178301 | 0.256359 | 0.131572 | 0.007433 |
| 5 | 0.317117 | 0.285092 | 0.399058 | 0.508581 | 0.230384 | 0.379580 | 0.002342 |
| 10 | 0.380258 | 0.355531 | 0.440730 | 0.452083 | 0.328127 | 0.288506 | 0.003752 |
| 15 | 0.383363 | 0.356962 | 0.451031 | 0.496267 | 0.312310 | 0.364737 | 0.003253 |
| 20 | 0.358107 | 0.324699 | 0.447165 | 0.572867 | 0.260462 | 0.424383 | 0.002350 |
| 24 | 0.388395 | 0.356113 | 0.470100 | 0.501226 | 0.317029 | 0.338789 | 0.003270 |
| 27 | 0.410985 | 0.385975 | 0.472592 | 0.431429 | 0.392391 | 0.317124 | 0.004702 |
| 29 | 0.408533 | 0.383883 | 0.471876 | 0.451401 | 0.373101 | 0.338149 | 0.004273 |
| 32 | 0.414819 | 0.387069 | 0.485840 | 0.442915 | 0.390074 | 0.334371 | 0.004553 |
| 34 | 0.401746 | 0.371851 | 0.477059 | 0.467689 | 0.352101 | 0.321070 | 0.003892 |
| 36 | 0.423805 | 0.403841 | 0.476913 | 0.444466 | 0.404980 | 0.322966 | 0.004710 |

The trajectory is finite and late-budget-active. The best checkpoint is the final epoch, so the late-improving budget was useful for observing the intended comparison. However, the late improvement primarily raises recall and footprint after a high-precision/low-recall mid-run phase; it does not recover connectivity. Epoch 20 briefly had high connectivity (0.424383) and high precision, but with weak recall and Dice. Later epochs improved aggregate Dice only by accepting a broader, less connected operating point.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3229, 0.5313, 0.5998, and 0.3604. This confirms finite non-collapsed predictions on retained examples, but does not overturn the aggregate evidence that soft alignment did not produce the desired connected temporal-support repair.

## Interpretation

Classify ABI-328 as negative-to-mixed capped temporal-family development evidence for the exact soft-shift temporal-alignment C4 line-state mechanism. The mechanism avoids ABI-327's extreme under-recall and is more controlled than ABI-325's broad positive-tail reinjection, but it does not beat ABI-324's aggregate/source/connectivity balance. Its strongest contribution is showing that local alignment can recover some recall and MIT balance without ABI-325-scale broadening, but the recovered evidence remains poorly connected and slightly less precise than ABI-324.

Comparator roles after ABI-328:

- ABI-324 remains the strongest local balanced temporal C4 aggregate/connectivity comparator.
- ABI-325 remains a positive-tail recall diagnostic, not a balanced comparator.
- ABI-326 remains evidence that a selective tail-consensus guard does not recover connectivity or aggregate Dice.
- ABI-327 remains negative evidence for an early change-salience gate.
- ABI-328 adds negative-to-mixed evidence that small soft-shift alignment alone is insufficient to solve the same temporal C4 trade-off.
- ABI-311 remains the five-frame persistence/contrast line-state parent.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the broad recall-heavy temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-328 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249, and it does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-328 and do not spend another Run on a close continuation of this exact soft-shift C4 alignment branch. The ABI-324/325/326/327/328 sequence now gives enough bounded evidence that local temporal C4 reinjection/guard/salience/soft-shift variants are not reliably improving the main failure mode: connected true-positive evidence at threshold 0.5 while preserving compactness and source balance.

No immediate Evaluation Request is justified from ABI-328 because the capped aggregate/source/connectivity metrics are near ABI-326 and below ABI-324, without a clear hidden favorable trade-off. The next Candidate, if one is submitted later, should broaden away from this exact temporal C4 repair line toward a materially different temporal attention/alignment mechanism, modern lightweight temporal backbone, or trusted policy direction that explicitly targets connected-line continuity and MIT/source balance.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_055012_ba7890/candidate/PROPOSAL.md`
- `run_20260917_055012_ba7890/candidate/README.md`
- `run_20260917_055012_ba7890/candidate/manifest.yaml`
- `run_20260917_055012_ba7890/candidate/budget_request.yaml`
- `run_20260917_055012_ba7890/resolved_manifest.yaml`
- `run_20260917_055012_ba7890/execution.json`
- `run_20260917_055012_ba7890/outputs/model_summary.json`
- `run_20260917_055012_ba7890/outputs/best_metrics.json`
- `run_20260917_055012_ba7890/outputs/final_metrics.json`
- `run_20260917_055012_ba7890/outputs/metrics.jsonl`
- `run_20260917_055012_ba7890/outputs/resource_profile.json`
- `run_20260917_055012_ba7890/outputs/validation_postprocessing/index.json`
- `run_20260917_055012_ba7890/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260917_031010_2dd7e6/outputs/best_metrics.json` and `/history/research-notes/abi327-temporal-fiveframe-change-salience-c4-line-state-late36.md` for ABI-327 comparison context
- `run_20260917_002229_d43b7a/outputs/best_metrics.json` and `/history/research-notes/abi326-temporal-fiveframe-selective-tail-consensus-guard-late36.md` for ABI-326 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
