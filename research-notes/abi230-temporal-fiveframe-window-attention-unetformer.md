# ABI-230 five-frame temporal window-attention U-NetFormer

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-230, Candidate `abi230_temporal_fiveframe_window_attention_unetformer_bce_dice_line_centerline_aux_v1`, Run `run_20260910_150603_7065ec`.

ABI-230 was a temporal/window-attention family-development continuation after ABI-229. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]` and `frame_selection_policy: temporal_eligible_center`. The hypothesis was that ABI-229's compact local-window U-NetFormer backbone would combine with ABI-226's five-frame temporal context to improve persistence/change evidence and thin-line connectivity. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-230 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-2, -1, 0, 1, 2]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,883,276, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.84 / 5.09 GB.
- Training wall time: 1,465.3 s; validation wall time: 1,102.3 s; total Run wall time: 2,569.2 s.

This is successful finite/resource evidence for the five-frame temporal window-attention formulation, but it is a negative scientific result for the proposed combination.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8.

| Metric | ABI-230 best epoch 8 |
| --- | ---: |
| Filtered Dice | 0.358285 |
| Raw Dice | 0.374020 |
| Filtered IoU | 0.218239 |
| Filtered precision | 0.399750 |
| Filtered recall | 0.324614 |
| Filtered contrail connectivity | 0.225921 |
| Filtered predicted-positive fraction | 0.004198 |
| Raw predicted-positive fraction | 0.004532 |
| MIT filtered Dice | 0.349067 |
| Google filtered Dice | 0.381970 |
| MIT filtered recall | 0.304173 |
| Google filtered recall | 0.385431 |
| Train loss | 0.851498 |
| Validation loss | 0.875844 |

The selected Result is finite and noncollapsed, but it underperforms both immediate comparison targets on filtered Dice, source-stratified Dice, precision, recall, and connectivity except for a negligible connectivity tie with ABI-226.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.211829 | 0.189434 | 0.240229 | 0.218330 | 0.198500 | 0.104859 | 0.006556 |
| 2 | 0.270170 | 0.346148 | 0.221542 | 0.262016 | 0.290084 | 0.212735 | 0.003309 |
| 3 | 0.258810 | 0.280930 | 0.239920 | 0.247463 | 0.283482 | 0.133533 | 0.004415 |
| 4 | 0.266725 | 0.416908 | 0.196088 | 0.249549 | 0.310078 | 0.246804 | 0.002431 |
| 5 | 0.310020 | 0.438947 | 0.239634 | 0.295309 | 0.347576 | 0.233721 | 0.002822 |
| 6 | 0.338012 | 0.338018 | 0.338006 | 0.329219 | 0.359682 | 0.162266 | 0.005169 |
| 7 | 0.297519 | 0.467572 | 0.218172 | 0.276633 | 0.351779 | 0.220546 | 0.002412 |
| 8 | 0.358285 | 0.399750 | 0.324614 | 0.349067 | 0.381970 | 0.225921 | 0.004198 |
| 9 | 0.350785 | 0.336100 | 0.366812 | 0.343663 | 0.368030 | 0.160717 | 0.005642 |
| 10 | 0.351091 | 0.399720 | 0.313011 | 0.335946 | 0.388749 | 0.192524 | 0.004048 |
| 11 | 0.338768 | 0.341992 | 0.335603 | 0.330450 | 0.358345 | 0.168327 | 0.005073 |
| 12 | 0.286268 | 0.265139 | 0.311056 | 0.283002 | 0.293006 | 0.128046 | 0.006065 |

The trajectory rises through epoch 8 and then fails to recover. The final epoch is a large aggregate regression from the selected checkpoint (-0.072017 filtered Dice) with much weaker precision, source metrics, and connectivity. This does not satisfy late-improving continuation criteria.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-222 attention 12ep | ABI-223 attention late36 | ABI-226 five-frame scout | ABI-229 window attention | ABI-230 five-frame window attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 36 | 10 | 8 | 8 |
| Filtered Dice | 0.345570 | 0.374329 | 0.419776 | 0.378604 | 0.376958 | 0.358285 |
| Raw Dice | 0.361077 | 0.392066 | 0.438487 | 0.394881 | 0.393997 | 0.374020 |
| Filtered precision | 0.407234 | 0.466148 | 0.483764 | 0.428061 | 0.434428 | 0.399750 |
| Filtered recall | 0.300125 | 0.312729 | 0.370738 | 0.339391 | 0.332917 | 0.324614 |
| Filtered connectivity | 0.231399 | 0.281396 | 0.412427 | 0.224851 | 0.313635 | 0.225921 |
| MIT filtered Dice | 0.330415 | 0.357658 | 0.398498 | 0.366586 | 0.364086 | 0.349067 |
| Google filtered Dice | 0.385184 | 0.416510 | 0.476764 | 0.409886 | 0.410445 | 0.381970 |
| Filtered predicted-positive fraction | 0.003810 | 0.003468 | 0.003962 | 0.004099 | 0.003962 | 0.004198 |
| Parameter count | 3,050,475 | 3,095,836 | 3,095,836 | 3,098,332 | 3,880,780 | 3,883,276 |

Relative to ABI-229, ABI-230 is -0.018673 filtered Dice, -0.019977 raw Dice, -0.034678 precision, -0.008303 recall, -0.087714 connectivity, -0.015019 MIT filtered Dice, and -0.028475 Google filtered Dice. Relative to ABI-226, it is -0.020318 filtered Dice, -0.020861 raw Dice, -0.028311 precision, -0.014777 recall, -0.017519 MIT filtered Dice, and -0.027916 Google filtered Dice; connectivity is only +0.001070, too small to support the hypothesized line-continuity benefit.

ABI-230 remains above the ABI-218 matched single-frame control on aggregate filtered Dice by +0.012715, but it is below the stronger same-budget temporal baselines ABI-222, ABI-226, and ABI-229. It is far below the ABI-223 late36 temporal frontier.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result, with whole-validation filtered Dice 0.4312. ABI-223 remains the capped temporal-family frontier, with filtered Dice 0.419776 at epoch 36 and strong MIT/Google source behavior. ABI-230 is neither a promotion candidate nor a whole-validation diagnostic candidate.

## Interpretation

Classify ABI-230 as a completed bad_research_result for the exact five-frame window-attention combination. The Run is resource-safe and nondegenerate, so no repair is indicated. The scientific failure is that adding the wider five-frame window to ABI-229's local-attention backbone diluted rather than improved the useful temporal evidence: the selected checkpoint is lower on overlap, source balance, precision/recall, and connectivity, and the final epochs show instability rather than late improvement.

This does not eliminate temporal modeling as a family: ABI-223 and several 12-epoch scouts remain positive relative to the matched single-frame control. It does weaken the hypothesis that simply pairing five-frame context with the current compact non-shifted window-attention U-NetFormer is beneficial. Further work should either return to the simpler three-frame/late-improving attention branch or broaden to a different underexplored family rather than make another small five-frame window-attention tweak.

## Decision

Do not promote ABI-230, do not request whole-validation diagnostics, do not create a repair Candidate, and do not request a `late_improving` continuation of this exact branch.

For the next research step, prefer broadening away from temporal window-attention toward another underexplored in-contract family, such as spectral/SZA-gated mixture-of-experts or a materially different long-range differentiable Hough/Radon-style voting module. If the campaign stays temporal, use ABI-223 as the stronger temporal anchor rather than ABI-230.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_150603_7065ec/candidate/PROPOSAL.md`
- `run_20260910_150603_7065ec/candidate/README.md`
- `run_20260910_150603_7065ec/candidate/manifest.yaml`
- `run_20260910_150603_7065ec/resolved_manifest.yaml`
- `run_20260910_150603_7065ec/outputs/model_summary.json`
- `run_20260910_150603_7065ec/outputs/best_metrics.json`
- `run_20260910_150603_7065ec/outputs/final_metrics.json`
- `run_20260910_150603_7065ec/outputs/metrics.jsonl`
- `run_20260910_150603_7065ec/outputs/resource_profile.json`
- `run_20260910_150603_7065ec/outputs/validation_postprocessing/index.json`
- `run_20260910_150603_7065ec/outputs/prediction_samples/samples.json`
- `run_20260910_141659_818da0` for ABI-229 three-frame window-attention comparison context
- `run_20260910_120441_916a03` for ABI-226 five-frame temporal comparison context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260908_150315_9aea3f` for ABI-222 same-budget temporal-attention context
- `run_20260908_123030_05ad37` for ABI-218 matched temporal-eligible single-frame control
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
