# ABI-352 full-spectral BTD+SZA C4 cross-scale detail agreement

research-figures: []

## Scope

This note records ABI-352, Candidate `abi352_fullspectral_btd_sza_c4_crossscale_detail_agreement_unet_bce_dice_line_centerline_aux_v1`, and Run `run_20260919_044205_9523b3`.

ABI-352 was an exploratory mechanism-changing continuation of the single-frame C4/orientation branch. It kept provider-owned `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW, constant LR, and batch size 4. The architectural change was a pre-head cross-scale detail-agreement block: full-resolution decoder features, high-resolution signed detail, stem evidence, and coarser decoder context are fused before the final heads, then C4 line context is injected through a learned line/detail agreement gate.

This is capped representative exploratory evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-352 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,970,653, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 8,822,962,176 / 10,431,234,048 bytes.
- Training wall time: 1,380.6 s; validation wall time: 1,375.2 s; total Run wall time: 2,757.7 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-352 cross-scale detail agreement | ABI-343 precision-veto recall | ABI-342 recall bridge | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 32 | 36 | 31 | 34 |
| Filtered Dice | 0.387651 | 0.409827 | 0.415499 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.371563 | 0.392320 | 0.398614 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.426257 | 0.453242 | 0.460044 | 0.468855 | 0.468151 |
| Filtered precision | 0.378511 | 0.417766 | 0.397609 | 0.480886 | 0.439467 |
| Filtered recall | 0.397243 | 0.402184 | 0.435075 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.292383 | 0.379763 | 0.405280 | 0.392524 | 0.457773 |
| Filtered predicted-positive fraction | 0.003803 | 0.003489 | 0.003965 | 0.002767 | 0.003433 |
| Filtered predicted-positive pixels | 510,432 | 468,221 | 532,191 | 371,346 | 460,724 |

ABI-352 is finite and non-collapsed, but its selected exploratory checkpoint is not a comparator replacement. Relative to ABI-249, it recovers recall (+0.0301) but loses much more precision (-0.1024), aggregate Dice (-0.0287), MIT Dice (-0.0249), Google Dice (-0.0426), and connectivity (-0.1001), while predicting about 139k more filtered-positive pixels. Relative to ABI-342, ABI-352 is less broad than the recall bridge (-21,759 filtered-positive pixels) but also lower on recall (-0.0378), precision (-0.0191), connectivity (-0.1129), and filtered Dice (-0.0278). Relative to ABI-343, it is both broader (+42,211 filtered-positive pixels) and weaker on Dice, precision, recall, and connectivity.

The intended pre-head detail-agreement block therefore did not yet solve the C4 trade-off: it raises fixed-threshold recall above ABI-249, but not compactly, and connected-line evidence is weaker than the established C4 comparators. The source pattern is informative rather than catastrophic, but both Dataset Sources underperform ABI-249/342/343, with the larger gap on Google.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.400575 versus filtered Dice 0.387651; raw recall was 0.424735 versus filtered recall 0.397243; raw predicted-positive pixels were 545,030 versus 510,432 filtered. Artifact Filters removed 34,598 predicted-positive pixels and lowered the score.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.208928 | 0.231963 | 0.170375 | 0.172404 | 0.265086 | 0.088862 | 0.005572 |
| 2 | 0.293279 | 0.307152 | 0.263663 | 0.239646 | 0.377842 | 0.176757 | 0.005713 |
| 3 | 0.303932 | 0.304259 | 0.303208 | 0.316933 | 0.291955 | 0.235788 | 0.003338 |
| 4 | 0.300335 | 0.300660 | 0.299660 | 0.275236 | 0.330472 | 0.176925 | 0.004351 |
| 5 | 0.320756 | 0.302537 | 0.364048 | 0.428200 | 0.256416 | 0.356957 | 0.002170 |
| 6 | 0.366443 | 0.356808 | 0.389388 | 0.385994 | 0.348777 | 0.264523 | 0.003274 |
| 7 | 0.331052 | 0.324956 | 0.344424 | 0.341056 | 0.321618 | 0.207596 | 0.003417 |
| 8 | 0.353661 | 0.338480 | 0.389728 | 0.427778 | 0.301434 | 0.310060 | 0.002553 |
| 9 | 0.380898 | 0.367660 | 0.413788 | 0.407253 | 0.357748 | 0.307607 | 0.003183 |
| 10 | 0.339996 | 0.315953 | 0.395956 | 0.471415 | 0.265876 | 0.385583 | 0.002044 |
| 11 | 0.361027 | 0.362193 | 0.358388 | 0.326124 | 0.404298 | 0.203130 | 0.004492 |
| 12 | 0.387651 | 0.371563 | 0.426257 | 0.378511 | 0.397243 | 0.292383 | 0.003803 |

The trajectory is finite, noisy, and late-improving by the selection metric: epoch 12 is the best aggregate filtered-Dice checkpoint. ABI-352 also outperforms ABI-249 and ABI-342 at their own epoch-12 aggregate filtered Dice, although ABI-343 was already slightly stronger by epoch 12 and much stronger by its late-budget selected checkpoint. The pattern is therefore ambiguous rather than a hard execution or optimization stop.

The concern is that the useful states are not aligned. Epoch 10 briefly reaches compact high precision and higher connectivity (0.4714 precision, 0.3856 connectivity) but has weak recall and Dice. Epochs 11-12 recover recall and aggregate Dice but lose compactness and connectivity. This mirrors the broader C4-family failure mode: final selected checkpoints trade among recall, clutter footprint, and connected-line continuity rather than improving all three.

## Prediction sample check

The retained fixed first-four validation samples all had near-zero sample Dice and IoU. These fixed first-n samples are Harness traceability artifacts, not representative diagnostics, and should not override aggregate validation metrics. The sample set does not justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-352 as technically healthy but non-frontier exploratory C4-family evidence. The pre-head cross-scale detail-agreement mechanism is not a promotion candidate and does not replace ABI-249, ABI-342, ABI-343, or ABI-202. It does, however, produce a finite final-epoch-best trajectory under only 12 epochs, so it is not eliminated by execution failure or prediction collapse.

The scientific readout is specific: moving the C4 recall support before the final head did not automatically preserve compactness or connected-line continuity. Cross-scale detail agreement can raise thresholded positives, but in this implementation the selected state is still broader and less connected than the desired C4 operating point. If this branch is continued, it should be treated as a bounded late-improving close continuation or a mechanism-changing refinement that explicitly stabilizes the compact high-connectivity state observed around epoch 10 while preserving the recall/Dice gains seen at epoch 12. It should not become an unchanged series of final-logit gain/veto variants.

Comparator roles remain unchanged:

- ABI-202 remains the aggregate whole-validation filtered-Dice reference.
- ABI-249 remains the compact high-precision single-frame C4 comparator.
- ABI-342 remains the recall-biased C4 diagnostic.
- ABI-343 remains the precision-veto diagnostic.
- ABI-352 is a pre-head cross-scale detail-agreement diagnostic with ambiguous late-improving exploratory behavior.

## Decision

Do not promote ABI-352 and do not request whole-validation evaluation in this Autonomy Step. The capped exploratory result is below the current C4 comparators and does not create a near-frontier promotion case.

A future handoff may reasonably choose one of two paths: request an approved `late_improving` close-continuation for ABI-352 because the selected checkpoint is at epoch 12 and finite/source-informative, or broaden to a different mechanism that moves continuity support earlier and more stably. Either path must remain within provider-owned inputs, losses, metrics, Artifact Filters, sampling, augmentation, execution, and lifecycle boundaries.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_044205_9523b3/candidate/PROPOSAL.md`
- `run_20260919_044205_9523b3/candidate/README.md`
- `run_20260919_044205_9523b3/candidate/manifest.yaml`
- `run_20260919_044205_9523b3/resolved_manifest.yaml`
- `run_20260919_044205_9523b3/execution.json`
- `run_20260919_044205_9523b3/run_metadata.json`
- `run_20260919_044205_9523b3/outputs/model_summary.json`
- `run_20260919_044205_9523b3/outputs/best_metrics.json`
- `run_20260919_044205_9523b3/outputs/final_metrics.json`
- `run_20260919_044205_9523b3/outputs/metrics.jsonl`
- `run_20260919_044205_9523b3/outputs/resource_profile.json`
- `run_20260919_044205_9523b3/outputs/validation_postprocessing/index.json`
- `run_20260919_044205_9523b3/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 comparison context
- `run_20260918_055403_f17232/outputs/best_metrics.json` for ABI-342 comparison context
- `run_20260918_081800_9f0872/outputs/best_metrics.json` for ABI-343 comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 comparison context
- `/history/research-notes/abi342-fullspectral-btd-sza-c4-recall-bridge-late36.md`
- `/history/research-notes/abi343-fullspectral-btd-sza-c4-precision-veto-recall-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
