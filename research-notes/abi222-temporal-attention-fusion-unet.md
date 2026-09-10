# ABI-222 temporal-attention fusion U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-222, Candidate `abi222_temporal_attention_fusion_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_150315_9aea3f`.

ABI-222 was the temporal-family scout/continuation proposed after ABI-221. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. It replaced ABI-221's recurrent ConvGRU state with a compact per-pixel temporal-attention fusion block over bounded per-frame ABI+SZA+BTD features plus signed/absolute change embeddings before a single compact U-Net/ASPP decoder. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-222 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,095,836, below the 25,000,000-parameter ceiling.
- Batch size: 2, no Resource Failure retry.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 2.63 / 2.88 GB.
- Training wall time: 899.2 s; validation wall time: 941.0 s; total Run wall time: 1,841.9 s.

This is successful finite/resource evidence for a compact temporal-attention architecture. It is heavier than ABI-219/220 but cheaper than ABI-221's ConvGRU state while producing the strongest capped temporal-family primary metric so far.

## Best-validation metrics

The best checkpoint was epoch 12 by `val/filtered_dice`; therefore the best-validation and final metrics are the same checkpoint.

| Metric | ABI-222 best epoch 12 |
| --- | ---: |
| Filtered Dice | 0.374329 |
| Raw Dice | 0.392066 |
| Filtered IoU | 0.230261 |
| Filtered precision | 0.466148 |
| Filtered recall | 0.312729 |
| Filtered contrail connectivity | 0.281396 |
| Filtered predicted-positive fraction | 0.003468 |
| Raw predicted-positive fraction | 0.003742 |
| MIT filtered Dice | 0.357658 |
| Google filtered Dice | 0.416510 |
| MIT filtered recall | 0.286143 |
| Google filtered recall | 0.391829 |
| Train loss | 0.798724 |
| Validation loss | 0.858292 |

## Learning trajectory

ABI-222 learned rapidly through epoch 6, oscillated between recall-oriented and precision-oriented checkpoints, and reached its best filtered Dice at the final exploratory epoch.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.201726 | 0.211910 | 0.284766 | 0.156182 | 0.197548 | 0.211616 | 0.195738 | 0.002835 |
| 2 | 0.262099 | 0.275765 | 0.388417 | 0.197779 | 0.250353 | 0.291752 | 0.323712 | 0.002632 |
| 3 | 0.307331 | 0.322174 | 0.386836 | 0.254936 | 0.297768 | 0.330391 | 0.274822 | 0.003407 |
| 4 | 0.298846 | 0.311816 | 0.339879 | 0.266653 | 0.287246 | 0.326310 | 0.210820 | 0.004056 |
| 5 | 0.316469 | 0.328946 | 0.318217 | 0.314741 | 0.304213 | 0.345255 | 0.157616 | 0.005113 |
| 6 | 0.354556 | 0.368931 | 0.305529 | 0.422326 | 0.355963 | 0.351356 | 0.198937 | 0.007146 |
| 7 | 0.263420 | 0.278230 | 0.577113 | 0.170658 | 0.237856 | 0.332674 | 0.372698 | 0.001529 |
| 8 | 0.367017 | 0.384391 | 0.461388 | 0.304695 | 0.346440 | 0.419285 | 0.267648 | 0.003414 |
| 9 | 0.373965 | 0.386864 | 0.339805 | 0.415761 | 0.365944 | 0.392532 | 0.213729 | 0.006325 |
| 10 | 0.347445 | 0.364428 | 0.462408 | 0.278264 | 0.321496 | 0.411920 | 0.267657 | 0.003111 |
| 11 | 0.321702 | 0.332907 | 0.281538 | 0.375231 | 0.309367 | 0.350742 | 0.198146 | 0.006890 |
| 12 | 0.374329 | 0.392066 | 0.466148 | 0.312729 | 0.357658 | 0.416510 | 0.281396 | 0.003468 |

The trajectory is finite, source-informative, and noncollapsed. Predicted-positive fractions remained small but nonzero, and both Dataset Sources reached their best or near-best filtered Dice late in training. The final checkpoint is not simply an all-precision collapse: recall remains above the ABI-218 matched single-frame control, and both MIT and Google Dice are above prior temporal-family bests. However, the temporal branch still oscillates between high-recall/low-precision and high-precision/lower-recall regimes.

## Matched temporal-family comparison

| Metric | ABI-218 single-frame control best | ABI-219 temporal-difference best | ABI-220 change-confidence best | ABI-221 ConvGRU state best | ABI-222 attention fusion best |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 8 | 11 | 10 | 12 |
| Filtered Dice | 0.345570 | 0.367589 | 0.368730 | 0.363826 | 0.374329 |
| Raw Dice | 0.361077 | 0.383372 | 0.384987 | 0.380351 | 0.392066 |
| Filtered precision | 0.407234 | 0.406513 | 0.417944 | 0.449905 | 0.466148 |
| Filtered recall | 0.300125 | 0.335468 | 0.329885 | 0.305396 | 0.312729 |
| Filtered contrail connectivity | 0.231399 | 0.288750 | 0.278802 | 0.305528 | 0.281396 |
| MIT filtered Dice | 0.330415 | 0.352675 | 0.350694 | 0.343643 | 0.357658 |
| Google filtered Dice | 0.385184 | 0.403426 | 0.415136 | 0.415624 | 0.416510 |
| Filtered predicted-positive fraction | 0.003810 | 0.004266 | 0.004080 | 0.003509 | 0.003468 |
| Parameter count | 3,050,475 | 3,060,963 | 3,073,336 | 3,134,248 | 3,095,836 |
| Peak CUDA allocated | 1.19 GB | 1.55 GB | 1.83 GB | 3.32 GB | 2.63 GB |
| Total Run wall time | 1,580.2 s | 1,647.0 s | 1,704.6 s | 2,039.5 s | 1,841.9 s |

ABI-222 beats the ABI-218 temporal-eligible single-frame control by +0.0288 filtered Dice, +0.0126 filtered recall, +0.0500 connectivity, +0.0272 MIT filtered Dice, and +0.0313 Google filtered Dice. This preserves the controlled evidence that provider-owned temporal context is helping beyond temporal-eligible population effects.

Against the prior temporal-difference frontier, ABI-222 improves over ABI-220 by +0.0056 filtered Dice, +0.0482 precision, +0.0026 connectivity, +0.0070 MIT Dice, and +0.0014 Google Dice, while giving up -0.0172 recall. It improves over ABI-219 by +0.0067 filtered Dice, +0.0596 precision, +0.0050 MIT Dice, and +0.0131 Google Dice, while giving up -0.0227 recall and -0.0074 connectivity. Against ABI-221, ABI-222 improves filtered Dice, raw Dice, precision, recall, MIT Dice, and Google Dice while using fewer parameters, less memory, and less wall time; ABI-221 retains the higher best-checkpoint connectivity.

## Interpretation

ABI-222 is the strongest capped temporal-family Result so far and satisfies the proposal's primary success criterion by exceeding ABI-220 by about 0.0056 filtered Dice while remaining clearly above the ABI-218 matched single-frame control. The temporal-attention mechanism appears to provide a better precision-calibrated temporal fusion than fixed difference gates or ConvGRU state, especially on the final checkpoint where both source-stratified Dice and validation loss are strong.

The Result still does not challenge the mature single-frame ABI-202 frontier: ABI-202's capped best filtered Dice is about 0.4276 and its whole-validation filtered Dice is 0.4312. This gap is not temporal-family elimination evidence because ABI-222 is finite, source-informative, controlled against ABI-218, and still improving or ambiguous at the exploratory ceiling.

The late trajectory matters. ABI-222 reaches its best checkpoint at epoch 12, with the lowest observed train loss and validation loss, after epoch-10/11 oscillation. That pattern is more compatible with truncation or unsettled optimization than with a clear plateau. Unlike ABI-219/220/221, the final exploratory epoch is also the primary-metric best, making ABI-222 a reasonable close-continuation candidate for the approved late-improving budget.

## Decision

Do not promote ABI-222 and do not request whole-validation diagnostics from this capped Result alone.

Classify ABI-222 as a successful temporal-attention scout and the current temporal-family capped frontier. The best next in-contract step is a close continuation of ABI-222 under the approved `late_improving` budget: preserve the architecture, provider-owned `abi_16ch_plus_sza_temporal` input, `temporal_eligible_center` frame policy, offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, batch size 2, and constant learning rate, while adding a candidate-local `budget_request.yaml` citing `run_20260908_150315_9aea3f` as parent evidence. If that longer run plateaus or loses the matched-control margin, then broaden to a five-frame temporal-difference/attention scout using the allowlisted `[-2, -1, 0, 1, 2]` window rather than continuing small three-frame attention mutations.

No Capability Request, Evaluation Request, Campaign Report, or Candidate Submission is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_150315_9aea3f/candidate/PROPOSAL.md`
- `run_20260908_150315_9aea3f/candidate/README.md`
- `run_20260908_150315_9aea3f/resolved_manifest.yaml`
- `run_20260908_150315_9aea3f/outputs/model_summary.json`
- `run_20260908_150315_9aea3f/outputs/best_metrics.json`
- `run_20260908_150315_9aea3f/outputs/final_metrics.json`
- `run_20260908_150315_9aea3f/outputs/metrics.jsonl`
- `run_20260908_150315_9aea3f/outputs/resource_profile.json`
- `run_20260908_150315_9aea3f/outputs/validation_postprocessing/index.json`
- `run_20260908_150315_9aea3f/outputs/prediction_samples/samples.json`
- `run_20260908_142018_0ea94f` for the ABI-221 temporal ConvGRU comparison target
- `run_20260908_134203_8bbb6f` for the ABI-220 temporal change-confidence comparison target
- `run_20260908_130608_80d612` for the ABI-219 temporal-difference comparison target
- `run_20260908_123030_05ad37` for the ABI-218 temporal-eligible single-frame matched control
- `run_20260904_043143_ee0005` for the ABI-202 current best whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
