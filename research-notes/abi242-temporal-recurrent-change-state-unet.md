# ABI-242 temporal recurrent change-state U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-242, Candidate `abi242_temporal_recurrent_change_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_055200_52c75f`.

ABI-242 tested whether a compact bidirectional ConvGRU-style temporal state over provider-owned previous, center, and next ABI+SZA frames could improve the temporal frontier's recall/connectivity balance. The Candidate consumed trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, data loading, cache reads, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-242 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,157,779, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.07 / 3.32 GiB.
- Training wall time: 995.9 s; validation wall time: 1,017.2 s; total Run wall time: 2,014.8 s.

This is successful finite/resource evidence for the recurrent temporal change-state formulation. Resource use stayed well inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 12, which was also the final exploratory epoch.

| Metric | ABI-242 best/final epoch 12 |
| --- | ---: |
| Filtered Dice | 0.376521 |
| Raw Dice | 0.391788 |
| Filtered IoU | 0.231922 |
| Filtered precision | 0.384767 |
| Filtered recall | 0.368620 |
| Filtered contrail connectivity | 0.201293 |
| Filtered predicted-positive fraction | 0.004953 |
| Raw predicted-positive fraction | 0.005347 |
| MIT filtered Dice | 0.367296 |
| Google filtered Dice | 0.398964 |
| MIT filtered recall | 0.340495 |
| Google filtered recall | 0.452299 |
| Train loss | 0.801293 |
| Validation loss | 0.856780 |

The selected checkpoint is finite, noncollapsed, and source-informative. Both Dataset Sources retain nontrivial filtered Dice and recall, with Google recall higher than MIT recall. However, the intended recurrent state did not recover line continuity: selected-checkpoint filtered connectivity is only 0.201293, below ABI-241, ABI-240, ABI-238, ABI-223, and ABI-202 comparison points.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.205502 | 0.213222 | 0.184443 | 0.231990 | 0.213416 | 0.189973 | 0.139919 | 0.006502 |
| 2 | 0.244822 | 0.257599 | 0.389698 | 0.178473 | 0.232311 | 0.276156 | 0.314474 | 0.002368 |
| 3 | 0.280408 | 0.292771 | 0.324019 | 0.247143 | 0.273495 | 0.296716 | 0.200845 | 0.003943 |
| 4 | 0.285602 | 0.299248 | 0.343759 | 0.244276 | 0.278849 | 0.301109 | 0.152626 | 0.003674 |
| 5 | 0.310692 | 0.324410 | 0.364920 | 0.270495 | 0.304997 | 0.324024 | 0.151706 | 0.003832 |
| 6 | 0.330758 | 0.344637 | 0.333246 | 0.328307 | 0.324265 | 0.345880 | 0.187506 | 0.005093 |
| 7 | 0.337897 | 0.354289 | 0.453158 | 0.269380 | 0.323631 | 0.375138 | 0.208820 | 0.003073 |
| 8 | 0.357713 | 0.371798 | 0.366453 | 0.349380 | 0.352869 | 0.369481 | 0.170653 | 0.004929 |
| 9 | 0.345981 | 0.358315 | 0.319767 | 0.376877 | 0.337953 | 0.364475 | 0.167877 | 0.006093 |
| 10 | 0.362032 | 0.377213 | 0.383936 | 0.342492 | 0.350598 | 0.391250 | 0.196283 | 0.004612 |
| 11 | 0.350172 | 0.365744 | 0.388796 | 0.318528 | 0.345213 | 0.362075 | 0.175146 | 0.004235 |
| 12 | 0.376521 | 0.391788 | 0.384767 | 0.368620 | 0.367296 | 0.398964 | 0.201293 | 0.004953 |

The trajectory is mostly improving but noisy. Filtered Dice, raw Dice, validation loss, and train loss all reach their best observed values at the final epoch, and the final checkpoint recovers from the epoch-11 dip. This provides bounded late-improving evidence. Connectivity does not follow the same trend: it peaks early at epoch 2 and remains weak later, suggesting the recurrent state learns useful overlap/recall evidence without preserving continuous thin-line structure.

## Comparison context

| Metric | ABI-242 recurrent state | ABI-241 high-res change skip | ABI-240 line-accum late36 | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_055200_52c75f` | `run_20260911_050449_17cdcb` | `run_20260911_031326_43ed12` | `run_20260911_004137_f54c45` | `run_20260908_154531_8c7e2b` | `run_20260904_043143_ee0005` |
| Best epoch | 12 | 11 | 29 | 29 | 36 | 34 |
| Filtered Dice | 0.376521 | 0.384180 | 0.414892 | 0.420235 | 0.419776 | 0.427570 |
| Raw Dice | 0.391788 | 0.399916 | 0.431959 | 0.438718 | 0.438487 | 0.442746 |
| Filtered precision | 0.384767 | 0.400177 | 0.436241 | 0.488730 | 0.483764 | 0.439467 |
| Filtered recall | 0.368620 | 0.369412 | 0.395534 | 0.368578 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.201293 | 0.238980 | 0.264863 | 0.352239 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.367296 | 0.377453 | 0.397067 | 0.405383 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.398964 | 0.401490 | 0.460659 | 0.460838 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004953 | 0.004772 | 0.004687 | 0.003899 | 0.003962 | 0.003433 |

ABI-242 trails ABI-241 by -0.007659 filtered Dice with nearly identical recall and a slightly larger predicted-positive fraction, but lower precision and -0.037687 connectivity. It trails ABI-240 by -0.038371 filtered Dice, -0.026914 recall, and -0.063570 connectivity. Relative to ABI-238/223, ABI-242 roughly matches recall but requires more predicted-positive area, loses substantial precision, and has much weaker connectivity. It is not within 0.02 filtered Dice of the mature temporal frontier and remains below the ABI-202 single-frame frontier on overlap, recall, and connectivity.

## Interpretation

Classify ABI-242 as a finite, nondegenerate recurrent temporal scout with useful late-improving trajectory evidence but weak scientific support for the exact mechanism. The bidirectional ConvGRU-style state appears able to learn source-informative temporal overlap cues and improve through the exploratory ceiling, but it does not produce coherent line support. The low connectivity despite nontrivial recall suggests the state/fusion path may be accumulating fragmented temporal change evidence rather than maintaining contrail-length continuity.

This result does not eliminate temporal recurrent modeling as an architecture family: it is the first compact recurrent change-state scout, it is resource-safe, and the selected checkpoint is the final epoch. It does weaken the case for an unchanged recurrent-state extension as the next highest-value experiment. A late36 continuation is defensible only as a narrow budget probe because the approved longer-budget criteria are partially met; scientifically, the next recurrent-family continuation should change the continuity mechanism, for example by coupling the recurrent state to line-aware decoder support or by moving recurrence into a continuity-preserving feature scale, rather than simply repeating ABI-242 unchanged.

## Decision

Do not promote ABI-242 and do not request whole-validation diagnostics from this capped Result alone. Do not treat the low capped score as eliminating temporal modeling. Treat the exact ABI-242 formulation as resource-safe but connectivity-weak.

Recommended next action is a single in-contract Candidate continuation, not a batch: either a cautious late36 close-continuation if the campaign wants to test whether the final-epoch improvement continues, or preferably a revised recurrent/temporal architecture that adds a continuity-preserving line-state or line-aware decoder coupling while retaining provider-owned `[-1, 0, 1]` temporal inputs and trusted Line/Centerline auxiliary supervision. No Capability Request or Campaign Report is needed for this decision.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_055200_52c75f/candidate/PROPOSAL.md`
- `run_20260911_055200_52c75f/candidate/README.md`
- `run_20260911_055200_52c75f/candidate/manifest.yaml`
- `run_20260911_055200_52c75f/resolved_manifest.yaml`
- `run_20260911_055200_52c75f/outputs/model_summary.json`
- `run_20260911_055200_52c75f/outputs/best_metrics.json`
- `run_20260911_055200_52c75f/outputs/final_metrics.json`
- `run_20260911_055200_52c75f/outputs/metrics.jsonl`
- `run_20260911_055200_52c75f/outputs/resource_profile.json`
- `run_20260911_055200_52c75f/outputs/validation_postprocessing/index.json`
- `run_20260911_055200_52c75f/outputs/prediction_samples/samples.json`
- `run_20260911_050449_17cdcb` for ABI-241 high-resolution temporal change-skip context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
