# ABI-292 C4 soft-band recall calibrator U-Net

research-figures: []

## Scope

This note records ABI-292, Candidate `abi292_fullspectral_btd_sza_c4_softband_recall_calibrator_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_215909_27c6e3`.

ABI-292 was a C4/orientation-prior family-development continuation after ABI-283. ABI-283 found a compact high-precision/high-connectivity C4 operating point but underpredicted true contrails. ABI-292 kept the ABI-283 resource-profiled C4 U-Net body and changed the mask head by adding a differentiable soft evidence band around uncertain region logits, with learned detail/line support and clutter-disagreement vetoes. The intended effect was to recover fixed-threshold recall without returning to ABI-279/280-style broad clutter or losing ABI-283's connected-line advantage.

The Candidate used provider-approved `abi_16ch_plus_sza` inputs, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-292 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,078,698, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 10.57 / 11.88 GiB.
- Training wall time: 1,531.4 s; validation wall time: 1,418.6 s; total Run wall time: 2,952.1 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-292 best epoch 11 | ABI-292 final epoch 12 | ABI-283 compact C4 parent | ABI-249 compact C4 comparator | ABI-279 recall bridge | ABI-280 selective consensus | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.384676 | 0.367538 | 0.412957 | 0.416400 | 0.414518 | 0.415244 | 0.427570 |
| Raw Dice | 0.398552 | 0.382419 | 0.429271 | 0.432320 | 0.429448 | 0.430420 | 0.442746 |
| Filtered precision | 0.404530 | 0.468830 | 0.500379 | 0.480886 | 0.442551 | 0.425162 | 0.439467 |
| Filtered recall | 0.366680 | 0.302238 | 0.351539 | 0.367165 | 0.389825 | 0.405778 | 0.416301 |
| Filtered connectivity | 0.249203 | 0.385632 | 0.475887 | 0.392524 | 0.439185 | 0.316291 | 0.457773 |
| MIT filtered Dice | 0.371401 | 0.348431 | 0.393239 | 0.396436 | 0.398381 | 0.405113 | 0.411992 |
| Google filtered Dice | 0.417038 | 0.415522 | 0.464463 | 0.468855 | 0.457385 | 0.442121 | 0.468151 |
| Filtered predicted-positive fraction | 0.003285 | 0.002336 | 0.002546 | 0.002767 | 0.003192 | 0.003458 | 0.003433 |
| Filtered predicted-positive pixels | 440,855 | 313,540 | 341,691 | 371,346 | 428,416 | 464,188 | 460,724 |

ABI-292 is a negative result for the soft-band recall-calibrator head as implemented. Relative to ABI-283, the selected checkpoint raises filtered recall by only about +0.015, below the proposal's +0.02 target, while losing about -0.0283 filtered Dice, -0.0958 precision, -0.2267 connectivity, -0.0218 MIT Dice, and -0.0474 Google Dice. The filtered footprint expands by 99,164 pixels, so the recall gain is not clean compact evidence.

Relative to ABI-249, ABI-292 essentially matches recall but is much lower in aggregate/source Dice, precision, and connectivity, and has a larger filtered footprint. Relative to ABI-279/280, ABI-292 does not recover their recall or aggregate/source Dice; it is only somewhat more compact than ABI-280 and has lower connectivity than both ABI-279 and ABI-280 at the selected checkpoint. Relative to ABI-202, ABI-292 remains well below the aggregate reference on every main scientific metric except having a slightly smaller predicted-positive footprint.

The final epoch exposes a different operating point: precision and connectivity rebound to 0.4688 and 0.3856 with a compact 313,540-pixel footprint, but recall falls to 0.3022 and filtered Dice drops to 0.3675. This reinforces that the head is moving along the familiar C4 precision/recall curve rather than stabilizing a superior trade-off.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212693 | 0.230791 | 0.181615 | 0.178516 | 0.263055 | 0.134086 | 0.005340 |
| 2 | 0.272982 | 0.279171 | 0.260550 | 0.234838 | 0.325922 | 0.148217 | 0.005029 |
| 3 | 0.298994 | 0.307219 | 0.283275 | 0.267065 | 0.339595 | 0.149107 | 0.004608 |
| 4 | 0.335508 | 0.322442 | 0.366350 | 0.335235 | 0.335781 | 0.177530 | 0.003630 |
| 5 | 0.342611 | 0.332069 | 0.366411 | 0.374603 | 0.315654 | 0.305365 | 0.003053 |
| 6 | 0.357017 | 0.338382 | 0.403435 | 0.453071 | 0.294567 | 0.362194 | 0.002356 |
| 7 | 0.361134 | 0.340657 | 0.412631 | 0.459965 | 0.297262 | 0.400637 | 0.002342 |
| 8 | 0.354029 | 0.331027 | 0.408495 | 0.444593 | 0.294116 | 0.341680 | 0.002397 |
| 9 | 0.352324 | 0.343347 | 0.372091 | 0.365393 | 0.340158 | 0.237914 | 0.003373 |
| 10 | 0.374262 | 0.368111 | 0.387927 | 0.380144 | 0.368559 | 0.279014 | 0.003513 |
| 11 | 0.384676 | 0.371401 | 0.417038 | 0.404530 | 0.366680 | 0.249203 | 0.003285 |
| 12 | 0.367538 | 0.348431 | 0.415522 | 0.468830 | 0.302238 | 0.385632 | 0.002336 |

The trajectory is finite, non-collapsed, and source-informative, but not compellingly late-improving. Epochs 6-8 briefly resemble the compact C4 mode, with high precision and improving connectivity but low recall. Epochs 10-11 produce the best aggregate Dice by expanding the footprint and lowering precision/connectivity. Epoch 12 then swings back toward compactness, losing recall and Dice. The late behavior is therefore oscillatory rather than evidence that the exact head needs a longer budget.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3986 versus filtered Dice 0.3847, and raw predicted-positive pixels 470,026 versus filtered predicted-positive pixels 440,855. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were near zero, 1.0000, near zero, and near zero. This does not indicate aggregate collapse because validation metrics are finite and source-informative, but it does not provide a qualitative reason to override the weak aggregate trade-off.

## Interpretation

Classify ABI-292 as a finite, resource-safe, scientifically negative C4 family-development continuation. The soft-band recall calibrator did not meet the stated mechanism target: it failed to preserve ABI-283/249 precision and connectivity, recovered too little recall, and did not improve aggregate or source-stratified Dice. The selected checkpoint is broader and less connected than intended, while the final compact checkpoint underpredicts too strongly.

This result does not eliminate all C4/orientation-prior work, but it argues against another unchanged C4 bridge/calibrator head run. The C4 branch has now repeatedly exposed the same trade-off: compact high-precision/high-connectivity checkpoints suppress recall, while recall-support checkpoints broaden predictions and lose precision or continuity. Future work should be mechanism-changing or broaden away from this exact C4-head family, for example toward earlier calibrated evidence sharing, a different source-balanced architecture-level recall support path, or temporal evidence sharpening that raises true contrail logits at threshold 0.5 without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-292. Do not request whole-validation failure-bucket diagnostics for this capped result. Do not request an unchanged late-improving continuation of the ABI-292 soft-band recall-calibrator head; despite the best epoch occurring at epoch 11, the proposal's precision/connectivity/recall trade-off criteria were missed by a large margin and the final epoch regressed in Dice and recall.

Treat ABI-292 as evidence that uncertain-logit soft-band support is not enough to solve the C4 fixed-threshold recall problem while preserving compact connected-line evidence. A future Candidate, if pursued, should materially change the mechanism rather than extend this exact head.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_215909_27c6e3/candidate/PROPOSAL.md`
- `run_20260913_215909_27c6e3/candidate/README.md`
- `run_20260913_215909_27c6e3/candidate/manifest.yaml`
- `run_20260913_215909_27c6e3/resolved_manifest.yaml`
- `run_20260913_215909_27c6e3/execution.json`
- `run_20260913_215909_27c6e3/outputs/model_summary.json`
- `run_20260913_215909_27c6e3/outputs/best_metrics.json`
- `run_20260913_215909_27c6e3/outputs/final_metrics.json`
- `run_20260913_215909_27c6e3/outputs/metrics.jsonl`
- `run_20260913_215909_27c6e3/outputs/resource_profile.json`
- `run_20260913_215909_27c6e3/outputs/validation_postprocessing/index.json`
- `run_20260913_215909_27c6e3/outputs/prediction_samples/samples.json`
- `run_20260913_063411_d8a862/outputs/best_metrics.json` for ABI-283 compact C4 parent comparison context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 comparison context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-whole-validation-failure-bucket-review.md` for ABI-279 recall-bridge comparison context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` and `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md` for ABI-280 selective-consensus comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference comparison context
- `/history/research-notes/abi283-c4-crossscale-consensus-recall-bridge-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
