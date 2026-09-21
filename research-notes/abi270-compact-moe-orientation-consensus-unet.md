# ABI-270 compact MoE orientation-consensus U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-270, Candidate `abi270_fullspectral_btd_sza_compact_moe_orientation_consensus_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_151011_98165f`.

ABI-270 was a mechanism-changing continuation of the compact spectral/Solar Geometry Input mixture-of-experts branch after ABI-269. It kept the ABI-268/269 resource-safe compact MoE body but replaced the final line head with a conservative high-resolution multi-orientation consensus head intended to recover connected thin-line continuity without candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, coordinates, Dataset Source identity, or resource scheduling.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` inputs, used trusted `combined_source_balanced` sampling, `random_mirroring`, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary outputs. Candidate code remained architecture-only.

## Execution result

ABI-270 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,799,307, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 7.89 / 8.39 GB.
- Training wall time: 915.9 s; validation wall time: 1,120.5 s; total Run wall time: 2,038.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 9.

This is valid finite capped-validation evidence for the compact MoE plus orientation-consensus head. It is not whole-validation promotion evidence.

## Best-validation metrics

| Metric | ABI-270 best epoch 9 | ABI-269 compact MoE late36 | ABI-268 compact MoE parent | ABI-265 axial line-memory late36 | ABI-249 C4 line-context | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.376522 | 0.410444 | 0.398540 | 0.411977 | 0.416400 | 0.427570 |
| Raw Dice | 0.389645 | 0.424777 | 0.413801 | 0.427098 | 0.432320 | 0.442746 |
| Filtered precision | 0.371120 | 0.427505 | 0.446572 | 0.433940 | 0.480886 | 0.439467 |
| Filtered recall | 0.382084 | 0.394692 | 0.359837 | 0.392130 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.277459 | 0.318646 | 0.360615 | 0.433071 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.372338 | 0.394541 | 0.386144 | 0.401437 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.386156 | 0.450109 | 0.429981 | 0.438974 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003731 | 0.003346 | 0.002920 | 0.003275 | 0.002767 | 0.003433 |

ABI-270 underperformed ABI-269 by about -0.0339 filtered Dice, -0.0564 precision, -0.0126 recall, -0.0412 connectivity, -0.0222 MIT filtered Dice, and -0.0640 Google filtered Dice. Relative to the exploratory ABI-268 parent, it improved recall by about +0.0222 but lost about -0.0220 filtered Dice, -0.0755 precision, -0.0832 connectivity, and substantial Google/source balance. The orientation-consensus head therefore did not recover the compact MoE branch's connected-line weakness; it mostly made the selected checkpoint less precise and less source-balanced.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.211976 | 0.219128 | 0.198847 | 0.197045 | 0.229354 | 0.152438 | 0.004218 |
| 2 | 0.279072 | 0.287454 | 0.263681 | 0.242937 | 0.327836 | 0.146794 | 0.004890 |
| 3 | 0.308336 | 0.317345 | 0.291189 | 0.272636 | 0.354793 | 0.170207 | 0.004716 |
| 4 | 0.323822 | 0.319284 | 0.333794 | 0.324743 | 0.322906 | 0.206825 | 0.003603 |
| 5 | 0.321360 | 0.306899 | 0.354459 | 0.410607 | 0.263982 | 0.253095 | 0.002330 |
| 6 | 0.351812 | 0.353772 | 0.347719 | 0.334311 | 0.371246 | 0.208406 | 0.004024 |
| 7 | 0.359664 | 0.355656 | 0.368672 | 0.377820 | 0.343172 | 0.275703 | 0.003291 |
| 8 | 0.364231 | 0.361780 | 0.369773 | 0.363645 | 0.364819 | 0.230771 | 0.003635 |
| 9 | 0.376522 | 0.372338 | 0.386156 | 0.371120 | 0.382084 | 0.277459 | 0.003731 |
| 10 | 0.352837 | 0.336159 | 0.391717 | 0.444644 | 0.292453 | 0.320350 | 0.002383 |
| 11 | 0.370744 | 0.371171 | 0.369712 | 0.373406 | 0.368119 | 0.246731 | 0.003572 |
| 12 | 0.360450 | 0.339636 | 0.410249 | 0.431697 | 0.309389 | 0.291778 | 0.002597 |

The trajectory is finite and non-collapsed, but it is not late-improving. The best aggregate checkpoint occurs at epoch 9, then filtered Dice falls at epochs 10 and 12. Epoch 10 has the best connectivity for this run, but it reaches only 0.320350 and comes with low aggregate Dice, low MIT Dice, and low recall. The final epoch has the highest Google filtered Dice but a weak MIT score and recall drop, so it does not justify a late-improving continuation.

## Interpretation

Classify ABI-270 as a finite negative mechanism test. The conservative multi-orientation consensus head is resource-safe, but its selected checkpoint does not improve the intended connected-line metric versus ABI-269 or ABI-268. It also does not preserve ABI-269's Google/source lift or ABI-249-style precision. The added high-resolution orientation branches increase peak memory versus ABI-269 while delivering lower capped metrics.

This result is useful because it narrows the compact MoE continuity path: simply adding an agreement-gated orientation head at the final high-resolution stage is not sufficient to repair connected thin-line continuity. The failure mode is architectural rather than contractual or resource-related, so the exact ABI-270 head should not be repeated unchanged.

## Decision

Do not promote ABI-270, do not request whole-validation diagnostics, and do not request a late-improving budget for this exact orientation-consensus head. It is below ABI-269, ABI-268, ABI-265, ABI-249, and ABI-202 on selected-checkpoint filtered Dice and connectivity, and its best epoch is not late.

Future compact MoE work should be mechanism-changing if continued at all: for example, line continuity would need to be integrated earlier in the decoder or into the MoE state rather than appended as a final conservative head. Higher-value next hypotheses remain ABI-249-style C4/orientation priors plus recall/connectivity support, ABI-223-style temporal evidence sharpening, bounded line-continuity mechanisms with source-balanced behavior, or recall-preserving calibration/dual-evidence heads.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_151011_98165f/candidate/PROPOSAL.md`
- `run_20260912_151011_98165f/candidate/README.md`
- `run_20260912_151011_98165f/candidate/manifest.yaml`
- `run_20260912_151011_98165f/resolved_manifest.yaml`
- `run_20260912_151011_98165f/outputs/model_summary.json`
- `run_20260912_151011_98165f/outputs/best_metrics.json`
- `run_20260912_151011_98165f/outputs/final_metrics.json`
- `run_20260912_151011_98165f/outputs/metrics.jsonl`
- `run_20260912_151011_98165f/outputs/resource_profile.json`
- `run_20260912_151011_98165f/outputs/validation_postprocessing/index.json`
- `run_20260912_151011_98165f/outputs/prediction_samples/samples.json`
- `run_20260912_121857_19f67d` for ABI-269 compact MoE late36 context
- `run_20260912_113911_7a5f94` for ABI-268 compact MoE parent context
- `run_20260912_065321_ceab64` for ABI-265 selective axial line-memory context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
