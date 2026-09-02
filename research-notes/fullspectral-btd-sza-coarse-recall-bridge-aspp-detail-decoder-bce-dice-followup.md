# Full-spectral BTD+SZA coarse-recall-bridge ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-159 after Run `run_20260901_114031_58faad` completed.

Source Runs:

- ABI-159 coarse-recall-bridge ASPP/detail decoder with trusted BCE-Dice and Centerline auxiliary target: `run_20260901_114031_58faad`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity target and whole-validation-tested branch: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-158 full-scale skip Line+Centerline auxiliary continuation: `run_20260901_105011_c26d0c`
- ABI-157 deterministic-shuffle full-scale skip continuation: `run_20260901_095946_b45eb3`
- ABI-156 feature-calibrated full-scale skip continuation: `run_20260901_090713_9c7d32`
- ABI-155 final-head recall-calibrated full-scale skip continuation: `run_20260901_081321_b38989`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`

ABI-159 was a family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, the trusted 1,024-record-per-Dataset-Source/split representative cap, and the provider-derived `centerline_logits` auxiliary output at weight 0.02. The controlled change was adding a compact coarse recall bridge that projects ASPP context, decoder scales, and high-resolution detail to mask resolution before final full-scale skip refinement.

## Contract and resource observation

ABI-159 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,835,970 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,784.8 seconds total wall time, 1,440.0 seconds training wall time, 1,342.7 seconds validation wall time, 17.07 training samples per second, 18.30 validation samples per second, 9,469,136,384 bytes peak CUDA allocated, 11,540,627,456 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, which was also the final epoch.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_081321_b38989` | ABI-155 | final-head recall-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3834 | 0.3669 | 0.4252 | 0.4685 | 0.3244 | 0.3641 | 0.00251 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260901_105011_c26d0c` | ABI-158 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, Line+Centerline aux | 10 | 0.3742 | 0.3639 | 0.3974 | 0.3981 | 0.3531 | 0.2710 | 0.00321 |
| `run_20260901_114031_58faad` | ABI-159 | coarse-recall-bridge full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3740 | 0.3597 | 0.4071 | 0.4013 | 0.3501 | 0.2498 | 0.00316 |

ABI-159 did not support the coarse-recall-bridge hypothesis relative to ABI-154. The intended useful outcome was to raise filtered recall by at least about 0.015 while keeping filtered Dice within roughly 0.005-0.010 of ABI-154 and retaining materially better precision/connectivity than ABI-158. ABI-159 increased filtered recall from 0.3359 to 0.3501 (+0.0143), just below the target and not enough to offset the losses in aggregate filtered Dice from 0.3944 to 0.3740 (-0.0204), MIT filtered Dice from 0.3824 to 0.3597 (-0.0227), Google filtered Dice from 0.4260 to 0.4071 (-0.0189), filtered precision from 0.4777 to 0.4013 (-0.0763), and filtered connectivity from 0.4374 to 0.2498 (-0.1876). Filtered predicted-positive fraction increased from 0.00255 to 0.00316, consistent with a broader positive-area operating point rather than selective false-negative recovery.

Relative to ABI-158, ABI-159 was effectively lateral rather than a recovery. It had nearly identical aggregate filtered Dice (-0.0002), lower MIT filtered Dice (-0.0043), higher Google filtered Dice (+0.0097), slightly higher precision (+0.0032), slightly lower recall (-0.0029), and lower connectivity (-0.0212). Relative to ABI-156, the best local ABI-154 continuation after ABI-154 itself, ABI-159 lost aggregate filtered Dice (-0.0186), MIT filtered Dice (-0.0166), Google filtered Dice (-0.0281), precision (-0.0478), and connectivity (-0.1386) while only matching recall within noise (+0.0014). Relative to ABI-130, ABI-159 also trailed aggregate Dice (-0.0213), MIT Dice (-0.0182), Google Dice (-0.0332), precision (-0.0401), recall (-0.0077), and connectivity (-0.1353). Relative to ABI-068, ABI-159 had nearly matched precision but lower aggregate Dice, MIT Dice, Google Dice, recall, and connectivity.

## ABI-159 trajectory

ABI-159 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1873, 0.2799, 0.3048, 0.3172, 0.3259, 0.3482, 0.3698, 0.3543, 0.3521, 0.3613, 0.3615, and 0.3740. The selected best checkpoint was epoch 12 after a mid-run dip, so the branch was still making finite progress at the budget boundary.

At the selected checkpoint, ABI-159 had raw Dice 0.3880, filtered Dice 0.3740, filtered precision 0.4013, filtered recall 0.3501, filtered connectivity 0.2498, and filtered predicted-positive fraction 0.00316. Source-stratified filtered Dice was 0.3597 for MIT and 0.4071 for Google. MIT had filtered precision 0.4182, recall 0.3155, connectivity 0.2786, and predicted-positive fraction 0.00408. Google had filtered precision 0.3708, recall 0.4513, connectivity 0.2210, and predicted-positive fraction 0.00225.

The trajectory shows a useful distinction between overlap and continuity. ABI-159 recovered some recall and preserved non-degenerate source behavior, but its Contrail Connectivity Metric collapsed relative to ABI-154 and ABI-156. The final checkpoint's Google recall was high, but Google precision and connectivity were low enough that the extra coarse support appears to introduce fragmented or broad support rather than continuous thin-line discrimination. The raw-to-filtered differences were modest: raw Dice 0.3880 versus filtered Dice 0.3740, and raw predicted-positive fraction 0.00335 versus filtered 0.00316. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-159 as a completed, finite, non-collapsed, but scientifically negative result for this exact coarse-recall-bridge full-scale skip ASPP/detail branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result is informative because it tests a pre-final recall-support intervention after ABI-155, ABI-156, and ABI-158 showed that late calibration or extra local auxiliary supervision did not deliver a useful ABI-154 recall recovery. ABI-159 demonstrates that injecting coarse context before final refinement can slightly increase recall relative to ABI-154, but under the current capped budget that recall comes with a large precision/connectivity penalty and does not improve aggregate or source-stratified Dice. This extends the pattern that local additions around the full-scale skip ASPP/detail branch are not producing a better fixed-threshold operating point.

ABI-154 remains the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference. ABI-130 remains the SZA-aware ASPP/detail aggregate/reference branch. ABI-068 remains the local capped aggregate/source-balance reference. ABI-156 remains the strongest local full-scale skip continuation after ABI-154. ABI-155, ABI-157, ABI-158, and ABI-159 are negative controlled continuations for late calibration, traversal, extra Line Target supervision, and pre-final coarse recall support.

## Decision

Do not promote ABI-159, do not request whole-validation diagnostics for it, and do not repeat this exact coarse-recall-bridge branch unchanged. It failed the proposed useful-outcome test because the small ABI-154-relative recall gain did not meet the stated threshold and came with severe precision, connectivity, aggregate Dice, and MIT/Google source-stratified Dice losses.

The next useful direction should broaden away from adding local gates, auxiliary heads, or coarse-support paths to the full-scale skip ASPP/detail branch. Contract-compliant next options include a different architecture family that improves recall/continuity before ASPP-style bottlenecking, a different in-contract preprocessing/front-end inductive bias for thin spectral-line evidence, or a loss/data-policy axis that changes fixed-threshold calibration while keeping data loading, target derivation, losses, metrics, thresholding, Artifact Filters, and sampling provider-owned. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-159.

## Artifact references

- `run_20260901_114031_58faad/outputs/best_metrics.json`
- `run_20260901_114031_58faad/outputs/final_metrics.json`
- `run_20260901_114031_58faad/outputs/metrics.jsonl`
- `run_20260901_114031_58faad/outputs/resource_profile.json`
- `run_20260901_114031_58faad/outputs/model_summary.json`
- `run_20260901_114031_58faad/outputs/prediction_samples/samples.json`
- `run_20260901_114031_58faad/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_105011_c26d0c/outputs/best_metrics.json`
- `run_20260901_095946_b45eb3/outputs/best_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260901_081321_b38989/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
