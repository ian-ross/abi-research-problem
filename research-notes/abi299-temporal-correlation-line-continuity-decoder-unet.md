# ABI-299 temporal correlation line-continuity decoder U-Net

research-figures: []

## Scope

This note records ABI-299, Candidate `abi299_temporal_correlation_line_continuity_decoder_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_040326_98380c`.

ABI-299 was a bounded temporal family-development continuation after ABI-296/297/298. It kept the provider-stacked previous/center/next temporal input and the ABI-296/298 differentiable 3x3 local-correlation mechanism, but added an explicit lightweight line-continuity bridge inside the decoder/head. The bridge applied horizontal, vertical, and dilated diagonal depthwise line context to center-line, temporal-line, and multiscale decoder support. The intended mechanism was to keep the ABI-296/298 recall-support path while organizing that evidence into more connected thin-line predictions and reducing broad local-correlation clutter.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Execution result

ABI-299 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 3,290,051, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,139,785,728 / 6,446,645,248 bytes.
- Training wall time: 1,762.6 s; validation wall time: 1,170.3 s; total Run wall time: 2,934.6 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-299 line-continuity correlation | ABI-296 local correlation | ABI-297 hard orientation-agreement | ABI-298 soft-agreement correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 | ABI-289 dual-evidence temporal | ABI-290 precision-gated temporal | ABI-291 five-frame persistence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 9 | 11 | 9 | 36 | 29 | 32 | 8 | 9 | 10 |
| Filtered Dice | 0.396406 | 0.395208 | 0.383293 | 0.394320 | 0.419776 | 0.420235 | 0.422195 | 0.380244 | 0.379803 | 0.358719 |
| MIT filtered Dice | 0.383650 | 0.379768 | 0.366817 | 0.383015 | 0.398498 | 0.405383 | 0.400831 | 0.372684 | 0.368809 | 0.336776 |
| Google filtered Dice | 0.428424 | 0.433397 | 0.425897 | 0.422279 | 0.476764 | 0.460838 | 0.477410 | 0.398412 | 0.406267 | 0.414922 |
| Filtered precision | 0.408439 | 0.389486 | 0.449486 | 0.406272 | 0.483764 | 0.488730 | 0.448400 | 0.361568 | 0.384437 | 0.495053 |
| Filtered recall | 0.385063 | 0.401101 | 0.334093 | 0.383051 | 0.370738 | 0.368578 | 0.398883 | 0.400955 | 0.375279 | 0.281261 |
| Filtered connectivity | 0.268913 | 0.331894 | 0.259964 | 0.309064 | 0.412427 | 0.352239 | 0.243387 | 0.249988 | 0.245732 | 0.295736 |
| Filtered predicted-positive fraction | 0.004874 | 0.005324 | 0.003842 | 0.004874 | 0.003962 | 0.003899 | 0.004599 | 0.005733 | 0.005046 | 0.002937 |

ABI-299 is a useful but non-frontier temporal result. It is the best of the immediate ABI-296/297/298/299 local-correlation sequence by capped temporal-eligible `val/filtered_dice`, but only narrowly: +0.0012 versus ABI-296 and +0.0021 versus ABI-298. The improvement over ABI-296 comes from better precision and compactness, with filtered precision rising from 0.3895 to 0.4084 and filtered positive fraction falling from 0.005324 to 0.004874, but filtered recall falls from 0.4011 to 0.3851 and Google Dice falls from 0.4334 to 0.4284. Against ABI-298, ABI-299 is a small aggregate/source-balanced improvement, with similar compactness and slightly higher precision, recall, MIT Dice, and Google Dice.

The explicit line-continuity bridge did not solve the connected-line metric at the selected checkpoint. ABI-299 filtered connectivity is 0.2689, below ABI-296 (0.3319), below ABI-298 (0.3091), and far below ABI-223/238. It is only slightly above ABI-297 and the weaker recent temporal heads. Thus the bridge helped the primary precision/recall balance modestly, but it did not convert local-correlation support into the intended connected thin-line evidence at the best Dice checkpoint.

Relative to the stronger temporal comparators, ABI-299 remains below the temporal frontier. It trails ABI-223/238/285 by about 0.023 to 0.026 filtered Dice and remains weaker on source-stratified Dice, especially Google. Its recall exceeds ABI-223/238 but its precision and connectivity are much lower. ABI-285 keeps higher aggregate score and recall despite low connectivity. ABI-299 therefore narrows the local-correlation branch's gap only slightly; it does not change the promotion or diagnostic frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.220789 | 0.228363 | 0.206176 | 0.192282 | 0.259219 | 0.127544 | 0.006969 |
| 2 | 0.253456 | 0.241087 | 0.285949 | 0.378619 | 0.190486 | 0.275588 | 0.002601 |
| 3 | 0.294408 | 0.276590 | 0.340322 | 0.480954 | 0.212130 | 0.338930 | 0.002280 |
| 4 | 0.321169 | 0.302788 | 0.365783 | 0.383759 | 0.276133 | 0.270483 | 0.003720 |
| 5 | 0.355064 | 0.340469 | 0.390657 | 0.402056 | 0.317908 | 0.245518 | 0.004088 |
| 6 | 0.312331 | 0.296679 | 0.349088 | 0.391475 | 0.259806 | 0.283767 | 0.003431 |
| 7 | 0.338641 | 0.315486 | 0.401366 | 0.547432 | 0.245143 | 0.429280 | 0.002315 |
| 8 | 0.339931 | 0.330107 | 0.363726 | 0.343195 | 0.336728 | 0.196677 | 0.005072 |
| 9 | 0.396406 | 0.383650 | 0.428424 | 0.408439 | 0.385063 | 0.268913 | 0.004874 |
| 10 | 0.380689 | 0.365754 | 0.417505 | 0.429568 | 0.341798 | 0.278744 | 0.004113 |
| 11 | 0.324193 | 0.308566 | 0.361618 | 0.370689 | 0.288061 | 0.199268 | 0.004017 |
| 12 | 0.364979 | 0.338732 | 0.433335 | 0.494571 | 0.289200 | 0.386269 | 0.003023 |

The trajectory is finite, non-collapsed, and source-informative, but it is not clean late-improving evidence. The best checkpoint occurs at epoch 9 after an oscillatory path. Epoch 12 has much higher precision, Google Dice, and connectivity, but it sacrifices recall and MIT Dice enough to lower the primary metric to 0.3650. This suggests the continuity bridge can push the model toward compact/high-connectivity states, but the branch does not yet align those states with balanced fixed-threshold recall.

Raw-to-filtered differences at the selected checkpoint are modest: raw Dice 0.4123 versus filtered Dice 0.3964, raw recall 0.4156 versus filtered recall 0.3851, and raw predicted-positive fraction 0.005254 versus filtered predicted-positive fraction 0.004874. Artifact Filters remove some footprint, but they do not create the result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3507, 0.6306, 0.5240, and 0.4924. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-299 as a completed, resource-safe, scientifically useful temporal family-development result, but not a frontier or promotion candidate. It modestly improves the immediate local-correlation sequence's aggregate filtered Dice and precision/compactness trade-off, while preserving enough recall to avoid ABI-297's hard-veto failure. That makes it useful mechanism evidence: local temporal correlation plus an internal line-continuity bridge can slightly improve the operating point over local correlation alone or soft agreement alone.

The result also gives a bounded negative answer to the stronger line-continuity hypothesis. The bridge did not raise connectivity at the selected checkpoint and did not approach ABI-223/238 temporal-attention connectivity. Its high-connectivity final epoch came with suppressed recall and MIT Dice, implying that this design can compact and connect predictions but cannot simultaneously maintain the needed recall/source balance under the exploratory policy.

Do not treat the low connectivity as a reason to abandon all temporal work; the branch remains finite and informative. But the immediate ABI-296/297/298/299 local-correlation head/bridge sequence has now been adequately probed under the default budget. Another small local-correlation calibration tweak or unchanged late36 continuation would likely spend a Run on the same oscillatory precision/recall/connectivity curve. Future temporal work should be mechanism-changing: either return to ABI-223/238/285-style temporal attention or C4 temporal line state with explicit evidence sharpening at threshold 0.5, or introduce a substantially different continuity mechanism that couples connectivity to recall rather than trading one off against the other.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-299. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not request an unchanged late36 continuation of ABI-299; the exploratory run peaked at epoch 9 and later epochs traded recall/source balance for compactness/connectivity.

Record ABI-299 as the best but still non-frontier member of the ABI-296/297/298/299 local-correlation sequence and as evidence to stop the immediate local-correlation bridge branch unless the next hypothesis is mechanism-changing. A reasonable next Run, if temporal work continues, should broaden toward temporal-attention evidence sharpening or a different recall-preserving connectivity mechanism rather than another minor head calibration.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_040326_98380c/candidate/PROPOSAL.md`
- `run_20260914_040326_98380c/candidate/README.md`
- `run_20260914_040326_98380c/candidate/manifest.yaml`
- `run_20260914_040326_98380c/resolved_manifest.yaml`
- `run_20260914_040326_98380c/execution.json`
- `run_20260914_040326_98380c/outputs/model_summary.json`
- `run_20260914_040326_98380c/outputs/best_metrics.json`
- `run_20260914_040326_98380c/outputs/final_metrics.json`
- `run_20260914_040326_98380c/outputs/metrics.jsonl`
- `run_20260914_040326_98380c/outputs/resource_profile.json`
- `run_20260914_040326_98380c/outputs/validation_postprocessing/index.json`
- `run_20260914_040326_98380c/outputs/prediction_samples/samples.json`
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260914_015932_e13da3/outputs/best_metrics.json` and `/history/research-notes/abi297-temporal-orientation-agreement-correlation-unet.md` for ABI-297 hard orientation-agreement comparison context
- `run_20260914_030016_a73097/outputs/best_metrics.json` and `/history/research-notes/abi298-temporal-soft-agreement-correlation-recall-unet.md` for ABI-298 soft-agreement comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 directional temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` and `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md` for ABI-285 temporal C4 comparison context
- `run_20260913_194511_b462e0/outputs/best_metrics.json` and `/history/research-notes/abi289-temporal-attention-dual-evidence-recall-continuity-unet.md` for ABI-289 comparison context
- `run_20260913_202938_44793e/outputs/best_metrics.json` and `/history/research-notes/abi290-temporal-attention-precision-gated-continuity-unet.md` for ABI-290 comparison context
- `run_20260913_211453_8c6c4e/outputs/best_metrics.json` and `/history/research-notes/abi291-temporal-fiveframe-persistence-attention-directional-unet.md` for ABI-291 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
