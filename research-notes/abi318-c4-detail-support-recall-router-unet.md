# ABI-318 C4 detail/support recall-router U-Net

research-figures: []

## Scope

This note records ABI-318, Candidate `abi318_fullspectral_btd_sza_c4_detail_support_recall_router_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260915_151751_5a903e`.

ABI-318 was a bounded exploratory single-frame family-development continuation in the full-spectral BTD+Solar Geometry Input C4/orientation-prior branch. It kept provider-approved `abi_16ch_plus_sza` inputs and a compact C4 steerable line-context U-Net lineage, then replaced stricter protected/suppressive recall heads with a `C4DetailSupportRecallRouterHead`. The intended mechanism was to add a small bounded non-negative recall lift when C4 line context, signed high-resolution detail, and cross-scale decoder support agreed, while using a learned guard to attenuate disagreement.

The candidate did not implement Candidate-owned thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom loss, metric computation, data loading, sample selection, coordinate features, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-318 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,211,859, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 11,626,923,008 / 13,230,931,968 bytes.
- Training wall time: 1,628.3 s; validation wall time: 1,422.9 s; total Run wall time: 3,053.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 10.

## Best-validation metrics

| Metric | ABI-318 detail/support router | ABI-202 aggregate reference | ABI-249 compact C4 | ABI-279 C4 recall bridge | ABI-280 selective C4 | ABI-303 protected C4 | ABI-317 message passing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 10 | 34 | 31 | 22 | 22 | 9 | 12 |
| Filtered Dice | 0.380757 | 0.427570 | 0.416400 | 0.414518 | 0.415244 | 0.377921 | 0.378578 |
| MIT filtered Dice | 0.368268 | 0.411992 | 0.396436 | 0.398381 | 0.405113 | 0.361436 | 0.358874 |
| Google filtered Dice | 0.409862 | 0.468151 | 0.468855 | 0.457385 | 0.442121 | 0.419321 | 0.429382 |
| Filtered precision | 0.421317 | 0.439467 | 0.480886 | 0.442551 | 0.425162 | 0.446396 | 0.430076 |
| Filtered recall | 0.347322 | 0.416301 | 0.367165 | 0.389825 | 0.405778 | 0.327659 | 0.338094 |
| Filtered connectivity | 0.293015 | 0.457773 | 0.392524 | 0.439185 | 0.316291 | 0.322926 | 0.384513 |
| Filtered predicted-positive fraction | 0.002987 | 0.003433 | 0.002767 | 0.003192 | 0.003458 | 0.002660 | 0.002849 |

ABI-318 is finite and source-informative, but it is not a frontier Result. It is only slightly above ABI-303 and ABI-317 in aggregate filtered Dice. Relative to ABI-303, the router gained about +0.0028 filtered Dice, +0.0197 recall, and +0.0068 MIT Dice, but it lost precision, Google Dice, and connectivity. Relative to ABI-317, it gained about +0.0022 filtered Dice and +0.0092 recall, but lost about -0.0905 connectivity and -0.0195 Google Dice.

Against the actual comparators, the gap is larger. ABI-318 is below ABI-249 by about -0.0356 filtered Dice, -0.0282 MIT Dice, -0.0590 Google Dice, -0.0596 precision, -0.0198 recall, and -0.0995 connectivity. Against ABI-279/280, ABI-318 does not preserve the recall-bridge gains; against ABI-202 it remains lower by about -0.0468 filtered Dice, -0.0437 MIT Dice, -0.0583 Google Dice, -0.0182 precision, -0.0690 recall, and -0.1648 connectivity.

At the selected checkpoint, raw Dice was 0.394898 versus filtered Dice 0.380757, raw recall was 0.372287 versus filtered recall 0.347322, and raw predicted-positive fraction was 0.003166 versus filtered predicted-positive fraction 0.002987. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.214152 | 0.237425 | 0.174612 | 0.169160 | 0.291748 | 0.132019 | 0.006250 |
| 2 | 0.204083 | 0.244461 | 0.148443 | 0.136630 | 0.403076 | 0.108628 | 0.010690 |
| 3 | 0.296508 | 0.303160 | 0.283465 | 0.263467 | 0.339023 | 0.155630 | 0.004663 |
| 4 | 0.286500 | 0.285445 | 0.288697 | 0.270155 | 0.304950 | 0.133416 | 0.004090 |
| 5 | 0.355124 | 0.350979 | 0.365039 | 0.332659 | 0.380844 | 0.263124 | 0.004149 |
| 6 | 0.318753 | 0.315766 | 0.324631 | 0.288089 | 0.356724 | 0.210502 | 0.004487 |
| 7 | 0.354104 | 0.348596 | 0.366708 | 0.340036 | 0.369385 | 0.203270 | 0.003936 |
| 8 | 0.360619 | 0.344062 | 0.400438 | 0.413759 | 0.319575 | 0.257244 | 0.002799 |
| 9 | 0.373968 | 0.364052 | 0.397753 | 0.380157 | 0.367977 | 0.239487 | 0.003508 |
| 10 | 0.380757 | 0.368268 | 0.409862 | 0.421317 | 0.347322 | 0.293015 | 0.002987 |
| 11 | 0.362361 | 0.350520 | 0.390144 | 0.340413 | 0.387335 | 0.206309 | 0.004123 |
| 12 | 0.363509 | 0.352646 | 0.391389 | 0.422019 | 0.319248 | 0.323627 | 0.002741 |

The trajectory is finite and non-collapsed, but it does not justify a late-improving continuation. The best checkpoint occurs at epoch 10, not the final epoch, and the final two epochs trade recall, precision, and connectivity without improving aggregate Dice. Epoch 11 reached the run's highest selected recall (0.3873) but did so with lower precision, lower Dice, and weak connectivity; epoch 12 regained some connectivity but lost recall. This indicates an oscillating calibration surface rather than a clearly truncated learning curve.

The source split is source-informative but not favorable. The best checkpoint's MIT/Google filtered-Dice gap is about 0.0416, which is smaller than ABI-317's gap, but both sources are still materially below ABI-202/249/279/280. The branch therefore did not solve the intended C4 high-precision/low-recall trade-off.

## Prediction sample check

The retained fixed first-four validation prediction samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 1.0, 1.0, near zero, and near zero. This confirms finite retained outputs but does not provide qualitative evidence for promotion or elimination.

## Interpretation

Classify ABI-318 as a valid, resource-feasible, scientifically useful but negative/mixed C4 detail-support recall-router scout. The bounded non-negative router is safer than broad clutter-producing recall heads and slightly improves over ABI-303/317 aggregate Dice, but the effect size is small and comes with weak connected-line evidence. The mechanism does not recover ABI-249's precision, ABI-279/280's recall balance, or ABI-202's aggregate/connectivity frontier.

The main lesson is that another late residual head over compact C4 predictions is not enough. The router can move the threshold-0.5 footprint, but it alternates among under-recall, lower-precision recall, and low-connectivity states. Future work should avoid unchanged C4 residual-head continuations and should instead broaden to a mechanism that directly raises true contrail evidence while preserving continuity, such as temporal evidence sharpening, a materially different line-continuity architecture, or a trusted loss/calibration policy if made available through the contract.

## Decision

Do not promote ABI-318. Do not request whole-validation diagnostics for this capped exploratory Result. Do not request an unchanged late36 continuation: the best epoch was not final, the final trajectory regressed/oscillated, and the selected metrics are too far below ABI-202/249/279/280.

Record ABI-318 as bounded negative evidence for this exact C4 detail/support recall-router branch. A future proposal should materially change the mechanism rather than spend another Run on a similar single-frame C4 residual recall head.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_151751_5a903e/candidate/PROPOSAL.md`
- `run_20260915_151751_5a903e/candidate/README.md`
- `run_20260915_151751_5a903e/candidate/manifest.yaml`
- `run_20260915_151751_5a903e/resolved_manifest.yaml`
- `run_20260915_151751_5a903e/execution.json`
- `run_20260915_151751_5a903e/outputs/model_summary.json`
- `run_20260915_151751_5a903e/outputs/best_metrics.json`
- `run_20260915_151751_5a903e/outputs/final_metrics.json`
- `run_20260915_151751_5a903e/outputs/metrics.jsonl`
- `run_20260915_151751_5a903e/outputs/resource_profile.json`
- `run_20260915_151751_5a903e/outputs/validation_postprocessing/index.json`
- `run_20260915_151751_5a903e/outputs/prediction_samples/samples.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-c4-dual-evidence-recall-bridge-late36.md` for ABI-279 recall-bridge context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` and `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md` for ABI-280 selective-consensus context
- `run_20260914_095802_a2f059/outputs/best_metrics.json` and `/history/research-notes/abi303-c4-centerline-protected-recall-bridge-unet.md` for ABI-303 protected-C4 context
- `run_20260915_140910_e2f4a6/outputs/best_metrics.json` and `/history/research-notes/abi317-directional-message-passing-aspp-unet.md` for ABI-317 message-passing context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
