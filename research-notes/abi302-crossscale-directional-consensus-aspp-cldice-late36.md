# ABI-302 cross-scale directional-consensus ASPP with trusted clDice loss

research-figures: []

## Scope

This note records ABI-302, Candidate `abi302_fullspectral_btd_sza_crossscale_directional_consensus_aspp_cldice_late36_line_centerline_aux_v1`, Run `run_20260914_065219_50e898`.

ABI-302 was a one-factor training-policy continuation of ABI-202, the current aggregate whole-validation reference. It kept the ABI-202 full-spectral BTD+Solar Geometry Input cross-scale directional-consensus ASPP architecture and changed only the trusted primary loss from `bce_dice` to `bce_dice_cldice`. The intended mechanism was to test whether provider-owned clDice connectivity pressure could improve connected thin-line continuity and fixed-threshold recall/source balance without Candidate-owned losses, thresholds, postprocessing, or Artifact Filters.

The Candidate consumed only provider-owned `abi_16ch_plus_sza` tensors. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, trusted BCE-Dice-clDice primary loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-302 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: approved `late_improving`, requested for 36 epochs from parent Run `run_20260904_043143_ee0005` and granted by the Harness.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,172,287, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 10,612,409,344 / 12,083,789,824 bytes.
- Training wall time: 5,967.2 s; validation wall time: 4,607.1 s; total Run wall time: 10,577.0 s, within the late-improving timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 32.

## Best-validation metrics

| Metric | ABI-302 clDice loss | ABI-202 BCE-Dice parent | ABI-249 C4 compact | ABI-279 C4 recall bridge | ABI-196 prior ASPP | ABI-184 precision/connectivity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 32 | 34 | 31 | 22 | 34 | 23 |
| Filtered Dice | 0.407105 | 0.427570 | 0.416400 | 0.414518 | 0.413262 | 0.406566 |
| MIT filtered Dice | 0.398270 | 0.411992 | 0.396436 | 0.398381 | 0.400678 | 0.387920 |
| Google filtered Dice | 0.428892 | 0.468151 | 0.468855 | 0.457385 | 0.444215 | 0.455529 |
| Filtered precision | 0.377587 | 0.439467 | 0.480886 | 0.442551 | 0.435019 | 0.485025 |
| Filtered recall | 0.441628 | 0.416301 | 0.367165 | 0.389825 | 0.393577 | 0.349955 |
| Filtered connectivity | 0.398449 | 0.457773 | 0.392524 | 0.439185 | 0.374629 | 0.463361 |
| Filtered predicted-positive fraction | 0.004238 | 0.003433 | 0.002767 | 0.003192 | 0.003278 | 0.002615 |

ABI-302 is a finite but mostly negative one-factor loss-policy result. It answers the central ABI-202 continuation question: adding trusted clDice pressure did raise capped filtered recall, but it did not improve connected-line continuity and did not preserve aggregate/source Dice or precision.

Relative to ABI-202, ABI-302 loses about -0.0205 filtered Dice, -0.0137 MIT filtered Dice, -0.0393 Google filtered Dice, -0.0619 precision, and -0.0593 connectivity. Its main positive movement is recall, +0.0253, but the footprint broadens from 0.003433 to 0.004238 filtered predicted-positive fraction. This is the opposite of the desired clean continuity improvement: recall increases through a less selective, lower-precision operating point while connectivity falls.

Relative to ABI-249, ABI-302 has higher recall (+0.0745) and similar capped connectivity (+0.0059), but much lower precision (-0.1033), lower Google Dice (-0.0400), and lower aggregate Dice (-0.0093). Relative to ABI-279's C4 recall bridge, ABI-302 again raises recall (+0.0518) but gives up precision (-0.0650), Google Dice (-0.0285), aggregate Dice (-0.0074), and connectivity (-0.0407). ABI-302 therefore behaves more like a broad recall-biased loss-policy variant than a better line-continuity solution.

At the selected checkpoint, raw Dice was 0.420621 versus filtered Dice 0.407105, raw recall was 0.473111 versus filtered recall 0.441628, and raw predicted-positive fraction was 0.004528 versus filtered predicted-positive fraction 0.004238. Artifact Filters remove some footprint, but they do not create the result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.178381 | 0.213730 | 0.130903 | 0.125678 | 0.307207 | 0.108593 | 0.008858 |
| 2 | 0.252978 | 0.275490 | 0.214695 | 0.197272 | 0.352523 | 0.161622 | 0.006475 |
| 3 | 0.293471 | 0.310629 | 0.262148 | 0.235991 | 0.387966 | 0.173385 | 0.005957 |
| 4 | 0.301837 | 0.315184 | 0.276482 | 0.236706 | 0.416418 | 0.170190 | 0.006375 |
| 5 | 0.343928 | 0.338848 | 0.355081 | 0.343371 | 0.344486 | 0.292609 | 0.003635 |
| 6 | 0.357443 | 0.360326 | 0.350847 | 0.326619 | 0.394692 | 0.253090 | 0.004379 |
| 7 | 0.370712 | 0.364289 | 0.385124 | 0.375517 | 0.366028 | 0.336960 | 0.003532 |
| 8 | 0.352361 | 0.350209 | 0.357059 | 0.358346 | 0.346573 | 0.260288 | 0.003505 |
| 9 | 0.354941 | 0.342002 | 0.386197 | 0.433785 | 0.300350 | 0.384229 | 0.002509 |
| 10 | 0.350413 | 0.341739 | 0.369383 | 0.367397 | 0.334930 | 0.280770 | 0.003303 |
| 11 | 0.323087 | 0.344528 | 0.280547 | 0.266257 | 0.410758 | 0.155992 | 0.005590 |
| 12 | 0.375197 | 0.361953 | 0.408271 | 0.437303 | 0.328537 | 0.369650 | 0.002722 |
| 13 | 0.363102 | 0.360676 | 0.368423 | 0.308974 | 0.440224 | 0.243724 | 0.005163 |
| 14 | 0.351686 | 0.344347 | 0.367649 | 0.356804 | 0.346713 | 0.284887 | 0.003521 |
| 15 | 0.370210 | 0.368200 | 0.374961 | 0.323720 | 0.432293 | 0.233284 | 0.004839 |
| 16 | 0.339837 | 0.339090 | 0.341387 | 0.285164 | 0.420446 | 0.186594 | 0.005343 |
| 17 | 0.372642 | 0.366720 | 0.385873 | 0.366051 | 0.379475 | 0.190308 | 0.003757 |
| 18 | 0.382792 | 0.364363 | 0.428758 | 0.470898 | 0.322459 | 0.504789 | 0.002481 |
| 19 | 0.364914 | 0.357685 | 0.380809 | 0.353952 | 0.376575 | 0.225767 | 0.003855 |
| 20 | 0.362935 | 0.361329 | 0.366613 | 0.317325 | 0.423857 | 0.177599 | 0.004840 |
| 21 | 0.382672 | 0.383183 | 0.381478 | 0.343657 | 0.431678 | 0.242267 | 0.004552 |
| 22 | 0.385083 | 0.379615 | 0.399613 | 0.333003 | 0.456473 | 0.290628 | 0.004967 |
| 23 | 0.387507 | 0.375153 | 0.419110 | 0.456376 | 0.336698 | 0.416136 | 0.002673 |
| 24 | 0.366753 | 0.349628 | 0.406397 | 0.398755 | 0.339506 | 0.313977 | 0.003085 |
| 25 | 0.389054 | 0.376541 | 0.421391 | 0.442382 | 0.347200 | 0.349668 | 0.002844 |
| 26 | 0.381114 | 0.360080 | 0.431395 | 0.437101 | 0.337841 | 0.364815 | 0.002801 |
| 27 | 0.393972 | 0.382711 | 0.421768 | 0.434422 | 0.360413 | 0.378329 | 0.003006 |
| 28 | 0.365967 | 0.343454 | 0.419628 | 0.439873 | 0.313324 | 0.367822 | 0.002581 |
| 29 | 0.391790 | 0.388260 | 0.399838 | 0.364603 | 0.423357 | 0.247747 | 0.004208 |
| 30 | 0.380222 | 0.370223 | 0.403540 | 0.422928 | 0.345350 | 0.282440 | 0.002959 |
| 31 | 0.343076 | 0.345094 | 0.338820 | 0.286438 | 0.427634 | 0.190469 | 0.005410 |
| 32 | 0.407105 | 0.398270 | 0.428892 | 0.377587 | 0.441628 | 0.398449 | 0.004238 |
| 33 | 0.393943 | 0.386844 | 0.410479 | 0.396678 | 0.391246 | 0.320530 | 0.003574 |
| 34 | 0.390401 | 0.387039 | 0.397975 | 0.368287 | 0.415341 | 0.248944 | 0.004087 |
| 35 | 0.377535 | 0.373674 | 0.386345 | 0.361702 | 0.394817 | 0.220227 | 0.003955 |
| 36 | 0.389112 | 0.387894 | 0.392015 | 0.351571 | 0.435630 | 0.215370 | 0.004490 |

The trajectory is finite, non-collapsed, and source-informative, but it is oscillatory. The best checkpoint occurs at epoch 32, so the approved longer budget was useful for finding the strongest capped operating point. However, late epochs do not show a stable path toward ABI-202-quality precision/connectivity: epoch 36 keeps high recall but ends with much lower connectivity (0.2154) and lower filtered Dice than epoch 32. Several earlier high-connectivity epochs, especially epoch 18, are compact/high-precision but low-recall states and do not solve the proposal's recall/connectivity balance target.

The retained fixed `first_n` prediction samples all have near-zero per-sample Dice. They are traceability artifacts selected by the Harness retention policy, not representative diagnostics. Population metrics and predicted-positive fractions show the model is not an all-negative collapse, but the retained samples do not supply qualitative support for promotion.

## Interpretation

Classify ABI-302 as a completed, resource-safe, scientifically useful negative result for switching the ABI-202 architecture from trusted BCE-Dice to trusted BCE-Dice-clDice under the approved late-improving budget. The loss-policy change answered a focused question: provider-owned clDice pressure can push the strongest architecture toward higher fixed-threshold recall, but under this training setup it does not translate into better filtered Dice or connected thin-line continuity. Instead, it lowers precision and source balance, especially on Google, while reducing the very connectivity metric it was meant to improve.

This result does not argue against all connectivity-oriented training or architecture ideas. It does narrow this exact ABI-202 loss-policy branch: the mature BCE-Dice parent remains stronger overall, and ABI-302's recall lift is not clean enough to replace ABI-202 or ABI-249/279 as a comparator. The failure mode is scientific rather than contractual or resource-related: clDice pressure changed the precision/recall operating point but did not create a more reliable connected-line representation.

Future work should not repeat ABI-302 unchanged and should not request another longer budget for the same architecture/loss combination. If training-policy work continues, it should be mechanism-changing rather than another local clDice tweak; higher-value hypotheses are likely in selective recall calibration, C4/orientation-prior recall support that controls negative-patch clutter, or temporal/line-continuity designs that couple recall to connected evidence without broadening false positives. Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-302. Do not request whole-validation diagnostics for this capped Result. The capped selected checkpoint remains below ABI-202 and ABI-249 on aggregate filtered Dice, below ABI-202/279/184 on connectivity, and achieves its recall gain with a major precision/source-balance regression. ABI-302 already used the approved late-improving budget, so there is no unchanged continuation to request.

Record ABI-302 as bounded evidence that trusted BCE-Dice remains preferable to trusted BCE-Dice-clDice for the ABI-202 cross-scale directional-consensus ASPP architecture under the current contract. Stop this exact loss-policy branch unless a future proposal changes the mechanism substantially.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_065219_50e898/candidate/PROPOSAL.md`
- `run_20260914_065219_50e898/candidate/README.md`
- `run_20260914_065219_50e898/candidate/manifest.yaml`
- `run_20260914_065219_50e898/candidate/budget_request.yaml`
- `run_20260914_065219_50e898/resolved_manifest.yaml`
- `run_20260914_065219_50e898/execution.json`
- `run_20260914_065219_50e898/outputs/model_summary.json`
- `run_20260914_065219_50e898/outputs/best_metrics.json`
- `run_20260914_065219_50e898/outputs/final_metrics.json`
- `run_20260914_065219_50e898/outputs/metrics.jsonl`
- `run_20260914_065219_50e898/outputs/resource_profile.json`
- `run_20260914_065219_50e898/outputs/validation_postprocessing/index.json`
- `run_20260914_065219_50e898/outputs/prediction_samples/samples.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 BCE-Dice parent context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 C4 steerable line-context comparator context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-whole-validation-failure-bucket-review.md` for ABI-279 C4 recall-bridge context
- `run_20260903_195527_248472/outputs/best_metrics.json` for ABI-196 prior ASPP comparator context
- `run_20260902_213856_2c04ac/outputs/best_metrics.json` for ABI-184 precision/connectivity comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
