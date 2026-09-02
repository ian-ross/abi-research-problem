# Full-spectral BTD+SZA ASPP/detail decoder boundary-calibrated BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-141 after Run `run_20260831_210158_e9ce5e` completed.

Source Runs:

- ABI-141 ASPP/detail decoder BTD+SZA boundary-calibrated BCE-Dice Centerline+Boundary auxiliary continuation: `run_20260831_210158_e9ce5e`
- ABI-130 ASPP/detail decoder BTD+SZA BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-133 ASPP/detail decoder BTD+SZA BCE-Dice Line+Centerline auxiliary comparison: `run_20260831_144720_475594`
- ABI-136 ASPP/detail decoder BTD+SZA coarse-objectness-gate BCE-Dice comparison: `run_20260831_171408_56b121`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice connectivity reference: `run_20260827_230540_bf4ce3`

ABI-141 was a controlled family-development continuation of ABI-130. It kept the compact full-spectral BTD+SZA ASPP/detail encoder-decoder, provider-approved `abi_16ch_plus_sza` input, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended change was a neutral-initialized boundary/detail residual calibration branch plus a provider-derived Boundary Target auxiliary output `boundary_logits` with trusted `weighted_bce` weight 0.01, while preserving Centerline Target auxiliary output `centerline_logits` with weight 0.02.

## Contract and resource observation

ABI-141 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records `input_spec.mode: abi_16ch_plus_sza`, Solar Geometry Input source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `centerline_logits` and `boundary_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,692,332 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,391.7 seconds total wall time, 1,095.0 seconds training wall time, 1,294.8 seconds validation wall time, 6,297,450,496 bytes peak CUDA allocated, 7,323,254,784 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_144720_475594` | ABI-133 | ABI-130 plus Line+Centerline aux | 12 | 0.3879 | 0.3727 | 0.4254 | 0.4269 | 0.3554 | 0.3390 | 0.00298 |
| `run_20260831_171408_56b121` | ABI-136 | ABI-130 plus coarse objectness gate | 7 | 0.3786 | 0.3674 | 0.4077 | 0.4456 | 0.3290 | 0.3715 | 0.00268 |
| `run_20260831_210158_e9ce5e` | ABI-141 | ABI-130 plus Boundary+Centerline aux and boundary residual | 12 | 0.3815 | 0.3643 | 0.4245 | 0.4412 | 0.3360 | 0.3498 | 0.00276 |

ABI-141 did not meet the preregistered useful-evidence criteria. Relative to ABI-130, aggregate filtered Dice decreased from 0.3953 to 0.3815 (-0.0138), outside the planned about-0.01 near-tie tolerance. MIT filtered Dice decreased from 0.3779 to 0.3643 (-0.0136), Google filtered Dice decreased from 0.4404 to 0.4245 (-0.0159), and filtered recall decreased from 0.3578 to 0.3360 (-0.0219). Filtered precision was essentially tied with ABI-130, 0.4412 versus 0.4415, so the boundary branch did not buy better negative-patch discipline at the aggregate operating point.

The clearest negative is connectivity. The proposal expected the Boundary Target and detail residual to recover part of ABI-126/ABI-066 connectivity. Instead, ABI-141 reached filtered connectivity 0.3498, below ABI-130's 0.3851, ABI-126's 0.4517, ABI-066's 0.4731, and ABI-068's 0.3900. The result also trails ABI-133's Line+Centerline auxiliary run on aggregate filtered Dice and MIT Dice, while nearly tying ABI-133 on Google Dice. It is only slightly above ABI-136's coarse-objectness gate on aggregate Dice, and ABI-136 had higher precision and connectivity despite a lower Google operating point.

The one partial positive is positive-area control: ABI-141 kept filtered predicted-positive fraction at 0.00276, lower than ABI-130's 0.00294 and similar to ABI-066's 0.00276. But because Dice, recall, MIT/Google source metrics, and connectivity all moved down relative to ABI-130, this looks more like conservative under-segmentation than useful calibration. It does not justify a whole-validation diagnostic ahead of ABI-130, ABI-126, ABI-068, or ABI-066.

## ABI-141 trajectory

ABI-141 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2192, 0.2402, 0.3286, 0.3270, 0.3238, 0.3587, 0.3493, 0.3574, 0.3539, 0.3628, 0.3720, and 0.3815. The selected checkpoint was the final epoch 12, so there was late improvement rather than terminal divergence. However, the trajectory remained below ABI-130's final 0.3953 and did not develop the expected connectivity advantage.

At the selected checkpoint, raw Dice was 0.3959 and filtered Dice was 0.3815. Filtered precision was 0.4412, filtered recall 0.3360, filtered connectivity 0.3498, and filtered predicted-positive fraction 0.00276. Source-stratified filtered Dice was 0.3643 for MIT and 0.4245 for Google. MIT had filtered precision 0.4464, recall 0.3077, connectivity 0.3329, and predicted-positive fraction 0.00372. Google had filtered precision 0.4305, recall 0.4186, connectivity 0.3667, and predicted-positive fraction 0.00180. Both Dataset Sources were finite and non-collapsed, but the MIT recall/Dice weakness that ABI-130 partly mitigated reappeared.

Raw-to-filtered differences were modest: raw Dice 0.3959 versus filtered Dice 0.3815, and raw predicted-positive fraction 0.00294 versus filtered 0.00276. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are all near-zero-Dice `first_n` traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-141 as a completed, finite, resource-feasible, non-collapsed, but negative capped family-development result for the exact ABI-130 plus boundary-calibrated auxiliary branch. The Run supplies useful evidence by answering the intended question: adding low-weight Boundary Target supervision and a bounded boundary/detail residual did not recover the ABI-126/ABI-066 connectivity advantage and did not preserve ABI-130's aggregate Dice, source balance, or recall.

This outcome reinforces the recent pattern that simple auxiliary/head-level modifications to the SZA-aware ASPP/detail BCE-Dice branch are not enough. ABI-133's Line auxiliary, ABI-136's coarse objectness gate, and ABI-141's Boundary auxiliary/residual all underperformed ABI-130. ABI-130 remains the best ASPP/detail SZA-calibrated default-threshold reference, ABI-126 remains the cleaner ASPP/detail high-precision/connectivity comparator, ABI-068 remains the local aggregate/source-balance reference, and ABI-066 remains the stronger connectivity reference.

This is capped representative evidence only, not full-data promotion evidence. Canonical MCAST 2.1 and the full 3,088-sample Working Validation Split remain the promotion context.

## Decision

Do not promote ABI-141. Do not repeat the exact ABI-130 architecture/loss/input with the same boundary-calibrated residual and Boundary Target auxiliary supervision. Do not request whole-validation diagnostics for ABI-141 ahead of stronger and already more informative references, because the capped result lost aggregate Dice, MIT Dice, Google Dice, recall, and connectivity relative to ABI-130.

For later Autonomy Steps, broaden away from incremental ASPP/detail auxiliary or calibration-head tweaks unless a proposal can state a materially different in-contract mechanism. Promising directions include a different architecture family, a preprocessing/front-end design using approved ABI channels and BTDs without coordinate inputs, or a training-policy/loss/augmentation frontier within the provider allowlists. Any continuation must leave thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

No new Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_210158_e9ce5e/outputs/best_metrics.json`
- `run_20260831_210158_e9ce5e/outputs/final_metrics.json`
- `run_20260831_210158_e9ce5e/outputs/metrics.jsonl`
- `run_20260831_210158_e9ce5e/outputs/resource_profile.json`
- `run_20260831_210158_e9ce5e/outputs/model_summary.json`
- `run_20260831_210158_e9ce5e/outputs/prediction_samples/samples.json`
- `run_20260831_210158_e9ce5e/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_144720_475594/outputs/best_metrics.json`
- `run_20260831_171408_56b121/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
