# ABI-319 temporal shift-bank C4 alignment-confidence line U-Net

research-figures: []

## Scope

This note records ABI-319, Candidate `abi319_temporal_shiftbank_c4_alignment_confidence_line_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260915_162050_163586`.

ABI-319 was a bounded exploratory family-development continuation after ABI-315. It kept provider-owned three-frame temporal input with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, then coupled ABI-315-style local shift-bank temporal alignment to an alignment-confidence-gated C4 orientation line-state. The hypothesis was that learned alignment confidence would preserve center-frame detail where temporal matching is ambiguous while using confident previous/next support to stabilize connected thin-line evidence.

The candidate did not implement Candidate-owned data loading, temporal lookup, target construction, losses, metrics, thresholds, postprocessing, Artifact Filters, longitude/latitude features, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior. This is capped temporal-eligible feasibility evidence only, not full Working Validation Split promotion evidence.

## Execution result

ABI-319 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,815,497, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 8,072,058,880 / 8,761,901,056 bytes.
- Training wall time: 1,934.9 s; validation wall time: 1,255.3 s; total Run wall time: 3,192.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 10.

## Best-validation metrics

| Metric | ABI-319 shift-bank C4 confidence | ABI-315 shift-bank scout | ABI-311 five-frame C4 | ABI-309 recall-heavy C4 | ABI-306 compact C4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 10 | 12 | 27 | 29 | 36 |
| Filtered Dice | 0.405847 | 0.389886 | 0.425000 | 0.423544 | 0.422548 |
| MIT filtered Dice | 0.387897 | 0.377376 | 0.403831 | 0.402446 | 0.402764 |
| Google filtered Dice | 0.451369 | 0.420154 | 0.482615 | 0.478510 | 0.476152 |
| Filtered precision | 0.463906 | 0.412308 | 0.459703 | 0.401806 | 0.493422 |
| Filtered recall | 0.360703 | 0.369776 | 0.395169 | 0.447768 | 0.369478 |
| Filtered connectivity | 0.360704 | 0.266017 | 0.366735 | 0.316074 | 0.299384 |
| Filtered predicted-positive fraction | 0.004020 | 0.004636 | 0.004444 | 0.005761 | 0.003871 |

ABI-319 is a useful positive mechanism-change relative to ABI-315 but not a new temporal frontier. Versus ABI-315, it improves filtered Dice by about +0.0160, MIT Dice by +0.0105, Google Dice by +0.0312, precision by +0.0516, and connectivity by +0.0947 while reducing predicted-positive fraction by about -0.00062. The cost is lower recall, about -0.0091. This supports the intended alignment-confidence/C4 coupling: it made shift-bank alignment cleaner and more connected rather than simply expanding the footprint.

Against stronger temporal C4 comparators, ABI-319 remains below the frontier. Relative to ABI-311 it is lower by about -0.0192 filtered Dice, -0.0159 MIT Dice, -0.0312 Google Dice, and -0.0345 recall, while precision is similar and connectivity is only slightly lower. Relative to ABI-309 it avoids the broad recall-heavy footprint and has higher precision/connectivity, but loses too much recall and aggregate Dice. Relative to ABI-306 it improves connectivity but does not match the compact high-precision result.

At the selected checkpoint, raw Dice was 0.423294 versus filtered Dice 0.405847, raw recall was 0.389046 versus filtered recall 0.360703, and raw predicted-positive fraction was 0.004333 versus filtered predicted-positive fraction 0.004020. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.280252 | 0.276669 | 0.288984 | 0.337183 | 0.239768 | 0.218251 | 0.003676 |
| 2 | 0.305437 | 0.294712 | 0.331500 | 0.391905 | 0.250229 | 0.245043 | 0.003301 |
| 3 | 0.331843 | 0.325403 | 0.345709 | 0.316908 | 0.348257 | 0.174773 | 0.005681 |
| 4 | 0.318385 | 0.296445 | 0.371070 | 0.402094 | 0.263524 | 0.246382 | 0.003388 |
| 5 | 0.320411 | 0.299032 | 0.375766 | 0.522639 | 0.231021 | 0.388379 | 0.002285 |
| 6 | 0.350162 | 0.335940 | 0.382805 | 0.372360 | 0.330461 | 0.232541 | 0.004588 |
| 7 | 0.312003 | 0.286253 | 0.381491 | 0.585684 | 0.212640 | 0.460616 | 0.001877 |
| 8 | 0.364507 | 0.348968 | 0.403806 | 0.420493 | 0.321677 | 0.299819 | 0.003955 |
| 9 | 0.384815 | 0.377995 | 0.400843 | 0.360745 | 0.412326 | 0.271291 | 0.005909 |
| 10 | 0.405847 | 0.387897 | 0.451369 | 0.463906 | 0.360703 | 0.360704 | 0.004020 |
| 11 | 0.391315 | 0.373999 | 0.435483 | 0.442741 | 0.350592 | 0.356399 | 0.004094 |
| 12 | 0.363738 | 0.344248 | 0.411028 | 0.449265 | 0.305568 | 0.267612 | 0.003516 |

The trajectory is finite and source-informative, but it does not justify an unchanged late36 continuation. The best checkpoint occurs at epoch 10, followed by two consecutive aggregate and source-specific declines. Epoch 9 briefly reaches the run's highest recall, but with lower precision, a larger footprint, and weaker connectivity. Epoch 7 briefly reaches very high connectivity and precision, but recall and Dice are too low. This indicates a noisy precision/recall/connectivity calibration surface rather than a clearly truncated learning curve.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3060, 0.5833, 0.5270, and 0.3992. This confirms finite non-collapsed predictions with mixed retained-sample behavior, but it is not promotion evidence.

## Interpretation

Classify ABI-319 as a valid, resource-feasible, scientifically useful but non-frontier shift-bank/C4 continuation. It successfully tests the proposed mechanism change: alignment confidence plus C4 orientation consensus clearly repairs much of ABI-315's weak connectivity and precision without broadening the footprint. However, the cleaner line state suppresses recall enough that ABI-319 still trails ABI-311, ABI-309, and ABI-306 on aggregate filtered Dice and source metrics.

The main lesson is that local temporal alignment can be made cleaner, but it still does not raise enough true contrail logits at the fixed 0.5 threshold. The branch's best states alternate among high precision/low recall, recall-heavy/lower-connectivity, and balanced but sub-frontier checkpoints. This points away from an unchanged shift-bank continuation and toward a mechanism that preserves the ABI-319 confidence/C4 cleanliness while adding recall-protected evidence: for example temporal attention evidence sharpening, a dual-evidence recall head tied to center-frame detail, or a different temporal line-state update that explicitly protects true-positive recall without Candidate-owned thresholding.

## Decision

Do not promote ABI-319. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped exploratory Result. Do not request an unchanged late36 continuation: the selected best epoch is not final, the final trajectory regresses, and the Result remains materially below stronger temporal C4 comparators.

Record ABI-319 as bounded positive evidence for alignment-confidence-gated C4 line consensus over ABI-315, and bounded negative evidence that this exact shift-bank/C4 design is sufficient for the current temporal frontier. A future proposal should be mechanism-changing and recall-protecting rather than another direct shift-bank refinement.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_162050_163586/candidate/PROPOSAL.md`
- `run_20260915_162050_163586/candidate/README.md`
- `run_20260915_162050_163586/candidate/manifest.yaml`
- `run_20260915_162050_163586/resolved_manifest.yaml`
- `run_20260915_162050_163586/execution.json`
- `run_20260915_162050_163586/outputs/model_summary.json`
- `run_20260915_162050_163586/outputs/best_metrics.json`
- `run_20260915_162050_163586/outputs/final_metrics.json`
- `run_20260915_162050_163586/outputs/metrics.jsonl`
- `run_20260915_162050_163586/outputs/resource_profile.json`
- `run_20260915_162050_163586/outputs/validation_postprocessing/index.json`
- `run_20260915_162050_163586/outputs/prediction_samples/samples.json`
- `run_20260915_100642_28e66d/outputs/best_metrics.json` and `/history/research-notes/abi315-temporal-shiftbank-alignment-detail-unet-syntax-repair.md` for ABI-315 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
