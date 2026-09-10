# ABI-220 temporal change-confidence gate

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-220, Candidate `abi220_temporal_change_confidence_gate_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_134203_8bbb6f`.

ABI-220 was the temporal-family continuation proposed after ABI-219. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. It preserved ABI-219's explicit temporal-difference feature groups, but replaced the simple temporal stem gate with a center-frame path plus learned spatial/channel confidence gates for signed and absolute temporal-change residuals. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-220 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,073,336, below the 25,000,000-parameter ceiling.
- Batch size: 2, no Resource Failure retry.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 1.83 / 2.11 GB.
- Training wall time: 792.6 s; validation wall time: 910.2 s; total Run wall time: 1,704.6 s.

This is successful finite/resource evidence for a compact temporal change-confidence gate. Its resource profile remains close to ABI-219, with only about 12k additional parameters and about 58 s additional total wall time.

## Best-validation metrics

The best checkpoint was epoch 11 by `val/filtered_dice`.

| Metric | ABI-220 best epoch 11 |
| --- | ---: |
| Filtered Dice | 0.368730 |
| Raw Dice | 0.384987 |
| Filtered IoU | 0.226038 |
| Filtered precision | 0.417944 |
| Filtered recall | 0.329885 |
| Filtered contrail connectivity | 0.278802 |
| Filtered predicted-positive fraction | 0.004080 |
| Raw predicted-positive fraction | 0.004398 |
| MIT filtered Dice | 0.350694 |
| Google filtered Dice | 0.415136 |
| MIT filtered recall | 0.301876 |
| Google filtered recall | 0.413217 |
| Train loss | 0.821388 |
| Validation loss | 0.869309 |

Final epoch 12 did not exceed the best checkpoint: filtered Dice 0.344701, raw Dice 0.360502, filtered precision 0.435534, filtered recall 0.285217, MIT filtered Dice 0.323994, Google filtered Dice 0.398829, connectivity 0.294375, and filtered predicted-positive fraction 0.003385. The final-epoch shift again moved toward fewer predicted positives and lower recall, with slightly higher precision and connectivity than the best epoch.

## Learning trajectory

ABI-220 learned steadily through epoch 7, oscillated at epochs 8-10, reached the primary-metric best at epoch 11, then dropped at epoch 12.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.153001 | 0.159088 | 0.142285 | 0.165463 | 0.155920 | 0.147541 | 0.112293 | 0.006012 |
| 2 | 0.204262 | 0.214106 | 0.300647 | 0.154675 | 0.192145 | 0.232073 | 0.182116 | 0.002660 |
| 3 | 0.250079 | 0.259878 | 0.233741 | 0.268871 | 0.248841 | 0.252532 | 0.144412 | 0.005947 |
| 4 | 0.259893 | 0.271433 | 0.294358 | 0.232652 | 0.246808 | 0.291950 | 0.213027 | 0.004086 |
| 5 | 0.286048 | 0.299288 | 0.382426 | 0.228470 | 0.268055 | 0.330218 | 0.215028 | 0.003088 |
| 6 | 0.329602 | 0.344149 | 0.378614 | 0.291824 | 0.314711 | 0.366526 | 0.212780 | 0.003985 |
| 7 | 0.353672 | 0.369711 | 0.436953 | 0.297055 | 0.330170 | 0.413769 | 0.297314 | 0.003514 |
| 8 | 0.326319 | 0.341410 | 0.402180 | 0.274535 | 0.303348 | 0.385537 | 0.275102 | 0.003529 |
| 9 | 0.351403 | 0.365098 | 0.342378 | 0.360916 | 0.334140 | 0.393835 | 0.233305 | 0.005449 |
| 10 | 0.359939 | 0.375460 | 0.398896 | 0.327915 | 0.343215 | 0.402838 | 0.282856 | 0.004250 |
| 11 | 0.368730 | 0.384987 | 0.417944 | 0.329885 | 0.350694 | 0.415136 | 0.278802 | 0.004080 |
| 12 | 0.344701 | 0.360502 | 0.435534 | 0.285217 | 0.323994 | 0.398829 | 0.294375 | 0.003385 |

The trajectory is source-informative and noncollapsed. Both Dataset Sources improved from epoch 1, and predicted-positive fractions stayed small but nonzero. ABI-220 did not solve the temporal branch's precision/recall oscillation: epoch 9 had the strongest recall but weaker precision/connectivity, while epochs 7, 11, and 12 favored higher precision or connectivity at lower recall.

## Matched temporal-family comparison

| Metric | ABI-218 single-frame control best | ABI-219 temporal-difference best | ABI-220 change-confidence best |
| --- | ---: | ---: | ---: |
| Best epoch | 11 | 8 | 11 |
| Filtered Dice | 0.345570 | 0.367589 | 0.368730 |
| Raw Dice | 0.361077 | 0.383372 | 0.384987 |
| Filtered precision | 0.407234 | 0.406513 | 0.417944 |
| Filtered recall | 0.300125 | 0.335468 | 0.329885 |
| Filtered contrail connectivity | 0.231399 | 0.288750 | 0.278802 |
| MIT filtered Dice | 0.330415 | 0.352675 | 0.350694 |
| Google filtered Dice | 0.385184 | 0.403426 | 0.415136 |
| Filtered predicted-positive fraction | 0.003810 | 0.004266 | 0.004080 |
| Parameter count | 3,050,475 | 3,060,963 | 3,073,336 |
| Peak CUDA allocated | 1.19 GB | 1.55 GB | 1.83 GB |
| Total Run wall time | 1,580.2 s | 1,647.0 s | 1,704.6 s |

ABI-220 narrowly improved ABI-219's best filtered Dice by 0.0011 and raw Dice by 0.0016. It also improved precision by 0.0114 and Google filtered Dice by 0.0117. However, it slightly reduced recall by 0.0056, connectivity by 0.0099, and MIT filtered Dice by 0.0020. Against the ABI-218 matched single-frame control, ABI-220 still preserves a clear temporal-input benefit: +0.0232 filtered Dice, +0.0298 filtered recall, +0.0474 connectivity, +0.0203 MIT filtered Dice, and +0.0300 Google filtered Dice.

## Interpretation

ABI-220 confirms that the temporal-difference branch remains viable and resource-comparable, but its change-confidence gate is not a decisive improvement over ABI-219. The small primary-metric gain is useful because it keeps temporal modeling ahead of the matched single-frame control on the same temporal-eligible population. The source split is also informative: Google benefited from the gate, while MIT and connectivity did not. That tradeoff suggests the gate may be emphasizing cleaner center-frame confidence rather than consistently preserving moving thin-line evidence.

The Result still does not challenge ABI-202 or the mature single-frame frontier. ABI-202's capped best filtered Dice remains about 0.4276 and its whole-validation filtered Dice is 0.4312. This gap is not temporal-family elimination evidence because the temporal branch is young, finite, source-informative, and controlled against ABI-218; it does argue against spending more steps on small ABI-219-style gate mutations.

The best checkpoint occurred near the end of the exploratory budget, but the final epoch dropped materially and repeated the branch's precision/recall oscillation. I therefore would not request the 36-epoch late-improving budget for ABI-220 itself. The approved longer budget is better reserved for a close continuation whose 12-epoch trajectory shows clearer monotonic truncation or a stronger scientific tradeoff.

## Decision

Do not promote ABI-220 and do not request whole-validation diagnostics or late-improving budget from this capped Result alone.

Classify ABI-220 as a successful but only marginal temporal-family continuation. It preserves ABI-219's improvement over the temporal-eligible single-frame control, but does not meaningfully improve the temporal branch's recall/connectivity stability. Stop simple temporal-difference stem/gate tuning for now.

The best next in-contract hypothesis is to broaden within temporal modeling while retaining provider-owned temporal inputs: a compact ConvGRU or temporal-attention scout over per-frame bounded ABI+SZA+BTD features, still using `abi_16ch_plus_sza_temporal`, `temporal_eligible_center`, offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, batch size 2, and the exploratory 12-epoch budget. A five-frame temporal-difference scout is another option, but the next step should first test whether learned temporal state/attention improves on explicit difference features without candidate-owned temporal sampling or postprocessing.

No Capability Request, Evaluation Request, Campaign Report, or second Candidate Submission is required from this Result. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_134203_8bbb6f/candidate/PROPOSAL.md`
- `run_20260908_134203_8bbb6f/candidate/README.md`
- `run_20260908_134203_8bbb6f/resolved_manifest.yaml`
- `run_20260908_134203_8bbb6f/outputs/model_summary.json`
- `run_20260908_134203_8bbb6f/outputs/best_metrics.json`
- `run_20260908_134203_8bbb6f/outputs/final_metrics.json`
- `run_20260908_134203_8bbb6f/outputs/metrics.jsonl`
- `run_20260908_134203_8bbb6f/outputs/resource_profile.json`
- `run_20260908_134203_8bbb6f/outputs/validation_postprocessing/index.json`
- `run_20260908_134203_8bbb6f/outputs/prediction_samples/samples.json`
- `run_20260908_130608_80d612` for the ABI-219 temporal-difference comparison target
- `run_20260908_123030_05ad37` for the ABI-218 temporal-eligible single-frame matched control
- `run_20260908_114854_409a12` for the ABI-217 temporal Siamese/change context
- `run_20260904_043143_ee0005` for the ABI-202 current best whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
