# ABI-223 temporal-attention fusion U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-223, Candidate `abi223_temporal_attention_fusion_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260908_154531_8c7e2b`.

ABI-223 was a close continuation of ABI-222. It kept the same compact temporal-attention fusion U-Net over provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, random mirroring, BCE-Dice loss, and trusted Line/Centerline auxiliary targets. The only intended change was the approved `late_improving` budget request from 12 to 36 epochs. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-223 completed the approved late-improving 36-epoch budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; `training.max_epochs` effective value 36.
- Parent Run cited by the budget request: `run_20260908_150315_9aea3f` (ABI-222).
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,095,836, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 2.76 / 3.02 GB.
- Training wall time: 2,688.8 s; validation wall time: 2,853.5 s; total Run wall time: 5,544.3 s.

This is successful finite/resource evidence for the temporal-attention family and confirms that the approved longer budget was useful for this branch.

## Best-validation metrics

The best checkpoint was epoch 36 by `val/filtered_dice`; therefore the final checkpoint is also the best checkpoint.

| Metric | ABI-223 best epoch 36 |
| --- | ---: |
| Filtered Dice | 0.419776 |
| Raw Dice | 0.438487 |
| Filtered IoU | 0.265643 |
| Filtered precision | 0.483764 |
| Filtered recall | 0.370738 |
| Filtered contrail connectivity | 0.412427 |
| Filtered predicted-positive fraction | 0.003962 |
| Raw predicted-positive fraction | 0.004284 |
| MIT filtered Dice | 0.398498 |
| Google filtered Dice | 0.476764 |
| MIT filtered recall | 0.342396 |
| Google filtered recall | 0.455062 |
| Train loss | 0.776993 |
| Validation loss | 0.844079 |

The Result is noncollapsed and source-informative. Filtered precision is high relative to the temporal family, filtered recall improved materially over ABI-222, and both Dataset Sources improved.

## Learning trajectory

ABI-223 preserved ABI-222's oscillatory precision/recall behavior but converted the longer budget into a substantially stronger final checkpoint. The best primary metric occurred at the final epoch rather than in the early exploratory window.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.206708 | 0.218023 | 0.278204 | 0.164444 | 0.202824 | 0.216564 | 0.162514 | 0.003057 |
| 6 | 0.361072 | 0.376337 | 0.433821 | 0.309239 | 0.347546 | 0.394756 | 0.242899 | 0.003686 |
| 12 | 0.374329 | 0.392066 | 0.466148 | 0.312729 | 0.357658 | 0.416510 | 0.281396 | 0.003468 |
| 18 | 0.383063 | 0.400958 | 0.410596 | 0.359003 | 0.363850 | 0.431296 | 0.228960 | 0.004523 |
| 24 | 0.381421 | 0.399892 | 0.471144 | 0.320407 | 0.356502 | 0.448590 | 0.287972 | 0.003517 |
| 30 | 0.400043 | 0.415941 | 0.409046 | 0.391427 | 0.385051 | 0.438136 | 0.229818 | 0.004947 |
| 36 | 0.419776 | 0.438487 | 0.483764 | 0.370738 | 0.398498 | 0.476764 | 0.412427 | 0.003962 |

The epoch-36 jump is not just a positive-fraction expansion: the filtered positive fraction remains modest while precision, recall, source Dice, and connectivity all improve together. Because the best checkpoint lands exactly at the 36-epoch ceiling, this branch still looks late-improving, but the current trusted budget has been exhausted.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-219 temporal difference | ABI-220 change confidence | ABI-221 ConvGRU state | ABI-222 attention 12ep | ABI-223 attention late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 8 | 11 | 10 | 12 | 36 |
| Filtered Dice | 0.345570 | 0.367589 | 0.368730 | 0.363826 | 0.374329 | 0.419776 |
| Raw Dice | 0.361077 | 0.383372 | 0.384987 | 0.380351 | 0.392066 | 0.438487 |
| Filtered precision | 0.407234 | 0.406513 | 0.417944 | 0.449905 | 0.466148 | 0.483764 |
| Filtered recall | 0.300125 | 0.335468 | 0.329885 | 0.305396 | 0.312729 | 0.370738 |
| Filtered connectivity | 0.231399 | 0.288750 | 0.278802 | 0.305528 | 0.281396 | 0.412427 |
| MIT filtered Dice | 0.330415 | 0.352675 | 0.350694 | 0.343643 | 0.357658 | 0.398498 |
| Google filtered Dice | 0.385184 | 0.403426 | 0.415136 | 0.415624 | 0.416510 | 0.476764 |
| Filtered predicted-positive fraction | 0.003810 | 0.004266 | 0.004080 | 0.003509 | 0.003468 | 0.003962 |
| Parameter count | 3,050,475 | 3,060,963 | 3,073,336 | 3,134,248 | 3,095,836 | 3,095,836 |

ABI-223 improves over ABI-222 by +0.045447 filtered Dice, +0.046421 raw Dice, +0.017616 precision, +0.058009 recall, +0.131031 connectivity, +0.040840 MIT filtered Dice, and +0.060254 Google filtered Dice. It improves over the ABI-218 matched single-frame temporal-eligible control by +0.074206 filtered Dice, +0.070613 filtered recall, +0.181028 connectivity, +0.068083 MIT filtered Dice, and +0.091580 Google filtered Dice. This is the clearest evidence so far that provider-owned temporal context helps beyond temporal-eligible population effects.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result in the campaign, with whole-validation filtered Dice 0.4312. On capped validation, ABI-202's best checkpoint had filtered Dice 0.427570, raw Dice 0.442746, precision 0.439467, recall 0.416301, connectivity 0.457773, MIT filtered Dice 0.411992, and Google filtered Dice 0.468151.

ABI-223 is close but not a promotion result by itself. Relative to ABI-202 capped best, ABI-223 is lower on primary filtered Dice (-0.007795), filtered recall (-0.045563), connectivity (-0.045346), and MIT filtered Dice (-0.013494), while higher on filtered precision (+0.044296), Google filtered Dice (+0.008613), and raw Dice is nearly tied (-0.004259). It should be treated as strong capped temporal-family feasibility evidence, not as a full-data or production claim.

## Interpretation

The approved late-improving budget was scientifically justified for ABI-222 and productive for ABI-223. The same temporal-attention architecture moved from a useful but immature 12-epoch scout to a competitive capped Result. The main gains were not confined to one Dataset Source or to precision-only calibration: filtered recall, source Dice, connectivity, and positive-fraction stability all improved.

The remaining weakness is that ABI-223 still lags ABI-202's capped primary metric, MIT Dice, recall, and continuity. This suggests the three-frame temporal-attention branch is promising but not yet sufficient to displace the mature single-frame spectral/spatial frontier. Since ABI-223 used the current maximum approved late-improving budget and selected the final epoch, further progress should come from a changed temporal architecture or input window rather than another unbounded continuation of the same three-frame candidate.

## Decision

Do not promote ABI-223 and do not claim a full-validation win. Classify it as a successful late-improving temporal-family Result and the current capped temporal-family frontier.

The best next in-contract step is to broaden within temporal modeling: a sequential five-frame scout using the allowlisted offsets `[-2, -1, 0, 1, 2]`, still through provider-owned `abi_16ch_plus_sza_temporal` and `temporal_eligible_center`, with a compact architecture that reuses ABI-223's finite temporal-attention/change front end while adding wider-window temporal evidence. The scout should remain resource-bounded and sequential because the five-frame input changes memory and wall-time behavior. A trusted Post-Run Evaluation can also be useful later for temporal-family failure buckets, but ABI-223's capped score alone is not a promotion decision.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_154531_8c7e2b/candidate/PROPOSAL.md`
- `run_20260908_154531_8c7e2b/candidate/README.md`
- `run_20260908_154531_8c7e2b/candidate/budget_request.yaml`
- `run_20260908_154531_8c7e2b/resolved_manifest.yaml`
- `run_20260908_154531_8c7e2b/outputs/model_summary.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/final_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/resource_profile.json`
- `run_20260908_154531_8c7e2b/outputs/validation_postprocessing/index.json`
- `run_20260908_154531_8c7e2b/outputs/prediction_samples/samples.json`
- `run_20260908_150315_9aea3f` for ABI-222 temporal-attention parent evidence
- `run_20260908_142018_0ea94f` for ABI-221 temporal ConvGRU comparison context
- `run_20260908_134203_8bbb6f` for ABI-220 temporal change-confidence comparison context
- `run_20260908_130608_80d612` for ABI-219 temporal-difference comparison context
- `run_20260908_123030_05ad37` for ABI-218 temporal-eligible single-frame matched control
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
