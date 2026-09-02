# Full-spectral BTD+SZA ASPP/detail decoder low-learning-rate BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-148 after Run `run_20260901_025820_cd85e5` completed.

Source Runs:

- ABI-148 full-spectral BTD+SZA ASPP/detail decoder low-learning-rate BCE-Dice Centerline-auxiliary continuation: `run_20260901_025820_cd85e5`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-143 SZA-aware soft ridge-gate U-Net BCE-Dice Centerline-auxiliary reference: `run_20260831_224534_27b73d`
- ABI-147 negative SZA-aware hybrid ridge-ASPP/detail BCE-Dice reference: `run_20260901_021228_9ca4b9`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-148 was a controlled training-policy continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, the compact ASPP/detail encoder-decoder architecture, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was to lower AdamW learning rate from `0.0003` to `0.0002`.

## Contract and resource observation

ABI-148 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,620,010 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,177.0 seconds total wall time, 993.5 seconds training wall time, 1,181.6 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 9 rather than the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_021228_9ca4b9` | ABI-147 | hybrid ridge-ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3804 | 0.3705 | 0.4051 | 0.4260 | 0.3436 | 0.2849 | 0.00292 |
| `run_20260901_025820_cd85e5` | ABI-148 | ASPP/detail decoder, low-LR BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3752 | 0.3718 | 0.3835 | 0.3706 | 0.3798 | 0.2571 | 0.00371 |

ABI-148 did not meet its controlled low-learning-rate success criteria. Relative to ABI-130, aggregate filtered Dice fell by 0.0201, MIT filtered Dice by 0.0061, Google filtered Dice by 0.0569, precision by 0.0708, and connectivity by 0.1279. Filtered recall rose by 0.0220, but the gain came with a higher predicted-positive fraction and did not improve overlap or source balance. This is the opposite of the intended stabilization effect: lowering learning rate did not recover precision/connectivity and instead weakened the Google side of the SZA-aware ASPP/detail branch.

Relative to ABI-126, ABI-148 improves MIT filtered Dice by 0.0082 and recall by 0.0548, but loses 0.0107 aggregate Dice, 0.0580 Google Dice, 0.1040 precision, and 0.1946 connectivity. Relative to ABI-143, ABI-148 is lower by 0.0196 aggregate filtered Dice, 0.0098 MIT Dice, 0.0453 Google Dice, 0.0399 precision, and 0.0438 connectivity, while essentially tying recall. Relative to ABI-147, ABI-148 moves to a more recall-forward operating point, but aggregate and especially Google Dice remain lower. Relative to ABI-068, ABI-148 is lower on aggregate/source Dice, precision, recall, and connectivity.

## ABI-148 trajectory

ABI-148 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1832, 0.2806, 0.2732, 0.3237, 0.3244, 0.2957, 0.3605, 0.3534, 0.3752, 0.3652, 0.3727, and 0.3540. The selected checkpoint was epoch 9; epochs 10-11 remained close but below the selected checkpoint, and the final epoch dropped further.

At the selected checkpoint, source-stratified filtered Dice was 0.3718 for MIT and 0.3835 for Google. MIT had filtered precision 0.3874, recall 0.3574, connectivity 0.2915, and predicted-positive fraction 0.00498. Google had filtered precision 0.3366, recall 0.4455, connectivity 0.2228, and predicted-positive fraction 0.00244. The branch is not collapsed, but it shifts ABI-130 toward higher recall, lower precision, lower connectivity, and weaker Google overlap.

The final epoch illustrates the instability rather than solving it: filtered Dice fell to 0.3540 while precision rose to 0.4720, recall fell to 0.2832, and connectivity rose to 0.4212. That late high-precision/high-connectivity point was too under-recalling to be selected by the trusted `val/filtered_dice` metric. The lower fixed learning rate therefore did not produce a smoother or clearly better calibration trajectory within the 12-epoch cap.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3878 versus filtered Dice 0.3752, and raw predicted-positive fraction was 0.00396 versus filtered 0.00371. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples all have near-zero per-sample Dice, but they remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-148 as a completed, finite, non-collapsed, negative controlled training-policy result for the SZA-aware ASPP/detail BCE-Dice branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The exact low-learning-rate change did not stabilize ABI-130's useful operating point; it lowered aggregate and Google filtered Dice and failed to recover ABI-126-like precision/connectivity.

This narrows the SZA-aware ASPP/detail tuning branch rather than eliminating full-spectral BTD+SZA modeling. ABI-130 remains the stronger SZA-aware ASPP/detail point and has whole-validation diagnostic support. ABI-126 remains the stronger ASPP/detail precision/connectivity branch. ABI-143 remains a stronger nearby SZA-aware BCE-Dice ridge branch. ABI-068 remains the local capped aggregate filtered-Dice reference. The last ABI-130 continuations suggest that simple SZA-aware loss, micro-architecture, auxiliary, and learning-rate edits are not reliably improving the main precision/connectivity/source-balance tradeoff.

## Decision

Do not promote ABI-148 and do not request whole-validation diagnostics for it. The Run underperforms ABI-130, ABI-143, ABI-126, and ABI-068 on aggregate filtered Dice and has no compensating precision, connectivity, source, or calibration advantage. It satisfies the proposal hard-stop condition for this exact low-learning-rate branch: aggregate/source metrics are materially below ABI-130 without the intended precision/connectivity gain.

Stop this exact low-learning-rate ASPP/detail BCE-Dice branch. Future work should broaden away from additional SZA-aware ASPP/detail fine-tuning unless a new mechanism directly addresses negative-patch clutter, source-balanced connectivity, or calibration under the existing contract. Reasonable next frontiers remain distinct architecture families, in-contract front-end/preprocessing designs, data-policy/augmentation tests, or a more explicit calibration mechanism that does not move thresholding or postprocessing into Candidate code. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-148.

## Artifact references

- `run_20260901_025820_cd85e5/outputs/best_metrics.json`
- `run_20260901_025820_cd85e5/outputs/final_metrics.json`
- `run_20260901_025820_cd85e5/outputs/metrics.jsonl`
- `run_20260901_025820_cd85e5/outputs/resource_profile.json`
- `run_20260901_025820_cd85e5/outputs/model_summary.json`
- `run_20260901_025820_cd85e5/outputs/prediction_samples/samples.json`
- `run_20260901_025820_cd85e5/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260901_021228_9ca4b9/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
