# ABI-300 temporal attention evidence-sharpened recall U-Net

research-figures: []

## Scope

This note records ABI-300, Candidate `abi300_temporal_attention_evidence_sharpened_recall_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260914_050146_4e9b36`.

ABI-300 was a bounded temporal family-development continuation after the ABI-296/297/298/299 local-correlation branch. It returned to the ABI-223/238 temporal-attention U-Net family and added an evidence-sharpening head with region, line, detail, and temporal-agreement streams. The intended mechanism was to raise true contrail logits at the fixed 0.5 threshold while retaining ABI-223/238-style precision/connectivity and avoiding the broader local-correlation footprint seen in ABI-296/299.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and `temporal_eligible_center` selection. It used trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, cache reads, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Execution result

ABI-300 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`; frame offsets `[-1, 0, 1]`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `temporal_eligible_center`.
- Capped sample counts: 2,048 train and 1,614 temporal-eligible validation ABI Patches.
- Parameter count: 3,227,456, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,967,547,392 / 5,305,794,560 bytes.
- Training wall time: 1,362.7 s; validation wall time: 1,085.6 s; total Run wall time: 2,450.0 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 10.

## Best-validation metrics

| Metric | ABI-300 evidence-sharpened attention | ABI-299 correlation line-continuity | ABI-296 local correlation | ABI-223 temporal attention | ABI-238 directional temporal attention | ABI-285 temporal C4 line-state late36 | ABI-289 dual-evidence temporal | ABI-290 precision-gated temporal | ABI-291 five-frame persistence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 10 | 9 | 9 | 36 | 29 | 32 | 8 | 9 | 10 |
| Filtered Dice | 0.370607 | 0.396406 | 0.395208 | 0.419776 | 0.420235 | 0.422195 | 0.380244 | 0.379803 | 0.358719 |
| MIT filtered Dice | 0.357208 | 0.383650 | 0.379768 | 0.398498 | 0.405383 | 0.400831 | 0.372684 | 0.368809 | 0.336776 |
| Google filtered Dice | 0.403910 | 0.428424 | 0.433397 | 0.476764 | 0.460838 | 0.477410 | 0.398412 | 0.406267 | 0.414922 |
| Filtered precision | 0.420466 | 0.408439 | 0.389486 | 0.483764 | 0.488730 | 0.448400 | 0.361568 | 0.384437 | 0.495053 |
| Filtered recall | 0.331319 | 0.385063 | 0.401101 | 0.370738 | 0.368578 | 0.398883 | 0.400955 | 0.375279 | 0.281261 |
| Filtered connectivity | 0.242191 | 0.268913 | 0.331894 | 0.412427 | 0.352239 | 0.243387 | 0.249988 | 0.245732 | 0.295736 |
| Filtered predicted-positive fraction | 0.004074 | 0.004874 | 0.005324 | 0.003962 | 0.003899 | 0.004599 | 0.005733 | 0.005046 | 0.002937 |

ABI-300 is a completed but negative temporal-attention family-development result. It did not recover the ABI-223/238/285 temporal frontier and did not beat the immediate ABI-296/299 local-correlation references. Its best filtered Dice, 0.3706, trails ABI-223/238/285 by about 0.049 to 0.052 and trails ABI-296/299 by about 0.025 to 0.026. It is also weaker than the recent ABI-289/290 temporal evidence heads, although it remains above ABI-291's five-frame persistence scout.

The evidence-sharpening head appears to have shifted the model toward a smaller, more conservative footprint rather than recall sharpening. Against ABI-296, ABI-300 improves precision from 0.3895 to 0.4205 and reduces filtered predicted-positive fraction from 0.005324 to 0.004074, but recall falls from 0.4011 to 0.3313, MIT Dice falls from 0.3798 to 0.3572, Google Dice falls from 0.4334 to 0.4039, and connectivity falls from 0.3319 to 0.2422. Against ABI-299, ABI-300 preserves a similar compactness/precision direction but again loses recall, source-stratified Dice, and connectivity. This is the opposite of the intended fixed-threshold recall-support mechanism.

Relative to ABI-223/238, ABI-300 fails on both sides of the intended trade-off: it does not raise recall above those comparators, and it does not preserve their precision or connected-line behavior. ABI-300's recall is lower than ABI-223/238, its precision is much lower, and its connectivity is far below ABI-223/238. The result therefore does not support this particular uncertainty-band evidence-sharpening design as a way to improve the temporal-attention frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.198763 | 0.195217 | 0.206631 | 0.246550 | 0.166492 | 0.164431 | 0.003491 |
| 2 | 0.216743 | 0.215614 | 0.219063 | 0.247572 | 0.192741 | 0.185437 | 0.004025 |
| 3 | 0.291496 | 0.282211 | 0.313129 | 0.342147 | 0.253908 | 0.216725 | 0.003836 |
| 4 | 0.252524 | 0.234426 | 0.296302 | 0.351451 | 0.197057 | 0.234591 | 0.002899 |
| 5 | 0.348730 | 0.331933 | 0.389229 | 0.414206 | 0.301129 | 0.279883 | 0.003758 |
| 6 | 0.332999 | 0.324883 | 0.352419 | 0.355411 | 0.313247 | 0.235826 | 0.004556 |
| 7 | 0.328446 | 0.304069 | 0.393050 | 0.505081 | 0.243345 | 0.318816 | 0.002491 |
| 8 | 0.369240 | 0.361039 | 0.389639 | 0.401276 | 0.341942 | 0.239146 | 0.004405 |
| 9 | 0.367791 | 0.359348 | 0.387489 | 0.356131 | 0.380240 | 0.224714 | 0.005520 |
| 10 | 0.370607 | 0.357208 | 0.403910 | 0.420466 | 0.331319 | 0.242191 | 0.004074 |
| 11 | 0.361987 | 0.344289 | 0.405760 | 0.422942 | 0.316388 | 0.194402 | 0.003867 |
| 12 | 0.367835 | 0.347382 | 0.420527 | 0.462754 | 0.305227 | 0.217187 | 0.003410 |

The trajectory is finite, non-collapsed, and source-informative, but it is not late-improving evidence for an unchanged 36-epoch continuation. The best checkpoint occurs at epoch 10 after oscillatory precision/recall behavior. Epoch 12 improves Google Dice and precision, but it suppresses recall and MIT Dice enough to remain below the best primary metric. Epoch 9 shows the highest recall but does so by widening the predicted-positive fraction and dropping precision, and still does not reach the local-correlation or temporal-attention comparators. This pattern suggests the evidence-sharpening head is another precision/recall trade-off surface rather than a clean threshold-evidence improvement.

Raw-to-filtered differences at the selected checkpoint are modest: raw Dice 0.3862 versus filtered Dice 0.3706, raw recall 0.3571 versus filtered recall 0.3313, and raw predicted-positive fraction 0.004389 versus filtered predicted-positive fraction 0.004074. Artifact Filters remove some footprint, but they do not create the result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4197, 0.5345, 0.5328, and 0.3906. These samples support that the selected checkpoint is not a trivial all-negative or all-positive collapse, but they are not a substitute for whole-population temporal-eligible metrics.

## Interpretation

Classify ABI-300 as a completed, resource-safe, scientifically useful negative result for this exact temporal-attention evidence-sharpening head. It provides a bounded answer to the proposal's central question: adding uncertainty-band region/line/detail/agreement support to the ABI-223/238 attention family did not raise fixed-threshold recall and did not preserve the temporal-attention family's precision/connectivity advantages. The learned support/clutter gates likely made the footprint more conservative without sufficient true-positive recovery.

This should not eliminate temporal attention as a family. ABI-223/238 remain strong temporal comparators, and ABI-285 still provides useful recall-oriented temporal C4 evidence. However, ABI-300's specific calibration-style evidence-sharpening head has a hard local stop under the exploratory policy: it is finite, but it misses its stated success criteria, peaks before the final epoch, and underperforms both the temporal-attention frontier and the immediate local-correlation branch.

Future temporal work should avoid another minor uncertainty-band head tweak or unchanged late36 continuation of ABI-300. If temporal work continues, the next hypothesis should be mechanism-changing: for example, a different attention-line continuity design that couples connected-line support to recall instead of subtractive gating, or a pivot back to C4/orientation priors with explicit recall support. If no such mechanism is available, broaden away from this temporal head design rather than spending another Run on the same precision/recall surface.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal cache access, sample selection, coordinates, Dataset Source identity, downloads, or resource scheduling.

## Decision

Do not promote ABI-300. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped result. Do not request an unchanged late36 continuation of ABI-300; the exploratory run peaked at epoch 10 and final epochs traded toward higher precision/Google Dice at lower recall and MIT Dice rather than a clean rising primary trajectory.

Record ABI-300 as a bounded negative result for the temporal-attention evidence-sharpening head. The temporal branch remains eligible only for mechanism-changing follow-up; this exact head design should stop.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_050146_4e9b36/candidate/PROPOSAL.md`
- `run_20260914_050146_4e9b36/candidate/README.md`
- `run_20260914_050146_4e9b36/candidate/manifest.yaml`
- `run_20260914_050146_4e9b36/resolved_manifest.yaml`
- `run_20260914_050146_4e9b36/execution.json`
- `run_20260914_050146_4e9b36/outputs/model_summary.json`
- `run_20260914_050146_4e9b36/outputs/best_metrics.json`
- `run_20260914_050146_4e9b36/outputs/final_metrics.json`
- `run_20260914_050146_4e9b36/outputs/metrics.jsonl`
- `run_20260914_050146_4e9b36/outputs/resource_profile.json`
- `run_20260914_050146_4e9b36/outputs/validation_postprocessing/index.json`
- `run_20260914_050146_4e9b36/outputs/prediction_samples/samples.json`
- `run_20260914_010510_9ea033/outputs/best_metrics.json` and `/history/research-notes/abi296-temporal-local-correlation-center-detail-unet.md` for ABI-296 local-correlation comparison context
- `run_20260914_040326_98380c/outputs/best_metrics.json` and `/history/research-notes/abi299-temporal-correlation-line-continuity-decoder-unet.md` for ABI-299 line-continuity correlation comparison context
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
