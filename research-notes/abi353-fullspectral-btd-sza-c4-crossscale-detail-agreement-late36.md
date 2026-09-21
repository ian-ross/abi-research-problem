# ABI-353 full-spectral BTD+SZA C4 cross-scale detail agreement late36

research-figures: []

## Scope

This note records ABI-353, Candidate `abi353_fullspectral_btd_sza_c4_crossscale_detail_agreement_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_053527_64085b`, and Harness-owned Post-Run Evaluation `eval_evalreq_abi353_wholeval_failure_buckets_v1`.

ABI-353 was the approved late-improving continuation of ABI-352. It intentionally preserved the ABI-352 single-frame architecture and training policy: provider-owned `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, batch size 4, and the pre-head cross-scale detail-agreement fusion feeding C4 rotation-shared line context.

The capped Run is representative feasibility evidence. The Post-Run Evaluation is a whole Working Validation Split diagnostic for the selected checkpoint, not promotion authority.

## Execution result

ABI-353 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested `late_improving` budget was approved from ABI-352 parent evidence.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Trusted augmentation policy: `random_mirroring`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,970,653, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 8,822,962,176 / 10,431,234,048 bytes.
- Training wall time: 4,132.0 s; validation wall time: 4,049.5 s; total Run wall time: 8,183.9 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 34.

## Capped best-validation metrics

| Metric | ABI-353 late36 cross-scale detail agreement | ABI-352 exploratory parent | ABI-343 C4 precision-veto recall | ABI-342 C4 recall bridge | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 12 | 32 | 36 | 31 | 34 |
| Filtered Dice | 0.417439 | 0.387651 | 0.409827 | 0.415499 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.401665 | 0.371563 | 0.392320 | 0.398614 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.456492 | 0.426257 | 0.453242 | 0.460044 | 0.468855 | 0.468151 |
| Filtered precision | 0.442512 | 0.378511 | 0.417766 | 0.397609 | 0.480886 | 0.439467 |
| Filtered recall | 0.395056 | 0.397243 | 0.402184 | 0.435075 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.348271 | 0.292383 | 0.379763 | 0.405280 | 0.392524 | 0.457773 |
| Filtered predicted-positive pixels | 434,203 | 510,432 | 468,221 | 532,191 | 371,346 | 460,724 |

The late budget substantially improves the ABI-352 parent by aggregate filtered Dice (+0.0298), MIT Dice (+0.0301), Google Dice (+0.0302), precision (+0.0640), and connectivity (+0.0559), while reducing the filtered predicted-positive footprint by 76,229 pixels. It answers the ABI-352 trajectory question positively in the narrow sense that the branch was genuinely late-improving and the exploratory checkpoint was not the best achievable state.

However, the selected capped checkpoint is not a clean comparator replacement. Relative to ABI-249, ABI-353 is only +0.0010 filtered Dice and +0.0279 recall, but it loses substantial precision (-0.0384), Google Dice (-0.0124), and connectivity (-0.0443), while predicting 62,857 more filtered-positive pixels. Relative to ABI-342, ABI-353 improves compactness and precision but gives back much of the recall and connectivity that made ABI-342 diagnostically useful. Relative to ABI-202, it remains lower on aggregate Dice, both sources, recall, and connectivity.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected capped checkpoint, raw Dice was 0.432201 versus filtered Dice 0.417439; raw recall was 0.421721 versus filtered recall 0.395056; raw predicted-positive pixels were 462,775 versus 434,203 filtered. Artifact Filters removed 28,572 predicted-positive pixels and lowered the score.

## Whole-validation diagnostic

The whole-validation evaluation on the canonical 3,088-sample Working Validation Split gives a similar but slightly harsher readout.

| Metric | ABI-353 whole-val diagnostic | ABI-249 whole-val C4 comparator | ABI-202 whole-val reference |
| --- | ---: | ---: | ---: |
| Filtered Dice | 0.417547 | 0.419702 | 0.431156 |
| MIT filtered Dice | 0.402795 | 0.399130 | 0.414066 |
| Google filtered Dice | 0.444614 | 0.460084 | 0.464440 |
| Filtered precision | 0.441948 | 0.486539 | 0.443073 |
| Filtered recall | 0.395699 | 0.369010 | 0.419864 |
| Filtered connectivity | 0.349933 | 0.397527 | 0.462504 |
| Filtered predicted-positive pixels | 635,129 | 538,008 | 672,206 |

ABI-353 transfers as a near-ABI-249 aggregate result but does not displace ABI-249. It improves MIT filtered Dice and recall versus ABI-249, but the cost is lower precision, lower Google Dice, much weaker connectivity, and about 97k extra filtered-positive pixels. Compared with ABI-202, ABI-353 is lower on every primary quality dimension except having nearly equal precision and a smaller prediction footprint.

The source pattern is instructive: ABI-353's capped validation suggested balanced source gains, but the whole-validation diagnostic exposes a Google transfer gap. Its MIT filtered Dice is slightly above ABI-249, while Google filtered Dice is -0.0155 below ABI-249 and -0.0198 below ABI-202. This is not a catastrophic source failure, but it is not a source-balance breakthrough.

Raw versus filtered whole-validation behavior again does not indicate Artifact Filter dependence. Whole-val raw Dice was 0.432008 versus filtered Dice 0.417547; raw recall was 0.421557 versus filtered recall 0.395699; raw predicted-positive pixels were 675,042 versus 635,129 filtered. Artifact Filters removed 39,913 pixels and lowered the score.

## Failure-bucket observations

The whole-validation failure buckets show the trade-off clearly.

| Bucket metric | ABI-353 | ABI-249 | ABI-202 |
| --- | ---: | ---: | ---: |
| Positive samples | 1,085 | 1,085 | 1,085 |
| Complete positive misses | 123 | 134 | 140 |
| Positive recall < 0.20 | 231 | 280 | 240 |
| Positive recall < 0.50 | 626 | 684 | 602 |
| Positive median recall | 0.4443 | 0.3978 | 0.4597 |
| Positive median Dice | 0.4370 | 0.4310 | 0.4275 |
| Positive median connectivity | 0.4462 | 0.4251 | 0.4248 |
| Positive connectivity < 0.20 | 212 | 241 | 230 |
| Negative samples | 2,003 | 2,003 | 2,003 |
| Negative samples with any prediction | 1,379 | 1,217 | 1,013 |
| Negative samples >50 predicted pixels | 655 | 425 | 437 |
| Negative samples >200 predicted pixels | 71 | 39 | 77 |
| Total negative-patch predicted pixels | 96,138 | 66,218 | 71,310 |

ABI-353 improves positive-tail coverage relative to ABI-249: fewer complete misses, fewer low-recall positives, higher positive median recall/Dice/connectivity, and fewer low-connectivity positives. That is the main success of the late continuation. But the gain is bought with much more negative-patch touch rate and clutter: 162 more negative samples touched than ABI-249, 230 more negative patches above 50 predicted pixels, and about 30k more total negative-patch predicted pixels. Against ABI-202, ABI-353 has fewer complete misses and low-connectivity positives, but it trails on low-recall positive count and has more negative-patch predicted pixels.

Source-stratified buckets keep the residual imbalance visible:

| Source bucket | MIT | Google |
| --- | ---: | ---: |
| Positive samples | 533 | 552 |
| Positive median recall | 0.3929 | 0.5000 |
| Positive median Dice | 0.3983 | 0.4878 |
| Positive median connectivity | 0.3968 | 0.4996 |
| Complete positive misses | 63 | 60 |
| Positive recall < 0.25 | 153 | 131 |
| Negative samples | 699 | 1,304 |
| Negative samples with any prediction | 411 | 968 |
| Negative samples >128 predicted pixels | 67 | 108 |
| Negative samples >512 predicted pixels | 4 | 4 |
| Total negative-patch predicted pixels | 33,407 | 62,731 |

Google positives are easier for ABI-353 at the median, but Google also contributes most negative-patch clutter because there are many more Google negative patches in the whole validation split. MIT remains the weaker positive-recall/connectivity source. This combination explains why aggregate recall improves over ABI-249 while Google Dice still underperforms: ABI-353 broadens prediction support but does not keep ABI-249's compactness on Google.

## Threshold behavior

The threshold sweep shows only modest diagnostic headroom around the fixed 0.5 threshold:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low threshold | 0.05 | 0.421807 | 0.368926 | 0.492384 | 946,745 |
| Best filtered Dice | 0.10 | 0.424592 | 0.392829 | 0.461944 | 834,169 |
| Near-balance reference | 0.20 | 0.423460 | 0.412945 | 0.434525 | 746,433 |
| Primary evaluation | 0.50 | 0.417547 | 0.441948 | 0.395699 | 635,129 |
| High-precision reference | 0.70 | 0.410636 | 0.458494 | 0.371824 | 575,270 |
| Very high threshold | 0.90 | 0.381673 | 0.490244 | 0.312472 | 452,134 |

The best diagnostic threshold is +0.0070 filtered Dice above the trusted fixed 0.5 threshold, but it requires substantially broader predictions and lower precision. This is useful architecture evidence for sub-threshold recall reserve, not authorization for Candidate-owned thresholding, calibration, postprocessing, metrics, losses, Artifact Filters, or validation selection.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.210534 | 0.233478 | 0.171913 | 0.175152 | 0.263828 | 0.091276 | 0.005458 |
| 5 | 0.333812 | 0.316064 | 0.373713 | 0.406929 | 0.282968 | 0.310259 | 0.002520 |
| 10 | 0.355500 | 0.337891 | 0.394216 | 0.420624 | 0.307839 | 0.298360 | 0.002652 |
| 12 | 0.391024 | 0.371477 | 0.436892 | 0.425858 | 0.361457 | 0.346733 | 0.003076 |
| 16 | 0.384916 | 0.372593 | 0.414055 | 0.415490 | 0.358533 | 0.233677 | 0.003127 |
| 20 | 0.379859 | 0.362058 | 0.422275 | 0.425146 | 0.343292 | 0.248091 | 0.002926 |
| 24 | 0.381793 | 0.358426 | 0.436397 | 0.423577 | 0.347513 | 0.272663 | 0.002973 |
| 28 | 0.406077 | 0.381840 | 0.467532 | 0.499265 | 0.342204 | 0.451439 | 0.002484 |
| 31 | 0.398836 | 0.372656 | 0.465922 | 0.502591 | 0.330589 | 0.470563 | 0.002384 |
| 34 | 0.417439 | 0.401665 | 0.456492 | 0.442512 | 0.395056 | 0.348271 | 0.003235 |
| 36 | 0.403217 | 0.379763 | 0.464140 | 0.512144 | 0.332499 | 0.429292 | 0.002353 |

The trajectory confirms late-budget value and state instability. ABI-353 did not plateau at the exploratory boundary; it gained materially after epoch 12 and selected epoch 34. But the compact/high-connectivity states around epochs 28, 31, and 36 are not aligned with the best aggregate filtered-Dice state at epoch 34. The final epoch is high precision and high connectivity but low recall; epoch 34 is higher recall and aggregate Dice but lower compactness/connectivity. This instability is the same C4-family coupling problem seen in ABI-342/343/352.

## Interpretation

Classify ABI-353 as useful but non-frontier single-frame C4-family evidence.

The positive result is that late training validates ABI-352's pre-head cross-scale detail-agreement mechanism as more than an exploratory false start. It becomes near-ABI-249 on whole-validation aggregate filtered Dice, improves positive-tail recall buckets, and produces source-informative MIT gains. This makes it a helpful diagnostic for recall-support design.

The negative result is that the mechanism still fails the intended compact C4 success criterion. It does not preserve ABI-249's precision/compactness, does not recover ABI-202's aggregate/connectivity balance, and does not stabilize high-connectivity compact states at the selected checkpoint. The whole-validation diagnostic also shows a Google transfer penalty and increased negative-patch clutter. Therefore ABI-249 remains the compact high-precision single-frame C4 comparator, ABI-202 remains the aggregate whole-validation reference, ABI-342 remains the recall-biased C4 diagnostic, ABI-343 remains the precision-veto diagnostic, and ABI-353 is a late-improved cross-scale detail-agreement diagnostic rather than a new frontier target.

Do not run another unchanged late36 continuation of ABI-352/353. Future work in this area should be mechanism-changing: separate a stable compact C4 anchor from a recall sidecar more explicitly, move continuity support earlier without widening negative-patch clutter, or combine this positive-tail lesson with temporal/center-frame evidence sharpening. Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of bounds.

## Decision

Do not promote ABI-353. The whole-validation diagnostic is near ABI-249 on aggregate Dice but misses the compactness/connectivity criteria and remains below ABI-202.

The exact cross-scale detail-agreement late36 question is answered. A future handoff should broaden or materially change the mechanism rather than repeat this branch unchanged.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_053527_64085b/candidate/PROPOSAL.md`
- `run_20260919_053527_64085b/candidate/README.md`
- `run_20260919_053527_64085b/candidate/manifest.yaml`
- `run_20260919_053527_64085b/candidate/budget_request.yaml`
- `run_20260919_053527_64085b/resolved_manifest.yaml`
- `run_20260919_053527_64085b/execution.json`
- `run_20260919_053527_64085b/run_metadata.json`
- `run_20260919_053527_64085b/outputs/model_summary.json`
- `run_20260919_053527_64085b/outputs/best_metrics.json`
- `run_20260919_053527_64085b/outputs/final_metrics.json`
- `run_20260919_053527_64085b/outputs/metrics.jsonl`
- `run_20260919_053527_64085b/outputs/resource_profile.json`
- `run_20260919_053527_64085b/outputs/validation_postprocessing/index.json`
- `run_20260919_053527_64085b/outputs/prediction_samples/samples.json`
- `run_20260919_053527_64085b/outputs/evaluations/eval_evalreq_abi353_wholeval_failure_buckets_v1/summary.json`
- `run_20260919_053527_64085b/outputs/evaluations/eval_evalreq_abi353_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260919_053527_64085b/outputs/evaluations/eval_evalreq_abi353_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260919_053527_64085b/outputs/evaluations/eval_evalreq_abi353_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260919_044205_9523b3/outputs/best_metrics.json` and `/history/research-notes/abi352-fullspectral-btd-sza-c4-crossscale-detail-agreement.md`
- `run_20260918_081800_9f0872/outputs/best_metrics.json` and `/history/research-notes/abi343-fullspectral-btd-sza-c4-precision-veto-recall-late36.md`
- `run_20260918_055403_f17232/outputs/best_metrics.json` and `/history/research-notes/abi342-fullspectral-btd-sza-c4-recall-bridge-late36.md`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
