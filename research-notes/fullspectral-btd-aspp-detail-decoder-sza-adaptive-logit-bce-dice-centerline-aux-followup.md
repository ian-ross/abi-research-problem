# Full-spectral BTD+SZA ASPP/detail decoder adaptive-logit BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-137 after Run `run_20260831_180256_71be83` completed.

Source Runs:

- ABI-137 SZA-aware ASPP/detail decoder adaptive-logit BCE-Dice Centerline-auxiliary continuation: `run_20260831_180256_71be83`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-136 SZA-aware ASPP/detail decoder coarse-objectness-gate negative comparator: `run_20260831_171408_56b121`
- ABI-135 deterministic-shuffle negative data-policy comparator: `run_20260831_162753_adfc95`
- ABI-131, ABI-132, and ABI-133 SZA-aware ASPP/detail local head/auxiliary comparators: `run_20260831_130730_08040a`, `run_20260831_135752_1ac18c`, and `run_20260831_144720_475594`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`

ABI-137 was a family-development continuation of ABI-130. It kept ABI-130's provider-approved `abi_16ch_plus_sza` input, deterministic raw ABI plus thermal BTD plus Solar Geometry front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was an additive adaptive logit-calibration mask head intended to move ABI-130's threshold-sweep recall upside toward the Harness fixed threshold without candidate-owned thresholding, postprocessing, Artifact Filters, losses, data handling, or target transforms.

## Contract and resource observation

ABI-137 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, combined source-balanced traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,665,294 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,273.5 seconds total wall time, 1,051.2 seconds training wall time, 1,220.3 seconds validation wall time, 6,174,455,808 bytes peak CUDA allocated, 6,805,258,240 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_130730_08040a` | ABI-131 | ABI-130 plus continuity bridge | 12 | 0.3880 | 0.3720 | 0.4279 | 0.4235 | 0.3581 | 0.2703 | 0.00306 |
| `run_20260831_135752_1ac18c` | ABI-132 | ABI-130 plus region-line agreement head | 12 | 0.3853 | 0.3730 | 0.4163 | 0.4394 | 0.3431 | 0.2971 | 0.00283 |
| `run_20260831_144720_475594` | ABI-133 | ABI-130 plus Line+Centerline auxiliary targets | 12 | 0.3879 | 0.3727 | 0.4254 | 0.4269 | 0.3554 | 0.3390 | 0.00302 |
| `run_20260831_162753_adfc95` | ABI-135 | ABI-130 architecture with deterministic-shuffle traversal | 12 | 0.3758 | 0.3703 | 0.3880 | 0.3394 | 0.4209 | 0.2174 | 0.00449 |
| `run_20260831_171408_56b121` | ABI-136 | ABI-130 plus coarse objectness gate | 7 | 0.3786 | 0.3674 | 0.4077 | 0.4456 | 0.3290 | 0.3715 | 0.00268 |
| `run_20260831_180256_71be83` | ABI-137 | ABI-130 plus adaptive additive logit-calibration head | 12 | 0.3779 | 0.3694 | 0.3988 | 0.3988 | 0.3590 | 0.2561 | 0.00326 |

ABI-137 did not meet the adaptive-logit calibration hypothesis relative to ABI-130. Filtered recall was essentially tied/slightly higher, 0.3590 versus 0.3578 (+0.0012), and MIT filtered Dice was only moderately lower, 0.3694 versus 0.3779 (-0.0084). However, the hoped-for threshold-sweep gain did not convert into a better fixed-threshold operating point. Aggregate filtered Dice fell from 0.3953 to 0.3779 (-0.0174), Google filtered Dice fell from 0.4404 to 0.3988 (-0.0415), filtered precision fell from 0.4415 to 0.3988 (-0.0427), filtered connectivity fell from 0.3851 to 0.2561 (-0.1290), and filtered predicted-positive fraction rose from 0.00294 to 0.00326.

Relative to ABI-136, the additive head avoided the multiplicative gate's strongest recall suppression: filtered recall rose from 0.3290 to 0.3590. But this was not a useful trade. ABI-137 was slightly lower on aggregate filtered Dice, lower on Google filtered Dice, lower on precision, much lower on connectivity, and higher on predicted-positive fraction. Relative to ABI-135, ABI-137 recovered precision and positive-area discipline but lost the recall-heavy signal and still did not restore ABI-130-like Google performance or connectivity. Relative to ABI-126 and ABI-066, it also failed to recover the high precision/connectivity behavior that motivates the ASPP/detail and clDice references. Relative to ABI-068, it remained below the local capped aggregate-Dice/source-balance reference on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity.

## ABI-137 trajectory

ABI-137 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2248, 0.2793, 0.3150, 0.3182, 0.3304, 0.3359, 0.3484, 0.3400, 0.3608, 0.3455, 0.3537, and 0.3779. The selected checkpoint was the final epoch 12, so the Run retained a late improvement signal and did not show clear optimization failure.

The trajectory nevertheless did not approach ABI-130's final operating point. Epoch 7 reached the highest connectivity for ABI-137, 0.3868, but with low recall 0.2928 and only 0.3484 filtered Dice. Epoch 8 had high precision 0.4430 and Google Dice 0.4022, but recall was 0.2759. The final epoch recovered recall to 0.3590 and selected aggregate Dice, but connectivity remained low at 0.2561 and Google Dice stayed under 0.40. This looks like a late recall recovery that expands positive area without preserving line continuity or source balance.

At the selected checkpoint, source-stratified filtered Dice was 0.3694 for MIT and 0.3988 for Google. MIT had filtered precision 0.4104, recall 0.3359, connectivity 0.2694, and predicted-positive fraction 0.00442. Google had filtered precision 0.3744, recall 0.4266, connectivity 0.2428, and predicted-positive fraction 0.00210. Both Dataset Sources were finite and non-collapsed, but Google lost the main ABI-130 advantage and the aggregate connectivity deficit is severe for a line-segmentation branch.

Raw-to-filtered differences were modest: raw Dice was 0.3913 versus filtered Dice 0.3779, and raw predicted-positive fraction was 0.00348 versus filtered 0.00326. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one perfect empty/negative sample and three near-zero per-sample Dice examples, but the retention policy is `first_n`, so these bounded artifacts are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-137 as a completed, finite, non-collapsed, but negative family-development result for this exact adaptive additive logit-calibration head. It is not a candidate bug, contract violation, resource failure, or Harness failure. The branch answered the narrow calibration question: adding trainable margin/residual/context-bias logits did not recover ABI-130's whole-validation threshold-sweep upside at the fixed Harness threshold. Instead, it mostly behaved like another local head tweak, with a small recall movement but substantial losses in precision, Google Dice, connectivity, and aggregate filtered Dice.

This strengthens the recent pattern from ABI-131, ABI-132, ABI-133, ABI-135, ABI-136, and now ABI-137: incremental local continuity, agreement, auxiliary, traversal, objectness-gate, and additive-logit changes around the SZA-aware ASPP/detail BCE-Dice branch have not improved on ABI-130. ABI-130 remains the best SZA-aware ASPP/detail capped reference with whole-validation diagnostic support. ABI-126 remains the ASPP/detail high-precision/connectivity comparator, ABI-066 remains the high-connectivity reference, and ABI-068 remains the local capped aggregate-Dice/source-balance reference.

## Decision

Do not promote ABI-137. Do not request whole-validation diagnostics for ABI-137 from this capped result, because it failed the controlled comparison against ABI-130 and did not establish a distinctive useful operating point. Do not repeat the exact adaptive-logit head branch unchanged.

For a later Autonomy Step, broaden away from incremental SZA-aware ASPP/detail local head changes. A stronger next hypothesis should use a distinct architecture, preprocessing/calibration mechanism, loss/data-policy frontier, or other in-contract idea that targets false positives and line connectivity without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, sampling, target derivation, or metrics.

No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260831_180256_71be83/outputs/best_metrics.json`
- `run_20260831_180256_71be83/outputs/final_metrics.json`
- `run_20260831_180256_71be83/outputs/metrics.jsonl`
- `run_20260831_180256_71be83/outputs/resource_profile.json`
- `run_20260831_180256_71be83/outputs/model_summary.json`
- `run_20260831_180256_71be83/outputs/prediction_samples/samples.json`
- `run_20260831_180256_71be83/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_171408_56b121/outputs/best_metrics.json`
- `run_20260831_162753_adfc95/outputs/best_metrics.json`
- `run_20260831_130730_08040a/outputs/best_metrics.json`
- `run_20260831_135752_1ac18c/outputs/best_metrics.json`
- `run_20260831_144720_475594/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
