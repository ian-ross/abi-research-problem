# Full-spectral BTD+SZA signed-detail full-scale skip ASPP late36 follow-up

research-figures: []

## Scope

This note records ABI-181 after late-improving Run `run_20260902_150611_cbbf35` completed.

Source Runs:

- ABI-181 signed-detail full-scale skip ASPP late36 BCE-Dice Centerline-auxiliary continuation: `run_20260902_150611_cbbf35`
- ABI-173 parent signed-detail full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary Run: `run_20260901_234732_bd5917`
- ABI-154 SZA-aware full-scale skip ASPP/detail precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 prior whole-validation-tested SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 broader frequency-gated line U-Net aggregate/source-balance comparator: `run_20260828_010836_4ccc77`
- ABI-179 and ABI-180 recent UPerNet family scouts: `run_20260902_054206_a6b406`, `run_20260902_063801_88ca01`

ABI-181 was an exact architecture close-continuation of ABI-173. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, the signed high-resolution local and mid-scale positive/negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The only intended research change from ABI-173 was the Harness-reviewed late-improving budget request. The request was approved: `budget_class_effective: late_improving`, `effective_max_epochs: 36`, and `effective_training_wall_clock_timeout_seconds: 10800`.

## Contract and resource observation

ABI-181 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,810 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 8,674.5 seconds total wall time, 4,558.1 seconds training wall time, 4,114.2 seconds validation wall time, 16.18 training samples per second, 17.92 validation samples per second, 9,040,003,584 bytes peak CUDA allocated, and 10,506,731,520 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 22.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail full-scale skip ASPP late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 signed-detail full-scale skip ASPP | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 SZA-aware ASPP/detail decoder | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_054206_a6b406` | ABI-179 UPerNet pyramid/detail decoder | 12 | 0.3939 | 0.3774 | 0.4354 | 0.4520 | 0.3490 | 0.2895 | 0.00280 |
| `run_20260902_063801_88ca01` | ABI-180 UPerNet directional line context | 12 | 0.3885 | 0.3738 | 0.4242 | 0.4304 | 0.3541 | 0.2943 | 0.00298 |

ABI-181 is the strongest capped best-validation Result observed so far by the Harness selection metric `val/filtered_dice`. Relative to ABI-173, the late-improving budget raised best filtered Dice from 0.3962 to 0.4104, MIT filtered Dice from 0.3838 to 0.3962, Google filtered Dice from 0.4269 to 0.4486, precision from 0.4238 to 0.4423, recall from 0.3720 to 0.3828, and connectivity from 0.3203 to 0.3639, while leaving filtered predicted-positive fraction essentially unchanged.

Relative to ABI-154, ABI-181 gives much higher capped filtered Dice and recall, but still trails ABI-154's precision and connectivity. Relative to ABI-130, ABI-181 improves aggregate, MIT, and Google capped filtered Dice, with similar precision and higher recall, but lower connectivity. Relative to ABI-068, ABI-181 improves aggregate, MIT, and Google capped filtered Dice plus precision and positive-area discipline, while trailing ABI-068 on recall and connectivity. These are capped representative comparisons only; ABI-181 has not yet received a whole-validation diagnostic.

## Late-improving trajectory

ABI-181 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1877, 0.2957, 0.2873, 0.2542, 0.3180, 0.3606, 0.3532, 0.3221, 0.3797, 0.3539, 0.3666, 0.4014, 0.3637, 0.3469, 0.3978, 0.3894, 0.3456, 0.3825, 0.3889, 0.3930, 0.4060, 0.4104, 0.3730, 0.3706, 0.3721, 0.3962, 0.3898, 0.3932, 0.3998, 0.3756, 0.3873, 0.3826, 0.3986, 0.4084, 0.4080, 0.3802`.

The extension hypothesis was supported: ABI-173's final-epoch-12 improvement was not merely a short-budget fluctuation, because ABI-181 exceeded the parent at epoch 12 and then reached a clearly higher selected checkpoint at epoch 22. The post-22 trajectory was noisy rather than monotonically improving. Epochs 34 and 35 again approached the selected score, but the final epoch degraded to filtered Dice 0.3802 with lower precision, higher recall, lower connectivity, and larger positive-area fraction. This argues against another unchanged epoch-extension branch: the 36-epoch budget already clarified that the architecture can reach a better mid-run checkpoint, but the later trajectory does not show stable continued improvement.

At the selected epoch 22 checkpoint, raw Dice was 0.4254, filtered Dice was 0.4104, filtered precision was 0.4423, filtered recall was 0.3828, filtered connectivity was 0.3639, and filtered predicted-positive fraction was 0.00314. Source-stratified filtered Dice was 0.3962 for MIT and 0.4486 for Google. MIT had filtered precision 0.4388, recall 0.3611, connectivity 0.3519, and predicted-positive fraction 0.00444; Google had filtered precision 0.4509, recall 0.4464, connectivity 0.3759, and predicted-positive fraction 0.00183.

Raw-to-filtered differences were modest: raw Dice 0.4254 versus filtered Dice 0.4104, raw recall 0.4098 versus filtered recall 0.3828, and raw predicted-positive fraction 0.00336 versus filtered predicted-positive fraction 0.00314. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples again include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy; these are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-181 as a completed, finite, non-collapsed, scientifically positive capped late-improving continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The main result is that extra trusted epochs materially improved the signed-detail full-scale skip ASPP branch beyond the exploratory ceiling. ABI-181 improves the parent ABI-173 on every primary capped aggregate/source metric at the selected checkpoint and becomes the strongest capped filtered-Dice Result in the local Research History. The improvement is source-informative rather than driven by a single Dataset Source: both MIT and Google filtered Dice increased over ABI-173.

The result remains mixed because connectivity still does not recover the ABI-154 or ABI-068 connected-line level, and the final epoch degraded after a noisy plateau. The selected checkpoint is valid under Harness-owned best-checkpoint selection, but capped evidence alone is insufficient for promotion. Given ABI-173's whole-validation diagnostic, the key question is now whether ABI-181's large capped gain survives on the full 3,088-sample Working Validation Split or whether it reflects capped-subset epoch noise and/or increased negative-patch clutter not captured by aggregate capped metrics.

## Decision

Do not promote ABI-181 from capped representative evidence and do not repeat ABI-181 unchanged. Retain ABI-181 as the current capped best-validation Result and as positive evidence that the late-improving budget surface is scientifically useful for close continuations whose exploratory Run ended at the best epoch.

A reasonable next Autonomy Step is a bounded whole-validation failure-bucket Evaluation Request for `run_20260902_150611_cbbf35`. The diagnostic should test whether ABI-181's selected epoch 22 gains over ABI-173, ABI-154, ABI-130, ABI-068, and the canonical MCAST context survive on the full Working Validation Split; whether connectivity remains an actionable weakness; and whether negative-patch false positives or source-specific failure buckets offset the capped aggregate improvement. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/final_metrics.json`
- `run_20260902_150611_cbbf35/outputs/metrics.jsonl`
- `run_20260902_150611_cbbf35/outputs/resource_profile.json`
- `run_20260902_150611_cbbf35/outputs/model_summary.json`
- `run_20260902_150611_cbbf35/outputs/prediction_samples/samples.json`
- `run_20260902_150611_cbbf35/outputs/validation_postprocessing/index.json`
- `run_20260902_150611_cbbf35/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/candidate/budget_request.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
