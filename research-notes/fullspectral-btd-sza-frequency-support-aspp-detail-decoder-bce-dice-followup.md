# Full-spectral BTD+SZA frequency-support ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-146 after Run `run_20260901_012037_c302cc` completed.

Source Runs:

- ABI-146 full-spectral BTD+SZA frequency-support ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260901_012037_c302cc`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary high-precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-143 recent SZA-aware ridge-family BCE-Dice reference: `run_20260831_224534_27b73d`

ABI-146 was a family-development continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, the compact ASPP/detail encoder-decoder lineage, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was to add a bounded additive frequency-support fusion path after line-aware refinement before the mask and centerline heads.

## Contract and resource observation

ABI-146 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,876,850 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,639.1 seconds total wall time, 1,290.6 seconds training wall time, 1,346.3 seconds validation wall time, 7,386,012,160 bytes peak CUDA allocated, 8,373,927,936 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260901_012037_c302cc` | ABI-146 | ASPP/detail decoder + frequency support, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3497 | 0.3260 | 0.4095 | 0.4914 | 0.2714 | 0.3125 | 0.00200 |

ABI-146 completed the controlled frequency-support test but did not meet its mechanism-specific success criteria. Relative to ABI-130, aggregate filtered Dice fell by 0.0456, MIT filtered Dice by 0.0518, Google filtered Dice by 0.0308, filtered recall by 0.0864, and filtered connectivity by 0.0726. Filtered precision improved by 0.0499 and filtered predicted-positive fraction decreased by 0.00094, so the frequency-support path did make the branch more conservative. That gain came with too much recall, MIT-Dice, and connectivity loss to count as useful family-development evidence.

Relative to ABI-126, ABI-146 improved precision by 0.0168 and reduced predicted-positive fraction by 0.00048, but lost 0.0362 aggregate filtered Dice, 0.0375 MIT filtered Dice, 0.0319 Google filtered Dice, 0.0537 recall, and 0.1392 connectivity. It therefore did not recover ABI-126's connectivity/precision profile in a useful SZA-aware form. Relative to ABI-066, it also lost 0.1606 connectivity while failing to improve aggregate or source-stratified filtered Dice. Relative to ABI-068 and ABI-143, ABI-146 is clearly lower on aggregate/source Dice and recall; its precision improvement is not enough to offset the overlap and continuity losses.

## ABI-146 trajectory

ABI-146 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1744, 0.2573, 0.2947, 0.3207, 0.2908, 0.3390, 0.3248, 0.3408, 0.3418, 0.3424, 0.3445, and 0.3497. The selected checkpoint was epoch 12, so the trajectory was still slowly improving late in training, but it remained well below ABI-130, ABI-126, ABI-143, and ABI-068 at the active 12-epoch cap.

At the selected checkpoint, source-stratified filtered Dice was 0.3260 for MIT and 0.4095 for Google. MIT had filtered precision 0.4936, recall 0.2434, connectivity 0.3273, and predicted-positive fraction 0.00266. Google had filtered precision 0.4871, recall 0.3533, connectivity 0.2976, and predicted-positive fraction 0.00134. The main failure mode is a conservative low-recall operating point, especially on MIT, rather than numerical failure or source-specific execution collapse.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3647 versus filtered Dice 0.3497, and raw predicted-positive fraction was 0.00213 versus filtered 0.00200. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-146 as a completed, finite, non-collapsed, negative controlled architecture-continuation result for the SZA-aware ASPP/detail decoder. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The additive frequency-support path produced a cleaner and more precise fixed-threshold mask than ABI-130, but it suppressed too much true contrail area and did not recover the intended connectivity.

This narrows the ASPP/detail micro-architecture branch rather than eliminating all SZA-aware or frequency-aware modeling. ABI-130 remains the stronger SZA-aware ASPP/detail point, ABI-126 remains the stronger ASPP/detail precision/connectivity comparator, and ABI-068 remains the local capped aggregate filtered-Dice reference. ABI-146 argues against further small non-suppressive feature-support additions to ABI-130 unless a new mechanism directly addresses the observed conservative recall/connectivity loss.

## Decision

Do not promote ABI-146 and do not request whole-validation diagnostics for it. The run underperforms ABI-130, ABI-126, ABI-143, ABI-066, and ABI-068 on aggregate filtered Dice, and its precision/clutter-discipline improvement is accompanied by a severe recall, MIT-Dice, and connectivity regression.

Stop this exact frequency-support continuation branch. Future work should broaden away from SZA-aware ASPP/detail micro-architecture changes toward a different architecture family, preprocessing/front-end, training policy, data policy, calibration mechanism, or diagnostic frontier under the existing contract. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-146.

## Artifact references

- `run_20260901_012037_c302cc/outputs/best_metrics.json`
- `run_20260901_012037_c302cc/outputs/final_metrics.json`
- `run_20260901_012037_c302cc/outputs/metrics.jsonl`
- `run_20260901_012037_c302cc/outputs/resource_profile.json`
- `run_20260901_012037_c302cc/outputs/model_summary.json`
- `run_20260901_012037_c302cc/outputs/prediction_samples/samples.json`
- `run_20260901_012037_c302cc/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
