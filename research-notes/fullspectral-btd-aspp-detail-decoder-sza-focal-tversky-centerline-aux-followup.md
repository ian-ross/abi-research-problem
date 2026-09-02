# Full-spectral BTD+SZA ASPP/detail decoder focal-Tversky centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-145 after Run `run_20260901_003521_ea26c0` completed.

Source Runs:

- ABI-145 full-spectral BTD+SZA ASPP/detail decoder focal-Tversky Centerline-auxiliary continuation: `run_20260901_003521_ea26c0`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-121 non-SZA ASPP/detail decoder focal-Tversky Centerline-auxiliary reference: `run_20260831_041559_43da35`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-143 and ABI-144 recent BTD+SZA ridge-family BCE-Dice references: `run_20260831_224534_27b73d` and `run_20260831_234016_e7916c`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-145 was a controlled family-development continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, the compact ASPP/detail encoder-decoder architecture, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was to replace trusted `bce_dice` primary loss with trusted `focal_tversky`.

## Contract and resource observation

ABI-145 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,620,010 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,187.7 seconds total wall time, 992.7 seconds training wall time, 1,193.1 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 7 rather than the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, ABI-16+BTD | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_234016_e7916c` | ABI-144 | additive ridge-residual U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3839 | 0.3644 | 0.4335 | 0.4796 | 0.3200 | 0.3778 | 0.00242 |
| `run_20260901_003521_ea26c0` | ABI-145 | ASPP/detail decoder, focal-Tversky, ABI-16+BTD+SZA | 7 | 0.3628 | 0.3641 | 0.3598 | 0.3324 | 0.3993 | 0.2810 | 0.00435 |

ABI-145 completed the controlled loss test but did not meet its mechanism-specific success criteria. Versus ABI-130, aggregate filtered Dice fell by 0.0325, MIT filtered Dice by 0.0137, Google filtered Dice by 0.0806, precision by 0.1090, and connectivity by 0.1040. Filtered recall increased by 0.0414 and filtered predicted-positive fraction rose by 0.00142. This is the expected focal-Tversky direction, but the added positive area did not improve source-balanced overlap.

The result is also worse than the non-SZA focal-Tversky ASPP/detail reference ABI-121: aggregate filtered Dice is lower by 0.0256, MIT filtered Dice by 0.0194, Google filtered Dice by 0.0407, precision by 0.0202, and recall by 0.0331, although connectivity is higher by 0.0495. Thus adding Solar Geometry Input to the focal-Tversky ASPP/detail branch did not reproduce ABI-130's BCE-Dice calibration benefit; it instead degraded the focal-Tversky branch's capped Dice and source behavior.

Relative to the ABI-068 local capped aggregate-Dice reference, ABI-145 is lower by 0.0336 aggregate filtered Dice, 0.0245 MIT filtered Dice, 0.0563 Google filtered Dice, 0.0668 precision, and 0.1090 connectivity, while recall is only 0.0057 higher. Relative to ABI-143 and ABI-144, ABI-145 has a more recall-forward operating point but lower aggregate Dice and weaker Google behavior. This does not support continued small loss-only tuning of the SZA-aware ASPP/detail branch.

## ABI-145 trajectory

ABI-145 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1928, 0.1898, 0.2423, 0.2470, 0.2657, 0.2126, 0.3628, 0.3368, 0.3622, 0.3195, 0.3148, and 0.3553. The selected checkpoint was epoch 7, with epoch 9 nearly tied, and the final epoch remained below the selected checkpoint. This is a noisy but finite trajectory rather than a clear late-improving continuation like ABI-130.

At the selected checkpoint, source-stratified filtered Dice was nearly balanced but low: 0.3641 for MIT and 0.3598 for Google. MIT had filtered precision 0.3572, recall 0.3713, connectivity 0.3287, and predicted-positive fraction 0.00561. Google had filtered precision 0.2874, recall 0.4810, connectivity 0.2334, and predicted-positive fraction 0.00309. The main failure mode is not source collapse; it is a recall-forward, low-precision operating point with especially weak Google precision and connectivity.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3748 versus filtered Dice 0.3628, and raw predicted-positive fraction was 0.00462 versus filtered 0.00435. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-145 as a completed, finite, non-collapsed, negative controlled loss-continuation result for the SZA-aware ASPP/detail decoder. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. It clearly demonstrates that focal-Tversky over-expands the SZA-aware ASPP/detail branch's positive area without improving capped aggregate or source-stratified filtered Dice.

The result narrows the ASPP/detail family rather than eliminating it. ABI-130 remains the stronger SZA-aware ASPP/detail point because it kept BCE-Dice's precision and Google strength while recovering some MIT recall. ABI-121 remains the stronger focal-Tversky ASPP/detail point because it achieved higher aggregate/source Dice without SZA. ABI-126 remains a useful high-precision/connectivity comparator, and ABI-068 remains the local capped aggregate-Dice reference. ABI-145 argues against combining SZA and focal-Tversky in this exact architecture at the active budget.

## Decision

Do not promote ABI-145 and do not request whole-validation diagnostics for it. The run underperforms ABI-130, ABI-121, ABI-126, ABI-143, ABI-144, and ABI-068 on aggregate filtered Dice, and its recall gain over ABI-130 is not enough to offset the large precision, Google-Dice, and connectivity losses.

Stop this exact loss-continuation branch. Future work should not repeat focal-Tversky on the SZA-aware ASPP/detail decoder unchanged. If revisiting ASPP/detail, prefer ABI-130-like BCE-Dice calibration/continuity variants or whole-validation diagnostics on ABI-130 rather than further small loss-only modifications. More broadly, keep broadening across architecture, front-end, data-policy, calibration, and continuity mechanisms under the existing contract; no Capability Request, Evaluation Request, or Campaign Report is required from ABI-145.

## Artifact references

- `run_20260901_003521_ea26c0/outputs/best_metrics.json`
- `run_20260901_003521_ea26c0/outputs/final_metrics.json`
- `run_20260901_003521_ea26c0/outputs/metrics.jsonl`
- `run_20260901_003521_ea26c0/outputs/resource_profile.json`
- `run_20260901_003521_ea26c0/outputs/model_summary.json`
- `run_20260901_003521_ea26c0/outputs/prediction_samples/samples.json`
- `run_20260901_003521_ea26c0/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260831_234016_e7916c/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
