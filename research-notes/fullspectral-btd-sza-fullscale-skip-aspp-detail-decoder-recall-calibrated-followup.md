# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder recall-calibrated BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-155 after Run `run_20260901_081321_b38989` completed.

Source Runs:

- ABI-155 recall-calibrated full-scale skip ASPP/detail decoder continuation: `run_20260901_081321_b38989`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity comparison target: `run_20260901_071026_32d3ec`, with whole-validation diagnostic `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice precision/connectivity comparator: `run_20260831_085615_d05ab3`

ABI-155 was a family-development continuation of ABI-154. It preserved provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a low-capacity recall-calibrated mask head with a bounded local residual and small trainable logit bias intended to move ABI-154's lower-threshold recall upside toward the Harness fixed threshold.

## Contract and resource observation

ABI-155 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,844,974 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,795.6 seconds total wall time, 1,452.6 seconds training wall time, 1,340.9 seconds validation wall time, 9,036,184,576 bytes peak CUDA allocated, 10,617,880,576 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_081321_b38989` | ABI-155 | recall-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3834 | 0.3669 | 0.4252 | 0.4685 | 0.3244 | 0.3641 | 0.00251 |

ABI-155 did not meet the intended recall-calibration outcome. Relative to ABI-154, aggregate filtered Dice fell from 0.3944 to 0.3834 (-0.0110), MIT filtered Dice fell from 0.3824 to 0.3669 (-0.0155), Google filtered Dice was essentially flat-to-lower at 0.4252 (-0.0008), filtered recall fell from 0.3359 to 0.3244 (-0.0114), and filtered connectivity fell from 0.4374 to 0.3641 (-0.0733). The positive-area discipline was retained, with filtered predicted-positive fraction 0.00251 versus ABI-154's 0.00255, and precision remained high at 0.4685, but neither recall nor Dice improved.

Relative to ABI-130, ABI-155 is lower on aggregate filtered Dice (-0.0119), MIT Dice (-0.0110), Google Dice (-0.0152), recall (-0.0334), and connectivity (-0.0210), while preserving higher precision (+0.0271) and lower predicted-positive fraction. Relative to ABI-068, ABI-155 has much lower recall (-0.0692), MIT Dice (-0.0217), aggregate Dice (-0.0130), and connectivity (-0.0259), with a precision-forward but under-recall operating point. Relative to ABI-126, ABI-155 does not recover the non-SZA precision/connectivity branch: aggregate Dice is lower by 0.0025, Google Dice is lower by 0.0163, precision is lower by 0.0061, and connectivity is lower by 0.0876, with only a small MIT Dice improvement.

## ABI-155 trajectory

ABI-155 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2209, 0.2876, 0.3081, 0.3085, 0.3123, 0.3511, 0.3675, 0.3671, 0.3586, 0.3543, 0.3673, and 0.3834. The final epoch was the selected checkpoint and the best capped filtered Dice for this Run.

The trajectory was improving at the end, but it improved to a weaker operating point than the branch it was meant to repair. Epoch 12 had raw Dice 0.3987, filtered Dice 0.3834, filtered precision 0.4685, filtered recall 0.3244, filtered connectivity 0.3641, and filtered predicted-positive fraction 0.00251. Source-stratified filtered Dice was 0.3669 for MIT and 0.4252 for Google. MIT had filtered precision 0.4755, recall 0.2987, connectivity 0.3664, and predicted-positive fraction 0.00339; Google had filtered precision 0.4540, recall 0.3998, connectivity 0.3618, and predicted-positive fraction 0.00163.

The raw-to-filtered gap remained modest and does not indicate primary Artifact Filter dependence: raw Dice was 0.3987 versus filtered Dice 0.3834, and raw predicted-positive fraction was 0.00267 versus filtered 0.00251. The fixed first-four retained prediction artifacts are traceability samples under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-155 as a completed, finite, non-collapsed, scientifically negative result for the specific recall-calibrated mask-head variant. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The negative result is scientific: the bounded local residual and small trainable bias did not move ABI-154's lower-threshold recall upside into the fixed-threshold metrics, and it materially reduced connectivity and MIT Dice while keeping the model conservative.

This result weakens the local hypothesis that ABI-154 can be improved by a simple final-head calibration patch. It does not eliminate the broader SZA-aware ASPP/detail family, because ABI-130 and ABI-154 remain valid complementary branches: ABI-130 is the stronger aggregate/default-threshold SZA-aware ASPP/detail reference, and ABI-154 is the whole-validation-tested precision/connectivity branch. It also does not supersede ABI-068 as the current capped aggregate/source-balance reference.

## Decision

Do not promote ABI-155, do not request whole-validation diagnostics for it, and do not repeat this exact recall-calibrated mask-head variant unchanged. Retain ABI-154 as the SZA-aware full-scale-skip precision/connectivity reference and ABI-130 as the SZA-aware ASPP/detail aggregate/reference branch.

The next useful direction should broaden beyond simple additive/bias calibration on ABI-154. Contract-compliant options include a different SZA-aware ASPP/detail calibration mechanism that acts earlier in feature fusion rather than only at the final logits, a data-policy or loss continuation if tied to a controlled hypothesis, or a broader architecture-family scout that attacks the persistent precision/recall/connectivity trade-off without candidate-owned thresholding, Artifact Filters, postprocessing, losses, data loading, or sampling implementation. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-155.

## Artifact references

- `run_20260901_081321_b38989/outputs/best_metrics.json`
- `run_20260901_081321_b38989/outputs/final_metrics.json`
- `run_20260901_081321_b38989/outputs/metrics.jsonl`
- `run_20260901_081321_b38989/outputs/resource_profile.json`
- `run_20260901_081321_b38989/outputs/model_summary.json`
- `run_20260901_081321_b38989/outputs/prediction_samples/samples.json`
- `run_20260901_081321_b38989/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
