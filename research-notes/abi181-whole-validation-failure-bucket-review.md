# ABI-181 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1` for ABI-181 Run `run_20260902_150611_cbbf35`.

The evaluation request asked whether ABI-181's late-improving capped gains from the selected epoch-22 checkpoint survive on the full 3,088-sample Working Validation Split, and whether failure buckets show that the gain is offset by connectivity weakness, negative-patch clutter, threshold instability, or Dataset Source-specific degradation. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-181 signed-detail full-scale skip ASPP late36 BCE-Dice Centerline-auxiliary Run: `run_20260902_150611_cbbf35`, Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-173 parent signed-detail full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary Run: `run_20260901_234732_bd5917`, Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice precision/connectivity reference: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice whole-validation aggregate reference: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky whole-validation aggregate/source-balance comparator: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-181 reached:

| Metric | ABI-181 whole validation |
| --- | ---: |
| Filtered Dice | 0.4124 |
| MIT filtered Dice | 0.3988 |
| Google filtered Dice | 0.4395 |
| Filtered precision | 0.4466 |
| Filtered recall | 0.3832 |
| Filtered contrail connectivity | 0.3676 |
| Filtered predicted-positive pixels | 608,649 |
| Filtered false-positive pixels | 336,853 |
| Filtered false-negative pixels | 437,567 |

ABI-181's capped late-improving signal survived whole-validation evaluation. The capped best-validation filtered Dice was 0.4104 at epoch 22; whole-validation filtered Dice was 0.4124. MIT filtered Dice was essentially unchanged-to-better relative to the cap, 0.3962 capped versus 0.3988 whole validation. Google filtered Dice softened from 0.4486 capped to 0.4395 whole validation but remained above the parent and above recent SZA-aware ASPP/detail comparators. Precision, recall, connectivity, and predicted-positive fraction stayed close to the capped operating point.

Relative to ABI-173, ABI-181 improved full-validation filtered Dice from 0.3973 to 0.4124, MIT filtered Dice from 0.3870 to 0.3988, Google filtered Dice from 0.4161 to 0.4395, precision from 0.4263 to 0.4466, recall from 0.3719 to 0.3832, and connectivity from 0.3197 to 0.3676. It also reduced filtered predicted-positive pixels from 618,932 to 608,649, false-positive pixels from 355,097 to 336,853, and false-negative pixels from 445,528 to 437,567. The late-improving budget therefore produced a real whole-validation improvement over the exact architecture parent rather than only a capped-subset fluctuation.

Relative to ABI-154, ABI-181 has higher filtered Dice, MIT filtered Dice, Google filtered Dice, and recall, but lower precision and lower connectivity. ABI-154 remains the cleaner connected-line reference. Relative to ABI-130, ABI-181 improves aggregate, MIT, and Google filtered Dice, improves precision and recall slightly, and lowers false-negative pixels, but still trails ABI-130 on connectivity. Relative to ABI-068, ABI-181 improves aggregate and Google filtered Dice plus precision and false-positive burden, while ABI-068 remains better on recall, connectivity, and MIT filtered Dice. ABI-181 is therefore the strongest whole-validation-tested aggregate filtered-Dice result in the local Research History, but not a uniformly better precision/connectivity/recall result.

Against the canonical full-validation MCAST summaries, ABI-181's filtered Dice 0.4124 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873) in this shared evaluation context. ABI-181's precision is close to MCAST 1.1 and above MCAST 2.1, its recall is above MCAST 1.1 and below MCAST 2.1, and its connectivity is between MCAST 2.1 and MCAST 1.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows limited additional filtered-Dice upside and good precision/recall balance near a lower threshold. ABI-181's filtered Dice improves from 0.4124 at the fixed 0.5 threshold to 0.4186 at threshold 0.15. The closest filtered precision/recall balance is threshold 0.25, with Dice 0.4179, precision 0.4182, recall 0.4177, and a precision/recall gap of about 0.0005. Raw Dice similarly improves from 0.4271 at threshold 0.5 to 0.4320 at threshold 0.20.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that ABI-181's selected checkpoint is reasonably calibrated at the fixed threshold, with modest residual threshold-sweep headroom.

## Failure-bucket observations

Failure buckets support the whole-validation aggregate improvement while clarifying the remaining tradeoff:

1. Negative-patch clutter improved materially versus ABI-173 but did not reach ABI-154's false-positive discipline. Among 2,003 negative validation patches, 1,286 had at least one filtered predicted-positive pixel. Median negative-patch false-positive count was 9 pixels. Total negative-patch false-positive pixels were 77,592, with 223 negative patches above 100 filtered false-positive pixels, 10 above 500, and none above 1,000. This is much lower than ABI-173's 1,423 nonempty negative patches and 100,043 negative-patch false-positive pixels, close to ABI-130's 77,746 total negative-patch false-positive pixels but with more nonempty negatives, and still worse than ABI-154's 1,032 nonempty negatives and 61,426 negative-patch false-positive pixels.
2. Positive-patch severe misses are mixed. ABI-181 had 32 positive validation patches with zero filtered predicted-positive pixels, worse than ABI-173's 17 and ABI-068's 26, but better than ABI-130's 37 and ABI-154's 52. It had 169 positive patches below 0.1 filtered Dice, 239 below 0.2 filtered Dice, and 258 below 0.2 filtered recall. Relative to ABI-173, low-Dice positive patches improved slightly while zero-prediction positives worsened.
3. Median positive-patch quality improved over the parent. Median positive-patch filtered Dice was 0.4118, median precision 0.4928, and median recall 0.4207. ABI-173 medians were 0.4000, 0.4615, and 0.4081. By Dataset Source, ABI-181's median positive-patch filtered Dice was 0.3877 on MIT and 0.4458 on Google; median precision was 0.4392 on MIT and 0.5461 on Google; median recall was 0.3968 on MIT and 0.4386 on Google. The Google positive-patch operating point is strong, while MIT remains the weaker source and helps explain why ABI-068 still has a source-balance advantage.

Artifact Filters removed 41,553 predicted-positive pixels over the full split, corresponding to 166,212 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4271 versus filtered Dice 0.4124; raw predicted-positive pixels were 650,202 versus 608,649 filtered. Filtering removed both false positives and true positives enough to lower Dice slightly. This does not indicate primary Artifact Filter dependence; the raw-to-filtered gap is comparable to recent SZA-aware ASPP/detail branches.

The retained diagnostic sample pairs and GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Interpretation

Classify ABI-181's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the late-improving signed-detail full-scale skip ASPP branch. The evaluation confirms that the Harness-owned longer budget can produce a meaningful selected-checkpoint improvement for late-improving close continuations.

ABI-181 should replace ABI-173 as the whole-validation-tested signed-detail full-scale skip ASPP reference and replace ABI-130/ABI-173 as the local whole-validation aggregate filtered-Dice reference. It should not erase the rest of the frontier: ABI-154 remains the precision/connectivity reference, and ABI-068 remains useful as a MIT/source-balance and recall/connectivity comparator. The main unresolved weakness is not aggregate overlap but preserving ABI-181's improved precision and recall while recovering stronger connected-line structure and reducing the remaining MIT weakness without increasing positive-area clutter.

## Decision

Do not promote ABI-181 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-181 as the strongest whole-validation-tested aggregate filtered-Dice Result in local Research History and as positive evidence for using the late-improving budget on eligible close continuations. Do not repeat ABI-181 unchanged: the 36-epoch trajectory already clarified the exact same architecture, and the failure buckets point to architecture/calibration refinement rather than another unchanged epoch extension.

A reasonable next in-contract hypothesis is a controlled continuation from ABI-181/ABI-173 that preserves signed full-resolution detail and full-scale skip recall while adding a conservative line-continuity or MIT-robust detail calibration mechanism under trusted `bce_dice` or `focal_tversky`, provider-derived Centerline Target supervision, approved `abi_16ch_plus_sza` input, and Harness-owned sampling/augmentation/loss/metric/Artifact Filter boundaries. No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/summary.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/final_metrics.json`
- `run_20260902_150611_cbbf35/outputs/metrics.jsonl`
- `run_20260902_150611_cbbf35/outputs/resource_profile.json`
- `run_20260902_150611_cbbf35/outputs/model_summary.json`
- `run_20260902_150611_cbbf35/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/candidate/budget_request.yaml`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
