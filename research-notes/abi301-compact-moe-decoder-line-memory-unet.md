# ABI-301 compact MoE decoder line-memory U-Net

research-figures: []

## Scope

This note records ABI-301, Candidate `abi301_fullspectral_btd_sza_compact_moe_decoder_line_memory_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_055639_e6bfa3`.

ABI-301 was a bounded compact spectral/Solar Geometry Input mixture-of-experts family-development continuation after ABI-269 and ABI-270. ABI-269 recovered aggregate/source balance under the approved late budget but still had weak connected-line continuity. ABI-270 tested a final high-resolution orientation-consensus head and did not repair that weakness. ABI-301 moved multi-orientation line-memory support into the decoder stages so line evidence could shape features before final logits rather than act as a late conservative head.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` tensors. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-301 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 2,090,400, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 14,832,402,944 / 15,430,844,416 bytes.
- Training wall time: 1,585.7 s; validation wall time: 1,321.6 s; total Run wall time: 2,909.2 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-301 decoder line-memory MoE | ABI-270 final-head orientation MoE | ABI-269 compact MoE late36 | ABI-268 compact MoE parent | ABI-265 axial line-memory | ABI-249 C4 line-context | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 9 | 34 | 12 | 34 | 31 | 34 |
| Filtered Dice | 0.378359 | 0.376522 | 0.410444 | 0.398540 | 0.411977 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.368502 | 0.372338 | 0.394541 | 0.386144 | 0.401437 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.401508 | 0.386156 | 0.450109 | 0.429981 | 0.438974 | 0.468855 | 0.468151 |
| Filtered precision | 0.397998 | 0.371120 | 0.427505 | 0.446572 | 0.433940 | 0.480886 | 0.439467 |
| Filtered recall | 0.360567 | 0.382084 | 0.394692 | 0.359837 | 0.392130 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.208908 | 0.277459 | 0.318646 | 0.360615 | 0.433071 | 0.392524 | 0.457773 |
| Filtered predicted-positive fraction | 0.003283 | 0.003731 | 0.003346 | 0.002920 | 0.003275 | 0.002767 | 0.003433 |

ABI-301 is a completed but negative compact-MoE line-continuity result. It slightly improves filtered Dice over ABI-270 (+0.0018) and raises precision/Google Dice versus that final-head orientation experiment, but it loses ABI-270 recall and sharply loses connectivity. More importantly, it remains far below ABI-269 late36, ABI-268, ABI-265, ABI-249, and ABI-202 on the proposal's target connected-line metric.

Relative to ABI-269, ABI-301 loses about -0.0321 filtered Dice, -0.0260 MIT filtered Dice, -0.0486 Google filtered Dice, -0.0295 precision, -0.0341 recall, and -0.1097 connectivity. Relative to ABI-268, it is also lower on aggregate/source Dice and connectivity, with only a negligible recall tie. The decoder-level line-memory mechanism therefore did not preserve the compact MoE branch's late-budget source balance and did not recover the connected-line weakness.

At the selected checkpoint, raw Dice was 0.391980 versus filtered Dice 0.378359, raw recall was 0.384892 versus filtered recall 0.360567, and raw predicted-positive fraction was 0.003493 versus filtered predicted-positive fraction 0.003283. Artifact Filters remove some footprint, but they do not create the result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.219173 | 0.230210 | 0.198410 | 0.196552 | 0.247678 | 0.082451 | 0.004566 |
| 2 | 0.294058 | 0.287636 | 0.308619 | 0.344747 | 0.256365 | 0.184719 | 0.002695 |
| 3 | 0.307885 | 0.298162 | 0.329162 | 0.320960 | 0.295833 | 0.190716 | 0.003340 |
| 4 | 0.314496 | 0.311563 | 0.320686 | 0.277102 | 0.363556 | 0.166573 | 0.004754 |
| 5 | 0.342580 | 0.329147 | 0.373646 | 0.400586 | 0.299248 | 0.263704 | 0.002707 |
| 6 | 0.346732 | 0.336586 | 0.370273 | 0.361115 | 0.333451 | 0.204601 | 0.003346 |
| 7 | 0.347381 | 0.354662 | 0.332511 | 0.305983 | 0.401734 | 0.154598 | 0.004758 |
| 8 | 0.363057 | 0.349609 | 0.394967 | 0.421497 | 0.318849 | 0.220445 | 0.002741 |
| 9 | 0.378359 | 0.368502 | 0.401508 | 0.397998 | 0.360567 | 0.208908 | 0.003283 |
| 10 | 0.367861 | 0.350956 | 0.407855 | 0.427558 | 0.322792 | 0.225307 | 0.002736 |
| 11 | 0.371877 | 0.372022 | 0.371553 | 0.365980 | 0.377967 | 0.166014 | 0.003742 |
| 12 | 0.375515 | 0.366147 | 0.397373 | 0.404907 | 0.350101 | 0.219885 | 0.003133 |

The trajectory is finite, non-collapsed, and source-informative, but it is not late-improving evidence for an unchanged 36-epoch continuation. The selected checkpoint is epoch 9. Epoch 12 nearly recovers the selected filtered Dice and slightly improves connectivity over epoch 9, but it remains lower on the primary metric, lower on recall, and far below the line-continuity comparators. The trajectory is better interpreted as an oscillatory precision/recall/source-balance surface than as a branch still cleanly improving toward the proposal's success criteria.

The retained fixed `first_n` prediction samples all have near-zero per-sample Dice. They are traceability artifacts selected by the Harness retention policy, not representative diagnostics. Population metrics and predicted-positive fractions show the model is not an all-negative collapse, but the retained samples do not supply qualitative support for promotion.

## Interpretation

Classify ABI-301 as a finite, resource-safe, scientifically useful negative result for integrated decoder-stage line memory in the compact MoE branch. Moving line-memory blocks earlier in the decoder avoided the exact ABI-270 final-head design, but it did not couple continuity support to recall. Instead, the branch stayed below the compact MoE parent/late36 lineage and lost substantial connected-line evidence versus ABI-269, ABI-268, ABI-265, ABI-249, and ABI-202.

This should not eliminate line-continuity mechanisms broadly, but it does narrow the compact spectral/Solar Geometry Input MoE branch. ABI-269 remains the compact MoE aggregate comparator, not a frontier, and ABI-301 does not supply a reason to spend an unchanged late36 budget on the decoder-line-memory variant. The failure mode is architectural rather than contractual or resource-related: the mechanism added cost and line-memory structure without stabilizing connected thin-line predictions.

Future work should not repeat ABI-301 unchanged. If MoE work continues, it should be mechanism-changing and address why line support collapses into a weak connectivity/precision-recall trade-off. Higher-value next hypotheses are more likely in a different frontier: C4/orientation priors with recall/connectivity support, temporal attention with a stronger line organization mechanism, or a bounded non-MoE line accumulation design. Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-301. Do not request whole-validation diagnostics for this capped Result. Do not request an unchanged late-improving continuation of ABI-301; the run peaks at epoch 9 and the final epoch remains below the selected checkpoint and far below the intended connectivity comparators.

Record ABI-301 as a bounded negative result for decoder-integrated line memory in the compact MoE family. Stop this exact compact MoE line-continuity branch unless a future proposal changes the mechanism substantially.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_055639_e6bfa3/candidate/PROPOSAL.md`
- `run_20260914_055639_e6bfa3/candidate/README.md`
- `run_20260914_055639_e6bfa3/candidate/manifest.yaml`
- `run_20260914_055639_e6bfa3/resolved_manifest.yaml`
- `run_20260914_055639_e6bfa3/execution.json`
- `run_20260914_055639_e6bfa3/outputs/model_summary.json`
- `run_20260914_055639_e6bfa3/outputs/best_metrics.json`
- `run_20260914_055639_e6bfa3/outputs/final_metrics.json`
- `run_20260914_055639_e6bfa3/outputs/metrics.jsonl`
- `run_20260914_055639_e6bfa3/outputs/resource_profile.json`
- `run_20260914_055639_e6bfa3/outputs/validation_postprocessing/index.json`
- `run_20260914_055639_e6bfa3/outputs/prediction_samples/samples.json`
- `run_20260912_151011_98165f/outputs/best_metrics.json` and `/history/research-notes/abi270-compact-moe-orientation-consensus-unet.md` for ABI-270 final-head orientation context
- `run_20260912_121857_19f67d/outputs/best_metrics.json` and `/history/research-notes/abi269-compact-spectral-moe-line-unet-late36.md` for ABI-269 compact MoE late36 context
- `run_20260912_113911_7a5f94/outputs/best_metrics.json` for ABI-268 compact MoE parent context
- `run_20260912_065321_ceab64/outputs/best_metrics.json` for ABI-265 selective axial line-memory context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 current aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
