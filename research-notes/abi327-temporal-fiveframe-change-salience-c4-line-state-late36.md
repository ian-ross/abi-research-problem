# ABI-327 temporal five-frame change-salience C4 line-state late36

research-figures: []

## Scope

This note records ABI-327, Candidate `abi327_temporal_fiveframe_change_salience_c4_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_031010_2dd7e6`.

ABI-327 was a close, mechanism-changing continuation of the ABI-324/325/326 five-frame temporal C4 line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change moved temporal repair earlier than ABI-325/326: center-vs-neighbor motion, before/after slope, and center-vs-attended-gap features were projected into a bounded change-salience state that gates the early C4 line state before the encoder pyramid.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-327 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324 (`run_20260916_184108_954ec7`), ABI-311 (`run_20260915_015552_1ac51f`), and ABI-326 (`run_20260917_002229_d43b7a`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,270,676, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 7,025,498,112 / 7,377,780,736 bytes.
- Training wall time: 5,489.5 s; validation wall time: 3,460.5 s; total Run wall time: 8,952.1 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 22.

## Best-validation metrics

| Metric | ABI-327 change-salience | ABI-324 detail-consensus | Delta vs ABI-324 | ABI-326 selective guard | ABI-325 positive-tail | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 22 | 27 | -5 | 36 | 27 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.408640 | 0.429430 | -0.020790 | 0.424161 | 0.427745 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.386226 | 0.408188 | -0.021961 | 0.406687 | 0.412855 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.468667 | 0.487231 | -0.018564 | 0.471630 | 0.466540 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.502123 | 0.470412 | +0.031711 | 0.447015 | 0.425680 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.344502 | 0.395017 | -0.050515 | 0.403530 | 0.429830 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.325101 | 0.397925 | -0.072824 | 0.268164 | 0.327452 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 375,163 | 459,172 | -84,009 | 493,619 | 552,142 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-327 is finite, non-collapsed, and source-informative, but it is a negative result for the proposed early change-salience gate. It becomes the most compact/high-precision point in this local comparison, but that compactness is bought by under-recall and lower source Dice. The best checkpoint trails ABI-324 by -0.020790 aggregate filtered Dice, -0.021961 MIT Dice, -0.018564 Google Dice, -0.050515 recall, and -0.072824 connectivity. Its predicted-positive footprint is smaller than ABI-324 by 84,009 filtered pixels, but that looks like missed true positives rather than a useful clutter repair.

Compared with ABI-326, ABI-327 improves precision (+0.055108) and connectivity (+0.056937) and sharply reduces footprint (-118,456 filtered pixels), but it loses aggregate Dice (-0.015521), MIT Dice (-0.020460), and recall (-0.059028). Compared with ABI-325, it avoids broad positive-tail reinjection but loses the intended MIT/recall benefit. Compared with ABI-306 and ABI-223, the precision is competitive, but aggregate/source Dice and recall are too weak. ABI-327 therefore does not support further close continuation of the early temporal-change-salience C4 gate.

At the selected checkpoint, raw Dice was 0.427617 versus filtered Dice 0.408640, raw recall was 0.372335 versus filtered recall 0.344502, and raw predicted-positive pixels were 405,429 versus 375,163 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.233694 | 0.227064 | 0.249926 | 0.301540 | 0.190832 | 0.185395 | 0.003265 |
| 5 | 0.317024 | 0.296461 | 0.369449 | 0.426887 | 0.252159 | 0.221049 | 0.003055 |
| 10 | 0.349588 | 0.326861 | 0.404541 | 0.445112 | 0.287852 | 0.226906 | 0.003342 |
| 15 | 0.369324 | 0.350827 | 0.418860 | 0.503259 | 0.291642 | 0.308522 | 0.003001 |
| 20 | 0.355048 | 0.333538 | 0.410336 | 0.529470 | 0.267048 | 0.295511 | 0.002610 |
| 22 | 0.408640 | 0.386226 | 0.468667 | 0.502123 | 0.344502 | 0.325101 | 0.003547 |
| 27 | 0.396118 | 0.372579 | 0.456316 | 0.458596 | 0.348617 | 0.283545 | 0.003930 |
| 29 | 0.391839 | 0.369452 | 0.445532 | 0.397825 | 0.385930 | 0.220304 | 0.005012 |
| 32 | 0.403760 | 0.379399 | 0.466908 | 0.497108 | 0.340000 | 0.294039 | 0.003538 |
| 34 | 0.406835 | 0.385724 | 0.460561 | 0.464490 | 0.361877 | 0.259219 | 0.004031 |
| 36 | 0.406640 | 0.384692 | 0.463164 | 0.442630 | 0.376062 | 0.230296 | 0.004392 |

The trajectory is finite and late-budget-active but oscillatory. The best epoch appears after a high-precision, low-recall phase and is followed by broader recall attempts with lower connectivity. Final epoch 36 nearly recovers best Dice, but with lower precision and much weaker connectivity. This reinforces that the early salience gate can change the precision/recall operating point, but it does not stably combine recall, MIT balance, and connected-line continuity.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3567, approximately 0.0000, 0.5750, and 0.3253. This confirms finite non-collapsed predictions with at least one missed retained sample, consistent with the aggregate under-recall interpretation.

## Interpretation

Classify ABI-327 as negative capped temporal-family development evidence for the exact early change-salience C4 line-state gate. Moving the temporal repair earlier did not solve the ABI-324/325/326 trade-off. It produced a compact, high-precision checkpoint, but the result under-recovers true positives, trails ABI-324 and ABI-311 on aggregate/source/connectivity balance, and does not restore ABI-223-like connected-line behavior.

Comparator roles after ABI-327:

- ABI-324 remains the strongest local balanced temporal C4 aggregate/connectivity comparator.
- ABI-325 remains a recall/MIT-tail diagnostic variant, not a balanced comparator.
- ABI-326 remains evidence that a simple selective consensus guard is not enough to rescue positive-tail reinjection.
- ABI-327 adds evidence that early change-salience gating is also not enough to rescue this temporal C4 line-state branch.
- ABI-311 remains the five-frame persistence/contrast line-state parent.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the broad recall-heavy temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-327 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249, and it does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, or resource scheduling.

## Decision

Do not promote ABI-327 and do not spend another Run on a close continuation of this early change-salience C4 gate. The ABI-324/325/326/327 sequence now gives enough bounded evidence that this exact temporal C4 tail/salience repair line is not the right mechanism for simultaneously improving MIT/positive-tail recall, compactness, and connected-line continuity.

No immediate Evaluation Request is justified from ABI-327 because the capped aggregate/source/connectivity metrics do not suggest a hidden favorable failure-bucket trade-off relative to ABI-324. The next Candidate, if one is submitted later, should broaden away from this exact temporal C4 salience/reinjection/guard branch toward a materially different temporal alignment/change mechanism, modern lightweight backbone, trusted data/loss/augmentation policy, or line-continuity approach.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_031010_2dd7e6/candidate/PROPOSAL.md`
- `run_20260917_031010_2dd7e6/candidate/README.md`
- `run_20260917_031010_2dd7e6/candidate/manifest.yaml`
- `run_20260917_031010_2dd7e6/candidate/budget_request.yaml`
- `run_20260917_031010_2dd7e6/resolved_manifest.yaml`
- `run_20260917_031010_2dd7e6/execution.json`
- `run_20260917_031010_2dd7e6/outputs/model_summary.json`
- `run_20260917_031010_2dd7e6/outputs/best_metrics.json`
- `run_20260917_031010_2dd7e6/outputs/final_metrics.json`
- `run_20260917_031010_2dd7e6/outputs/metrics.jsonl`
- `run_20260917_031010_2dd7e6/outputs/resource_profile.json`
- `run_20260917_031010_2dd7e6/outputs/validation_postprocessing/index.json`
- `run_20260917_031010_2dd7e6/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
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
