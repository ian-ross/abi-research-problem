# Full-spectral BTD ABI-only full-scale skip ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-164 after Run `run_20260901_154457_428cec` completed.

Source Runs:

- ABI-164 ABI-only full-scale skip ASPP/detail decoder with trusted BCE-Dice and Centerline auxiliary target: `run_20260901_154457_428cec`
- ABI-154 SZA-aware full-scale skip ASPP/detail decoder primary comparison target: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-156 feature-calibrated SZA-aware full-scale skip continuation: `run_20260901_090713_9c7d32`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate reference: `run_20260831_121006_7d24be`
- ABI-126 ABI-only ASPP/detail decoder BCE-Dice precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`

ABI-164 was a controlled input/front-end continuation of ABI-154. It retained the full-scale skip ASPP/detail decoder topology, deterministic thermal BTD planes from approved ABI channels, trusted `bce_dice` primary loss, Centerline auxiliary target weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the 1,024-record-per-Dataset-Source/split representative cap. The controlled change was removing provider-approved Solar Geometry Input and using `abi_16ch` instead of `abi_16ch_plus_sza`.

## Contract and resource observation

ABI-164 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch`, approved GOES ABI source channel indices 0-15, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Solar Geometry Input was also excluded by design. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,741,354 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,518.1 seconds total wall time, 1,246.1 seconds training wall time, 1,270.0 seconds validation wall time, 19.72 training samples per second, 19.35 validation samples per second, 8,006,177,792 bytes peak CUDA allocated, 9,420,406,784 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260831_085615_d05ab3` | ABI-126 | ABI-only ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_154457_428cec` | ABI-164 | ABI-only full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3711 | 0.3516 | 0.4201 | 0.4694 | 0.3068 | 0.3525 | 0.00237 |

ABI-164 did not support the hypothesis that removing Solar Geometry Input would preserve ABI-154-like precision/connectivity while recovering source balance or recall. Relative to ABI-154, ABI-164 lost aggregate filtered Dice by -0.0233, MIT filtered Dice by -0.0309, Google filtered Dice by -0.0059, precision by -0.0083, recall by -0.0291, connectivity by -0.0849, and predicted-positive fraction by -0.00018. The removal of SZA therefore made the full-scale branch more conservative without improving its source balance or fixed-threshold recall.

Relative to ABI-126, which is the non-SZA ASPP/detail precision/connectivity comparator, ABI-164 also fell short: aggregate filtered Dice -0.0148, MIT filtered Dice -0.0120, Google filtered Dice -0.0213, precision -0.0053, recall -0.0183, and connectivity -0.0992. This argues that simply combining ABI-only input with ABI-154's full-scale skip fusion did not inherit the best properties of either branch. Relative to ABI-068, ABI-164 improved Google filtered Dice by +0.0040 and precision by +0.0702, but lost aggregate filtered Dice by -0.0253, MIT filtered Dice by -0.0370, recall by -0.0868, and connectivity by -0.0375.

## ABI-164 trajectory

ABI-164 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2228, 0.2566, 0.2905, 0.2962, 0.3376, 0.3429, 0.3324, 0.3635, 0.3430, 0.3543, 0.3515, and 0.3711. The selected best checkpoint was the final epoch 12, so the exact ABI-only full-scale branch was still improving late in the active budget, but from a materially worse operating point than the current references.

At epoch 12, ABI-164 had raw Dice 0.3865, filtered Dice 0.3711, filtered precision 0.4694, filtered recall 0.3068, filtered connectivity 0.3525, and filtered predicted-positive fraction 0.00237. Source-stratified filtered Dice was 0.3516 for MIT and 0.4201 for Google. Raw-to-filtered differences were modest: raw Dice 0.3865 versus filtered Dice 0.3711, raw recall 0.3277 versus filtered recall 0.3068, and raw predicted-positive fraction 0.00252 versus filtered 0.00237. This does not indicate primary Artifact Filter dependence.

The epoch trajectory shows repeated precision/recall swings rather than a clean late calibration improvement. Epoch 8 reached filtered Dice 0.3635 with recall 0.3700 but weak connectivity 0.1637; epoch 12 improved Dice and connectivity to 0.3711 and 0.3525 by moving back toward high precision and low predicted-positive fraction. The final fixed-threshold operating point remains under-recalled versus ABI-154, ABI-130, ABI-126, and ABI-068. The fixed first-four retained prediction samples all had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-164 as a completed, finite, non-collapsed but negative scientific result for the ABI-only input-axis variant of the full-scale skip ASPP/detail decoder. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result suggests that ABI-154's useful precision/connectivity behavior was not merely a property of the full-scale skip topology that transfers unchanged to ABI-only input. Removing SZA did not recover recall, did not improve aggregate/source balance, and substantially reduced connectivity. The late improvement means low score alone should not be treated as proof that all full-scale skip ideas are impossible, but the exact ABI-only ABI-154-derived branch did not meet its useful-outcome criterion and does not justify a whole-validation evaluation.

ABI-068 remains the current capped aggregate/source-balance reference. ABI-130 remains the SZA-aware ASPP/detail aggregate reference. ABI-154 remains the whole-validation-tested SZA-aware full-scale skip precision/connectivity reference. ABI-126 remains the stronger ABI-only ASPP/detail comparator. ABI-164 adds evidence that removing Solar Geometry Input from the full-scale skip branch is not a productive continuation under the current 12-epoch capped budget.

## Decision

Do not promote ABI-164, do not request whole-validation diagnostics for it, and do not repeat this exact ABI-only full-scale skip ASPP/detail branch unchanged. The run completed reliably, but it fell materially below ABI-154, ABI-130, ABI-126, and ABI-068 without a compensating gain in recall, source balance, precision, connectivity, or Artifact Filter robustness.

The next useful step should broaden away from local ASPP/detail/full-scale-skip variants. Contract-compliant next options include a materially different high-resolution line-continuity architecture, a different ABI spectral preprocessing/front-end that is not just SZA removal, or a data/loss/calibration frontier that directly targets the persistent fixed-threshold recall-versus-precision trade-off. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-164.

## Artifact references

- `run_20260901_154457_428cec/outputs/best_metrics.json`
- `run_20260901_154457_428cec/outputs/final_metrics.json`
- `run_20260901_154457_428cec/outputs/metrics.jsonl`
- `run_20260901_154457_428cec/outputs/resource_profile.json`
- `run_20260901_154457_428cec/outputs/model_summary.json`
- `run_20260901_154457_428cec/outputs/prediction_samples/samples.json`
- `run_20260901_154457_428cec/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
