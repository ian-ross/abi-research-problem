# ABI-286 temporal C4 continuity-evidence bridge U-Net

research-figures: []

## Scope

This note records ABI-286, Candidate `abi286_temporal_c4_continuity_evidence_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_123056_4152f3`.

ABI-286 is a mechanism-changing temporal-family continuation after ABI-285. ABI-285 produced strong capped temporal-eligible aggregate filtered Dice and recall, but its temporal-eligible failure-bucket review highlighted weak connected-line continuity and broader negative-patch clutter. ABI-286 keeps ABI-285's provider-owned temporal input path, offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, temporal attention/change stem, and early C4 orientation line state, then adds a full-resolution continuity-evidence bridge and dual evidence mask head after the decoder.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-286 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,315,269, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.55 / 6.86 GiB.
- Training wall time: 1,857.7 s; validation wall time: 1,155.6 s; total Run wall time: 3,015.2 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 8.

## Best-validation metrics

| Metric | ABI-286 best epoch 8 | ABI-286 final epoch 12 | ABI-285 temporal C4 late36 | ABI-284 temporal C4 exploratory | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 | ABI-238 temporal directional-context late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.393183 | 0.392836 | 0.422195 | 0.390090 | 0.419364 | 0.419776 | 0.420235 |
| Raw Dice | 0.409514 | 0.410837 | 0.439439 | 0.408012 | 0.436760 | 0.438487 | 0.438718 |
| Filtered precision | 0.419944 | 0.490766 | 0.448400 | 0.475285 | 0.454127 | 0.483764 | 0.488730 |
| Filtered recall | 0.369628 | 0.327487 | 0.398883 | 0.330796 | 0.389545 | 0.370738 | 0.368578 |
| Filtered connectivity | 0.280479 | 0.326472 | 0.243387 | 0.254710 | 0.282911 | 0.412427 | 0.352239 |
| MIT filtered Dice | 0.381112 | 0.373144 | 0.400831 | 0.371847 | 0.399386 | 0.398498 | 0.405383 |
| Google filtered Dice | 0.424115 | 0.444910 | 0.477410 | 0.436956 | 0.472606 | 0.476764 | 0.460838 |
| Filtered predicted-positive fraction | 0.004550 | 0.003450 | 0.004599 | 0.003598 | 0.004434 | 0.003962 | 0.003899 |
| Filtered predicted-positive pixels | 481,295 | 364,701 | 486,427 | 380,578 | 469,049 | 419,056 | 412,381 |

The continuity-evidence bridge produced mixed mechanism evidence. Relative to ABI-284's exploratory parent, ABI-286 is slightly higher on best filtered Dice (+0.0031), recall (+0.0388), MIT Dice (+0.0093), and connectivity (+0.0258), but lower on precision (-0.0553) and Google Dice (-0.0128). At the final epoch, ABI-286 is also similar in aggregate Dice to ABI-284 while showing much higher connectivity (+0.0718) and precision (+0.0155) with nearly equal recall (-0.0033). Thus the bridge does improve connectivity relative to the 12-epoch temporal C4 parent, especially by the final checkpoint.

Relative to ABI-285's late36 best checkpoint, ABI-286 does not preserve the stronger aggregate/recall/source-balance result: filtered Dice falls by 0.0290, recall by 0.0293, MIT Dice by 0.0197, and Google Dice by 0.0533. Connectivity improves by 0.0371 at ABI-286's selected checkpoint and by 0.0831 at its final epoch, but that gain is not enough to match ABI-274, ABI-223, or ABI-238 aggregate temporal-eligible performance. ABI-286 remains especially below ABI-223 and ABI-238 on connected-line continuity.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.230250 | 0.228793 | 0.233823 | 0.309991 | 0.183140 | 0.198870 | 0.003054 |
| 2 | 0.246607 | 0.241177 | 0.258213 | 0.241458 | 0.251981 | 0.115928 | 0.005395 |
| 3 | 0.310713 | 0.300477 | 0.333614 | 0.320455 | 0.301546 | 0.197762 | 0.004865 |
| 4 | 0.278795 | 0.252585 | 0.345617 | 0.444247 | 0.203139 | 0.246139 | 0.002364 |
| 5 | 0.348072 | 0.325028 | 0.407737 | 0.499209 | 0.267181 | 0.358163 | 0.002767 |
| 6 | 0.337601 | 0.312420 | 0.402043 | 0.464416 | 0.265188 | 0.300026 | 0.002952 |
| 7 | 0.339795 | 0.312625 | 0.412781 | 0.562089 | 0.243497 | 0.438765 | 0.002239 |
| 8 | 0.393183 | 0.381112 | 0.424115 | 0.419944 | 0.369628 | 0.280479 | 0.004550 |
| 9 | 0.376089 | 0.361843 | 0.410842 | 0.345913 | 0.412034 | 0.229327 | 0.006158 |
| 10 | 0.385215 | 0.364866 | 0.436946 | 0.450073 | 0.336695 | 0.291438 | 0.003867 |
| 11 | 0.370479 | 0.345301 | 0.436126 | 0.488316 | 0.298457 | 0.367820 | 0.003160 |
| 12 | 0.392836 | 0.373144 | 0.444910 | 0.490766 | 0.327487 | 0.326472 | 0.003450 |

The trajectory is finite, source-informative, and non-collapsed, but oscillatory. Epoch 8 is the aggregate-Dice optimum and is the only checkpoint combining recall near 0.37 with Dice near 0.393. Epoch 9 reaches the Run's highest recall, but with a broader footprint, lower precision, and lower connectivity. Epoch 12 nearly recovers the best aggregate Dice while shifting to a more compact, higher-precision, higher-connectivity state. That final state is useful evidence that the bridge can support continuity, but the 12-epoch budget does not show stable improvement into the ABI-285/274/223/238 temporal-eligible frontier.

Raw-to-filtered differences are modest and directionally conservative at the selected checkpoint: raw Dice 0.4095 versus filtered Dice 0.3932, and raw predicted-positive pixels 518,890 versus filtered predicted-positive pixels 481,295. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3304, 0.3226, 0.6435, and 0.3977. This is consistent with finite non-collapsed predictions and some strong per-sample behavior, but it does not establish aggregate promotion evidence.

## Interpretation

Classify ABI-286 as a finite, resource-safe, scientifically mixed temporal-family mechanism test. The full-resolution continuity-evidence bridge appears to improve connected-line organization relative to the immediate 12-epoch ABI-284 temporal C4 parent, particularly at the final epoch. It does not, however, preserve ABI-285's late36 recall/source-balance gains or reach ABI-223/238 connected-line continuity.

This means the bridge mechanism is not a new temporal frontier by itself. It is more useful as a diagnostic component: full-resolution continuity support can raise connectivity, but in this implementation it trades away too much aggregate and source-stratified Dice compared with the current temporal comparator set. The branch should not receive an unchanged late36 continuation unless there is a specific reason to believe the epoch-12 compact/high-connectivity state is still improving; the trajectory is ambiguous rather than clearly late-improving, and ABI-285 already showed that the related branch can become recall-heavy while still connectivity-limited.

## Decision

Do not promote ABI-286 and do not request whole-validation diagnostics from this capped temporal-eligible result. Do not repeat the exact ABI-286 bridge unchanged as an immediate late36 run. Future temporal work should keep the useful lesson--decoder-resolution continuity evidence can improve connectivity--but change the mechanism to preserve ABI-285-style recall/source balance, for example by a less suppressive bridge, explicit dual-path recall protection, or a calibrated evidence head that does not move thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_123056_4152f3/candidate/PROPOSAL.md`
- `run_20260913_123056_4152f3/candidate/README.md`
- `run_20260913_123056_4152f3/candidate/manifest.yaml`
- `run_20260913_123056_4152f3/resolved_manifest.yaml`
- `run_20260913_123056_4152f3/execution.json`
- `run_20260913_123056_4152f3/outputs/model_summary.json`
- `run_20260913_123056_4152f3/outputs/best_metrics.json`
- `run_20260913_123056_4152f3/outputs/final_metrics.json`
- `run_20260913_123056_4152f3/outputs/metrics.jsonl`
- `run_20260913_123056_4152f3/outputs/resource_profile.json`
- `run_20260913_123056_4152f3/outputs/validation_postprocessing/index.json`
- `run_20260913_123056_4152f3/outputs/prediction_samples/samples.json`
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260913_091156_167372/outputs/best_metrics.json` for ABI-284 temporal C4 exploratory comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context late36 comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
