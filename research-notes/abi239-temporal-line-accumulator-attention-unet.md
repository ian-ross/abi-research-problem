# ABI-239 temporal line-accumulator attention U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-239, Candidate `abi239_temporal_line_accumulator_attention_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_023156_f7eb6b`.

ABI-239 was a sequential temporal/Radon-hybrid family-development continuation of the ABI-223 temporal-attention branch. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. The intended architecture change was a low-resolution differentiable multi-orientation line accumulator inserted after temporal attention fusion and before encoder downsampling. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-239 completed the default exploratory 12-epoch budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; effective maximum epochs 12.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,126,436, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.19 / 3.47 GiB.
- Training wall time: 1,046.9 s; validation wall time: 983.1 s; total Run wall time: 2,031.6 s.

This is successful finite/resource evidence for the temporal line-accumulator branch. Resource use was close to ABI-238 and well inside the trusted ceiling.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final exploratory epoch 12.

| Metric | ABI-239 best/final epoch 12 |
| --- | ---: |
| Filtered Dice | 0.366274 |
| Raw Dice | 0.383403 |
| Filtered IoU | 0.224196 |
| Filtered precision | 0.457890 |
| Filtered recall | 0.305207 |
| Filtered contrail connectivity | 0.246821 |
| Filtered predicted-positive fraction | 0.003446 |
| Raw predicted-positive fraction | 0.003712 |
| MIT filtered Dice | 0.346223 |
| Google filtered Dice | 0.415466 |
| MIT filtered recall | 0.273845 |
| Google filtered recall | 0.398517 |
| Train loss | 0.802452 |
| Validation loss | 0.858316 |

The checkpoint is finite, noncollapsed, and source-informative. Google Dice is stronger than MIT Dice, but both sources have nontrivial filtered Dice and recall. Predictions are compact rather than all-positive, with filtered predicted-positive fraction 0.003446.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.216706 | 0.225882 | 0.238741 | 0.198395 | 0.216344 | 0.217497 | 0.160344 | 0.004296 |
| 2 | 0.232415 | 0.242463 | 0.264298 | 0.207397 | 0.226873 | 0.244159 | 0.134470 | 0.004057 |
| 3 | 0.277921 | 0.292228 | 0.407842 | 0.210776 | 0.258073 | 0.325425 | 0.257212 | 0.002672 |
| 4 | 0.288990 | 0.300388 | 0.290108 | 0.287880 | 0.281919 | 0.305046 | 0.135095 | 0.005130 |
| 5 | 0.218131 | 0.227343 | 0.243713 | 0.197410 | 0.211728 | 0.230991 | 0.095774 | 0.004187 |
| 6 | 0.296982 | 0.305212 | 0.236166 | 0.399984 | 0.317594 | 0.256776 | 0.141835 | 0.008755 |
| 7 | 0.269290 | 0.282969 | 0.425123 | 0.197057 | 0.250523 | 0.316658 | 0.173985 | 0.002396 |
| 8 | 0.364561 | 0.377594 | 0.349095 | 0.381462 | 0.354530 | 0.389165 | 0.195939 | 0.005649 |
| 9 | 0.363674 | 0.377677 | 0.354553 | 0.373276 | 0.354945 | 0.384500 | 0.212227 | 0.005443 |
| 10 | 0.360991 | 0.376414 | 0.416123 | 0.318759 | 0.347803 | 0.392965 | 0.177547 | 0.003960 |
| 11 | 0.353444 | 0.371517 | 0.507745 | 0.271068 | 0.333103 | 0.408138 | 0.349308 | 0.002760 |
| 12 | 0.366274 | 0.383403 | 0.457890 | 0.305207 | 0.346223 | 0.415466 | 0.246821 | 0.003446 |

The trajectory is noisy but not plateaued. Filtered Dice jumps from about 0.30 at epoch 6 to a higher band after epoch 8, then selects the final epoch. Training loss and validation loss also finish at their lowest reported values. Connectivity is unstable: epoch 11 has the best connectivity, but this coincides with lower recall and a more compact predicted-positive fraction.

## Comparison context

| Metric | ABI-223 epoch 12 | ABI-238 epoch 12 | ABI-239 epoch 12 | ABI-223 late36 best | ABI-238 late36 best | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best/selected epoch | 12 | 12 | 12 | 36 | 29 | 34 |
| Filtered Dice | 0.359161 | 0.357511 | 0.366274 | 0.419776 | 0.420235 | 0.427570 |
| Raw Dice | 0.376293 | 0.375189 | 0.383403 | 0.438487 | 0.438718 | 0.442746 |
| Filtered precision | 0.465419 | 0.470941 | 0.457890 | 0.483764 | 0.488730 | 0.439467 |
| Filtered recall | 0.292404 | 0.288115 | 0.305207 | 0.370738 | 0.368578 | 0.416301 |
| Filtered connectivity | 0.275357 | 0.242423 | 0.246821 | 0.412427 | 0.352239 | 0.457773 |
| MIT filtered Dice | 0.341557 | 0.337837 | 0.346223 | 0.398498 | 0.405383 | 0.411992 |
| Google filtered Dice | 0.404893 | 0.407224 | 0.415466 | 0.476764 | 0.460838 | 0.468151 |
| Filtered predicted-positive fraction | 0.003248 | 0.003163 | 0.003446 | 0.003962 | 0.003899 | 0.003433 |

At matched exploratory epoch 12, ABI-239 improves filtered Dice over ABI-223 by +0.007113 and over ABI-238 by +0.008763. It also improves recall over ABI-223 by +0.012803 and over ABI-238 by +0.017092, while preserving compact predictions and improving both MIT and Google filtered Dice. The tradeoff is precision and connectivity: precision is slightly lower than both temporal comparators at epoch 12, and connectivity is below ABI-223 by -0.028536 while only marginally above ABI-238 by +0.004398.

Against the mature late-budget frontier, ABI-239 is not yet competitive: it trails ABI-223 late36 by -0.053502 filtered Dice and -0.165606 connectivity, and trails ABI-202 by -0.061296 filtered Dice, -0.111094 recall, and -0.210952 connectivity. This gap is expected for an exploratory 12-epoch scout but prevents promotion or whole-validation diagnostic priority from this Result alone.

## Interpretation

Classify ABI-239 as a finite, source-informative, late-improving exploratory continuation rather than a promotion candidate. The low-resolution line accumulator did not deliver the intended immediate connectivity recovery: connectivity remains substantially below ABI-223's temporal-attention signal and far below ABI-202. However, the branch did improve matched 12-epoch filtered Dice, recall, MIT Dice, and Google Dice relative to ABI-223/ABI-238 exploratory checkpoints, and it selected the final epoch with declining train and validation losses.

The key scientific signal is that pre-encoder line accumulation may help the temporal branch escape the low-recall/low-Dice exploratory regime without causing collapse, but its current accumulator does not preserve long thin connectivity well enough. Because the best checkpoint is at the exploratory ceiling and the exact branch is finite/resource-safe, a close late36 continuation is justified under the approved late-improving budget policy if the next step wants to test whether the epoch-8-to-12 trajectory extends toward ABI-223. That continuation should be an unchanged or very close continuation of ABI-239, with `run_20260911_023156_f7eb6b` as parent evidence, not a new mechanism bundled into the budget request.

## Decision

Do not promote ABI-239 and do not request whole-validation diagnostics from this exploratory Result. Do not eliminate the branch on score alone. The best next in-contract action is a single late-improving close continuation of the same temporal line-accumulator architecture, using the approved `budget_request.yaml` path, because the Run is finite, noncollapsed, source-informative, and selected its best checkpoint at epoch 12 with losses still improving.

If the late36 continuation plateaus below ABI-223 or continues to show poor connectivity, stop this exact low-resolution line-accumulator branch and broaden again to a modern lightweight backbone or a different temporal mechanism that protects connectivity explicitly.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_023156_f7eb6b/candidate/PROPOSAL.md`
- `run_20260911_023156_f7eb6b/candidate/README.md`
- `run_20260911_023156_f7eb6b/candidate/manifest.yaml`
- `run_20260911_023156_f7eb6b/resolved_manifest.yaml`
- `run_20260911_023156_f7eb6b/outputs/model_summary.json`
- `run_20260911_023156_f7eb6b/outputs/best_metrics.json`
- `run_20260911_023156_f7eb6b/outputs/final_metrics.json`
- `run_20260911_023156_f7eb6b/outputs/metrics.jsonl`
- `run_20260911_023156_f7eb6b/outputs/resource_profile.json`
- `run_20260911_023156_f7eb6b/outputs/validation_postprocessing/index.json`
- `run_20260911_023156_f7eb6b/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention parent context
- `run_20260911_004137_f54c45` for ABI-238 temporal-attention directional-context context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
