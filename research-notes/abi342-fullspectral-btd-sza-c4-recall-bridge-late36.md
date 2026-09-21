# ABI-342 full-spectral BTD+SZA C4 recall bridge late36

research-figures: []

## Scope

This note records ABI-342, Candidate `abi342_fullspectral_btd_sza_c4_recall_bridge_late36_bce_dice_line_centerline_aux_v1`, and Run `run_20260918_055403_f17232`.

ABI-342 was a mechanism-changing continuation of the ABI-249 single-frame C4/orientation-prior branch. It kept provider-owned `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW, constant LR, batch size 4, and the approved late-improving budget. The architecture change was a bounded C4/Line-evidence-gated recall bridge in the mask head, intended to raise fixed-threshold recall while preserving ABI-249's compact high-precision behavior.

This is capped representative feasibility evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-342 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved from parent `run_20260911_111909_dd7ef7`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,917,654, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 8,555,962,880 / 9,873,391,616 bytes.
- Training wall time: 4,036.9 s; validation wall time: 4,049.1 s; total Run wall time: 8,088.8 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-342 C4 recall bridge | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: |
| Best epoch | 36 | 31 | 34 |
| Filtered Dice | 0.415499 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.398614 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.460044 | 0.468855 | 0.468151 |
| Filtered precision | 0.397609 | 0.480886 | 0.439467 |
| Filtered recall | 0.435075 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.405280 | 0.392524 | 0.457773 |
| Filtered predicted-positive fraction | 0.003965 | 0.002767 | 0.003433 |
| Filtered predicted-positive pixels | 532,191 | ~371,346 | ~460,411 |

The recall bridge did recover fixed-threshold recall: +0.0679 over ABI-249 and +0.0188 over ABI-202 on the capped validation split. It also modestly improved ABI-249 connectivity (+0.0128) and MIT filtered Dice (+0.0022). However, the recall gain was too expensive: filtered precision fell -0.0833 versus ABI-249 and -0.0419 versus ABI-202, filtered positive pixels rose by about 160k versus ABI-249 and 72k versus ABI-202, and aggregate filtered Dice remained below both references.

The source pattern is not a collapse, but it is not a comparator replacement. Google filtered Dice fell -0.0088 relative to ABI-249, while MIT rose only +0.0022. ABI-342 therefore shifts the C4 branch toward recall and MIT balance, but away from the compact high-precision operating point that made ABI-249 useful.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected epoch, raw Dice was 0.429444 and filtered Dice was 0.415499; raw recall was 0.466622 and filtered recall was 0.435075; raw predicted-positive pixels were 570,572 and filtered predicted-positive pixels were 532,191.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.181965 | 0.214561 | 0.135377 | 0.132543 | 0.290158 | 0.083147 | 0.007933 |
| 5 | 0.325931 | 0.304633 | 0.379861 | 0.488736 | 0.244489 | 0.469268 | 0.001813 |
| 10 | 0.353516 | 0.344520 | 0.372541 | 0.373776 | 0.335339 | 0.252238 | 0.003251 |
| 15 | 0.383603 | 0.377784 | 0.396911 | 0.358304 | 0.412746 | 0.263758 | 0.004174 |
| 20 | 0.375149 | 0.360256 | 0.409421 | 0.424756 | 0.335916 | 0.270633 | 0.002866 |
| 25 | 0.398669 | 0.379066 | 0.446722 | 0.448267 | 0.358953 | 0.336207 | 0.002902 |
| 30 | 0.387409 | 0.363179 | 0.447236 | 0.493214 | 0.318981 | 0.411035 | 0.002344 |
| 34 | 0.414828 | 0.397085 | 0.459144 | 0.430486 | 0.400270 | 0.383119 | 0.003369 |
| 36 | 0.415499 | 0.398614 | 0.460044 | 0.397609 | 0.435075 | 0.405280 | 0.003965 |

The trajectory was finite, non-collapsed, source-informative, and late-forming. High-precision/compact states appeared at epochs 5 and 30, while the selected final checkpoint moved strongly toward recall. The final epoch being best confirms that the approved late-improving budget was useful, but the policy does not provide another unchanged epoch extension beyond 36. Any continuation should change the mechanism, not request an unchanged later budget.

## Prediction sample check

The retained first-four validation samples had near-zero sample Dice values. These fixed first-n samples are traceability artifacts, not representative diagnostics, and should not override the aggregate validation metrics. The sample set does not justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-342 as useful but not frontier-improving capped C4-family evidence. It answers the mechanism question in one direction: ABI-249-style C4 orientation context can support a substantial recall lift at threshold 0.5. The current bridge does not preserve enough precision or compactness to replace ABI-249, and it does not approach ABI-202's aggregate/connectivity balance.

Comparator roles after ABI-342:

- ABI-202 remains the aggregate whole-validation filtered-Dice reference.
- ABI-249 remains the compact high-precision single-frame C4 comparator.
- ABI-342 is a recall-biased C4 diagnostic showing that C4 recall repair is possible but currently too broad.

Do not submit an unchanged late36 continuation of this exact recall bridge. If the C4/orientation-prior branch is revisited, the next mechanism should explicitly constrain clutter and preserve precision, for example by making the recall residual more conditional on cross-scale center-frame detail, disagreement vetoes, or connected-line consensus rather than simply scaling the existing residual.

## Decision

Do not promote ABI-342. Do not request a whole-validation diagnostic in this Autonomy Step: the capped result already misses the preregistered precision target and remains below both ABI-249 and ABI-202 aggregate filtered Dice. A future Evaluation Request could still be justified if the campaign specifically needs failure-bucket evidence for C4 recall repair, but ABI-342 is not currently a promotion or comparator-replacement candidate.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_055403_f17232/candidate/PROPOSAL.md`
- `run_20260918_055403_f17232/candidate/README.md`
- `run_20260918_055403_f17232/candidate/manifest.yaml`
- `run_20260918_055403_f17232/candidate/budget_request.yaml`
- `run_20260918_055403_f17232/resolved_manifest.yaml`
- `run_20260918_055403_f17232/execution.json`
- `run_20260918_055403_f17232/run_metadata.json`
- `run_20260918_055403_f17232/outputs/model_summary.json`
- `run_20260918_055403_f17232/outputs/best_metrics.json`
- `run_20260918_055403_f17232/outputs/final_metrics.json`
- `run_20260918_055403_f17232/outputs/metrics.jsonl`
- `run_20260918_055403_f17232/outputs/resource_profile.json`
- `run_20260918_055403_f17232/outputs/validation_postprocessing/index.json`
- `run_20260918_055403_f17232/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
