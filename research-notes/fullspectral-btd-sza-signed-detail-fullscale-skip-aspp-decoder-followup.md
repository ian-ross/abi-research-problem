# Full-spectral BTD+SZA signed-detail full-scale skip ASPP decoder follow-up

research-figures: []

## Scope

This note records ABI-173 after Run `run_20260901_234732_bd5917` completed.

Source Runs:

- ABI-173 signed-detail full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary continuation: `run_20260901_234732_bd5917`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice parent and whole-validation-tested precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`
- ABI-156 full-scale skip ASPP/detail feature-calibration continuation: `run_20260901_090713_9c7d32`
- ABI-168 compact sparse-oriented ASPP/detail continuation: `run_20260901_192929_0da8c3`
- ABI-171 full-scale skip ASPP/detail Centerline Target weight 0.01 comparison: `run_20260901_220525_8c0116`
- ABI-172 full-scale skip ASPP/detail focal-Tversky comparison: `run_20260901_225502_53acd2`

ABI-173 was a family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, the trusted 1,024-record-per-Dataset-Source/split representative cap, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architecture change was replacing the signed-unaware high-resolution detail stem with local and mid-scale positive/negative residual streams plus broad context before full-scale skip fusion.

## Contract and resource observation

ABI-173 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,810 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,861.2 seconds total wall time, 1,520.3 seconds training wall time, 1,338.9 seconds validation wall time, 16.17 training samples per second, 18.35 validation samples per second, 9,040,003,584 bytes peak CUDA allocated, and 10,506,731,520 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260901_192929_0da8c3` | ABI-168 | compact sparse-oriented ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3824 | 0.3680 | 0.4178 | 0.4019 | 0.3646 | 0.2609 | 0.00329 |
| `run_20260901_220525_8c0116` | ABI-171 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, centerline w0.01 | 8 | 0.3816 | 0.3703 | 0.4086 | 0.4101 | 0.3569 | 0.3473 | 0.00315 |
| `run_20260901_225502_53acd2` | ABI-172 | full-scale skip ASPP/detail decoder, focal-Tversky, ABI-16+BTD+SZA | 10 | 0.3578 | 0.3552 | 0.3631 | 0.3185 | 0.4081 | 0.2312 | 0.00464 |

ABI-173 is a useful positive-but-mixed capped continuation. Relative to ABI-154, the signed-detail stem achieved the intended default-threshold recall recovery and modest overlap gains: aggregate filtered Dice rose from 0.3944 to 0.3962 (+0.0018), MIT filtered Dice from 0.3824 to 0.3838 (+0.0014), Google filtered Dice from 0.4260 to 0.4269 (+0.0008), and filtered recall from 0.3359 to 0.3720 (+0.0361). The cost was meaningful: filtered precision fell from 0.4777 to 0.4238 (-0.0539), filtered connectivity fell from 0.4374 to 0.3203 (-0.1171), and filtered predicted-positive fraction rose from 0.00255 to 0.00318.

Relative to ABI-130, ABI-173 is slightly higher on capped aggregate filtered Dice (+0.0009), MIT filtered Dice (+0.0060), and recall (+0.0142), while lower on Google filtered Dice (-0.0135), precision (-0.0177), connectivity (-0.0648), and positive-area discipline. Relative to ABI-068, ABI-173 is essentially an aggregate capped near-tie, lower by only 0.00017 filtered Dice, with higher Google Dice and precision but lower MIT Dice, recall, and connectivity. This makes ABI-173 the strongest capped SZA-aware ASPP/detail-family aggregate result observed so far, but not a clear replacement for ABI-068, ABI-130, or the whole-validation-tested ABI-154 precision/connectivity branch.

## ABI-173 trajectory

ABI-173 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2111, 0.2975, 0.3007, 0.2897, 0.3408, 0.3672, 0.3623, 0.3430, 0.3602, 0.3624, 0.3768, and 0.3962. The final epoch was the selected checkpoint and the best capped filtered Dice for this Run.

The trajectory is extension-informative: after entering the 0.34-0.37 band by epoch 5-10, epochs 11-12 improved again and ended at the Run maximum rather than plateauing or collapsing. At the selected checkpoint, raw Dice was 0.4106, filtered Dice was 0.3962, filtered precision was 0.4238, filtered recall was 0.3720, filtered connectivity was 0.3203, and filtered predicted-positive fraction was 0.00318. Source-stratified filtered Dice was 0.3838 for MIT and 0.4269 for Google. MIT had filtered precision 0.4330, recall 0.3447, connectivity 0.3245, and predicted-positive fraction 0.00430; Google had filtered precision 0.4045, recall 0.4519, connectivity 0.3162, and predicted-positive fraction 0.00206.

Raw-to-filtered differences were modest but not negligible: raw Dice was 0.4106 versus filtered Dice 0.3962, raw recall was 0.3977 versus filtered recall 0.3720, and raw predicted-positive fraction was 0.00340 versus filtered 0.00318. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-173 as a completed, finite, non-collapsed, scientifically useful capped family-development result for the SZA-aware full-scale skip ASPP/detail branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The signed-detail stem is the first recent ABI-154-local architecture change to recover meaningful recall while also improving capped aggregate/source Dice over ABI-154. It avoids the severe precision collapse of ABI-172 focal-Tversky and the weaker overlap/connectivity of ABI-168/171. However, it gives back a substantial part of ABI-154's defining precision/connectivity advantage. The result is therefore not a simple promotion candidate from capped evidence; it is a new capped SZA-aware ASPP/detail aggregate branch whose trade-off needs whole-validation diagnostics before it can displace ABI-130 or ABI-154 as the SZA-aware ASPP/detail reference.

The main design lesson is that signed positive/negative detail residuals can shift the default threshold toward useful recall without a trusted-loss change, but the current implementation does not preserve enough line connectivity. Future in-contract development should avoid another unconstrained recall-expansion tweak and instead test whether signed detail can be paired with a conservative connectivity-preserving decoder or calibrated line evidence. Because ABI-173 ended at its best epoch, low score alone is not elimination evidence for signed-detail preprocessing.

## Decision

Do not promote ABI-173 from capped representative evidence and do not repeat it unchanged. Retain ABI-173 as the strongest capped SZA-aware ASPP/detail-family aggregate result, ABI-154 as the whole-validation-tested precision/connectivity branch, ABI-130 as the whole-validation-tested SZA-aware ASPP/detail aggregate reference, and ABI-068 as the capped aggregate/source-balance comparator.

A reasonable next Autonomy Step is a bounded whole-validation failure-bucket Evaluation Request for `run_20260901_234732_bd5917`. The diagnostic should test whether ABI-173's capped aggregate/MIT/Google gains over ABI-154 survive on the full 3,088-sample Working Validation Split, whether its lower connectivity versus ABI-154/130 is a full-validation blocker, and whether its recall recovery creates unacceptable negative-patch clutter. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/final_metrics.json`
- `run_20260901_234732_bd5917/outputs/metrics.jsonl`
- `run_20260901_234732_bd5917/outputs/resource_profile.json`
- `run_20260901_234732_bd5917/outputs/model_summary.json`
- `run_20260901_234732_bd5917/outputs/prediction_samples/samples.json`
- `run_20260901_234732_bd5917/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260901_192929_0da8c3/outputs/best_metrics.json`
- `run_20260901_220525_8c0116/outputs/best_metrics.json`
- `run_20260901_225502_53acd2/outputs/best_metrics.json`
