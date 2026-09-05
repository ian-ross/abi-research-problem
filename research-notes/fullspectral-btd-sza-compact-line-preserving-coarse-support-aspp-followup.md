# Full-spectral BTD+SZA compact line-preserving coarse-support ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-212, Candidate `abi212_fullspectral_btd_sza_compact_line_preserving_coarse_support_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260904_172606_3f797b`.

ABI-212 was the resource-safe continuation of ABI-211 (`run_20260904_162059_678c48`), which exhausted the 3,600-second exploratory wall-clock budget during epoch 12 after finite partial validation. ABI-212 kept the same in-contract hypothesis: use broad decoder/stem/full-scale context only as a bounded additive support cue while preserving the signed-detail thin-line stream. The architecture was compacted by reducing learned spectral projection width, base width, full-scale fusion width, and directional/refiner cost.

The Run used provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived BTD/SZA/cos-SZA features, trusted BCE-Dice primary loss, provider-derived Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at learning rate 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. Candidate code did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, sampling behavior, augmentation, training loops, runtime downloads, persistence writes, or resource scheduling.

Primary comparisons are ABI-211 for resource/partial-signal recovery, ABI-210 as the preceding compact support-bridge result, ABI-201/203 as stronger exploratory same-family references, ABI-202 as the current late-improving whole-validation aggregate reference, and ABI-184 as the precision/connectivity discipline reference.

## Capped exploratory metrics

ABI-212 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as best by `val/filtered_dice`, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-212 capped best/final |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3875 |
| MIT filtered Dice | 0.3759 |
| Google filtered Dice | 0.4172 |
| Filtered precision | 0.4170 |
| Filtered recall | 0.3618 |
| Filtered contrail connectivity | 0.3235 |
| Filtered predicted-positive fraction | 0.003144 |
| Raw Dice | 0.4017 |
| Raw recall | 0.3870 |
| Train loss | 0.8517 |
| Validation loss | 0.8838 |

The finite trajectory improved from 0.2142 filtered Dice at epoch 1 to the selected 0.3875 at epoch 12. The final four filtered-Dice values were 0.3681, 0.3777, 0.3759, and 0.3875; validation loss also edged down from 0.8860 at epoch 9 to 0.8838 at epoch 12. This is not prediction collapse or numerical failure, but the best checkpoint remains below stronger same-family exploratory references.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_162059_678c48` | ABI-211 full line-preserving coarse support | exploratory, failed | 9 observed | 0.3778 | 0.3607 | 0.4233 | 0.4584 | 0.3213 | 0.3793 | 0.002540 |
| `run_20260904_172606_3f797b` | ABI-212 compact line-preserving coarse support | exploratory | 12 | 0.3875 | 0.3759 | 0.4172 | 0.4170 | 0.3618 | 0.3235 | 0.003144 |
| `run_20260904_152018_ce1309` | ABI-210 compact spectral-ridge support | exploratory | 12 | 0.3952 | 0.3865 | 0.4163 | 0.3974 | 0.3931 | 0.2515 | 0.003584 |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional-consensus ASPP | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated same-family probe | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional-consensus ASPP | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-212 solved the immediate resource problem from ABI-211 and exceeded ABI-211's partial best filtered Dice by about 0.0096 while completing the missing epoch-12 validation. It also increased MIT filtered Dice and recall relative to ABI-211. The cost of that compaction/recovery was a weaker precision/connectivity/positive-area profile: precision fell by about 0.0414, connectivity by about 0.0558, and the filtered predicted-positive fraction rose from 0.002540 to 0.003144.

Relative to ABI-210, ABI-212 is a different support tradeoff rather than an improvement: it gains precision and connectivity over ABI-210's recall-heavy, low-connectivity spectral-support result, but loses aggregate filtered Dice and recall. Relative to ABI-201 and ABI-203, it is below the local exploratory frontier on aggregate filtered Dice and especially below ABI-201/202/184 on connectivity. Relative to ABI-202, it is lower on aggregate, both Dataset Sources, precision, recall, and connectivity.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved model used approved `abi_16ch_plus_sza` input mode, excluded forbidden longitude/latitude channels, and emitted `mask_logits`, `line_logits`, and `centerline_logits`.

The model summary reports 4,867,671 parameters, under the 25,000,000-parameter ceiling. Resource profiling completed successfully with peak CUDA allocation of 7,902,104,064 bytes, peak reserved CUDA memory of 9,466,544,128 bytes, and total Run wall time of 2,862.8 seconds. This is comfortably below the 3,600-second exploratory timeout and materially safer than ABI-211, but the branch did not recover enough scientific quality to justify expanding this exact support bridge.

## Interpretation

Classify ABI-212 as a valid, finite, resource-repairing but scientifically mixed-to-negative capped exploratory Result. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, or unknown failure. It confirms that the compact line-preserving coarse-support implementation is executable under the current envelope, but does not show that this support bridge improves the ABI-202 lineage's false-positive/connectivity problem.

The important design lesson is that broad support cues remain risky even when used as bounded additive features. In ABI-212, compaction made the Run feasible and improved recall versus ABI-211, but the resulting operating point no longer retained ABI-211/ABI-201/ABI-184 precision and connectivity discipline. Together with ABI-210, this is negative evidence against continuing broad support-expansion bridges as the next local search path.

## Decision

Do not promote ABI-212, do not request whole-validation diagnostics for this exact Run, and do not request a late36 continuation for this exact compact line-preserving coarse-support branch.

Retain ABI-202 as the current whole-validation-tested aggregate filtered-Dice reference, ABI-184 as the precision/connectivity and stricter positive-area-discipline reference, and ABI-203 as the stronger same-family exploratory foreground-calibrated probe. Treat ABI-212 as resource-feasibility evidence and as negative evidence for further broad support-bridge expansion under the active exploratory budget.

A reasonable next in-contract hypothesis is to broaden away from support-expansion bridges: either an architecture scout that separates candidate-local line continuity refinement from coarse context without using broad support to overwrite the line path, or a conservative ABI-202 continuation that improves clutter specificity through narrower feature modulation. Candidate code must continue to use only provider-approved ABI/SZA inputs and must not implement data loading, losses, metrics, Artifact Filters, thresholding, sampling behavior, augmentation, coordinate features, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_172606_3f797b/outputs/best_metrics.json`
- `run_20260904_172606_3f797b/outputs/final_metrics.json`
- `run_20260904_172606_3f797b/outputs/metrics.jsonl`
- `run_20260904_172606_3f797b/outputs/resource_profile.json`
- `run_20260904_172606_3f797b/outputs/model_summary.json`
- `run_20260904_172606_3f797b/outputs/prediction_samples/samples.json`
- `run_20260904_172606_3f797b/resolved_manifest.yaml`
- `run_20260904_172606_3f797b/candidate/PROPOSAL.md`
- `run_20260904_162059_678c48/outputs/metrics.jsonl`
- `run_20260904_162059_678c48/outputs/logs/harness_timeout.log`
- `run_20260904_152018_ce1309/outputs/best_metrics.json`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
