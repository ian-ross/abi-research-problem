# ABI-221 temporal ConvGRU state U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-221, Candidate `abi221_temporal_convgru_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_142018_0ea94f`.

ABI-221 was the temporal-family scout/continuation proposed after ABI-220. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. It replaced ABI-219/220's hand-combined temporal-difference gates with a compact bidirectional ConvGRU state over bounded per-frame ABI+SZA+BTD features before a single compact U-Net/ASPP decoder. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-221 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,134,248, below the 25,000,000-parameter ceiling.
- Batch size: 2, no Resource Failure retry.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 3.32 / 3.57 GB.
- Training wall time: 1,018.0 s; validation wall time: 1,019.6 s; total Run wall time: 2,039.5 s.

This is successful finite/resource evidence for a compact recurrent temporal-state design, but it is noticeably heavier than ABI-219/220: about +61k parameters over ABI-220, +1.49 GB peak CUDA allocation, and +335 s total wall time.

## Best-validation metrics

The best checkpoint was epoch 10 by `val/filtered_dice`.

| Metric | ABI-221 best epoch 10 |
| --- | ---: |
| Filtered Dice | 0.363826 |
| Raw Dice | 0.380351 |
| Filtered IoU | 0.222364 |
| Filtered precision | 0.449905 |
| Filtered recall | 0.305396 |
| Filtered contrail connectivity | 0.305528 |
| Filtered predicted-positive fraction | 0.003509 |
| Raw predicted-positive fraction | 0.003788 |
| MIT filtered Dice | 0.343643 |
| Google filtered Dice | 0.415624 |
| MIT filtered recall | 0.277339 |
| Google filtered recall | 0.388870 |
| Train loss | 0.823434 |
| Validation loss | 0.867195 |

Final epoch 12 did not exceed the best checkpoint: filtered Dice 0.358820, raw Dice 0.374237, filtered precision 0.399441, filtered recall 0.325699, MIT filtered Dice 0.343388, Google filtered Dice 0.396790, connectivity 0.203534, and filtered predicted-positive fraction 0.004215. The final checkpoint recovered some recall but lost precision, Google Dice, and especially connectivity.

## Learning trajectory

ABI-221 learned steadily through epoch 10, then dropped sharply at epoch 11 and partially recovered at epoch 12.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.156933 | 0.165494 | 0.243038 | 0.115879 | 0.152120 | 0.168516 | 0.176985 | 0.002465 |
| 2 | 0.220085 | 0.230495 | 0.309093 | 0.170878 | 0.207327 | 0.250049 | 0.173386 | 0.002858 |
| 3 | 0.252983 | 0.260381 | 0.209749 | 0.318667 | 0.253531 | 0.251907 | 0.118732 | 0.007854 |
| 4 | 0.280624 | 0.292365 | 0.331879 | 0.243082 | 0.263949 | 0.318938 | 0.189037 | 0.003786 |
| 5 | 0.303158 | 0.315093 | 0.305840 | 0.300522 | 0.302600 | 0.304419 | 0.181120 | 0.005080 |
| 6 | 0.324006 | 0.336202 | 0.320861 | 0.327213 | 0.315051 | 0.344994 | 0.194287 | 0.005272 |
| 7 | 0.345640 | 0.362543 | 0.468701 | 0.273761 | 0.323735 | 0.402238 | 0.357244 | 0.003019 |
| 8 | 0.351230 | 0.365990 | 0.404210 | 0.310529 | 0.335808 | 0.391531 | 0.296395 | 0.003971 |
| 9 | 0.362942 | 0.376360 | 0.344422 | 0.383567 | 0.349332 | 0.396493 | 0.266312 | 0.005757 |
| 10 | 0.363826 | 0.380351 | 0.449905 | 0.305396 | 0.343643 | 0.415624 | 0.305528 | 0.003509 |
| 11 | 0.309069 | 0.324772 | 0.451380 | 0.234984 | 0.283337 | 0.375897 | 0.276971 | 0.002691 |
| 12 | 0.358820 | 0.374237 | 0.399441 | 0.325699 | 0.343388 | 0.396790 | 0.203534 | 0.004215 |

The trajectory is finite, source-informative, and noncollapsed. Both Dataset Sources improved substantially from epoch 1, and predicted-positive fractions remained small but nonzero. However, the recurrent state did not stabilize the temporal branch's precision/recall oscillation. Epoch 9 reached the strongest recall but with lower precision; epoch 10 produced the best primary metric through a precision/Google-Dice shift; epoch 12 restored some recall but lost connectivity.

## Matched temporal-family comparison

| Metric | ABI-218 single-frame control best | ABI-219 temporal-difference best | ABI-220 change-confidence best | ABI-221 ConvGRU state best |
| --- | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 8 | 11 | 10 |
| Filtered Dice | 0.345570 | 0.367589 | 0.368730 | 0.363826 |
| Raw Dice | 0.361077 | 0.383372 | 0.384987 | 0.380351 |
| Filtered precision | 0.407234 | 0.406513 | 0.417944 | 0.449905 |
| Filtered recall | 0.300125 | 0.335468 | 0.329885 | 0.305396 |
| Filtered contrail connectivity | 0.231399 | 0.288750 | 0.278802 | 0.305528 |
| MIT filtered Dice | 0.330415 | 0.352675 | 0.350694 | 0.343643 |
| Google filtered Dice | 0.385184 | 0.403426 | 0.415136 | 0.415624 |
| Filtered predicted-positive fraction | 0.003810 | 0.004266 | 0.004080 | 0.003509 |
| Parameter count | 3,050,475 | 3,060,963 | 3,073,336 | 3,134,248 |
| Peak CUDA allocated | 1.19 GB | 1.55 GB | 1.83 GB | 3.32 GB |
| Total Run wall time | 1,580.2 s | 1,647.0 s | 1,704.6 s | 2,039.5 s |

ABI-221 still beats the ABI-218 temporal-eligible single-frame control by +0.0183 filtered Dice, +0.0053 filtered recall, +0.0741 connectivity, +0.0132 MIT filtered Dice, and +0.0304 Google filtered Dice. That preserves evidence that provider-owned temporal context can help over the matched center-frame population.

Against the stronger temporal-difference branch, ABI-221 underperforms ABI-219 by -0.0038 filtered Dice and -0.0301 recall, while improving precision by +0.0434, connectivity by +0.0168, and Google filtered Dice by +0.0122. Compared with ABI-220, it underperforms by -0.0049 filtered Dice and -0.0245 recall, while improving precision by +0.0320, connectivity by +0.0267, and Google filtered Dice by +0.0005. The recurrent state therefore produced a higher-precision, somewhat more Google-favorable checkpoint, not a better overall temporal-family frontier.

## Interpretation

ABI-221 confirms that a compact recurrent temporal-state model is feasible under the current provider-owned temporal input contract, but it does not improve the temporal branch's primary capped Result. The best checkpoint is source-informative and nondegenerate, yet its lower recall suggests the ConvGRU fusion may be suppressing ambiguous thin-line positives rather than preserving moving contrail evidence. Its higher connectivity at the best checkpoint is useful secondary evidence, but the epoch-12 connectivity collapse means this exact recurrent design does not yet stabilize line continuity.

The Result remains far below the mature ABI-202 frontier: ABI-202's capped best filtered Dice is about 0.4276 and its whole-validation filtered Dice is 0.4312. This gap is not global temporal-family elimination evidence because ABI-219/220/221 all remain finite, matched-control-positive, and source-informative. It does argue against further close tuning of this exact three-frame ConvGRU state design unless a later diagnostic identifies a specific repairable failure mode.

The best checkpoint occurred at epoch 10 rather than the final epoch, final filtered Dice was lower, and the late trajectory oscillated rather than monotonically improving. ABI-221 therefore does not justify the approved 36-epoch `late_improving` budget.

## Decision

Do not promote ABI-221 and do not request whole-validation diagnostics or late-improving budget from this capped Result alone.

Classify ABI-221 as a successful but negative/mixed recurrent temporal-state scout. It preserves a useful margin over the ABI-218 matched single-frame control, but it does not beat ABI-219/220 on the primary metric and pays a meaningful memory/time cost. Hard-stop this exact ConvGRU state branch for now; do not eliminate temporal modeling globally.

The best next in-contract direction is to broaden the temporal branch rather than continue small three-frame gate/recurrent mutations. Two reasonable next hypotheses are: (1) a lightweight per-pixel or windowed temporal-attention scout over three provider-owned frames that can reweight center/neighbor features without recurrent state overhead, or (2) a five-frame temporal-difference scout using the allowlisted `[-2, -1, 0, 1, 2]` window to test whether wider persistence/advection evidence is more useful than a more complex three-frame fusion block. Either should remain sequential, exploratory, provider-owned, and architecture-only.

No Capability Request, Evaluation Request, Campaign Report, or second Candidate Submission is required from this Result. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_142018_0ea94f/candidate/PROPOSAL.md`
- `run_20260908_142018_0ea94f/candidate/README.md`
- `run_20260908_142018_0ea94f/resolved_manifest.yaml`
- `run_20260908_142018_0ea94f/outputs/model_summary.json`
- `run_20260908_142018_0ea94f/outputs/best_metrics.json`
- `run_20260908_142018_0ea94f/outputs/final_metrics.json`
- `run_20260908_142018_0ea94f/outputs/metrics.jsonl`
- `run_20260908_142018_0ea94f/outputs/resource_profile.json`
- `run_20260908_142018_0ea94f/outputs/validation_postprocessing/index.json`
- `run_20260908_142018_0ea94f/outputs/prediction_samples/samples.json`
- `run_20260908_134203_8bbb6f` for the ABI-220 temporal change-confidence comparison target
- `run_20260908_130608_80d612` for the ABI-219 temporal-difference comparison target
- `run_20260908_123030_05ad37` for the ABI-218 temporal-eligible single-frame matched control
- `run_20260904_043143_ee0005` for the ABI-202 current best whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
