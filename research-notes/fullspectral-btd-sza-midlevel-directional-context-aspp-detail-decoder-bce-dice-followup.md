# Full-spectral BTD+SZA mid-level directional-context ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-160 after Run `run_20260901_123418_da6b1e` completed.

Source Runs:

- ABI-160 mid-level directional-context ASPP/detail decoder with trusted BCE-Dice and Centerline auxiliary target: `run_20260901_123418_da6b1e`
- ABI-159 coarse-recall-bridge ASPP/detail decoder immediate negative control: `run_20260901_114031_58faad`
- ABI-158 full-scale skip Line+Centerline auxiliary continuation: `run_20260901_105011_c26d0c`
- ABI-156 feature-calibrated full-scale skip continuation: `run_20260901_090713_9c7d32`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity target and whole-validation-tested branch: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`

ABI-160 was a family-development continuation of the SZA-aware ASPP/detail decoder family. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, the trusted 1,024-record-per-Dataset-Source/split representative cap, and the provider-derived `centerline_logits` auxiliary output at weight 0.02. The controlled change was adding a bounded mid-level horizontal/vertical/dilated directional-context residual after the 64 x 64 encoder stage and before the deepest ASPP bottleneck.

## Contract and resource observation

ABI-160 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 11,080,971 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,314.3 seconds total wall time, 1,039.0 seconds training wall time, 1,273.2 seconds validation wall time, 23.65 training samples per second, 19.30 validation samples per second, 6,127,139,328 bytes peak CUDA allocated, 6,698,303,488 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 11; final epoch 12 was slightly worse by the primary metric.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260901_105011_c26d0c` | ABI-158 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, Line+Centerline aux | 10 | 0.3742 | 0.3639 | 0.3974 | 0.3981 | 0.3531 | 0.2710 | 0.00321 |
| `run_20260901_114031_58faad` | ABI-159 | coarse-recall-bridge full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3740 | 0.3597 | 0.4071 | 0.4013 | 0.3501 | 0.2498 | 0.00316 |
| `run_20260901_123418_da6b1e` | ABI-160 | mid-level directional-context ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 11 | 0.3831 | 0.3819 | 0.3861 | 0.4023 | 0.3656 | 0.3252 | 0.00329 |

ABI-160 partially recovered from ABI-159 but did not support the proposed mid-level directional-context hypothesis strongly enough to continue this exact branch unchanged. Relative to ABI-159, ABI-160 improved best filtered Dice by +0.0091, MIT filtered Dice by +0.0223, filtered recall by +0.0154, filtered connectivity by +0.0754, and predicted-positive fraction by +0.00013, while Google filtered Dice fell by -0.0210 and precision was essentially flat (+0.0010). This indicates that moving directional support before the deepest ASPP bottleneck is materially better than ABI-159's coarse recall bridge, especially for MIT and connectivity, but still not a balanced improvement.

Relative to the principal ABI-130/ABI-154 references, ABI-160 remains below the useful-outcome band. Compared with ABI-130, ABI-160 lost aggregate filtered Dice (-0.0122), Google filtered Dice (-0.0543), precision (-0.0391), and connectivity (-0.0599), while improving recall only slightly (+0.0077) and MIT Dice (+0.0040). Compared with ABI-154, ABI-160 improved recall (+0.0297) and nearly matched MIT Dice (-0.0005), but lost aggregate filtered Dice (-0.0113), Google filtered Dice (-0.0399), precision (-0.0753), and connectivity (-0.1123). Compared with ABI-068, ABI-160 trailed aggregate Dice (-0.0133), MIT Dice (-0.0067), Google Dice (-0.0300), recall (-0.0280), and connectivity (-0.0648), with only slightly higher precision (+0.0032).

The pre-bottleneck directional residual therefore changed the trade-off in the intended recall direction but did not preserve the source balance and continuity that made ABI-130/ABI-154/ABI-068 stronger capped references.

## ABI-160 trajectory

ABI-160 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1817, 0.2556, 0.2513, 0.2983, 0.3304, 0.3649, 0.3692, 0.3586, 0.3785, 0.3491, 0.3831, and 0.3794. The selected best checkpoint was epoch 11, with a small final-epoch regression at epoch 12.

At the selected checkpoint, ABI-160 had raw Dice 0.3975, filtered Dice 0.3831, filtered precision 0.4023, filtered recall 0.3656, filtered connectivity 0.3252, and filtered predicted-positive fraction 0.00329. Source-stratified filtered Dice was 0.3819 for MIT and 0.3861 for Google. MIT had filtered precision 0.4131, recall 0.3551, connectivity 0.3428, and predicted-positive fraction 0.00464. Google had filtered precision 0.3767, recall 0.3960, connectivity 0.3076, and predicted-positive fraction 0.00194.

At final epoch 12, aggregate filtered Dice was 0.3794, raw Dice 0.3935, filtered precision 0.4115, filtered recall 0.3519, filtered connectivity 0.2947, MIT filtered Dice 0.3637, and Google filtered Dice 0.4174. This source swap between epochs 11 and 12 is a warning sign: the branch did not settle into a stable MIT/Google-balanced operating point by the 12-epoch budget. Raw-to-filtered differences remained modest at the final checkpoint: raw Dice 0.3935 versus filtered Dice 0.3794, and raw predicted-positive fraction 0.00330 versus filtered 0.00310. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-160 as a completed, finite, non-collapsed, mixed-to-negative scientific result for this exact mid-level directional-context ASPP/detail branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result is informative because it separates the placement of directional context from ABI-159's late coarse-recall bridge. ABI-160 shows that pre-bottleneck directional context can recover some recall and connectivity versus the late bridge, but under the current capped budget that improvement is insufficient and source-unstable: the best checkpoint sacrifices Google performance, precision, and connectivity relative to ABI-130/ABI-154, while the final checkpoint loses MIT performance and connectivity. This reinforces the pattern that local additions to the SZA-aware ASPP/detail decoder are not reliably improving the capped fixed-threshold operating point.

ABI-154 remains the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference. ABI-130 remains the SZA-aware ASPP/detail aggregate/reference branch. ABI-068 remains the local capped aggregate/source-balance reference. ABI-156 remains the strongest local full-scale skip continuation after ABI-154. ABI-155 through ABI-160 are negative or mixed controlled continuations around the full-scale skip/ASPP/detail branch.

## Decision

Do not promote ABI-160, do not request whole-validation diagnostics for it, and do not repeat this exact mid-level directional-context branch unchanged. It failed the proposed useful-outcome test because it did not keep aggregate filtered Dice within roughly 0.005-0.010 of ABI-130/ABI-154 while improving recall/connectivity and preserving source balance.

The next useful direction should broaden away from adding more local residual/gate/auxiliary refinements to the full-scale skip ASPP/detail branch. Contract-compliant next options include a different front-end/preprocessing inductive bias for thin spectral-line evidence, a data-policy or loss-axis comparison that directly targets fixed-threshold calibration, or a materially different architecture family with high-resolution line continuity that is not built around the same ASPP/detail/full-scale-skip pattern. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-160.

## Artifact references

- `run_20260901_123418_da6b1e/outputs/best_metrics.json`
- `run_20260901_123418_da6b1e/outputs/final_metrics.json`
- `run_20260901_123418_da6b1e/outputs/metrics.jsonl`
- `run_20260901_123418_da6b1e/outputs/resource_profile.json`
- `run_20260901_123418_da6b1e/outputs/model_summary.json`
- `run_20260901_123418_da6b1e/outputs/prediction_samples/samples.json`
- `run_20260901_123418_da6b1e/resolved_manifest.yaml`
- `run_20260901_114031_58faad/outputs/best_metrics.json`
- `run_20260901_105011_c26d0c/outputs/best_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
