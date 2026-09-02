# Full-spectral BTD+SZA nested-skip U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-139 after Run `run_20260831_193933_70bcc7` completed.

Source Runs:

- ABI-139 SZA-aware nested-skip U-Net BCE-Dice Centerline-auxiliary continuation: `run_20260831_193933_70bcc7`
- ABI-079 full-spectral BTD nested-skip U-Net focal-Tversky scout: `run_20260828_104353_1455f1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`

ABI-139 was a family-development continuation of ABI-079. It kept the compact nested-skip high-resolution decoder path, changed the input to provider-approved `abi_16ch_plus_sza`, added deterministic thermal brightness-temperature-difference and SZA-derived front-end features from approved channels only, used trusted `bce_dice` primary loss, retained provider-derived Centerline Target auxiliary supervision at weight 0.02, and trained under combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

## Contract and resource observation

ABI-139 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 6,629,731 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 1,768.7 seconds total wall time, 613.6 seconds training wall time, 1,153.3 seconds validation wall time, 5,122,162,176 bytes peak CUDA allocated, 6,419,382,272 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_193933_70bcc7` | ABI-139 | nested-skip U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3355 | 0.3302 | 0.3488 | 0.3510 | 0.3213 | 0.1679 | 0.00332 |
| `run_20260828_104353_1455f1` | ABI-079 | nested-skip U-Net, focal-Tversky, ABI-16+BTD | 9 | 0.2984 | 0.3153 | 0.2650 | 0.2284 | 0.4300 | 0.1265 | 0.00682 |

ABI-139 partially repaired ABI-079's excessive positive-area profile, but did not validate the full SZA+BCE nested-skip hypothesis. Against ABI-079, ABI-139 improved aggregate filtered Dice by +0.0371, Google filtered Dice by +0.0838, filtered precision by +0.1226, filtered connectivity by +0.0414, and reduced filtered predicted-positive fraction from 0.00682 to 0.00332. Those changes show that the ABI-130 calibration axis did temper the permissive nested-skip profile.

However, the repair was incomplete. ABI-139 missed the proposal's stronger useful-evidence threshold of at least +0.05 aggregate filtered Dice over ABI-079, reduced recall from 0.4300 to 0.3213, kept MIT filtered Dice below 0.35, and left filtered connectivity far below 0.30. Against ABI-130, aggregate filtered Dice fell by -0.0598, Google filtered Dice by -0.0916, precision by -0.0904, recall by -0.0366, connectivity by -0.2172, and positive-area discipline was slightly worse. ABI-139 also remained below ABI-068, ABI-126, and ABI-066 on the main capped operating-point references.

## ABI-139 trajectory

ABI-139 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1433, 0.2160, 0.1864, 0.2621, 0.2879, 0.3066, 0.3012, 0.3265, 0.3344, 0.3295, 0.3343, and 0.3355. The final epoch was the selected best checkpoint, but improvement had mostly flattened after epoch 8.

The best checkpoint showed source-stratified filtered Dice of 0.3302 for MIT and 0.3488 for Google. MIT had filtered precision 0.3615, recall 0.3039, connectivity 0.1790, and predicted-positive fraction 0.00454. Google had filtered precision 0.3283, recall 0.3721, connectivity 0.1568, and predicted-positive fraction 0.00209. Both Dataset Sources were finite and non-collapsed, but neither source reached the desired Dice/connectivity region, and Google precision remained weak compared with the SZA-aware ASPP/detail reference.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3472 versus filtered Dice 0.3355, and raw predicted-positive fraction was 0.00353 versus filtered 0.00332. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples all have near-zero per-sample Dice under the `first_n` retention policy; these bounded artifacts are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-139 as a completed, finite, non-collapsed, mixed-to-negative family-development result. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The narrow question was whether ABI-130's SZA+BCE calibration axis could make the nested-skip architecture competitive while retaining useful high-resolution multi-depth evidence. The answer is mostly negative: calibration improved ABI-079's clutter and Google behavior, but not enough to approach ABI-130/ABI-068 or to recover line connectivity.

This result suggests that the nested-skip decoder's extra dense skip fusion is not currently the limiting missing ingredient for the campaign's best capped operating point. The source-balanced finite trajectory is still useful evidence, because it separates the ABI-079 failure mode into an objective/input calibration issue and a remaining architecture/connectivity weakness. But without a sharper new mechanism, further nested-skip work should be lower priority than broader architecture or calibration frontiers.

## Decision

Do not promote ABI-139. Do not request whole-validation diagnostics for ABI-139 from this capped result, because it did not become locally competitive with ABI-130, ABI-068, ABI-126, or ABI-066 and did not establish a distinctive high-connectivity or high-precision operating point. Do not repeat the exact SZA+BCE nested-skip branch unchanged.

For a later Autonomy Step, broaden away from nested-skip and incremental SZA-aware ASPP/detail local tweaks unless a clearly distinct in-contract mechanism targets the observed failure mode. Reasonable future directions include a different architecture family, deterministic feature calibration, data-policy or loss-policy variants, or line-connectivity mechanisms that remain entirely inside the Candidate Experiment Contract and do not move thresholding, postprocessing, Artifact Filters, data loading, target derivation, metrics, or sampling into candidate code.

No new Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_193933_70bcc7/outputs/best_metrics.json`
- `run_20260831_193933_70bcc7/outputs/final_metrics.json`
- `run_20260831_193933_70bcc7/outputs/metrics.jsonl`
- `run_20260831_193933_70bcc7/outputs/resource_profile.json`
- `run_20260831_193933_70bcc7/outputs/model_summary.json`
- `run_20260831_193933_70bcc7/outputs/prediction_samples/samples.json`
- `run_20260831_193933_70bcc7/resolved_manifest.yaml`
- `run_20260828_104353_1455f1/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
