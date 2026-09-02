# Full-spectral BTD+SZA ASPP/detail decoder coarse-objectness-gate follow-up

research-figures: []

## Scope

This note records ABI-136 after Run `run_20260831_171408_56b121` completed.

Source Runs:

- ABI-136 SZA-aware ASPP/detail decoder coarse-objectness-gate BCE-Dice Centerline-auxiliary continuation: `run_20260831_171408_56b121`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-135 deterministic-shuffle negative data-policy comparator: `run_20260831_162753_adfc95`
- ABI-134 SZA-aware frequency-gated line U-Net BCE-Dice comparator: `run_20260831_153303_7701f1`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`

ABI-136 was a family-development continuation of ABI-130. It kept ABI-130's provider-approved `abi_16ch_plus_sza` input, deterministic raw ABI plus thermal BTD plus Solar Geometry front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a neutral-initialized coarse objectness gate before the final line-aware refinement, intended to improve precision/connectivity and predicted-positive discipline without candidate-owned thresholding, postprocessing, Artifact Filters, or data handling.

## Contract and resource observation

ABI-136 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, combined source-balanced traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,694,050 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,396.2 seconds total wall time, 1,120.9 seconds training wall time, 1,273.4 seconds validation wall time, 7,006,310,912 bytes peak CUDA allocated, 8,277,458,944 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 7, not the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_153303_7701f1` | ABI-134 | frequency-gated line U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3866 | 0.3714 | 0.4238 | 0.4033 | 0.3712 | 0.3279 | 0.00334 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_171408_56b121` | ABI-136 | ABI-130 plus coarse objectness gate | 7 | 0.3786 | 0.3674 | 0.4077 | 0.4456 | 0.3290 | 0.3715 | 0.00268 |
| `run_20260831_162753_adfc95` | ABI-135 | ABI-130 architecture with deterministic-shuffle traversal | 12 | 0.3758 | 0.3703 | 0.3880 | 0.3394 | 0.4209 | 0.2174 | 0.00449 |

ABI-136 did not meet the coarse-objectness-gate hypothesis relative to ABI-130. The gate delivered a small precision and positive-area improvement at its best checkpoint: filtered precision rose from 0.4415 to 0.4456, and filtered predicted-positive fraction fell from 0.00294 to 0.00268. However, the intended cleaner trade-off did not hold. Aggregate filtered Dice fell from 0.3953 to 0.3786 (-0.0167), MIT filtered Dice fell from 0.3779 to 0.3674 (-0.0105), Google filtered Dice fell from 0.4404 to 0.4077 (-0.0327), filtered recall fell from 0.3578 to 0.3290 (-0.0288), and filtered connectivity fell from 0.3851 to 0.3715 (-0.0136).

Relative to ABI-126 and ABI-066, ABI-136 also failed to recover the high precision/connectivity reference behavior. It trailed ABI-126 on aggregate Dice, Google Dice, precision, connectivity, and positive-area discipline; it only modestly exceeded ABI-126 recall. It trailed ABI-066 on aggregate Dice, MIT/Google Dice, recall, connectivity, and positive-area discipline while only narrowly exceeding precision. Relative to ABI-068, ABI-136 was more conservative and slightly higher-precision, but it lost aggregate Dice, MIT Dice, Google Dice, recall, and connectivity. The result therefore does not establish a useful new operating point.

## ABI-136 trajectory

ABI-136 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2005, 0.2693, 0.3082, 0.3055, 0.3172, 0.3457, 0.3786, 0.3708, 0.3543, 0.3290, 0.3697, and 0.3514. The selected best checkpoint was epoch 7, after which the trajectory oscillated and did not recover the ABI-130-like aggregate result.

The gate behaved as a conservative calibrator at some epochs, but not as a net improvement. Epoch 7 selected the best Dice with filtered precision 0.4456, recall 0.3290, connectivity 0.3715, and predicted-positive fraction 0.00268. Epoch 12 became much more conservative, with filtered precision 0.4937, recall 0.2728, connectivity 0.3877, predicted-positive fraction 0.00200, and lower filtered Dice 0.3514. This late behavior shows the coarse objectness path could suppress positive area, but it suppressed recall and overlap too strongly rather than selectively removing clutter.

At the selected checkpoint, source-stratified filtered Dice was 0.3674 for MIT and 0.4077 for Google. Google remained the stronger Dataset Source, but ABI-136 lost most of ABI-130's Google advantage and did not compensate with improved MIT behavior. Raw-to-filtered differences were modest: raw Dice was 0.3932 versus filtered Dice 0.3786, and raw predicted-positive fraction was 0.00286 versus filtered 0.00268. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-136 as a completed, finite, non-collapsed, but negative family-development result for this exact coarse-objectness-gate branch. It is not a candidate bug, contract violation, resource failure, or Harness failure. The Run supplied useful evidence: a neutral coarse objectness gate can make the SZA-aware ASPP/detail branch more conservative, but under the current budget it did not improve the desired precision/connectivity trade-off and instead damaged recall, Google Dice, and aggregate filtered Dice.

This strengthens the recent pattern from ABI-131, ABI-132, ABI-133, ABI-135, and now ABI-136: simple local head/refiner/traversal changes around ABI-130 are not recovering a better fixed-threshold balance. ABI-130 remains the best SZA-aware ASPP/detail capped reference with whole-validation diagnostic support. ABI-126 remains the ASPP/detail high-precision/connectivity comparator, ABI-066 remains the high-connectivity reference, and ABI-068 remains the local capped aggregate-Dice/source-balance reference.

## Decision

Do not promote ABI-136. Do not request whole-validation diagnostics for ABI-136 from this capped result, because it failed the controlled comparison against ABI-130 and did not establish a distinctive useful operating point. Do not repeat the exact coarse-objectness-gate branch unchanged.

For a later Autonomy Step, broaden away from incremental SZA-aware ASPP/detail gate/head tweaks. A stronger next hypothesis should either use a distinct architecture family or a different in-contract calibration/preprocessing/loss/data-policy frontier that directly addresses false positives and connectivity without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, sampling, or target derivation.

No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260831_171408_56b121/outputs/best_metrics.json`
- `run_20260831_171408_56b121/outputs/final_metrics.json`
- `run_20260831_171408_56b121/outputs/metrics.jsonl`
- `run_20260831_171408_56b121/outputs/resource_profile.json`
- `run_20260831_171408_56b121/outputs/model_summary.json`
- `run_20260831_171408_56b121/outputs/prediction_samples/samples.json`
- `run_20260831_171408_56b121/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_162753_adfc95/outputs/best_metrics.json`
- `run_20260831_153303_7701f1/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
