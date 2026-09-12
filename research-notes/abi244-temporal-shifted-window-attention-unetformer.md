# ABI-244 temporal shifted-window attention U-NetFormer

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-244, Candidate `abi244_temporal_shifted_window_attention_unetformer_bce_dice_line_centerline_aux_v1`, Run `run_20260911_072719_ade068`.

ABI-244 tested whether replacing ABI-229's fixed local windows with shifted Swin-style local attention would let thin contrail evidence cross window seams in a compact temporal U-NetFormer. The Candidate consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, cache reads, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-244 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,880,780, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.21 / 4.43 GiB.
- Training wall time: 1,383.0 s; validation wall time: 1,104.6 s; total Run wall time: 2,489.5 s.

This is successful finite/resource evidence for shifted-window temporal local attention. Resource use stayed well inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 11, not the final epoch 12.

| Metric | ABI-244 best epoch 11 | ABI-244 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.392808 | 0.373294 |
| Raw Dice | 0.408130 | 0.390071 |
| Filtered IoU | 0.244407 | 0.229478 |
| Filtered precision | 0.397628 | 0.438612 |
| Filtered recall | 0.388104 | 0.324909 |
| Filtered contrail connectivity | 0.290859 | 0.286032 |
| Filtered predicted-positive fraction | 0.005046 | 0.003829 |
| Raw predicted-positive fraction | 0.005451 | 0.004128 |
| MIT filtered Dice | 0.380020 | 0.353677 |
| Google filtered Dice | 0.426225 | 0.423004 |
| MIT filtered recall | 0.362821 | 0.294917 |
| Google filtered recall | 0.463327 | 0.414140 |
| Train loss | 0.812145 | 0.797388 |
| Validation loss | 0.859148 | 0.864508 |

The selected checkpoint is finite, noncollapsed, and source-informative. It improves over the final epoch by preserving much higher recall and MIT filtered Dice while accepting lower precision and a larger predicted-positive fraction.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.202101 | 0.211778 | 0.255386 | 0.167213 | 0.199130 | 0.208638 | 0.183733 | 0.003385 |
| 2 | 0.250144 | 0.260688 | 0.271989 | 0.231548 | 0.249009 | 0.252601 | 0.142514 | 0.004401 |
| 3 | 0.280675 | 0.291567 | 0.281866 | 0.279495 | 0.277900 | 0.286632 | 0.217064 | 0.005126 |
| 4 | 0.271760 | 0.285924 | 0.431925 | 0.198247 | 0.248780 | 0.329089 | 0.291633 | 0.002373 |
| 5 | 0.324587 | 0.339353 | 0.381194 | 0.282618 | 0.319304 | 0.336991 | 0.254270 | 0.003833 |
| 6 | 0.344181 | 0.355903 | 0.303525 | 0.397414 | 0.343452 | 0.345770 | 0.180350 | 0.006769 |
| 7 | 0.306679 | 0.323573 | 0.505116 | 0.220180 | 0.283026 | 0.369859 | 0.382374 | 0.002253 |
| 8 | 0.366396 | 0.384200 | 0.458508 | 0.305103 | 0.353169 | 0.400129 | 0.290959 | 0.003440 |
| 9 | 0.353296 | 0.366446 | 0.338333 | 0.369644 | 0.340257 | 0.384923 | 0.220577 | 0.005648 |
| 10 | 0.311778 | 0.328759 | 0.526935 | 0.221383 | 0.283247 | 0.386216 | 0.336301 | 0.002172 |
| 11 | 0.392808 | 0.408130 | 0.397628 | 0.388104 | 0.380020 | 0.426225 | 0.290859 | 0.005046 |
| 12 | 0.373294 | 0.390071 | 0.438612 | 0.324909 | 0.353677 | 0.423004 | 0.286032 | 0.003829 |

The trajectory is noisy rather than cleanly late-improving. Filtered Dice reaches a new local best at epoch 11, but final epoch 12 regresses in filtered Dice, recall, MIT filtered Dice, and validation loss while train loss continues downward. Connectivity peaks at epoch 7, not at the selected checkpoint, which weakens the shifted-window seam-crossing hypothesis.

## Comparison context

| Metric | ABI-244 shifted-window U-NetFormer | ABI-229 fixed-window U-NetFormer | ABI-223 temporal attention late36 | ABI-238 temporal directional late36 | ABI-240 temporal line-accum late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_072719_ade068` | `run_20260910_141659_818da0` | `run_20260908_154531_8c7e2b` | `run_20260911_004137_f54c45` | `run_20260911_031326_43ed12` | `run_20260904_043143_ee0005` |
| Budget | exploratory | exploratory | late36 | late36 | late36 | late36 |
| Best epoch | 11 | 8 | 36 | 29 | 29 | 34 |
| Filtered Dice | 0.392808 | 0.376958 | 0.419776 | 0.420235 | 0.414892 | 0.427570 |
| Raw Dice | 0.408130 | 0.393997 | 0.438487 | 0.438718 | 0.431959 | 0.442746 |
| Filtered precision | 0.397628 | 0.434428 | 0.483764 | 0.488730 | 0.436241 | 0.439467 |
| Filtered recall | 0.388104 | 0.332917 | 0.370738 | 0.368578 | 0.395534 | 0.416301 |
| Filtered connectivity | 0.290859 | 0.313635 | 0.412427 | 0.352239 | 0.264863 | 0.457773 |
| MIT filtered Dice | 0.380020 | 0.364086 | 0.398498 | 0.405383 | 0.397067 | 0.411992 |
| Google filtered Dice | 0.426225 | 0.410445 | 0.476764 | 0.460838 | 0.460659 | 0.468151 |
| Filtered predicted-positive fraction | 0.005046 | 0.003962 | 0.003962 | 0.003899 | 0.004687 | 0.003433 |

Relative to ABI-229, ABI-244 improves selected filtered Dice by +0.015850, MIT filtered Dice by +0.015934, Google filtered Dice by +0.015780, and filtered recall by +0.055187. The cost is lower precision (-0.036800), larger filtered predicted-positive fraction (+0.001084), and lower filtered connectivity (-0.022776). Thus shifted windows improved overlap and recall on the same exploratory temporal-eligible sample regime, but did not deliver the expected continuity gain.

Relative to the late36 temporal frontier, ABI-244 remains materially behind ABI-223 and ABI-238 on filtered Dice and connectivity. It has slightly higher selected recall than ABI-223/238, but this appears to come from broader positive predictions and lower precision rather than cleaner line continuity. It also remains below the ABI-202 single-frame frontier by -0.034762 filtered Dice and -0.166914 connectivity.

## Interpretation

Classify ABI-244 as a finite, nondegenerate, scientifically mixed family-development Result. It supports the compatibility of compact shifted-window attention with provider-owned temporal ABI+SZA tensors and gives a real filtered-Dice improvement over ABI-229's fixed-window U-NetFormer scout. However, the central mechanism was intended to reduce fixed-window fragmentation and improve thin-line continuity; the selected checkpoint instead lowers connectivity versus ABI-229 and relies on higher recall with a larger predicted-positive fraction.

The result does not eliminate modern temporal attention backbones: ABI-244 is trainable, source-informative, and above the prior exploratory fixed-window U-NetFormer. It does weaken the exact shifted-window replacement as a continuity solution. The branch's strongest evidence is recall/overlap, not line connectivity.

## Decision

Do not promote ABI-244 and do not request whole-validation diagnostics from this capped Result alone. Do not request a late36 continuation of the exact ABI-244 shifted-window branch: the best checkpoint is not the final epoch, final validation regresses, and the stated connectivity success criterion is not met.

Stop the exact shifted-window U-NetFormer continuation as a continuity mechanism. A future temporal modern-backbone scout should change the mechanism rather than merely extend this one: for example, a smaller global-token or cross-window line-memory module, a five-frame temporal attention model with explicit high-resolution detail preservation, or a calibration/selection-aware architecture that improves recall without sacrificing connectivity and precision. Any next Candidate should remain sequential unless it is a tightly profiled one-factor continuation under the Harness-owned resource policy.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_072719_ade068/candidate/PROPOSAL.md`
- `run_20260911_072719_ade068/candidate/README.md`
- `run_20260911_072719_ade068/candidate/manifest.yaml`
- `run_20260911_072719_ade068/resolved_manifest.yaml`
- `run_20260911_072719_ade068/outputs/model_summary.json`
- `run_20260911_072719_ade068/outputs/best_metrics.json`
- `run_20260911_072719_ade068/outputs/final_metrics.json`
- `run_20260911_072719_ade068/outputs/metrics.jsonl`
- `run_20260911_072719_ade068/outputs/resource_profile.json`
- `run_20260911_072719_ade068/outputs/validation_postprocessing/index.json`
- `run_20260911_072719_ade068/outputs/prediction_samples/samples.json`
- `run_20260910_141659_818da0` for ABI-229 fixed-window temporal U-NetFormer context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
