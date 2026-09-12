# ABI-247 temporal five-frame center-anchored persistence-attention U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-247, Candidate `abi247_temporal_fiveframe_centeranchored_persistence_attention_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_094409_00852e`.

ABI-247 tested whether extending ABI-223-style temporal attention from three provider-owned frames to the allowlisted five-frame window `[-2, -1, 0, 1, 2]` could improve temporal persistence/change evidence while explicitly anchoring fusion to the zero-offset target frame. The Candidate consumed trusted `abi_16ch_plus_sza_temporal` tensors, used `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, cache reads, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-247 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with five provider-supplied ABI+SZA frames.
- Temporal offsets: `[-2, -1, 0, 1, 2]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,098,332, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.39 / 3.62 GiB.
- Training wall time: 984.6 s; validation wall time: 1,026.3 s; total Run wall time: 2,012.5 s.

This is successful finite/resource evidence for center-anchored five-frame persistence attention. Resource use stayed inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8, not the final epoch 12. Final epoch 12 was very close on aggregate filtered Dice but changed the operating point toward slightly higher precision/connectivity and lower recall.

| Metric | ABI-247 best epoch 8 | ABI-247 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.369489 | 0.368468 |
| Raw Dice | 0.384401 | 0.383199 |
| Filtered IoU | 0.226609 | 0.225842 |
| Filtered precision | 0.371054 | 0.386064 |
| Filtered recall | 0.367936 | 0.352406 |
| Filtered contrail connectivity | 0.194644 | 0.224367 |
| Filtered predicted-positive fraction | 0.005126 | 0.004719 |
| Raw predicted-positive fraction | 0.005533 | 0.005106 |
| MIT filtered Dice | 0.361787 | 0.350126 |
| Google filtered Dice | 0.388682 | 0.412717 |
| MIT filtered recall | 0.343513 | 0.316298 |
| Google filtered recall | 0.440602 | 0.459838 |
| Train loss | 0.822636 | 0.800169 |
| Validation loss | 0.865493 | 0.859841 |

The selected checkpoint is finite, noncollapsed, and source-informative. The source split is mixed: best epoch 8 has better MIT Dice, while final epoch 12 has better Google Dice and connectivity. Neither checkpoint reaches ABI-226's five-frame exploratory Dice or ABI-222's three-frame exploratory Dice.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.221181 | 0.229685 | 0.199623 | 0.247959 | 0.228495 | 0.205631 | 0.148599 | 0.006421 |
| 2 | 0.244050 | 0.253982 | 0.261145 | 0.229055 | 0.239118 | 0.254659 | 0.120657 | 0.004534 |
| 3 | 0.292707 | 0.304847 | 0.298855 | 0.286808 | 0.292101 | 0.294052 | 0.161963 | 0.004961 |
| 4 | 0.304122 | 0.317670 | 0.356453 | 0.265190 | 0.295773 | 0.324301 | 0.189453 | 0.003846 |
| 5 | 0.310759 | 0.326174 | 0.422421 | 0.245788 | 0.289451 | 0.362906 | 0.312168 | 0.003008 |
| 6 | 0.297068 | 0.311296 | 0.391677 | 0.239272 | 0.281943 | 0.335480 | 0.181802 | 0.003158 |
| 7 | 0.304879 | 0.320963 | 0.510432 | 0.217351 | 0.281641 | 0.366808 | 0.319704 | 0.002201 |
| 8 | 0.369489 | 0.384401 | 0.371054 | 0.367936 | 0.361787 | 0.388682 | 0.194644 | 0.005126 |
| 9 | 0.366688 | 0.380495 | 0.352318 | 0.382281 | 0.358194 | 0.387330 | 0.187183 | 0.005609 |
| 10 | 0.361863 | 0.377802 | 0.417104 | 0.319543 | 0.341499 | 0.410793 | 0.205943 | 0.003960 |
| 11 | 0.358367 | 0.374542 | 0.410974 | 0.317700 | 0.343771 | 0.394681 | 0.211678 | 0.003996 |
| 12 | 0.368468 | 0.383199 | 0.386064 | 0.352406 | 0.350126 | 0.412717 | 0.224367 | 0.004719 |

The trajectory improves quickly through epoch 5, becomes conservative at epoch 7 with the highest precision/connectivity but low recall, then jumps to the selected recall-oriented epoch 8. Epochs 8-12 remain in a narrow filtered-Dice band, but the operating point oscillates between precision/connectivity and recall/positive-fraction. This does not show the clean late-improving pattern needed for an approved longer-budget continuation of the exact stem.

## Comparison context

| Metric | ABI-247 center-anchored five-frame | ABI-226 five-frame attention/difference | ABI-222 temporal-attention exploratory | ABI-223 temporal-attention late36 | ABI-238 temporal-directional late36 | ABI-244 shifted-window U-NetFormer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_094409_00852e` | `run_20260910_120441_916a03` | `run_20260908_150315_9aea3f` | `run_20260908_154531_8c7e2b` | `run_20260911_004137_f54c45` | `run_20260911_072719_ade068` |
| Budget | exploratory | exploratory | exploratory | late36 | late36 | exploratory |
| Best epoch | 8 | 10 | 12 | 36 | 29 | 11 |
| Filtered Dice | 0.369489 | 0.378604 | 0.374329 | 0.419776 | 0.420235 | 0.392808 |
| Raw Dice | 0.384401 | 0.394881 | 0.392066 | 0.438487 | 0.438718 | 0.408130 |
| Filtered precision | 0.371054 | 0.428061 | 0.466148 | 0.483764 | 0.488730 | 0.397628 |
| Filtered recall | 0.367936 | 0.339391 | 0.312729 | 0.370738 | 0.368578 | 0.388104 |
| Filtered connectivity | 0.194644 | 0.224851 | 0.281396 | 0.412427 | 0.352239 | 0.290859 |
| MIT filtered Dice | 0.361787 | 0.366586 | 0.357658 | 0.398498 | 0.405383 | 0.380020 |
| Google filtered Dice | 0.388682 | 0.409886 | 0.416510 | 0.476764 | 0.460838 | 0.426225 |
| Filtered predicted-positive fraction | 0.005126 | 0.004099 | 0.003468 | 0.003962 | 0.003899 | 0.005046 |

Relative to ABI-226, ABI-247 lowers filtered Dice by -0.009115, raw Dice by -0.010480, precision by -0.057007, connectivity by -0.030207, MIT filtered Dice by -0.004799, and Google filtered Dice by -0.021204. It improves recall by +0.028545, but with a larger predicted-positive fraction (+0.001027) rather than better overlap or continuity.

Relative to ABI-222, ABI-247 lowers filtered Dice by -0.004840, raw Dice by -0.007665, precision by -0.095093, Google filtered Dice by -0.027827, and connectivity by -0.086752. It improves recall by +0.055207 and MIT filtered Dice by +0.004129, but the recall gain is not enough to compensate for weaker precision, Google transfer, and line continuity.

Relative to ABI-223 and ABI-238, ABI-247 is materially behind the late36 temporal frontier: about -0.050 filtered Dice, essentially tied or slightly below on recall, and far lower on connectivity. Relative to ABI-244, ABI-247 is also behind by -0.023320 filtered Dice and -0.096215 connectivity while using a similar positive fraction.

## Interpretation

Classify ABI-247 as a finite but negative/mixed five-frame temporal Result. It demonstrates that center-anchored five-frame persistence attention is trainable and resource-safe under the provider-owned temporal tensor contract, but it does not support the hypothesis that explicit center anchoring rescues the wider five-frame window. The main intended benefit was improved five-frame persistence/change evidence without the continuity dilution seen in earlier five-frame branches. Instead, ABI-247 trades toward recall and positive area while losing precision, Google Dice, and connectivity relative to the direct ABI-226 five-frame target.

This Result does not eliminate temporal modeling or all five-frame use. It does argue against simply widening ABI-223-style attention to five frames with a center-biased fusion gate as the next local continuation. The stronger temporal evidence still comes from three-frame attention/directional mechanisms and from ABI-240's late-budget line accumulator for recall, while ABI-247 does not produce a compelling combined overlap/continuity operating point.

## Decision

Do not promote ABI-247 and do not request whole-validation diagnostics from this capped Result alone. Do not request a late36 continuation of the exact ABI-247 center-anchored five-frame persistence-attention stem: the selected checkpoint is not at the exploratory ceiling, final performance is only a partial operating-point recovery, and the branch underperforms both the direct five-frame comparison and the mature three-frame temporal frontier.

Stop this exact center-biased five-frame stem. Future work should change the mechanism rather than only resize or prolong it. Plausible next directions include returning to three-frame temporal attention with a different continuity-preserving decoder, using a materially different non-attention temporal-change mechanism, or broadening away from temporal models into rotation-aware/group-equivariant line networks, modern lightweight backbones, or calibration/uncertainty mechanisms that are not final-head dual-logit consensus.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_094409_00852e/candidate/PROPOSAL.md`
- `run_20260911_094409_00852e/candidate/README.md`
- `run_20260911_094409_00852e/candidate/manifest.yaml`
- `run_20260911_094409_00852e/resolved_manifest.yaml`
- `run_20260911_094409_00852e/outputs/model_summary.json`
- `run_20260911_094409_00852e/outputs/best_metrics.json`
- `run_20260911_094409_00852e/outputs/final_metrics.json`
- `run_20260911_094409_00852e/outputs/metrics.jsonl`
- `run_20260911_094409_00852e/outputs/resource_profile.json`
- `run_20260911_094409_00852e/outputs/validation_postprocessing/index.json`
- `run_20260911_094409_00852e/outputs/prediction_samples/samples.json`
- `run_20260910_120441_916a03` for ABI-226 five-frame attention/difference context
- `run_20260908_150315_9aea3f` for ABI-222 exploratory temporal-attention context
- `run_20260908_154531_8c7e2b` for ABI-223 late36 temporal-attention context
- `run_20260911_004137_f54c45` for ABI-238 temporal-directional late36 context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_072719_ade068` for ABI-244 shifted-window temporal U-NetFormer context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
