# Full-spectral BTD+SZA ASPP/detail decoder region-line agreement follow-up

research-figures: []

## Scope

This note records ABI-132 after Run `run_20260831_135752_1ac18c` completed.

Source Runs:

- ABI-132 SZA-aware ASPP/detail decoder region-line agreement continuation: `run_20260831_135752_1ac18c`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-131 SZA-aware ASPP/detail decoder continuity-bridge negative comparator: `run_20260831_130730_08040a`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice connectivity reference: `run_20260827_230540_bf4ce3`

ABI-132 was a family-development continuation of ABI-130. It kept the provider-approved `abi_16ch_plus_sza` input, normalized raw ABI plus deterministic thermal BTD plus Solar Geometry Input front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a zero-initialized bounded region-line agreement residual mask head intended to recover precision/connectivity without candidate-owned thresholding or Artifact Filters.

## Contract and resource observation

ABI-132 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. The model summary records input mode `abi_16ch_plus_sza`, primary `mask_logits`, and auxiliary `centerline_logits`; longitude and latitude source channels were excluded. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,803,011 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,479.3 seconds total wall time, 1,198.0 seconds training wall time, 1,279.4 seconds validation wall time, 6,802,106,880 bytes peak CUDA allocated, 7,358,906,368 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_130730_08040a` | ABI-131 | ABI-130 plus continuity bridge | 12 | 0.3880 | 0.3720 | 0.4279 | 0.4235 | 0.3581 | 0.2703 | 0.00306 |
| `run_20260831_135752_1ac18c` | ABI-132 | ABI-130 plus region-line agreement head | 12 | 0.3853 | 0.3730 | 0.4163 | 0.4394 | 0.3431 | 0.2971 | 0.00283 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |

ABI-132 did not meet the controlled region-line agreement hypothesis relative to ABI-130. Aggregate filtered Dice fell from 0.3953 to 0.3853, MIT filtered Dice from 0.3779 to 0.3730, Google filtered Dice from 0.4404 to 0.4163, filtered recall from 0.3578 to 0.3431, and filtered connectivity from 0.3851 to 0.2971. Filtered precision was approximately preserved at 0.4394 versus ABI-130's 0.4415, and filtered predicted-positive fraction decreased from 0.00294 to 0.00283, but this conservative shift came with lower recall, lower Dice, and much lower connectivity rather than a useful calibration improvement.

Relative to ABI-131, ABI-132 recovered some precision and connectivity from the simpler continuity bridge, but not enough to make the added region-line head useful. It still trails ABI-131 on aggregate Dice and Google Dice, trails ABI-130 on the main SZA-aware reference metrics, trails ABI-126/ABI-066 on the intended precision/connectivity discipline, and trails ABI-068 on capped aggregate Dice/source balance. The result is finite and source-informative, but it is negative evidence for this exact residual mask-head variant.

## ABI-132 trajectory

ABI-132 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1992, 0.2765, 0.3065, 0.2549, 0.3203, 0.3369, 0.3699, 0.3617, 0.3677, 0.3665, 0.3398, and 0.3853. The selected checkpoint was the final epoch 12, so the Run still had late improvement rather than a clean early plateau.

The late improvement did not solve the targeted trade-off. Epoch 8 briefly reached higher precision and connectivity (0.4385 precision, 0.3400 connectivity) but lower recall and Dice. Epoch 12 preserved precision while improving Dice, but connectivity remained well below ABI-130, ABI-126, ABI-066, and ABI-068. Source-stratified filtered Dice at epoch 12 was 0.3730 for MIT and 0.4163 for Google, confirming finite signal on both Dataset Sources but no source-specific improvement over ABI-130.

Raw-to-filtered differences were modest: raw Dice was 0.4001 versus filtered Dice 0.3853, and raw predicted-positive fraction was 0.00302 versus filtered 0.00283. The fixed first-four retained prediction samples had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-132 as a completed, finite, non-collapsed, but negative family-development result. It is not a candidate bug, contract violation, resource failure, or Harness failure. The bounded region-line agreement residual did make the head slightly more conservative than ABI-130, but it did not recover the desired precision/connectivity discipline and instead reduced aggregate overlap, Google performance, recall, and connectivity.

ABI-130 remains the better SZA-aware ASPP/detail reference because it has stronger capped aggregate Dice and already has whole-validation diagnostics confirming the SZA-assisted calibration/recall trade-off. ABI-126 remains the ASPP/detail high-precision/connectivity comparator, ABI-066 remains the high-connectivity line-family comparator, and ABI-068 remains the current local capped aggregate-Dice reference. ABI-132 does not eliminate Solar Geometry Input or the ASPP/detail family broadly, but it argues against further stacking simple continuity/agreement mask-head tweaks on ABI-130 without a distinct mechanism or diagnostic rationale.

## Decision

Do not promote ABI-132. Do not request whole-validation diagnostics for ABI-132 from this capped result, because it failed to improve ABI-130 on the intended capped metrics and did not produce a strong new precision/connectivity operating point. Do not repeat the exact region-line agreement residual head unchanged.

A reasonable next Autonomy Step is to broaden beyond simple SZA-aware ASPP/detail head geometry tweaks: either return to a stronger line-aware family with a new calibration or data-policy hypothesis, or test a different preprocessing/front-end or trusted loss/auxiliary-target combination that directly addresses false positives without damaging recall/connectivity.

## Artifact references

- `run_20260831_135752_1ac18c/outputs/best_metrics.json`
- `run_20260831_135752_1ac18c/outputs/final_metrics.json`
- `run_20260831_135752_1ac18c/outputs/metrics.jsonl`
- `run_20260831_135752_1ac18c/outputs/resource_profile.json`
- `run_20260831_135752_1ac18c/outputs/model_summary.json`
- `run_20260831_135752_1ac18c/outputs/prediction_samples/samples.json`
- `run_20260831_135752_1ac18c/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_130730_08040a/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
