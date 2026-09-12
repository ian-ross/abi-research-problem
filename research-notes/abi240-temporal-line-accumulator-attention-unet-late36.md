# ABI-240 temporal line-accumulator attention U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-240, Candidate `abi240_temporal_line_accumulator_attention_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260911_031326_43ed12`.

ABI-240 was the approved late36 close continuation of ABI-239 (`run_20260911_023156_f7eb6b`). It kept ABI-239's temporal line-accumulator attention U-Net architecture and changed only the Harness-validated budget class. The model consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-240 completed the approved late-improving 36-epoch budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: `late_improving`; request approved; effective maximum epochs 36.
- Parent evidence: ABI-239, Run `run_20260911_023156_f7eb6b`.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,126,436, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.19 / 3.47 GiB.
- Training wall time: 3,145.1 s; validation wall time: 2,997.8 s; total Run wall time: 6,144.8 s.

This is successful finite/resource evidence for the temporal line-accumulator branch under the longer budget. Resource use stayed well inside the trusted memory and timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 29. Final epoch 36 had lower filtered Dice but higher recall.

| Metric | ABI-240 best epoch 29 | ABI-240 final epoch 36 |
| --- | ---: | ---: |
| Filtered Dice | 0.414892 | 0.395183 |
| Raw Dice | 0.431959 | 0.410522 |
| Filtered IoU | 0.261743 | 0.246248 |
| Filtered precision | 0.436241 | 0.376162 |
| Filtered recall | 0.395534 | 0.416229 |
| Filtered contrail connectivity | 0.264863 | 0.207559 |
| Filtered predicted-positive fraction | 0.004687 | 0.005720 |
| Raw predicted-positive fraction | 0.005049 | 0.006153 |
| MIT filtered Dice | 0.397067 | 0.382221 |
| Google filtered Dice | 0.460659 | 0.429342 |
| MIT filtered recall | 0.364006 | 0.389931 |
| Google filtered recall | 0.489339 | 0.494471 |
| Train loss | 0.795517 | 0.774029 |
| Validation loss | 0.842781 | 0.850645 |

The selected checkpoint is finite, noncollapsed, and source-informative. Both MIT and Google retain nontrivial filtered Dice and recall. The longer budget substantially increases predicted-positive fraction and recall relative to ABI-239, but filtered connectivity remains weak for a line-continuity hypothesis.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.179523 | 0.185150 | 0.144536 | 0.236858 | 0.187879 | 0.164217 | 0.084625 | 0.008472 |
| 6 | 0.313039 | 0.328096 | 0.429320 | 0.246322 | 0.294356 | 0.359311 | 0.265027 | 0.002966 |
| 12 | 0.378473 | 0.392402 | 0.367737 | 0.389856 | 0.369990 | 0.398065 | 0.175295 | 0.005481 |
| 18 | 0.351651 | 0.365966 | 0.366272 | 0.338153 | 0.334542 | 0.392808 | 0.181997 | 0.004773 |
| 24 | 0.390877 | 0.408036 | 0.440131 | 0.351538 | 0.373500 | 0.437769 | 0.227073 | 0.004129 |
| 29 | 0.414892 | 0.431959 | 0.436241 | 0.395534 | 0.397067 | 0.460659 | 0.264863 | 0.004687 |
| 30 | 0.413526 | 0.431397 | 0.464800 | 0.372441 | 0.394794 | 0.461691 | 0.302654 | 0.004142 |
| 36 | 0.395183 | 0.410522 | 0.376162 | 0.416229 | 0.382221 | 0.429342 | 0.207559 | 0.005720 |

The late trajectory confirms ABI-239 was budget-truncated: filtered Dice rises from 0.366274 in the parent exploratory Run to 0.414892 at epoch 29. However, the branch does not show a clean final-epoch improvement. Dice peaks at epoch 29, remains near the top at epoch 30, then declines by epoch 36 even as train loss continues downward. This suggests late overfitting or calibration drift toward higher recall/lower precision rather than an unfinished monotonic trajectory.

Connectivity is unstable and remains the main failure mode. Epoch 15 reached connectivity 0.408337 with lower filtered Dice 0.402171 and lower recall 0.331571, but the selected epoch has connectivity only 0.264863. The branch can sometimes produce connected predictions, but its best-overlap checkpoint does not preserve the line continuity needed to challenge the temporal-attention or ABI-202 frontiers.

## Comparison context

| Metric | ABI-239 exploratory | ABI-240 late36 | ABI-223 temporal late36 | ABI-238 temporal directional late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_023156_f7eb6b` | `run_20260911_031326_43ed12` | `run_20260908_154531_8c7e2b` | `run_20260911_004137_f54c45` | `run_20260904_043143_ee0005` |
| Best epoch | 12 | 29 | 36 | 29 | 34 |
| Filtered Dice | 0.366274 | 0.414892 | 0.419776 | 0.420235 | 0.427570 |
| Raw Dice | 0.383403 | 0.431959 | 0.438487 | 0.438718 | 0.442746 |
| Filtered precision | 0.457890 | 0.436241 | 0.483764 | 0.488730 | 0.439467 |
| Filtered recall | 0.305207 | 0.395534 | 0.370738 | 0.368578 | 0.416301 |
| Filtered connectivity | 0.246821 | 0.264863 | 0.412427 | 0.352239 | 0.457773 |
| MIT filtered Dice | 0.346223 | 0.397067 | 0.398498 | 0.405383 | 0.411992 |
| Google filtered Dice | 0.415466 | 0.460659 | 0.476764 | 0.460838 | 0.468151 |
| Filtered predicted-positive fraction | 0.003446 | 0.004687 | 0.003962 | 0.003899 | 0.003433 |

ABI-240 improves the ABI-239 parent by +0.048617 filtered Dice, +0.090327 filtered recall, +0.050844 MIT filtered Dice, and +0.045193 Google filtered Dice. That validates the late-improving budget request and shows that pre-encoder line accumulation was not exhausted at 12 epochs.

Against the mature temporal frontier, ABI-240 is close on aggregate filtered Dice but loses on precision and especially connectivity. It trails ABI-223 by -0.004884 filtered Dice and -0.147564 connectivity, and trails ABI-238 by -0.005343 filtered Dice and -0.087377 connectivity. It has higher recall than both temporal comparators, but that appears to come from a larger predicted-positive fraction and lower precision rather than better connected thin-line structure. Against ABI-202, ABI-240 trails by -0.012679 filtered Dice and -0.192910 connectivity.

## Interpretation

Classify ABI-240 as a useful finite family-development result, not a promotion candidate. The late36 continuation answered the main ABI-239 question: the low-resolution temporal line accumulator was budget-truncated for overlap and recall, but its weak connectivity is durable enough to prevent promotion or whole-validation diagnostic priority from this Result alone.

The scientific signal is mixed. The mechanism produces near-frontier capped filtered Dice and strong recall, including source-informative MIT and Google behavior. But it does not convert temporal/Radon evidence into connected contrail masks at the selected checkpoint. The best-overlap operating point favors broader or fragmented positives; the high-connectivity epoch sacrifices too much Dice/recall to be the selected Result. This makes further unchanged late-budget repeats inappropriate.

## Decision

Do not promote ABI-240 and do not request whole-validation diagnostics from this Result alone. Do not eliminate temporal modeling overall. Stop the exact unchanged low-resolution line-accumulator late36 branch: it has now received the approved longer budget and still fails the intended connectivity recovery criterion.

A reasonable next in-contract hypothesis is to broaden within temporal modeling rather than repeat ABI-240: use a materially different temporal mechanism that preserves high-resolution line continuity, such as a high-resolution temporal-difference/attention skip path, a compact recurrent change block, or a modern lightweight temporal backbone with explicit continuity-preserving decoder features. Any next Candidate should be a new sequential scout or tightly justified one-factor continuation, not another ABI-239/240 budget extension.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_031326_43ed12/candidate/PROPOSAL.md`
- `run_20260911_031326_43ed12/candidate/README.md`
- `run_20260911_031326_43ed12/candidate/manifest.yaml`
- `run_20260911_031326_43ed12/candidate/budget_request.yaml`
- `run_20260911_031326_43ed12/resolved_manifest.yaml`
- `run_20260911_031326_43ed12/outputs/model_summary.json`
- `run_20260911_031326_43ed12/outputs/best_metrics.json`
- `run_20260911_031326_43ed12/outputs/final_metrics.json`
- `run_20260911_031326_43ed12/outputs/metrics.jsonl`
- `run_20260911_031326_43ed12/outputs/resource_profile.json`
- `run_20260911_031326_43ed12/outputs/validation_postprocessing/index.json`
- `run_20260911_031326_43ed12/outputs/prediction_samples/samples.json`
- `run_20260911_023156_f7eb6b` for ABI-239 exploratory parent context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
