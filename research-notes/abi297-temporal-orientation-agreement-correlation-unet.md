# ABI-297 temporal orientation-agreement correlation U-Net

research-figures: []

## Scope

This note records ABI-297, Candidate `abi297_temporal_orientation_agreement_correlation_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_015932_e13da3`.

ABI-297 was a bounded temporal family-development continuation after ABI-296. It kept ABI-296's provider-stacked previous/center/next temporal local-correlation mechanism, but added an orientation-agreement head intended to trust temporal support only when it agreed with center-frame directional line evidence. The intended mechanism was precision-preserving recall/connectivity: retain ABI-296's fixed-threshold temporal support while reducing its broader low-precision footprint.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-297 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 4,423,141, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,190,949,888 / 6,534,725,632 bytes.
- Training wall time: 1,864.9 s; validation wall time: 1,302.1 s; total Run wall time: 3,168.9 s, within but close to the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-297 orientation-agreement correlation | ABI-296 local correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 | ABI-289 dual-evidence temporal | ABI-290 precision-gated temporal | ABI-291 five-frame persistence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 9 | 36 | 29 | 32 | 8 | 9 | 10 |
| Filtered Dice | 0.383293 | 0.395208 | 0.419776 | 0.420235 | 0.422195 | 0.380244 | 0.379803 | 0.358719 |
| MIT filtered Dice | 0.366817 | 0.379768 | 0.398498 | 0.405383 | 0.400831 | 0.372684 | 0.368809 | 0.336776 |
| Google filtered Dice | 0.425897 | 0.433397 | 0.476764 | 0.460838 | 0.477410 | 0.398412 | 0.406267 | 0.414922 |
| Filtered precision | 0.449486 | 0.389486 | 0.483764 | 0.488730 | 0.448400 | 0.361568 | 0.384437 | 0.495053 |
| Filtered recall | 0.334093 | 0.401101 | 0.370738 | 0.368578 | 0.398883 | 0.400955 | 0.375279 | 0.281261 |
| Filtered connectivity | 0.259964 | 0.331894 | 0.412427 | 0.352239 | 0.243387 | 0.249988 | 0.245732 | 0.295736 |
| Filtered predicted-positive fraction | 0.003842 | 0.005324 | 0.003962 | 0.003899 | 0.004599 | 0.005733 | 0.005046 | 0.002937 |

ABI-297 partially confirms and mostly limits the hypothesis. The orientation-agreement gate did reduce footprint and recover precision relative to ABI-296: filtered precision improved from 0.3895 to 0.4495 and filtered predicted-positive fraction fell from 0.005324 to 0.003842. However, it gave back too much of ABI-296's useful temporal recall, dropping filtered recall from 0.4011 to 0.3341 and filtered Dice from 0.3952 to 0.3833. MIT filtered Dice also fell to 0.3668, while Google filtered Dice fell to 0.4259.

Against stronger temporal comparators, ABI-297 is not close enough to be a frontier result. It trails ABI-223/238/285 by about 0.0365 to 0.0389 filtered Dice and is lower on both source-stratified Dice values. It does match ABI-285's precision at the selected checkpoint and remains more compact than ABI-296/289/290, but its fixed-threshold recall is too low for the primary metric.

Relative to the most recent negative temporal mechanisms, ABI-297 is scientifically useful but not decisive. It beats ABI-289/290 slightly on aggregate filtered Dice while using a smaller filtered footprint, but not by enough to suggest a promotion or diagnostic request. It is much better than ABI-291 on Dice and MIT balance, but ABI-291 was already a poor underprediction direction.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.258963 | 0.253847 | 0.272797 | 0.415367 | 0.188125 | 0.317234 | 0.002341 |
| 2 | 0.291253 | 0.279812 | 0.322044 | 0.478417 | 0.209352 | 0.377397 | 0.002262 |
| 3 | 0.321769 | 0.303769 | 0.367921 | 0.469292 | 0.244812 | 0.356858 | 0.002697 |
| 4 | 0.327072 | 0.306090 | 0.380234 | 0.437936 | 0.261000 | 0.323217 | 0.003081 |
| 5 | 0.332093 | 0.320389 | 0.359128 | 0.365290 | 0.304428 | 0.207413 | 0.004308 |
| 6 | 0.380983 | 0.366957 | 0.414927 | 0.408727 | 0.356766 | 0.261982 | 0.004512 |
| 7 | 0.364745 | 0.342246 | 0.424849 | 0.501615 | 0.286556 | 0.324151 | 0.002953 |
| 8 | 0.379121 | 0.359566 | 0.429709 | 0.461926 | 0.321491 | 0.326000 | 0.003598 |
| 9 | 0.375551 | 0.365103 | 0.400439 | 0.376629 | 0.374480 | 0.211117 | 0.005140 |
| 10 | 0.378807 | 0.362198 | 0.419264 | 0.433131 | 0.336591 | 0.240229 | 0.004017 |
| 11 | 0.383293 | 0.366817 | 0.425897 | 0.449486 | 0.334093 | 0.259964 | 0.003842 |
| 12 | 0.379764 | 0.359060 | 0.435292 | 0.537234 | 0.293682 | 0.434542 | 0.002826 |

The trajectory is finite, non-collapsed, and source-informative, but it shows a precision/recall oscillation rather than clean late improvement. Epoch 6 already reached 0.3810 filtered Dice through broader recall. Epoch 9 recovered the highest recall but widened the footprint and reduced precision. Epoch 11 was selected by a modest aggregate Dice edge. Epoch 12 became very compact and high precision/connectivity, with filtered precision 0.5372 and connectivity 0.4345, but recall fell to 0.2937 and the primary metric declined.

This late behavior is informative: orientation agreement can force a compact, connected prediction regime, but under the current architecture it suppresses too much true contrail support. Although the best checkpoint occurs near the end, the epoch 6-12 pattern is a trade-off curve rather than evidence that an unchanged 36-epoch continuation is likely to become a temporal frontier. The total wall time was also close enough to the 3,600 s exploratory timeout that a late-budget request should require stronger scientific justification than this result provides.

Raw-to-filtered differences at the selected checkpoint are modest: raw Dice 0.4010 versus filtered Dice 0.3833, raw recall 0.3617 versus filtered recall 0.3341, and raw predicted-positive fraction 0.004156 versus filtered predicted-positive fraction 0.003842. Artifact Filters remove some footprint, but they do not create the result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3434, 0.4727, 0.5830, and 0.5301. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-297 as a completed, resource-safe, scientifically useful but non-frontier temporal family-development result. It shows that the orientation-agreement constraint successfully moves local temporal correlation toward a smaller and more precise prediction footprint. It also demonstrates a compact high-connectivity endpoint at epoch 12.

The cost is recall. The selected checkpoint underperforms ABI-296 because the agreement gate removes too much of the local-correlation support that made ABI-296 useful. The final checkpoint emphasizes this failure mode: high precision and high connectivity are available, but only by shrinking predictions below the recall needed at the fixed Harness threshold.

Do not treat this as a reason to abandon all temporal correlation work. ABI-296 and ABI-297 together isolate a useful mechanism boundary: local correlation can raise recall, while orientation agreement can compact predictions. A future mechanism-changing variant would need to decouple the compactness/continuity benefit from the hard recall suppression, for example by using orientation agreement as an additive confidence calibration branch rather than a veto, or by preserving a center-frame detail bypass that can recover thin positives when temporal orientation evidence is weak. That future work should still be bounded and should not implement Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, temporal cache access, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-297. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not request an unchanged late36 continuation of this exact orientation-agreement local-correlation design; the exploratory run is finite but below temporal comparators, oscillates along the precision/recall frontier, and ends with recall suppression rather than primary-metric improvement.

Keep the result as mechanism evidence: orientation agreement is useful for compactness and connectedness, but this implementation over-constrains recall. If spending another Run in this area, require a mechanism-changing design that preserves ABI-296-style recall support while using ABI-297-style agreement only as a soft calibration or auxiliary evidence branch. Otherwise broaden away from local temporal matching.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_015932_e13da3/candidate/PROPOSAL.md`
- `run_20260914_015932_e13da3/candidate/README.md`
- `run_20260914_015932_e13da3/candidate/manifest.yaml`
- `run_20260914_015932_e13da3/resolved_manifest.yaml`
- `run_20260914_015932_e13da3/execution.json`
- `run_20260914_015932_e13da3/outputs/model_summary.json`
- `run_20260914_015932_e13da3/outputs/best_metrics.json`
- `run_20260914_015932_e13da3/outputs/final_metrics.json`
- `run_20260914_015932_e13da3/outputs/metrics.jsonl`
- `run_20260914_015932_e13da3/outputs/resource_profile.json`
- `run_20260914_015932_e13da3/outputs/validation_postprocessing/index.json`
- `run_20260914_015932_e13da3/outputs/prediction_samples/samples.json`
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 temporal C4 comparison context
- `run_20260913_194511_b462e0/outputs/best_metrics.json` and `/history/research-notes/abi289-temporal-attention-dual-evidence-recall-continuity-unet.md` for ABI-289 comparison context
- `run_20260913_202938_44793e/outputs/best_metrics.json` and `/history/research-notes/abi290-temporal-attention-precision-gated-continuity-unet.md` for ABI-290 comparison context
- `run_20260913_211453_8c6c4e/outputs/best_metrics.json` and `/history/research-notes/abi291-temporal-fiveframe-persistence-attention-directional-unet.md` for ABI-291 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
