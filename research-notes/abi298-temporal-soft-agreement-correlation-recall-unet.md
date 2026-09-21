# ABI-298 temporal soft-agreement correlation recall U-Net

research-figures: []

## Scope

This note records ABI-298, Candidate `abi298_temporal_soft_agreement_correlation_recall_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_030016_a73097`.

ABI-298 was a bounded temporal family-development continuation after ABI-296 and ABI-297. It kept ABI-296's provider-stacked previous/center/next local-correlation mechanism and ABI-297's orientation-agreement evidence, but changed the head semantics: orientation agreement was used as a soft additive calibration signal rather than as a hard temporal-support veto. The intended mechanism was to preserve ABI-296-style fixed-threshold recall and center-detail support while recovering some of ABI-297's compactness and precision.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Execution result

ABI-298 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 4,423,141, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,192,522,752 / 6,534,725,632 bytes.
- Training wall time: 1,871.7 s; validation wall time: 1,337.5 s; total Run wall time: 3,211.0 s, within but close to the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 9.

## Best-validation metrics

| Metric | ABI-298 soft-agreement correlation | ABI-296 local correlation | ABI-297 hard orientation-agreement | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 | ABI-289 dual-evidence temporal | ABI-290 precision-gated temporal | ABI-291 five-frame persistence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 9 | 11 | 36 | 29 | 32 | 8 | 9 | 10 |
| Filtered Dice | 0.394320 | 0.395208 | 0.383293 | 0.419776 | 0.420235 | 0.422195 | 0.380244 | 0.379803 | 0.358719 |
| MIT filtered Dice | 0.383015 | 0.379768 | 0.366817 | 0.398498 | 0.405383 | 0.400831 | 0.372684 | 0.368809 | 0.336776 |
| Google filtered Dice | 0.422279 | 0.433397 | 0.425897 | 0.476764 | 0.460838 | 0.477410 | 0.398412 | 0.406267 | 0.414922 |
| Filtered precision | 0.406272 | 0.389486 | 0.449486 | 0.483764 | 0.488730 | 0.448400 | 0.361568 | 0.384437 | 0.495053 |
| Filtered recall | 0.383051 | 0.401101 | 0.334093 | 0.370738 | 0.368578 | 0.398883 | 0.400955 | 0.375279 | 0.281261 |
| Filtered connectivity | 0.309064 | 0.331894 | 0.259964 | 0.412427 | 0.352239 | 0.243387 | 0.249988 | 0.245732 | 0.295736 |
| Filtered predicted-positive fraction | 0.004874 | 0.005324 | 0.003842 | 0.003962 | 0.003899 | 0.004599 | 0.005733 | 0.005046 | 0.002937 |

ABI-298 is a useful but non-frontier temporal result. It improves clearly over ABI-297's hard orientation-agreement constraint: filtered Dice rises from 0.3833 to 0.3943, MIT filtered Dice from 0.3668 to 0.3830, recall from 0.3341 to 0.3831, and connectivity from 0.2600 to 0.3091. This supports the hypothesis that treating orientation agreement as a soft calibration branch avoids much of the recall suppression caused by the ABI-297 hard-veto design.

Against ABI-296, the result is a near tie on aggregate filtered Dice but not an outright improvement. ABI-298 is slightly lower on filtered Dice (-0.0009), recall (-0.0180), Google filtered Dice (-0.0111), and connectivity (-0.0228), while improving precision (+0.0168), MIT filtered Dice (+0.0032), and compactness (filtered predicted-positive fraction 0.004874 versus 0.005324). The soft-agreement head therefore moderated ABI-296's wide footprint without collapsing like ABI-297, but it did not recover enough Google/source aggregate score or continuity to become the stronger local-correlation variant.

Relative to stronger temporal comparators, ABI-298 remains below the temporal frontier. It trails ABI-223/238/285 by about 0.025 to 0.028 filtered Dice and is materially lower on source-stratified Dice, especially Google. It has higher recall than ABI-223/238 and better connectivity than ABI-285, but the combination is not clean enough: precision remains below ABI-223/238/285, and connectivity remains below ABI-223/238. Compared with recent weaker temporal heads (ABI-289/290/291), ABI-298 is better balanced and improves aggregate filtered Dice, but it is still not promotion-level.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.271841 | 0.282505 | 0.249046 | 0.247717 | 0.301171 | 0.173103 | 0.006285 |
| 2 | 0.314347 | 0.305158 | 0.337676 | 0.413139 | 0.253685 | 0.336363 | 0.003174 |
| 3 | 0.337233 | 0.327279 | 0.360913 | 0.377512 | 0.304721 | 0.260801 | 0.004173 |
| 4 | 0.297817 | 0.271537 | 0.364530 | 0.459620 | 0.220273 | 0.322131 | 0.002478 |
| 5 | 0.346251 | 0.330957 | 0.384073 | 0.412735 | 0.298214 | 0.266936 | 0.003735 |
| 6 | 0.331746 | 0.307730 | 0.394109 | 0.533999 | 0.240613 | 0.398964 | 0.002329 |
| 7 | 0.381964 | 0.365610 | 0.424745 | 0.478871 | 0.317678 | 0.398384 | 0.003429 |
| 8 | 0.389302 | 0.376118 | 0.421830 | 0.399143 | 0.379935 | 0.274731 | 0.004921 |
| 9 | 0.394320 | 0.383015 | 0.422279 | 0.406272 | 0.383051 | 0.309064 | 0.004874 |
| 10 | 0.384747 | 0.363672 | 0.437483 | 0.470150 | 0.325602 | 0.334681 | 0.003580 |
| 11 | 0.354242 | 0.339651 | 0.390569 | 0.455494 | 0.289818 | 0.247560 | 0.003289 |
| 12 | 0.382914 | 0.359895 | 0.440761 | 0.465457 | 0.325238 | 0.315950 | 0.003612 |

The trajectory is finite, non-collapsed, and source-informative, but it continues the temporal precision/recall oscillation rather than showing clean late improvement. Epochs 8-9 reach the best aggregate result through higher recall and a wider footprint. Epochs 10 and 12 shift toward higher precision, higher Google Dice, and a smaller footprint, but recall and MIT Dice fall enough to reduce the primary metric. Epoch 11 is a clear regression. This is not evidence for an unchanged late36 continuation: the best checkpoint occurs before the final quarter, and the final epoch is a trade-off endpoint rather than a continuing rise in `val/filtered_dice`.

Raw-to-filtered differences at the selected checkpoint are modest: raw Dice 0.4105 versus filtered Dice 0.3943, raw recall 0.4141 versus filtered recall 0.3831, raw predicted-positive fraction 0.005261 versus filtered predicted-positive fraction 0.004874. Artifact Filters remove some footprint, but they do not create the result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3085, 0.5593, 0.6796, and 0.4787. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-298 as a completed, resource-safe, scientifically useful temporal family-development result, but not a frontier or promotion candidate. The soft-agreement design answered the ABI-297 failure mode in the intended direction: it recovered much of the recall and connectivity lost by the hard agreement/veto design while retaining a smaller, more precise footprint than ABI-296. This makes the ABI-296/297/298 sequence useful mechanism evidence: local temporal correlation raises support, hard orientation agreement over-suppresses recall, and soft orientation agreement offers a middle operating point.

The middle operating point is not enough to displace stronger temporal comparators. ABI-298 remains below ABI-223/238/285 on aggregate and source-stratified filtered Dice, and it does not solve the campaign's central temporal line-continuity problem. It is also close enough to ABI-296 that another small head-only continuation risks spending Runs on the same oscillatory precision/recall curve.

The local-correlation branch should not be abandoned solely because it trails mature comparators, but the exact soft-agreement design has reached a bounded negative/mixed conclusion. Future temporal work should be mechanism-changing, not an unchanged late36 request and not another minor local-correlation calibration tweak. A useful next temporal hypothesis would need a stronger architectural change that preserves the center-detail/recall path while improving connected-line organization or precision at threshold 0.5, for example a line-continuity decoder that uses local-correlation support without expanding broad clutter, or a return to the ABI-223/238 attention family with explicit evidence sharpening. If no such mechanism is stated, broaden away from local temporal matching.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-298. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not request an unchanged late36 continuation of this exact soft-agreement local-correlation design; the exploratory run completed, peaked at epoch 9, and then oscillated toward compact lower-recall checkpoints.

Record ABI-298 as useful mechanism evidence and a bounded end to the immediate ABI-296/297 local-correlation head sequence. If spending another Run in temporal correlation, require a mechanism-changing continuity or cleanliness component; otherwise broaden the frontier.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_030016_a73097/candidate/PROPOSAL.md`
- `run_20260914_030016_a73097/candidate/README.md`
- `run_20260914_030016_a73097/candidate/manifest.yaml`
- `run_20260914_030016_a73097/resolved_manifest.yaml`
- `run_20260914_030016_a73097/execution.json`
- `run_20260914_030016_a73097/outputs/model_summary.json`
- `run_20260914_030016_a73097/outputs/best_metrics.json`
- `run_20260914_030016_a73097/outputs/final_metrics.json`
- `run_20260914_030016_a73097/outputs/metrics.jsonl`
- `run_20260914_030016_a73097/outputs/resource_profile.json`
- `run_20260914_030016_a73097/outputs/validation_postprocessing/index.json`
- `run_20260914_030016_a73097/outputs/prediction_samples/samples.json`
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260914_015932_e13da3/outputs/best_metrics.json` and `/history/research-notes/abi297-temporal-orientation-agreement-correlation-unet.md` for ABI-297 hard orientation-agreement comparison context
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
