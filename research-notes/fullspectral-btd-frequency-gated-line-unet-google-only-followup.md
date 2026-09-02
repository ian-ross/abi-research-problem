# Full-spectral BTD frequency-gated line U-Net Google-only follow-up

research-figures: []

## Scope

This note records ABI-106 after Run `run_20260830_101145_b69d10` completed.

Source Runs:

- ABI-106 Google-only data-policy continuation: `run_20260830_101145_b69d10`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-096 deterministic-shuffle data-policy continuation: `run_20260830_021504_c112f8`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`

ABI-106 was a data-policy family-development continuation of ABI-068. It retained the ABI-068 full-spectral ABI plus thermal BTD frequency-gated line U-Net architecture, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping. The controlled manifest change was selecting the trusted provider/Harness `google_only` sampling policy rather than ABI-068's `combined_source_balanced` traversal.

The hypothesis was that source-specialized Google training could clarify whether the frequency-gated focal-Tversky branch has a cleaner Google-source operating point that source-balanced traversal dilutes, while measuring MIT transfer cost through provider-owned validation metrics. This is capped representative data-policy evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-106 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and deterministic BTD features derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `data.sampling_policy: google_only`. `outputs/model_summary.json` reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,699.4 seconds total wall time, 1,308.1 seconds training wall time, 1,389.0 seconds validation wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure.

The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap; validation remained the capped combined MIT/Google validation set. The final and best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, source-balanced | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_021504_c112f8` | ABI-096 | ABI-068 branch, deterministic-shuffle sampling | 10 | 0.3628 | 0.3472 | 0.4024 | 0.4242 | 0.3169 | 0.4195 | 0.00271 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, non-amplifying decoder skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_101145_b69d10` | ABI-106 | ABI-068 branch, `google_only` sampling | 12 | 0.3590 | 0.3338 | 0.4199 | 0.3391 | 0.3815 | 0.3100 | 0.00408 |

ABI-106 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, Google filtered Dice improved only marginally, from 0.4161 to 0.4199 (+0.0038), short of the +0.01 criterion. Aggregate filtered Dice decreased from 0.3964 to 0.3590 (-0.0373), outside the allowed 0.03 band. MIT filtered Dice decreased from 0.3886 to 0.3338 (-0.0548), filtered precision decreased from 0.3992 to 0.3391 (-0.0601), filtered recall decreased from 0.3936 to 0.3815 (-0.0122), and filtered connectivity decreased from 0.3900 to 0.3100 (-0.0800). Filtered predicted-positive fraction increased from 0.00357 to 0.00408, about a 14% relative increase rather than the hoped-for 10% reduction.

Relative to ABI-066, ABI-106 lost aggregate filtered Dice (-0.0235), MIT filtered Dice (-0.0300), Google filtered Dice (-0.0092), precision (-0.1036), and connectivity (-0.1631), while gaining recall (+0.0447) and using a larger predicted-positive fraction. Relative to ABI-096, ABI-106 recovered some Google Dice and recall, but at lower precision, lower connectivity, higher positive area, and still lower aggregate Dice. Relative to ABI-105, ABI-106 shifted toward Google performance and away from MIT/source-balanced aggregate performance.

## ABI-106 trajectory

ABI-106 trained finitely and avoided terminal all-negative/all-positive collapse. Filtered Dice by epoch was 0.2340, 0.2555, 0.3154, 0.2917, 0.3170, 0.1347, 0.3187, 0.3389, 0.3566, 0.3578, 0.3558, and 0.3590. The selected checkpoint was the final epoch 12, so the run recovered after the epoch-6 dip and ended late-improving, though the last four epochs were nearly flat.

At the selected checkpoint, filtered Dice was 0.3590, filtered precision 0.3391, filtered recall 0.3815, filtered connectivity 0.3100, and filtered predicted-positive fraction 0.00408. Source-stratified filtered Dice was highly asymmetric: Google 0.4199 with Google recall 0.5126, versus MIT 0.3338 with MIT recall 0.3366. Training loss declined from 0.9159 at epoch 1 to 0.8054 at epoch 12, while validation loss moved from 0.9217 to 0.8875.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3702 versus filtered Dice 0.3590, and raw predicted-positive fraction 0.00433 versus filtered 0.00408. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-106 as finite, resource-feasible, non-collapsed, and diagnostically useful but negative capped evidence for the exact Google-only data-policy branch. It produced the expected source asymmetry direction: Google filtered Dice slightly exceeded ABI-068 and substantially exceeded ABI-105, while MIT transfer and aggregate metrics weakened. The magnitude is not enough to justify preferring `google_only` over the existing source-balanced traversal. The small Google gain came with lower aggregate Dice, lower precision, lower connectivity, and higher positive-area burden relative to ABI-068.

The result also argues against a near-term trusted source-mixture Capability Request based solely on this branch. ABI-096 showed that less source/positive balancing can raise precision/connectivity but hurts recall and source balance; ABI-106 showed that source specialization can preserve or slightly improve Google Dice but hurts MIT and aggregate performance. Together, these data-policy probes suggest that the current frequency-gated focal-Tversky branch is sensitive to traversal policy but has not revealed a clearly superior simple allowlisted policy.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-106 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-106. Stop the exact ABI-068 architecture plus focal-Tversky plus centerline auxiliary branch with `google_only` sampling. Do not request whole-validation failure-bucket diagnostics for ABI-106 ahead of ABI-068/066; the capped result is source-asymmetric but not strong enough to warrant scarce full-validation diagnostic priority.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. Prefer `combined_source_balanced` traversal for this branch unless a materially different, provider-owned data-policy hypothesis is introduced. A future useful hypothesis should broaden away from simple traversal swaps and small late gates toward a different contract-compliant mechanism for calibration, false-positive suppression, thin-line connectivity, or source robustness, while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_101145_b69d10/outputs/best_metrics.json`
- `run_20260830_101145_b69d10/outputs/final_metrics.json`
- `run_20260830_101145_b69d10/outputs/metrics.jsonl`
- `run_20260830_101145_b69d10/outputs/resource_profile.json`
- `run_20260830_101145_b69d10/outputs/model_summary.json`
- `run_20260830_101145_b69d10/outputs/prediction_samples/samples.json`
- `run_20260830_101145_b69d10/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260830_021504_c112f8/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
