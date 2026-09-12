# ABI-226 temporal five-frame attention/difference cache-ready repair

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-226, Candidate `abi226_temporal_fiveframe_attention_difference_unet_cache_ready_repair_bce_dice_line_centerline_aux_v1`, Run `run_20260910_120441_916a03`.

ABI-226 was a narrow repair of ABI-224 after the original five-frame temporal scout failed before training because the then-active temporal eligibility/cache surface exposed zero available samples for the requested sampling policy. It preserved the original five-frame hypothesis: use provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-2, -1, 0, 1, 2]`, `frame_selection_policy: temporal_eligible_center`, a compact temporal-attention/difference U-Net, BCE-Dice loss, random mirroring, and trusted Line/Centerline auxiliary targets. Candidate code remained architecture-only and did not implement temporal lookup, cache repair, data loading, missing-frame fallback, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Execution result

ABI-226 completed the 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure. The repair therefore resolved the practical data-loader blocker for the five-frame temporal scout and produced finite resource/metric evidence.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, no late-improving request.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-2, -1, 0, 1, 2]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sampling: provider-owned `combined_source_balanced` with 1,024 selected train ABI Patches per Dataset Source and 1,614 total validation ABI Patches after five-frame temporal eligibility.
- Five-frame selected validation counts: 915 MIT and 699 Google ABI Patches.
- Parameter count: 3,098,332, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.39 / 3.62 GB.
- Training wall time: 1,012.4 s; validation wall time: 1,105.3 s; total Run wall time: 2,119.4 s.

## Best-validation metrics

The best checkpoint was epoch 10 by `val/filtered_dice`.

| Metric | ABI-226 best epoch 10 |
| --- | ---: |
| Filtered Dice | 0.378604 |
| Raw Dice | 0.394881 |
| Filtered IoU | 0.233505 |
| Filtered precision | 0.428061 |
| Filtered recall | 0.339391 |
| Filtered contrail connectivity | 0.224851 |
| Filtered predicted-positive fraction | 0.004099 |
| Raw predicted-positive fraction | 0.004420 |
| MIT filtered Dice | 0.366586 |
| Google filtered Dice | 0.409886 |
| MIT filtered recall | 0.317207 |
| Google filtered recall | 0.405394 |
| Train loss | 0.815114 |
| Validation loss | 0.856664 |

The Result is finite, noncollapsed, and source-informative. However, it is not competitive with ABI-223's late36 three-frame temporal-attention frontier.

## Learning trajectory

ABI-226 improved through epoch 10, then regressed over epochs 11 and 12. This does not satisfy the current late-improving budget rationale: the best checkpoint is not at the final exploratory epoch, and the final checkpoint shows lower filtered Dice and worse connectivity.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.226484 | 0.235862 | 0.235004 | 0.218560 | 0.225226 | 0.229306 | 0.141433 | 0.004808 |
| 2 | 0.244694 | 0.256479 | 0.326360 | 0.195718 | 0.231887 | 0.274920 | 0.160086 | 0.003100 |
| 3 | 0.309396 | 0.323685 | 0.364141 | 0.268961 | 0.300064 | 0.331471 | 0.190856 | 0.003818 |
| 4 | 0.296224 | 0.310604 | 0.405011 | 0.233504 | 0.276075 | 0.346519 | 0.291355 | 0.002980 |
| 5 | 0.291396 | 0.303707 | 0.325883 | 0.263509 | 0.281380 | 0.314187 | 0.160950 | 0.004180 |
| 6 | 0.324144 | 0.338596 | 0.377978 | 0.283734 | 0.310190 | 0.359905 | 0.213867 | 0.003881 |
| 7 | 0.340472 | 0.356960 | 0.447389 | 0.274800 | 0.324030 | 0.381385 | 0.290192 | 0.003175 |
| 8 | 0.342198 | 0.356661 | 0.356922 | 0.328641 | 0.335453 | 0.358150 | 0.186159 | 0.004760 |
| 9 | 0.364125 | 0.378061 | 0.351827 | 0.377314 | 0.355263 | 0.385243 | 0.220474 | 0.005544 |
| 10 | 0.378604 | 0.394881 | 0.428061 | 0.339391 | 0.366586 | 0.409886 | 0.224851 | 0.004099 |
| 11 | 0.366740 | 0.381919 | 0.370640 | 0.362922 | 0.354224 | 0.397359 | 0.212726 | 0.005062 |
| 12 | 0.349465 | 0.362938 | 0.344471 | 0.354606 | 0.334100 | 0.385396 | 0.174188 | 0.005322 |

The best epoch is precision-led relative to epoch 9 and 11, while recall peaks at epoch 9/11. The final decline suggests either overfitting/instability or that the current five-frame fusion is not using the wider temporal context robustly.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-219 temporal difference | ABI-220 change confidence | ABI-221 ConvGRU state | ABI-222 attention 12ep | ABI-223 attention late36 | ABI-226 five-frame scout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 8 | 11 | 10 | 12 | 36 | 10 |
| Filtered Dice | 0.345570 | 0.367589 | 0.368730 | 0.363826 | 0.374329 | 0.419776 | 0.378604 |
| Raw Dice | 0.361077 | 0.383372 | 0.384987 | 0.380351 | 0.392066 | 0.438487 | 0.394881 |
| Filtered precision | 0.407234 | 0.406513 | 0.417944 | 0.449905 | 0.466148 | 0.483764 | 0.428061 |
| Filtered recall | 0.300125 | 0.335468 | 0.329885 | 0.305396 | 0.312729 | 0.370738 | 0.339391 |
| Filtered connectivity | 0.231399 | 0.288750 | 0.278802 | 0.305528 | 0.281396 | 0.412427 | 0.224851 |
| MIT filtered Dice | 0.330415 | 0.352675 | 0.350694 | 0.343643 | 0.357658 | 0.398498 | 0.366586 |
| Google filtered Dice | 0.385184 | 0.403426 | 0.415136 | 0.415624 | 0.416510 | 0.476764 | 0.409886 |
| Filtered predicted-positive fraction | 0.003810 | 0.004266 | 0.004080 | 0.003509 | 0.003468 | 0.003962 | 0.004099 |
| Parameter count | 3,050,475 | 3,060,963 | 3,073,336 | 3,134,248 | 3,095,836 | 3,095,836 | 3,098,332 |

ABI-226 exceeds the ABI-218 matched single-frame temporal-eligible control by +0.033034 filtered Dice and +0.039266 filtered recall, so the wider temporal input did not collapse below the non-temporal control. It also slightly exceeds the ABI-222 12-epoch three-frame temporal-attention scout on filtered Dice (+0.004275) and recall (+0.026662). But it remains far below ABI-223's late36 continuation: -0.041172 filtered Dice, -0.055703 precision, -0.031347 recall, -0.187576 connectivity, -0.031912 MIT filtered Dice, and -0.066878 Google filtered Dice.

The strongest negative signal is connectivity. If five-frame context were already improving line continuity, it should not trail every listed temporal model on filtered contrail connectivity.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result in the campaign, with whole-validation filtered Dice 0.4312. ABI-223 remains the capped temporal-family frontier, with filtered Dice 0.419776 at epoch 36 and strong gains over ABI-218 through ABI-222.

ABI-226 is useful as a repaired five-frame feasibility scout, not as a promotion result. It validates that the refreshed temporal eligibility/cache surface can support five-frame source-balanced training, but the architecture did not convert wider temporal context into better capped validation performance than the late-improving three-frame attention model.

## Interpretation

The repair portion succeeded: ABI-226 trained on nonzero MIT and Google five-frame temporal-eligible samples and completed within resource limits. The scientific five-frame result is mixed-to-negative. The best score is better than the 12-epoch three-frame attention scout and the single-frame control, but the run trails ABI-223 by a large margin and has especially weak connectivity. The final two epochs regress rather than strengthen the case for a longer budget.

A plausible failure mode is that the near/far difference stack and per-pixel temporal attention add temporal degrees of freedom without enforcing coherent line-level motion or persistence. The wider window may dilute center-frame evidence or emphasize cloud evolution artifacts unless the architecture has a stronger temporal-line continuity inductive bias.

## Decision

Do not promote ABI-226 and do not request a late-improving continuation of this exact five-frame attention/difference branch. Treat it as finite repair/resource evidence and a bounded negative result for this particular wider-window fusion design.

The next temporal-family step, if continuing temporal work, should change the temporal architecture rather than merely extend ABI-226. Reasonable in-contract options include a compact temporal-line consistency module, a motion/change branch with stronger center-frame anchoring, or a different underexplored architecture family such as rotation-aware line accumulation. Any five-frame continuation should be sequential and should have a specific fix for ABI-226's weak connectivity and late-epoch regression.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_120441_916a03/candidate/PROPOSAL.md`
- `run_20260910_120441_916a03/candidate/README.md`
- `run_20260910_120441_916a03/candidate/manifest.yaml`
- `run_20260910_120441_916a03/resolved_manifest.yaml`
- `run_20260910_120441_916a03/outputs/model_summary.json`
- `run_20260910_120441_916a03/outputs/best_metrics.json`
- `run_20260910_120441_916a03/outputs/final_metrics.json`
- `run_20260910_120441_916a03/outputs/metrics.jsonl`
- `run_20260910_120441_916a03/outputs/resource_profile.json`
- `run_20260910_120441_916a03/outputs/validation_postprocessing/index.json`
- `run_20260910_120441_916a03/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260908_172818_76b0fc` for ABI-224 original failed five-frame attempt
- `run_20260908_123030_05ad37` for ABI-218 temporal-eligible single-frame control
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
