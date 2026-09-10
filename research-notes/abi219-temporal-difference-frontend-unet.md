# ABI-219 temporal-difference front-end U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-219, Candidate `abi219_temporal_difference_frontend_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_130608_80d612`.

ABI-219 was the temporal-family continuation proposed after ABI-217 and ABI-218. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`, but replaced ABI-217's three full shared encoders and residual fusers with an explicit front-end stack of center-frame features, center-minus-neighbor evidence, next-minus-previous evidence, and absolute center-neighbor change before a single compact U-Net/ASPP decoder. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-219 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,060,963, below the 25,000,000-parameter ceiling.
- Batch size: 2, no Resource Failure retry.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 1.55 / 1.82 GB.
- Training wall time: 733.5 s; validation wall time: 912.0 s; total Run wall time: 1,647.0 s.

This is successful finite/resource evidence for a compact explicit temporal-difference front end. Its resource profile is much closer to ABI-218 than ABI-217 while retaining real three-frame temporal input.

## Best-validation metrics

The best checkpoint was epoch 8 by `val/filtered_dice`.

| Metric | ABI-219 best epoch 8 |
| --- | ---: |
| Filtered Dice | 0.367589 |
| Raw Dice | 0.383372 |
| Filtered IoU | 0.225182 |
| Filtered precision | 0.406513 |
| Filtered recall | 0.335468 |
| Filtered contrail connectivity | 0.288750 |
| Filtered predicted-positive fraction | 0.004266 |
| Raw predicted-positive fraction | 0.004604 |
| MIT filtered Dice | 0.352675 |
| Google filtered Dice | 0.403426 |
| MIT filtered recall | 0.303662 |
| Google filtered recall | 0.430097 |
| Train loss | 0.825383 |
| Validation loss | 0.870809 |

Final epoch 12 did not exceed the best checkpoint: filtered Dice 0.344659, raw Dice 0.361259, filtered precision 0.490400, filtered recall 0.265696, MIT filtered Dice 0.320317, Google filtered Dice 0.407241, connectivity 0.371735, and filtered predicted-positive fraction 0.002801. The final-epoch shift was toward fewer predicted positives, higher precision, and lower recall.

## Learning trajectory

ABI-219 learned rapidly through epoch 8, then oscillated between recall-oriented and precision-oriented checkpoints rather than monotonically improving.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.188251 | 0.195778 | 0.185716 | 0.190857 | 0.194021 | 0.177451 | 0.115310 | 0.005313 |
| 2 | 0.228871 | 0.237410 | 0.216130 | 0.243210 | 0.228453 | 0.229736 | 0.145785 | 0.005817 |
| 3 | 0.285586 | 0.296624 | 0.280237 | 0.291142 | 0.281350 | 0.294620 | 0.181303 | 0.005371 |
| 4 | 0.270070 | 0.282572 | 0.357754 | 0.216906 | 0.249573 | 0.319183 | 0.237517 | 0.003134 |
| 5 | 0.300208 | 0.311232 | 0.291098 | 0.309907 | 0.291073 | 0.319619 | 0.151602 | 0.005504 |
| 6 | 0.342414 | 0.355688 | 0.327575 | 0.358661 | 0.334432 | 0.361484 | 0.266833 | 0.005660 |
| 7 | 0.237280 | 0.250783 | 0.495794 | 0.155960 | 0.213580 | 0.300474 | 0.308884 | 0.001626 |
| 8 | 0.367589 | 0.383372 | 0.406513 | 0.335468 | 0.352675 | 0.403426 | 0.288750 | 0.004266 |
| 9 | 0.352125 | 0.366086 | 0.351651 | 0.352600 | 0.340889 | 0.378664 | 0.226408 | 0.005184 |
| 10 | 0.336476 | 0.353880 | 0.509873 | 0.251086 | 0.309597 | 0.404815 | 0.350250 | 0.002546 |
| 11 | 0.364243 | 0.381391 | 0.451206 | 0.305385 | 0.350253 | 0.401209 | 0.352653 | 0.003499 |
| 12 | 0.344659 | 0.361259 | 0.490400 | 0.265696 | 0.320317 | 0.407241 | 0.371735 | 0.002801 |

The trajectory is source-informative and noncollapsed. Both Dataset Sources improved substantially from epoch 1, and predicted-positive fractions stayed small but nonzero. Epochs 10-12 show stronger connectivity/precision at lower recall, so the branch may be sensitive to logit calibration or temporal-change gate strength, but this capped Run does not justify candidate-owned thresholding or postprocessing.

## Matched temporal-family comparison

| Metric | ABI-217 temporal Siamese best | ABI-218 single-frame control best | ABI-219 temporal-difference best |
| --- | ---: | ---: | ---: |
| Best epoch | 11 | 11 | 8 |
| Filtered Dice | 0.349086 | 0.345570 | 0.367589 |
| Raw Dice | 0.363412 | 0.361077 | 0.383372 |
| Filtered precision | 0.387277 | 0.407234 | 0.406513 |
| Filtered recall | 0.317751 | 0.300125 | 0.335468 |
| Filtered contrail connectivity | 0.265915 | 0.231399 | 0.288750 |
| MIT filtered Dice | 0.333794 | 0.330415 | 0.352675 |
| Google filtered Dice | 0.387537 | 0.385184 | 0.403426 |
| Filtered predicted-positive fraction | 0.004241 | 0.003810 | 0.004266 |
| Parameter count | 4,326,675 | 3,050,475 | 3,060,963 |
| Peak CUDA allocated | 2.82 GB | 1.19 GB | 1.55 GB |
| Total Run wall time | 2,013.8 s | 1,580.2 s | 1,647.0 s |

ABI-219 beat ABI-218 by 0.0220 filtered Dice, 0.0353 filtered recall, 0.0574 connectivity, 0.0223 MIT filtered Dice, and 0.0182 Google filtered Dice. It also beat ABI-217 by 0.0185 filtered Dice, 0.0177 filtered recall, and 0.0228 connectivity while using about 1.27M fewer parameters and 367 s less total wall time. This satisfies the proposal's scientific success criterion: explicit temporal-difference evidence produced a clearer improvement over the matched single-frame control than ABI-217's marginal temporal advantage.

## Interpretation

ABI-219 is the strongest early temporal-family Result so far and gives the first clear signal that provider-owned neighboring frames can help when converted into bounded change features before the decoder. The gain is not merely a temporal-eligible subset effect because ABI-218 used the same temporal-eligible population and nearly identical single-frame capacity. It is also not simply a scale effect because ABI-219 is much smaller and cheaper than ABI-217.

The Result still does not challenge ABI-202 or the mature single-frame frontier; ABI-202's capped best filtered Dice remains about 0.4276 and its whole-validation filtered Dice is 0.4312. However, ABI-219 is a finite, noncollapsed, source-balanced, materially different temporal mechanism with a controlled matched-control gain. Low score relative to ABI-202 is therefore not elimination evidence for temporal modeling. The temporal branch merits further bounded development.

The best checkpoint at epoch 8, followed by precision/recall oscillation, argues against immediately requesting the late-improving 36-epoch budget. The branch did not peak at the final exploratory epoch, and the final metric drop appears more like calibration/gate oscillation than truncation. A close continuation should first stabilize how temporal change contributes to recall and connectivity under the 12-epoch budget.

## Decision

Do not promote ABI-219 and do not request whole-validation diagnostics or late-improving budget from this capped Result alone.

Continue temporal-family development with a controlled close continuation. The best next in-contract hypothesis is to preserve ABI-219's explicit temporal-difference front end and compact single decoder, then add a lightweight learned temporal-change confidence/attention gate or residual calibration path that can retain epoch-8 recall while preserving the higher epoch-10/12 connectivity and precision. Keep the same provider-owned `abi_16ch_plus_sza_temporal` input, `temporal_eligible_center` policy, `[-1, 0, 1]` offsets, BCE-Dice loss, Line and Centerline auxiliaries, source-balanced sampling, random mirroring, and exploratory budget. If that controlled stabilization does not improve beyond ABI-219, broaden within temporal modeling to a compact ConvGRU/temporal-attention scout rather than continuing simple difference-stem tuning indefinitely.

No Capability Request, Evaluation Request, Campaign Report, or second Candidate Submission is required from this Result. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_130608_80d612/candidate/PROPOSAL.md`
- `run_20260908_130608_80d612/candidate/README.md`
- `run_20260908_130608_80d612/resolved_manifest.yaml`
- `run_20260908_130608_80d612/outputs/model_summary.json`
- `run_20260908_130608_80d612/outputs/best_metrics.json`
- `run_20260908_130608_80d612/outputs/final_metrics.json`
- `run_20260908_130608_80d612/outputs/metrics.jsonl`
- `run_20260908_130608_80d612/outputs/resource_profile.json`
- `run_20260908_130608_80d612/outputs/validation_postprocessing/index.json`
- `run_20260908_130608_80d612/outputs/prediction_samples/samples.json`
- `run_20260908_114854_409a12` for the ABI-217 temporal Siamese/change comparison target
- `run_20260908_123030_05ad37` for the ABI-218 temporal-eligible single-frame matched control
- `run_20260904_043143_ee0005` for the ABI-202 current best whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
