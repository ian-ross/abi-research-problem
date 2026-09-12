# ABI-257 temporal oriented recurrent line-state U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-257, Candidate `abi257_temporal_oriented_recurrent_line_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_235337_128345`.

ABI-257 was a mechanism-changing temporal recurrent family-development Candidate after ABI-255 and ABI-256. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 2, constant learning rate, and trusted Line/Centerline auxiliary outputs. The intended change was to move oriented line evidence into the temporal recurrent stem: frame embeddings were processed by an oriented line bank, center-anchored temporal line deltas were fused with bidirectional recurrent state and before/after change evidence, and the compact U-Net decoder consumed this line-aware temporal state.

Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-257 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,207,843, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.01 / 5.23 GB.
- Training wall time: 1,382.8 s; validation wall time: 1,145.0 s; total Run wall time: 2,529.5 s.

This is valid finite/resource evidence for the oriented recurrent line-state stem, but only capped temporal-eligible feasibility evidence, not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 9.

| Metric | ABI-257 best epoch 9 | ABI-257 final epoch 12 | ABI-256 centerline decoder | ABI-255 recurrent late36 | ABI-223 temporal-attn late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.375124 | 0.364019 | 0.388988 | 0.417348 | 0.419776 | 0.427570 |
| Raw Dice | 0.390882 | 0.380317 | 0.404980 | 0.435656 | 0.438487 | 0.442746 |
| Filtered precision | 0.391551 | 0.430668 | 0.415080 | 0.468293 | 0.483764 | 0.439467 |
| Filtered recall | 0.360020 | 0.315234 | 0.365981 | 0.376400 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.213486 | 0.254312 | 0.246300 | 0.281116 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.363565 | 0.348094 | 0.367406 | 0.400833 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.402919 | 0.404380 | 0.443100 | 0.463143 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004753 | 0.003784 | 0.004558 | 0.004155 | 0.003962 | 0.003433 |

Relative to ABI-255, ABI-257 regressed filtered Dice by about -0.0422, raw Dice by -0.0448, precision by -0.0767, recall by -0.0164, connectivity by -0.0676, MIT filtered Dice by -0.0373, and Google filtered Dice by -0.0602 at the selected checkpoint. Relative to ABI-256, ABI-257 also regressed filtered Dice, raw Dice, precision, recall, and Google Dice; its final epoch reached slightly higher connectivity than ABI-256's selected checkpoint, but only after losing additional overlap and recall.

The oriented recurrent line-state stem therefore did not meet its primary success criterion. Moving line evidence into the recurrent stem did not recover the ABI-255 connectivity deficit and did not outperform the previous decoder-side bridge.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232133 | 0.230550 | 0.235967 | 0.306262 | 0.186896 | 0.199872 | 0.003155 |
| 2 | 0.248119 | 0.255485 | 0.233096 | 0.226982 | 0.273597 | 0.135238 | 0.006231 |
| 3 | 0.297868 | 0.288763 | 0.318264 | 0.321713 | 0.277315 | 0.236710 | 0.004456 |
| 4 | 0.286130 | 0.269881 | 0.323987 | 0.338813 | 0.247626 | 0.138429 | 0.003778 |
| 5 | 0.322677 | 0.313039 | 0.345975 | 0.388431 | 0.275961 | 0.153084 | 0.003673 |
| 6 | 0.351664 | 0.344272 | 0.369418 | 0.365547 | 0.338797 | 0.193477 | 0.004791 |
| 7 | 0.281865 | 0.257235 | 0.347538 | 0.541187 | 0.190555 | 0.407937 | 0.001820 |
| 8 | 0.353063 | 0.337752 | 0.391600 | 0.393623 | 0.320081 | 0.231630 | 0.004204 |
| 9 | 0.375124 | 0.363565 | 0.402919 | 0.391551 | 0.360020 | 0.213486 | 0.004753 |
| 10 | 0.371780 | 0.358566 | 0.403756 | 0.428032 | 0.328596 | 0.210630 | 0.003969 |
| 11 | 0.363997 | 0.348720 | 0.401110 | 0.401700 | 0.332763 | 0.226606 | 0.004282 |
| 12 | 0.364019 | 0.348094 | 0.404380 | 0.430668 | 0.315234 | 0.254312 | 0.003784 |

The trajectory is finite and non-collapsed, but it is not late-improving on the primary selection metric. Filtered Dice peaks at epoch 9 and then declines/plateaus. The highest connectivity checkpoint, epoch 7, reaches 0.407937 only by shrinking predicted positives to 0.001820 and collapsing recall to 0.190555, similar to the unstable high-connectivity/low-recall behavior seen in ABI-256. By the selected Dice checkpoint, connectivity is below ABI-255 and below ABI-256's final checkpoint.

## Interpretation

Classify ABI-257 as a negative/mixed family-development Result for this exact oriented recurrent line-state stem. It confirms that the mechanism is resource-safe and source-informative, but the architecture did not solve the recurrent temporal branch's main weakness. The oriented line bank can form compact high-connectivity states, but those states are too conservative at the trusted threshold; when recall and overlap recover, the continuity advantage disappears.

This outcome should not be interpreted as eliminating temporal modeling or recurrent temporal evidence. ABI-255 remains useful compact recurrent temporal evidence, and ABI-223/238 remain stronger temporal attention/connectivity comparators. ABI-257 only argues against this exact stem as the next recurrent repair path, especially without a clear late-improving signal.

## Decision

Do not promote ABI-257. Do not submit an unchanged late36 continuation of this exact oriented recurrent line-state stem: the best checkpoint was epoch 9, final epoch 12 did not recover primary Dice, and the connectivity gains occurred only at a low-recall operating point.

If the campaign continues with temporal modeling, prefer a different mechanism rather than another local recurrent-stem repair: for example, return to temporal attention/change architectures that preserve ABI-223/238 connectivity, combine attention-style temporal evidence with explicit recall-preserving calibration/evidence heads, or broaden away from temporal modeling into a non-temporal rotation-aware line scout. Any follow-up must continue to avoid Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_235337_128345/candidate/PROPOSAL.md`
- `run_20260911_235337_128345/candidate/README.md`
- `run_20260911_235337_128345/candidate/manifest.yaml`
- `run_20260911_235337_128345/resolved_manifest.yaml`
- `run_20260911_235337_128345/outputs/model_summary.json`
- `run_20260911_235337_128345/outputs/best_metrics.json`
- `run_20260911_235337_128345/outputs/final_metrics.json`
- `run_20260911_235337_128345/outputs/metrics.jsonl`
- `run_20260911_235337_128345/outputs/resource_profile.json`
- `run_20260911_235337_128345/outputs/validation_postprocessing/index.json`
- `run_20260911_235337_128345/outputs/prediction_samples/samples.json`
- `run_20260911_230821_08caf0` for ABI-256 centerline-decoder bridge context
- `run_20260911_210922_27f346` for ABI-255 recurrent late36 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-attention late36 context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
