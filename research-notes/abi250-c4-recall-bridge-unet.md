# ABI-250 C4 recall-bridge U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-250, Candidate `abi250_fullspectral_btd_sza_c4_recall_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_135022_457598`.

ABI-250 was a mechanism-changing family-development continuation after ABI-249. It kept the provider-approved `abi_16ch_plus_sza` input, trusted BCE-Dice loss, source-balanced sampling, trusted random mirroring, constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs. It added a high-resolution full-scale support bridge before the C4 rotation-shared line-context head to test whether the C4 branch could recover recall/connectivity while preserving ABI-249's compact high-precision behavior. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-250 completed the default 12-epoch exploratory budget without contract, smoke, shape, numerical, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Budget: exploratory; no late-improving request.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,102,172, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 11.83 / 13.64 GiB.
- Training wall time: 1,821.8 s; validation wall time: 1,490.6 s; total Run wall time: 3,314.4 s.

Resource use stayed inside the exploratory timeout, but the added bridge is substantially heavier than ABI-249: ABI-250 used about 11.83 GiB peak allocated memory and 3,314 s total wall time for 12 epochs, versus ABI-249's about 7.70 GiB peak allocated memory and 7,642 s for 36 epochs. This resource cost matters because ABI-250 did not improve the C4 branch's metrics.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8. The final epoch 12 regressed materially, so the trajectory was finite but not a clean late-improving signal.

| Metric | ABI-250 best epoch 8 | ABI-250 final epoch 12 | ABI-249 best epoch 31 | ABI-248 scout epoch 12 |
| --- | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.379391 | 0.338180 | 0.416400 | 0.383829 |
| Raw Dice | 0.393414 | 0.349590 | 0.432320 | 0.399160 |
| Filtered precision | 0.417067 | 0.346266 | 0.480886 | 0.454139 |
| Filtered recall | 0.347959 | 0.330464 | 0.367165 | 0.332372 |
| Filtered connectivity | 0.349901 | 0.234887 | 0.392524 | 0.327777 |
| MIT filtered Dice | 0.364297 | 0.336512 | 0.396436 | 0.373157 |
| Google filtered Dice | 0.415800 | 0.341963 | 0.468855 | 0.411614 |
| Filtered predicted-positive fraction | 0.003023 | 0.003458 | 0.002767 | 0.002652 |
| Train loss | 0.855114 | 0.846261 | 0.811498 | 0.847672 |
| Validation loss | 0.884203 | 0.901749 | 0.873648 | 0.882328 |

Relative to ABI-249, ABI-250's selected checkpoint loses about -0.0370 filtered Dice, -0.0638 precision, -0.0192 recall, -0.0426 connectivity, -0.0321 MIT filtered Dice, and -0.0531 Google filtered Dice. Relative to the exploratory ABI-248 parent, ABI-250 is also slightly lower on selected filtered Dice and MIT Dice, despite predicting a somewhat larger positive fraction. The intended recall bridge therefore did not recover ABI-249's fixed-threshold coverage weakness.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.200867 | 0.218606 | 0.171587 | 0.161090 | 0.266729 | 0.101484 | 0.006000 |
| 2 | 0.252392 | 0.272373 | 0.217807 | 0.191940 | 0.368429 | 0.128755 | 0.006956 |
| 3 | 0.316594 | 0.301201 | 0.350822 | 0.354329 | 0.286122 | 0.231380 | 0.002926 |
| 4 | 0.311835 | 0.319840 | 0.296036 | 0.260368 | 0.388663 | 0.150846 | 0.005409 |
| 5 | 0.341416 | 0.316419 | 0.401511 | 0.454712 | 0.273317 | 0.394916 | 0.002178 |
| 6 | 0.373669 | 0.364242 | 0.395590 | 0.370977 | 0.376401 | 0.304363 | 0.003677 |
| 7 | 0.337887 | 0.344324 | 0.325031 | 0.283274 | 0.418587 | 0.189106 | 0.005355 |
| 8 | 0.379391 | 0.364297 | 0.415800 | 0.417067 | 0.347959 | 0.349901 | 0.003023 |
| 9 | 0.357276 | 0.338804 | 0.398983 | 0.372686 | 0.343090 | 0.304372 | 0.003336 |
| 10 | 0.369037 | 0.354317 | 0.403287 | 0.411770 | 0.334339 | 0.268582 | 0.002942 |
| 11 | 0.367746 | 0.358202 | 0.390050 | 0.378149 | 0.357900 | 0.278260 | 0.003430 |
| 12 | 0.338180 | 0.336512 | 0.341963 | 0.346266 | 0.330464 | 0.234887 | 0.003458 |

The trajectory is noisy rather than collapsed: both Dataset Sources retain nonzero Dice, predicted-positive fractions remain bounded, and the run is finite. However, the best epoch is in the middle of the exploratory run and the final epoch loses aggregate Dice, Google Dice, precision, recall, connectivity, and validation loss. That does not justify a late36 continuation under the current late-improving policy.

## Interpretation

Classify ABI-250 as a valid negative family-development result for the specific C4 high-resolution recall-bridge mechanism. The added bridge increased resource cost and did not solve ABI-249's primary weakness. It neither preserved ABI-249's high precision nor recovered enough recall/connectivity to approach ABI-202 or ABI-249.

This should not eliminate the broader rotation-aware/C4 idea: ABI-249 remains a useful high-precision comparator with whole-validation filtered Dice 0.4197 and source-informative behavior. It does, however, argue against continuing this exact high-resolution support-bridge branch or requesting late36 for ABI-250. More local C4 bridge/refiner mutations are unlikely to be the best next use of budget unless diagnostics identify a sharper one-factor mechanism.

## Decision

Do not promote ABI-250, do not request whole-validation diagnostics for it, and do not request a late-improving continuation. Treat ABI-249 as the retained C4 family representative and ABI-202 as the aggregate whole-validation frontier reference.

The next hypothesis should broaden away from this exact C4 support-bridge path. Reasonable in-contract directions include a different rotation-aware mechanism with lower resource cost, differentiable Hough/Radon-style line accumulation, modern compact attention/backbone scouts, spectral/SZA-gated mixture-of-experts, or a recall-preserving calibration-style architecture that does not move thresholding or postprocessing into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_135022_457598/candidate/PROPOSAL.md`
- `run_20260911_135022_457598/candidate/README.md`
- `run_20260911_135022_457598/candidate/manifest.yaml`
- `run_20260911_135022_457598/resolved_manifest.yaml`
- `run_20260911_135022_457598/outputs/model_summary.json`
- `run_20260911_135022_457598/outputs/best_metrics.json`
- `run_20260911_135022_457598/outputs/final_metrics.json`
- `run_20260911_135022_457598/outputs/metrics.jsonl`
- `run_20260911_135022_457598/outputs/resource_profile.json`
- `run_20260911_135022_457598/outputs/validation_postprocessing/index.json`
- `run_20260911_135022_457598/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7` for ABI-249 direct C4 parent context
- `run_20260911_102833_5db7f8` for ABI-248 exploratory C4 scout context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
