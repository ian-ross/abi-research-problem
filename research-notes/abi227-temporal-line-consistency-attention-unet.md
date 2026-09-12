# ABI-227 temporal line-consistency attention U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-227, Candidate `abi227_temporal_line_consistency_attention_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260910_124920_f1b455`.

ABI-227 was a temporal-attention family-development continuation after ABI-223 and ABI-226. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`. It kept the compact ABI-223-style temporal-attention/change U-Net and added a differentiable temporal-line consistency block with anisotropic/dilated line-context branches gated by center-frame and temporally attended evidence. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-227 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,133,588, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.51 / 3.77 GB.
- Training wall time: 1,044.3 s; validation wall time: 1,012.4 s; total Run wall time: 2,058.5 s.

This is successful finite/resource evidence for the added temporal-line consistency block, but not a clear primary-metric improvement over the prior temporal-attention scout.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 9.

| Metric | ABI-227 best epoch 9 |
| --- | ---: |
| Filtered Dice | 0.370657 |
| Raw Dice | 0.383841 |
| Filtered IoU | 0.227489 |
| Filtered precision | 0.341621 |
| Filtered recall | 0.405088 |
| Filtered contrail connectivity | 0.190346 |
| Filtered predicted-positive fraction | 0.006130 |
| Raw predicted-positive fraction | 0.006618 |
| MIT filtered Dice | 0.360838 |
| Google filtered Dice | 0.394514 |
| MIT filtered recall | 0.373264 |
| Google filtered recall | 0.499771 |
| Train loss | 0.812785 |
| Validation loss | 0.867758 |

The final epoch was not selected by the primary metric, but it is scientifically relevant because the line-consistency block produced its strongest continuity/precision behavior there: final filtered Dice 0.367698, filtered precision 0.471342, filtered recall 0.301418, filtered connectivity 0.378301, MIT filtered Dice 0.346088, and Google filtered Dice 0.423847.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.240635 | 0.250715 | 0.253339 | 0.229145 | 0.238183 | 0.246214 | 0.192863 | 0.004676 |
| 2 | 0.239445 | 0.251867 | 0.381326 | 0.174513 | 0.223681 | 0.278563 | 0.250491 | 0.002366 |
| 3 | 0.289759 | 0.300766 | 0.276439 | 0.304428 | 0.288015 | 0.293361 | 0.201412 | 0.005693 |
| 4 | 0.252888 | 0.263949 | 0.288875 | 0.224874 | 0.242368 | 0.277686 | 0.135298 | 0.004024 |
| 5 | 0.314354 | 0.329190 | 0.438019 | 0.245143 | 0.297261 | 0.356791 | 0.196113 | 0.002893 |
| 6 | 0.325411 | 0.337103 | 0.295340 | 0.362300 | 0.325632 | 0.324877 | 0.226781 | 0.006342 |
| 7 | 0.334690 | 0.352227 | 0.494850 | 0.252853 | 0.323394 | 0.364555 | 0.356488 | 0.002641 |
| 8 | 0.327422 | 0.340824 | 0.326357 | 0.328495 | 0.330633 | 0.320051 | 0.226057 | 0.005203 |
| 9 | 0.370657 | 0.383841 | 0.341621 | 0.405088 | 0.360838 | 0.394514 | 0.190346 | 0.006130 |
| 10 | 0.323107 | 0.337684 | 0.380460 | 0.280780 | 0.307150 | 0.360876 | 0.188469 | 0.003815 |
| 11 | 0.349422 | 0.365369 | 0.407917 | 0.305599 | 0.337446 | 0.378511 | 0.237833 | 0.003873 |
| 12 | 0.367698 | 0.385378 | 0.471342 | 0.301418 | 0.346088 | 0.423847 | 0.378301 | 0.003306 |

The trajectory is finite and noncollapsed but oscillatory. Epoch 9 is the best primary checkpoint because it expands recall and positive fraction, especially on Google. Epoch 12 recovers most of the primary metric while shifting to a higher-precision and higher-connectivity regime. That split suggests the added line-consistency module can strengthen continuous line evidence, but the current gating does not align that benefit with the primary Dice optimum.

## Temporal-family comparison

| Metric | ABI-218 single-frame control | ABI-222 attention 12ep | ABI-223 attention late36 | ABI-226 five-frame scout | ABI-227 line-consistency |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 36 | 10 | 9 |
| Filtered Dice | 0.345570 | 0.374329 | 0.419776 | 0.378604 | 0.370657 |
| Raw Dice | 0.361077 | 0.392066 | 0.438487 | 0.394881 | 0.383841 |
| Filtered precision | 0.407234 | 0.466148 | 0.483764 | 0.428061 | 0.341621 |
| Filtered recall | 0.300125 | 0.312729 | 0.370738 | 0.339391 | 0.405088 |
| Filtered connectivity | 0.231399 | 0.281396 | 0.412427 | 0.224851 | 0.190346 |
| MIT filtered Dice | 0.330415 | 0.357658 | 0.398498 | 0.366586 | 0.360838 |
| Google filtered Dice | 0.385184 | 0.416510 | 0.476764 | 0.409886 | 0.394514 |
| Filtered predicted-positive fraction | 0.003810 | 0.003468 | 0.003962 | 0.004099 | 0.006130 |
| Parameter count | 3,050,475 | 3,095,836 | 3,095,836 | 3,098,332 | 3,133,588 |

At its selected checkpoint, ABI-227 exceeds the ABI-218 matched single-frame temporal-eligible control by +0.025087 filtered Dice, +0.104963 filtered recall, and +0.030423 MIT filtered Dice, but has lower connectivity and only a small Google Dice margin. Relative to ABI-222 at the same 12-epoch budget, ABI-227 is lower on filtered Dice (-0.003672), raw Dice (-0.008225), precision (-0.124527), Google Dice (-0.021996), and selected-checkpoint connectivity (-0.091050), while higher on recall (+0.092359) and slightly higher on MIT Dice (+0.003180).

The final checkpoint tells a different but still mixed story: final ABI-227 connectivity (0.378301) is materially above ABI-222 and ABI-226, and close to ABI-223's late36 connectivity, but final filtered Dice remains below ABI-222 and ABI-226. Therefore the line-consistency mechanism did not fail to learn continuity; it failed to make continuity and primary overlap co-peak under the exploratory budget.

## Frontier context

ABI-202 remains the strongest whole-validation-tested Result, with whole-validation filtered Dice 0.4312. ABI-223 remains the capped temporal-family frontier, with filtered Dice 0.419776 at epoch 36 and a strong matched-control margin over ABI-218.

ABI-227 is not a promotion candidate and does not justify whole-validation diagnostics. Its capped Result is useful temporal-family evidence because it isolates a specific architectural attempt to repair line continuity, but the selected checkpoint is weaker than ABI-222/226 and far below ABI-223.

## Interpretation

Classify ABI-227 as a mixed-to-negative temporal-attention continuation, not a hard execution failure. The added temporal-line consistency block is resource-safe and can produce high final connectivity, but the primary checkpoint is recall-heavy, low-precision, and low-connectivity. The final checkpoint is connectivity-positive but primary-Dice-negative. This mismatch suggests that simply inserting anisotropic line context into the three-frame temporal stem is not enough; the architecture needs either better calibration of the line-consistency gate or a more materially different line/motion model.

Because the best primary metric occurs at epoch 9 and the final epoch has not surpassed ABI-222/226 on filtered Dice, ABI-227 does not meet the late-improving budget rationale. A longer continuation of this exact branch would risk spending the approved extended budget on an oscillatory variant that has not beaten the 12-epoch temporal-attention baseline.

## Decision

Do not promote ABI-227, do not request whole-validation diagnostics, and do not request a `late_improving` continuation of this exact line-consistency temporal-attention variant.

If the campaign continues temporal work, prefer a materially different temporal/line formulation rather than another small stem tweak: for example, a rotation-aware line-accumulation module, differentiable Hough/Radon-style voting, stronger center-frame anchoring for motion/change evidence, or a compact modern attention/backbone scout. ABI-227's final connectivity is a useful design clue, but the branch needs a new mechanism that aligns continuity with filtered Dice and source balance.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_124920_f1b455/candidate/PROPOSAL.md`
- `run_20260910_124920_f1b455/candidate/README.md`
- `run_20260910_124920_f1b455/candidate/manifest.yaml`
- `run_20260910_124920_f1b455/resolved_manifest.yaml`
- `run_20260910_124920_f1b455/outputs/model_summary.json`
- `run_20260910_124920_f1b455/outputs/best_metrics.json`
- `run_20260910_124920_f1b455/outputs/final_metrics.json`
- `run_20260910_124920_f1b455/outputs/metrics.jsonl`
- `run_20260910_124920_f1b455/outputs/resource_profile.json`
- `run_20260910_124920_f1b455/outputs/validation_postprocessing/index.json`
- `run_20260910_124920_f1b455/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260910_120441_916a03` for ABI-226 five-frame comparison context
- `run_20260908_150315_9aea3f` for ABI-222 same-budget temporal-attention context
- `run_20260908_123030_05ad37` for ABI-218 matched temporal-eligible single-frame control
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
