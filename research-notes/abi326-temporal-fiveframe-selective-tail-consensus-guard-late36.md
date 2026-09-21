# ABI-326 temporal five-frame selective tail consensus guard late36

research-figures: []

## Scope

This note records ABI-326, Candidate `abi326_temporal_fiveframe_selective_tail_consensus_guard_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_002229_d43b7a`.

ABI-326 was a close, mechanism-changing continuation of the ABI-324/325 five-frame temporal C4 line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change was a `SelectiveTailConsensusGuard` intended to retain ABI-325's useful positive-tail support only when decoder, center-detail, memory, and early line-state evidence agree.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-326 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-325 (`run_20260916_212722_d66d93`), ABI-324 (`run_20260916_184108_954ec7`), and ABI-311 (`run_20260915_015552_1ac51f`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,265,638, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 7,032,633,856 / 7,436,500,992 bytes.
- Training wall time: 5,752.0 s; validation wall time: 3,567.4 s; total Run wall time: 9,321.7 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-326 selective guard | ABI-324 detail-consensus | Delta vs ABI-324 | ABI-325 positive-tail | ABI-311 five-frame C4 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 27 | +9 | 27 | 27 | 36 | 29 | 36 |
| Filtered Dice | 0.424161 | 0.429430 | -0.005270 | 0.427745 | 0.425000 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.406687 | 0.408188 | -0.001501 | 0.412855 | 0.403831 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.471630 | 0.487231 | -0.015601 | 0.466540 | 0.482615 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.447015 | 0.470412 | -0.023397 | 0.425680 | 0.459703 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.403530 | 0.395017 | +0.008513 | 0.429830 | 0.395169 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.268164 | 0.397925 | -0.129761 | 0.327452 | 0.366735 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive pixels | 493,619 | 459,172 | +34,447 | 552,142 | 470,049 | 409,457 | 609,361 | 419,056 |

ABI-326 is finite, non-collapsed, and source-informative, but it does not meet the planned success criterion of retaining ABI-325's useful MIT/positive-tail recall while recovering ABI-324-like compactness, source balance, and connectivity.

The selective guard did make ABI-325 less broad: filtered predicted-positive pixels dropped by 58,523, precision improved by +0.021335, and Google Dice improved by +0.005090. However, the restriction removed much of ABI-325's intended recall/MIT benefit: aggregate filtered Dice fell by -0.003584, MIT Dice by -0.006168, recall by -0.026300, and connectivity by -0.059288 versus ABI-325.

Against ABI-324, ABI-326 is worse on aggregate Dice, both source Dice metrics, precision, predicted-positive compactness, and especially connectivity. The only favorable movement is a small recall increase (+0.008513), too small to offset the connectivity and Google/source-balance regression. Against ABI-311, ABI-326 is nearly tied on aggregate Dice but trades lower Google Dice and lower connectivity for modestly higher MIT Dice and recall. Against ABI-306, it gives a recall-heavy but lower-precision operating point. Against ABI-309, it is less broad and higher-precision but still weaker in recall/connectivity. Against ABI-223, it improves aggregate/MIT Dice and recall but trails badly on precision and connected-line continuity.

At the selected checkpoint, raw Dice was 0.441255 versus filtered Dice 0.424161, raw recall was 0.435298 versus filtered recall 0.403530, and raw predicted-positive pixels were 532,048 versus 493,619 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.220054 | 0.221088 | 0.217762 | 0.241538 | 0.202080 | 0.140016 | 0.004325 |
| 8 | 0.357107 | 0.337143 | 0.405691 | 0.370649 | 0.344519 | 0.216081 | 0.004805 |
| 16 | 0.364891 | 0.336396 | 0.438309 | 0.496266 | 0.288514 | 0.257075 | 0.003005 |
| 20 | 0.390649 | 0.363737 | 0.463261 | 0.531667 | 0.308755 | 0.438686 | 0.003002 |
| 25 | 0.372353 | 0.342671 | 0.450636 | 0.511599 | 0.292689 | 0.312559 | 0.002958 |
| 27 | 0.406609 | 0.382379 | 0.469727 | 0.446231 | 0.373450 | 0.293189 | 0.004326 |
| 30 | 0.394945 | 0.369633 | 0.462048 | 0.514086 | 0.320637 | 0.372817 | 0.003224 |
| 32 | 0.377661 | 0.352088 | 0.441386 | 0.473207 | 0.314218 | 0.252728 | 0.003433 |
| 36 | 0.424161 | 0.406687 | 0.471630 | 0.447015 | 0.403530 | 0.268164 | 0.004667 |

The trajectory is late-budget-dependent and oscillatory. Epoch 20 briefly reaches high precision and high connectivity, but with low recall and lower Dice. The final epoch becomes the selected checkpoint by raising recall and MIT Dice, but this comes with a broadening footprint and weak connectivity. This reinforces that temporal C4 feature-level tail support can shift operating points, but the current guard does not stably combine recall repair with connected-line continuity.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3738, 0.0769, 0.5082, and 0.2749. This confirms finite non-collapsed predictions, with one very weak retained first-n sample consistent with the broader evidence that selective support has not solved positive-tail continuity or low-recall failures.

## Interpretation

Classify ABI-326 as negative-to-mixed capped temporal-family development evidence for the exact ABI-325-style feature-reinjection branch. The selective guard partially controlled footprint and precision compared with ABI-325, but it also surrendered much of ABI-325's recall/MIT-tail repair and did not recover ABI-324's aggregate score, Google balance, compactness, or connected-line continuity.

Comparator roles after ABI-326:

- ABI-324 remains the strongest local balanced temporal C4 aggregate/connectivity comparator.
- ABI-325 remains a recall/MIT-tail diagnostic variant, not a balanced comparator.
- ABI-326 is evidence that a simple selective consensus guard is not enough to rescue the positive-tail reinjection branch.
- ABI-311 remains the five-frame persistence/contrast line-state parent.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the broad recall-heavy temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-326 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249, and it does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, or resource scheduling.

## Decision

Do not promote ABI-326 and do not spend another Run on a close continuation of the ABI-325/326 feature-level positive-tail reinjection/guard idea. ABI-324 remains the better temporal C4 balance point.

A future diagnostic can still use ABI-324/325/326 to understand positive-tail and negative-patch clutter trade-offs, but ABI-326's capped aggregate/source/connectivity evidence is not strong enough to require an immediate Evaluation Request as the next handoff. The next Candidate, if one is submitted later, should broaden away from this exact reinjection/guard branch toward a materially different temporal alignment/change, attention, calibration, data/loss/augmentation policy, or line-continuity mechanism that raises true-positive evidence without sacrificing ABI-324's compactness and connected-line behavior.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_002229_d43b7a/candidate/PROPOSAL.md`
- `run_20260917_002229_d43b7a/candidate/README.md`
- `run_20260917_002229_d43b7a/candidate/manifest.yaml`
- `run_20260917_002229_d43b7a/candidate/budget_request.yaml`
- `run_20260917_002229_d43b7a/resolved_manifest.yaml`
- `run_20260917_002229_d43b7a/execution.json`
- `run_20260917_002229_d43b7a/outputs/model_summary.json`
- `run_20260917_002229_d43b7a/outputs/best_metrics.json`
- `run_20260917_002229_d43b7a/outputs/final_metrics.json`
- `run_20260917_002229_d43b7a/outputs/metrics.jsonl`
- `run_20260917_002229_d43b7a/outputs/resource_profile.json`
- `run_20260917_002229_d43b7a/outputs/validation_postprocessing/index.json`
- `run_20260917_002229_d43b7a/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
