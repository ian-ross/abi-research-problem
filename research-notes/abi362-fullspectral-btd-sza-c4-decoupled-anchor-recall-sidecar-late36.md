# ABI-362 full-spectral BTD+SZA C4 decoupled anchor/recall-sidecar late36

research-figures: []

## Scope

This note records ABI-362, Candidate `abi362_fullspectral_btd_sza_c4_decoupled_anchor_recall_sidecar_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_020446_9c2fa1`.

ABI-362 was a close, mechanism-changing single-frame C4-family continuation after ABI-353/342/343/249 on capped GOES ABI Contrail Segmentation validation. It kept provider-owned `abi_16ch_plus_sza` inputs, trusted source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 4. The architectural question was whether decoupling the final mask evidence into a compact C4 anchor plus a bounded architecture-internal recall sidecar would preserve ABI-249/353 compactness while recovering fixed-threshold positives.

This is capped representative feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-362 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested `late_improving` budget was approved from late-selecting C4 parents.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Trusted augmentation policy: `random_mirroring`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,086,255, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 9,755,749,376 / 11,093,934,080 bytes.
- Training wall time: 4,461.6 s; validation wall time: 4,284.3 s; total Run wall time: 8,748.5 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 34.

## Capped best-validation metrics

| Metric | ABI-362 decoupled anchor/sidecar | ABI-353 cross-scale detail agreement | ABI-249 C4 comparator | ABI-342 recall bridge | ABI-343 precision-veto recall | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 34 | 31 | 36 | 32 | 34 |
| Filtered Dice | 0.407108 | 0.417439 | 0.416400 | 0.415499 | 0.409827 | 0.427570 |
| MIT filtered Dice | 0.390686 | 0.401665 | 0.396436 | 0.398614 | 0.392320 | 0.411992 |
| Google filtered Dice | 0.446130 | 0.456492 | 0.468855 | 0.460044 | 0.453242 | 0.468151 |
| Filtered precision | 0.417976 | 0.442512 | 0.480886 | 0.397609 | 0.417766 | 0.439467 |
| Filtered recall | 0.396791 | 0.395056 | 0.367165 | 0.435075 | 0.402184 | 0.416301 |
| Filtered connectivity | 0.359966 | 0.348271 | 0.392524 | 0.405280 | 0.379763 | 0.457773 |
| Filtered predicted-positive pixels | 461,711 | 434,203 | 371,346 | 532,191 | 468,221 | 460,724 |

ABI-362 is finite and source-informative, but it is a negative result for the decoupled-head hypothesis. Relative to ABI-353, it loses -0.0103 aggregate filtered Dice, -0.0110 MIT Dice, -0.0104 Google Dice, and -0.0245 precision while adding 27,508 filtered-positive pixels. The only intended improvement is small: +0.0017 recall and +0.0117 connectivity. That is not enough to justify the extra footprint or aggregate/source regression.

Relative to ABI-249, ABI-362 does recover recall (+0.0296), but with large costs: -0.0093 filtered Dice, -0.0057 MIT Dice, -0.0227 Google Dice, -0.0629 precision, -0.0326 connectivity, and 90,365 additional filtered-positive pixels. This is essentially the same C4-family failure mode the proposal tried to avoid: recall support broadens predictions without preserving the compact/high-precision C4 behavior.

Relative to ABI-202, ABI-362 predicts an almost identical capped filtered-positive pixel count but has lower aggregate Dice, both source Dice scores, precision, recall, and connectivity. It is not a new frontier target.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.421624 versus filtered Dice 0.407108; raw recall was 0.423950 versus filtered recall 0.396791; raw predicted-positive pixels were 491,727 versus 461,711 filtered. Artifact Filters removed 30,016 predicted-positive pixels and lowered the score.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.203471 | 0.231418 | 0.158515 | 0.152283 | 0.306494 | 0.124131 | 0.007293 |
| 5 | 0.336822 | 0.317250 | 0.385103 | 0.428189 | 0.277590 | 0.362586 | 0.002349 |
| 10 | 0.346461 | 0.343023 | 0.353323 | 0.339596 | 0.353609 | 0.225153 | 0.003773 |
| 12 | 0.363880 | 0.344122 | 0.412717 | 0.435396 | 0.312543 | 0.340838 | 0.002601 |
| 16 | 0.370633 | 0.352424 | 0.415282 | 0.440773 | 0.319752 | 0.302230 | 0.002629 |
| 20 | 0.344164 | 0.323487 | 0.396261 | 0.479077 | 0.268541 | 0.359383 | 0.002031 |
| 24 | 0.347987 | 0.319306 | 0.423356 | 0.525809 | 0.260043 | 0.570043 | 0.001792 |
| 28 | 0.380590 | 0.355044 | 0.444893 | 0.512659 | 0.302628 | 0.433641 | 0.002139 |
| 31 | 0.401415 | 0.385854 | 0.438909 | 0.424252 | 0.380912 | 0.312285 | 0.003253 |
| 34 | 0.407108 | 0.390686 | 0.446130 | 0.417976 | 0.396791 | 0.359966 | 0.003440 |
| 36 | 0.406488 | 0.387306 | 0.455761 | 0.474663 | 0.355437 | 0.386195 | 0.002713 |

The trajectory validates the late-budget request in a narrow sense: the branch improves materially after epoch 12 and selects epoch 34. However, it also reinforces the C4 coupling problem. Epoch 24 has very high connectivity and precision but extremely low recall and a tiny footprint. Epoch 34 is the best Dice/recall state but loses compactness and still underperforms the C4 comparators. The final epoch is nearly tied on aggregate Dice and improves precision/connectivity versus epoch 34, but it does so by dropping recall from 0.3968 to 0.3554.

Thus the decoupled anchor/sidecar did not stabilize a joint high-precision, high-recall, high-connectivity state. It merely exposes different unstable operating points under the trusted fixed-threshold evaluation.

## Interpretation

Classify ABI-362 as a finite, resource-safe, negative C4-family-development result. The architectural sidecar is contract-safe and computationally feasible, but the capped evidence does not support the hypothesis that a bounded anchor-uncertainty recall residual can preserve compact C4 behavior while raising useful recall.

Do not promote ABI-362. Do not request a whole-validation diagnostic: the capped best checkpoint is below ABI-353, ABI-249, ABI-342, ABI-343, and ABI-202 on aggregate filtered Dice and is below or only tie-level on the intended source/precision/recall/connectivity trade-off. The trajectory is sufficiently diagnostic for this exact mechanism.

Do not spend another Run on an unchanged decoupled anchor/recall-sidecar late36 continuation, a simple gate-strength change, or another local C4-head shuffle. Future work should broaden the mechanism: for example, a source-robust MIT-tail support path, a different lightweight line-continuity decoder, or a non-C4 calibration/dual-evidence architecture that raises true positives without relying on local anchor uncertainty. Candidate-owned thresholds, calibration selection, postprocessing, losses, metrics, Artifact Filters, data loading, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_020446_9c2fa1/candidate/PROPOSAL.md`
- `run_20260920_020446_9c2fa1/candidate/README.md`
- `run_20260920_020446_9c2fa1/candidate/manifest.yaml`
- `run_20260920_020446_9c2fa1/candidate/budget_request.yaml`
- `run_20260920_020446_9c2fa1/resolved_manifest.yaml`
- `run_20260920_020446_9c2fa1/execution.json`
- `run_20260920_020446_9c2fa1/run_metadata.json`
- `run_20260920_020446_9c2fa1/outputs/model_summary.json`
- `run_20260920_020446_9c2fa1/outputs/best_metrics.json`
- `run_20260920_020446_9c2fa1/outputs/final_metrics.json`
- `run_20260920_020446_9c2fa1/outputs/metrics.jsonl`
- `run_20260920_020446_9c2fa1/outputs/resource_profile.json`
- `run_20260920_020446_9c2fa1/outputs/validation_postprocessing/index.json`
- `run_20260920_020446_9c2fa1/outputs/prediction_samples/samples.json`
- `run_20260919_053527_64085b/outputs/best_metrics.json` and `/history/research-notes/abi353-fullspectral-btd-sza-c4-crossscale-detail-agreement-late36.md` for ABI-353 comparator context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-249 comparator context
- `run_20260918_055403_f17232/outputs/best_metrics.json` and `/history/research-notes/abi342-fullspectral-btd-sza-c4-recall-bridge-late36.md` for ABI-342 comparator context
- `run_20260918_081800_9f0872/outputs/best_metrics.json` and `/history/research-notes/abi343-fullspectral-btd-sza-c4-precision-veto-recall-late36.md` for ABI-343 comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-202 reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/initial-dataset-profile.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
