# ABI-246 temporal-attention dual-logit consensus U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-246, Candidate `abi246_temporal_attention_dual_logit_consensus_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_090216_5e68c5`.

ABI-246 tested whether replacing ABI-223's single final mask head with a learned dual-logit consensus head could improve early temporal-attention precision/recall balance. The Candidate consumed trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, cache reads, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-246 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,138,467, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.29 / 3.55 GiB.
- Training wall time: 1,024.8 s; validation wall time: 946.8 s; total Run wall time: 1,973.4 s.

This is successful finite/resource evidence for the dual-logit consensus head. Resource use stayed inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8, not the final epoch 12.

| Metric | ABI-246 best epoch 8 | ABI-246 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.349959 | 0.309231 |
| Raw Dice | 0.366892 | 0.321067 |
| Filtered IoU | 0.212091 | 0.182894 |
| Filtered precision | 0.451600 | 0.307584 |
| Filtered recall | 0.285665 | 0.310895 |
| Filtered contrail connectivity | 0.352117 | 0.147520 |
| Filtered predicted-positive fraction | 0.003270 | 0.005225 |
| Raw predicted-positive fraction | 0.003527 | 0.005648 |
| MIT filtered Dice | 0.332788 | 0.306503 |
| Google filtered Dice | 0.393155 | 0.315202 |
| MIT filtered recall | 0.259712 | 0.282622 |
| Google filtered recall | 0.362880 | 0.395013 |
| Train loss | 0.831765 | 0.814598 |
| Validation loss | 0.878760 | 0.890185 |

The selected checkpoint is finite and noncollapsed, but it is weak relative to the temporal-attention control. The final epoch shifts toward higher recall and much larger positive fraction while losing precision, filtered Dice, Google Dice, and especially connectivity. The selected epoch is not at the exploratory ceiling, so this Result does not support a late-improving continuation of the exact consensus-head formulation.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.181954 | 0.190012 | 0.199835 | 0.167010 | 0.182137 | 0.181564 | 0.150454 | 0.004320 |
| 2 | 0.232662 | 0.242973 | 0.258178 | 0.211736 | 0.233258 | 0.231364 | 0.151348 | 0.004240 |
| 3 | 0.260057 | 0.270917 | 0.270508 | 0.250384 | 0.259972 | 0.260234 | 0.138134 | 0.004785 |
| 4 | 0.279645 | 0.291510 | 0.314073 | 0.252019 | 0.272382 | 0.296695 | 0.141671 | 0.004148 |
| 5 | 0.302280 | 0.313304 | 0.279919 | 0.328524 | 0.302424 | 0.301971 | 0.139903 | 0.006067 |
| 6 | 0.331082 | 0.344438 | 0.341784 | 0.321030 | 0.331415 | 0.330363 | 0.200430 | 0.004856 |
| 7 | 0.329465 | 0.346572 | 0.492834 | 0.247442 | 0.310540 | 0.378784 | 0.436960 | 0.002596 |
| 8 | 0.349959 | 0.366892 | 0.451600 | 0.285665 | 0.332788 | 0.393155 | 0.352117 | 0.003270 |
| 9 | 0.347811 | 0.360466 | 0.318842 | 0.382570 | 0.347423 | 0.348649 | 0.193432 | 0.006203 |
| 10 | 0.301586 | 0.315271 | 0.349677 | 0.265124 | 0.290317 | 0.327710 | 0.191422 | 0.003920 |
| 11 | 0.308113 | 0.322459 | 0.377579 | 0.260236 | 0.291142 | 0.349464 | 0.242121 | 0.003563 |
| 12 | 0.309231 | 0.321067 | 0.307584 | 0.310895 | 0.306503 | 0.315202 | 0.147520 | 0.005225 |

The trajectory improves from epochs 1 through 8 and then becomes unstable. Epoch 7 gives the highest connectivity (0.436960) and precision (0.492834), but with low recall and a very low positive fraction. Epoch 9 recovers recall (0.382570) but drops connectivity to 0.193432 and expands positive fraction to 0.006203. The consensus head therefore appears to oscillate between overly conservative connected-line evidence and recall-oriented diffuse evidence rather than combining the two into a stable final mask.

## Comparison context

| Metric | ABI-246 dual-logit consensus | ABI-222 temporal attention exploratory | ABI-223 temporal attention late36 | ABI-238 temporal directional late36 | ABI-244 shifted-window U-NetFormer | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_090216_5e68c5` | `run_20260908_150315_9aea3f` | `run_20260908_154531_8c7e2b` | `run_20260911_004137_f54c45` | `run_20260911_072719_ade068` | `run_20260904_043143_ee0005` |
| Budget | exploratory | exploratory | late36 | late36 | exploratory | late36 |
| Best epoch | 8 | 12 | 36 | 29 | 11 | 34 |
| Filtered Dice | 0.349959 | 0.374329 | 0.419776 | 0.420235 | 0.392808 | 0.427570 |
| Raw Dice | 0.366892 | 0.392066 | 0.438487 | 0.438718 | 0.408130 | 0.442746 |
| Filtered precision | 0.451600 | 0.466148 | 0.483764 | 0.488730 | 0.397628 | 0.439467 |
| Filtered recall | 0.285665 | 0.312729 | 0.370738 | 0.368578 | 0.388104 | 0.416301 |
| Filtered connectivity | 0.352117 | 0.281396 | 0.412427 | 0.352239 | 0.290859 | 0.457773 |
| MIT filtered Dice | 0.332788 | 0.357658 | 0.398498 | 0.405383 | 0.380020 | 0.411992 |
| Google filtered Dice | 0.393155 | 0.416510 | 0.476764 | 0.460838 | 0.426225 | 0.468151 |
| Filtered predicted-positive fraction | 0.003270 | 0.003468 | 0.003962 | 0.003899 | 0.005046 | 0.003433 |

Relative to ABI-222, ABI-246 lowers selected filtered Dice by -0.024369, raw Dice by -0.025174, precision by -0.014547, recall by -0.027064, MIT filtered Dice by -0.024870, and Google filtered Dice by -0.023354. It improves connectivity by +0.070721 with a slightly smaller positive fraction, but the gain is not paired with useful overlap or recall. Relative to ABI-223 late36, ABI-246 is far behind on Dice, recall, and connectivity. Relative to the current whole-validation-tested ABI-202 frontier, ABI-246 is behind by -0.077611 filtered Dice, -0.130636 recall, and -0.105656 connectivity.

## Interpretation

Classify ABI-246 as a finite but negative/mixed calibration-head Result. It provides evidence that a dual-logit consensus mask head is trainable and resource-safe on provider-owned temporal tensors, but it does not support the hypothesis that this head improves the temporal-attention precision/recall balance. The most favorable view is that the head can create compact connected-line predictions at epochs 7-8; however, those predictions are under-recall and lose aggregate/source Dice. When the model later recovers recall, connectivity collapses and positive fraction expands.

The exact ABI-246 head should not be extended with a late36 budget. The best checkpoint occurs before the exploratory ceiling, the final epoch is materially worse than the selected checkpoint, and the head underperforms ABI-222, the direct exploratory comparison target. This does not eliminate temporal modeling or all calibration/uncertainty architectures, but it argues against simple final-head dual-logit agreement as the next local continuation.

## Decision

Do not promote ABI-246 and do not request whole-validation diagnostics from this capped Result alone. Do not request a late36 continuation of the exact dual-logit consensus-head branch.

Stop this exact mask-head-level consensus formulation. Future temporal work should change the mechanism rather than only resize or prolong this head. Plausible next directions include a five-frame temporal-change architecture that uses the now-available `[-2, -1, 0, 1, 2]` window, a recurrent/attention mechanism that acts earlier on motion/change features rather than only at the final logits, or a broader non-temporal rotation-aware/line-accumulation scout.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_090216_5e68c5/candidate/PROPOSAL.md`
- `run_20260911_090216_5e68c5/candidate/README.md`
- `run_20260911_090216_5e68c5/candidate/manifest.yaml`
- `run_20260911_090216_5e68c5/resolved_manifest.yaml`
- `run_20260911_090216_5e68c5/outputs/model_summary.json`
- `run_20260911_090216_5e68c5/outputs/best_metrics.json`
- `run_20260911_090216_5e68c5/outputs/final_metrics.json`
- `run_20260911_090216_5e68c5/outputs/metrics.jsonl`
- `run_20260911_090216_5e68c5/outputs/resource_profile.json`
- `run_20260911_090216_5e68c5/outputs/validation_postprocessing/index.json`
- `run_20260911_090216_5e68c5/outputs/prediction_samples/samples.json`
- `run_20260908_150315_9aea3f` for ABI-222 exploratory temporal-attention context
- `run_20260908_154531_8c7e2b` for ABI-223 late36 temporal-attention context
- `run_20260911_004137_f54c45` for ABI-238 temporal-directional late36 context
- `run_20260911_072719_ade068` for ABI-244 shifted-window temporal U-NetFormer context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
