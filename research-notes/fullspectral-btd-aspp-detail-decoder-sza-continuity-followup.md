# Full-spectral BTD+SZA ASPP/detail decoder continuity-bridge follow-up

research-figures: []

## Scope

This note records ABI-131 after Run `run_20260831_130730_08040a` completed.

Source Runs:

- ABI-131 SZA-aware ASPP/detail decoder continuity-bridge continuation: `run_20260831_130730_08040a`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-121 ASPP/detail decoder focal-Tversky Centerline-auxiliary recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-068 frequency-gated line U-Net focal-Tversky local aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-127 and ABI-128 as recent ASPP/detail BCE-Dice head/calibration follow-ups: `run_20260831_094013_5ba974` and `run_20260831_103509_961c81`

ABI-131 was a family-development continuation of ABI-130. It kept the provider-approved `abi_16ch_plus_sza` input, normalized raw ABI plus BTD plus SZA front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a neutral, identity-initialized multi-directional continuity bridge after the line-aware refinement block.

## Contract and resource observation

ABI-131 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. The model summary records input mode `abi_16ch_plus_sza` with forbidden longitude and latitude source channels excluded, primary `mask_logits`, and auxiliary `centerline_logits` with the provider-derived Centerline Target. It did not own data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem persistence, network access, pretrained weights, or lifecycle behavior.

`outputs/model_summary.json` reported 9,806,210 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,486.2 seconds total wall time, 1,181.3 seconds training wall time, 1,302.9 seconds validation wall time, 6,881,837,056 bytes peak CUDA allocated, 7,442,792,448 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, ABI-16+BTD | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_130730_08040a` | ABI-131 | ABI-130 plus neutral continuity bridge | 12 | 0.3880 | 0.3720 | 0.4279 | 0.4235 | 0.3581 | 0.2703 | 0.00306 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_094013_5ba974` | ABI-127 | ABI-126 plus Line+Centerline aux | 9 | 0.3797 | 0.3653 | 0.4150 | 0.4280 | 0.3412 | 0.3054 | 0.00289 |
| `run_20260831_103509_961c81` | ABI-128 | ABI-126 plus calibration-aware margin head | 9 | 0.3787 | 0.3586 | 0.4298 | 0.4120 | 0.3504 | 0.3473 | 0.00308 |

ABI-131 did not meet the controlled continuity-bridge hypothesis relative to ABI-130. Aggregate filtered Dice fell from 0.3953 to 0.3880 (-0.0072), MIT filtered Dice from 0.3779 to 0.3720 (-0.0059), Google filtered Dice from 0.4404 to 0.4279 (-0.0125), and filtered precision from 0.4415 to 0.4235 (-0.0180). Filtered recall was essentially tied, 0.3581 versus 0.3578, but the bridge did not convert that recall into better overlap or cleaner predictions.

The main targeted metric moved in the wrong direction: filtered connectivity dropped from ABI-130's 0.3851 to 0.2703 (-0.1147). It also remained far below ABI-126 and ABI-066, the ASPP/detail and frequency-gated connectivity references. Filtered predicted-positive fraction increased slightly from 0.00294 to 0.00306, so the bridge did not improve negative-patch discipline by becoming more conservative. The result is finite and source-informative, but it is a negative family-development result for this exact continuity bridge.

Relative to other ASPP/detail branches, ABI-131 still sits above ABI-126, ABI-127, and ABI-128 on aggregate filtered Dice, but it trails ABI-130's SZA-calibrated operating point and ABI-121's focal-Tversky recall/source-balance comparator. Its Google filtered Dice remains useful at 0.4279, but it no longer preserves ABI-130's near-leading Google strength or ABI-126's precision/connectivity strength. This makes ABI-131 an intermediate compromise rather than a new local reference.

## ABI-131 trajectory

ABI-131 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2074, 0.2849, 0.2922, 0.3342, 0.3083, 0.3547, 0.3447, 0.3405, 0.3788, 0.3654, 0.3585, and 0.3880. The selected checkpoint was the final epoch 12, so the branch had late improvement rather than a clean early plateau.

The late improvement was not sufficient to justify extending this exact design. Epoch 10 briefly showed higher precision (0.4475) but lower recall (0.3088) and lower Dice (0.3654); epoch 12 recovered recall and Dice but not ABI-130-level precision or connectivity. Connectivity stayed substantially below the intended ABI-130/ABI-126 reference range at the selected checkpoint. Source-stratified filtered Dice at epoch 12 was 0.3720 for MIT and 0.4279 for Google, confirming that both Dataset Sources contributed finite signal but neither improved over ABI-130.

Raw-to-filtered differences were modest: raw Dice was 0.4023 versus filtered Dice 0.3880, and raw predicted-positive fraction was 0.00327 versus filtered 0.00306. Artifact Filters removed a small fraction of predicted positives relative to the total positive prediction mass, so the primary conclusion is not an Artifact Filter dependence artifact. The fixed first-four retained prediction samples had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-131 as a completed, finite, non-collapsed, but negative family-development result. It is not a candidate bug, contract violation, resource failure, or Harness failure. The bridge preserved trainability and default-threshold recall, but failed the proposal's useful-result criterion because it reduced aggregate Dice, source Dice, precision, and especially connectivity relative to ABI-130 while slightly increasing predicted-positive area.

The result suggests that simply inserting a post-refinement multi-directional continuity bridge in the SZA-aware ASPP/detail BCE-Dice branch does not recover ABI-126/ABI-066 connectivity or negative-patch discipline. ABI-130 remains the better SZA-aware ASPP/detail capped and whole-validation-tested reference. ABI-126 remains the high-precision/connectivity ASPP/detail comparator, and ABI-068 remains the current local capped aggregate-Dice reference.

This does not eliminate the ASPP/detail family or Solar Geometry Input more broadly, because ABI-130's capped and whole-validation diagnostic evidence remains positive. It does, however, argue against repeating this exact ABI-131 continuity bridge unchanged. Future in-contract work should either pursue a more explicitly calibration-aware mechanism that does not damage connectivity, or broaden away from simple ASPP/detail head-geometry tweaks toward another architecture, preprocessing, loss, augmentation, or trusted data-policy frontier.

## Decision

Do not promote ABI-131. Do not request whole-validation diagnostics for ABI-131 from this capped result, because the controlled bridge failed to improve its capped comparison target on the intended metrics. Do not repeat the exact continuity bridge unchanged.

Retain ABI-130 as the SZA-aware ASPP/detail reference, ABI-126 as the ASPP/detail precision/connectivity reference, ABI-068 as the local capped aggregate-Dice reference, and ABI-066 as the high-connectivity line-family reference. A reasonable next Autonomy Step is a new, controlled in-contract hypothesis that broadens beyond this simple continuity bridge rather than a repair of ABI-131.

## Artifact references

- `run_20260831_130730_08040a/outputs/best_metrics.json`
- `run_20260831_130730_08040a/outputs/final_metrics.json`
- `run_20260831_130730_08040a/outputs/metrics.jsonl`
- `run_20260831_130730_08040a/outputs/resource_profile.json`
- `run_20260831_130730_08040a/outputs/model_summary.json`
- `run_20260831_130730_08040a/outputs/prediction_samples/samples.json`
- `run_20260831_130730_08040a/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_094013_5ba974/outputs/best_metrics.json`
- `run_20260831_103509_961c81/outputs/best_metrics.json`
