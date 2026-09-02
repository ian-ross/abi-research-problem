# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice Line+Centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-158 after Run `run_20260901_105011_c26d0c` completed.

Source Runs:

- ABI-158 full-scale skip ASPP/detail decoder with trusted Line and Centerline auxiliary targets: `run_20260901_105011_c26d0c`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity target and whole-validation-tested branch: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-157 deterministic-shuffle full-scale skip continuation: `run_20260901_095946_b45eb3`
- ABI-156 feature-calibrated full-scale skip continuation: `run_20260901_090713_9c7d32`
- ABI-155 final-head recall-calibrated full-scale skip continuation: `run_20260901_081321_b38989`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice precision/connectivity comparator: `run_20260831_085615_d05ab3`

ABI-158 was a family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled change was adding a provider-derived `line_logits` auxiliary output at trusted `weighted_bce` weight 0.01 alongside the existing `centerline_logits` auxiliary output at weight 0.02.

## Contract and resource observation

ABI-158 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `line_logits` and `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,741,891 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,533.2 seconds total wall time, 1,269.3 seconds training wall time, 1,261.8 seconds validation wall time, 19.36 training samples per second, 19.48 validation samples per second, 8,021,986,304 bytes peak CUDA allocated, 9,441,378,304 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 10.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_081321_b38989` | ABI-155 | final-head recall-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3834 | 0.3669 | 0.4252 | 0.4685 | 0.3244 | 0.3641 | 0.00251 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260901_095946_b45eb3` | ABI-157 | deterministic-shuffle full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 10 | 0.3730 | 0.3595 | 0.4063 | 0.4559 | 0.3157 | 0.3163 | 0.00251 |
| `run_20260901_105011_c26d0c` | ABI-158 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, Line+Centerline aux | 10 | 0.3742 | 0.3639 | 0.3974 | 0.3981 | 0.3531 | 0.2710 | 0.00321 |

ABI-158 did not support the Line+Centerline auxiliary-supervision hypothesis for the full-scale skip branch. Relative to ABI-154, aggregate filtered Dice fell from 0.3944 to 0.3742 (-0.0202), MIT filtered Dice fell from 0.3824 to 0.3639 (-0.0185), Google filtered Dice fell from 0.4260 to 0.3974 (-0.0286), filtered precision fell from 0.4777 to 0.3981 (-0.0796), and filtered connectivity fell from 0.4374 to 0.2710 (-0.1664). Filtered recall did rise from 0.3359 to 0.3531 (+0.0172), and filtered predicted-positive fraction rose from 0.00255 to 0.00321, but the recall gain was too small and too expensive in precision/connectivity to count as a useful recovery of ABI-154's conservative operating point.

Relative to ABI-130, ABI-158 was lower on aggregate filtered Dice (-0.0211), MIT filtered Dice (-0.0140), Google filtered Dice (-0.0430), precision (-0.0434), recall (-0.0048), and connectivity (-0.1141), while predicting slightly more filtered positive area. Relative to ABI-068, ABI-158 was lower on aggregate Dice (-0.0222), MIT Dice (-0.0247), Google Dice (-0.0187), recall (-0.0405), and connectivity (-0.1190), with nearly matched precision. Relative to ABI-157, ABI-158 slightly recovered aggregate and MIT Dice and recall, but further reduced Google Dice, precision, and connectivity. The controlled Line Target addition therefore behaved like an auxiliary burden or calibration disruption rather than a line-support improvement.

## ABI-158 trajectory

ABI-158 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2094, 0.2861, 0.2664, 0.3085, 0.3220, 0.3424, 0.3569, 0.3542, 0.3675, 0.3742, 0.3591, and 0.3698. The selected best checkpoint was epoch 10, followed by a lower epoch 11 and a partial precision-forward recovery at epoch 12.

At the best checkpoint, ABI-158 had raw Dice 0.3881, filtered Dice 0.3742, filtered precision 0.3981, filtered recall 0.3531, filtered connectivity 0.2710, and filtered predicted-positive fraction 0.00321. Source-stratified filtered Dice was 0.3639 for MIT and 0.3974 for Google. MIT had filtered precision 0.4239, recall 0.3189, connectivity 0.3182, and predicted-positive fraction 0.00406; Google had filtered precision 0.3539, recall 0.4531, connectivity 0.2239, and predicted-positive fraction 0.00236.

The final epoch shifted back toward ABI-154-like positive-area discipline but did not recover its aggregate result: filtered Dice 0.3698, precision 0.4726, recall 0.3037, connectivity 0.3511, predicted-positive fraction 0.00233, MIT filtered Dice 0.3489, and Google filtered Dice 0.4223. This final state confirms that the architecture can still produce a conservative high-precision operating point, but the extra Line Target head did not improve the selected fixed-threshold trade-off or preserve the full-scale skip branch's distinctive connectivity.

Raw-to-filtered differences at the selected checkpoint were modest: raw Dice was 0.3881 versus filtered Dice 0.3742, and raw predicted-positive fraction was 0.00342 versus filtered 0.00321. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction artifacts remain traceability samples under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-158 as a completed, finite, non-collapsed, scientifically negative result for the exact full-scale skip ASPP/detail Line+Centerline auxiliary variant. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result is informative because it tests a narrow auxiliary-supervision axis after ABI-154's whole-validation diagnostic showed real precision/connectivity gains but latent under-recall. Adding explicit Line Target supervision did move the selected checkpoint toward more predicted-positive area and slightly higher recall than ABI-154, but it damaged the very precision/connectivity qualities that made ABI-154 useful. This mirrors the broader pattern that simple auxiliary additions or local calibration heads have not produced a free default-threshold recall recovery inside the full-scale skip ASPP/detail branch.

ABI-154 remains the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference. ABI-130 remains the SZA-aware ASPP/detail aggregate/reference branch. ABI-068 remains the local capped aggregate/source-balance reference. ABI-156 remains the strongest local full-scale skip variant after ABI-154, while ABI-155, ABI-157, and ABI-158 are negative controlled continuations.

## Decision

Do not promote ABI-158, do not request whole-validation diagnostics for it, and do not repeat this exact Line+Centerline full-scale skip variant unchanged. It failed the proposed useful-outcome test because the small recall improvement over ABI-154 did not preserve ABI-154 precision, connectivity, aggregate Dice, source-stratified Dice, or positive-area discipline.

The next useful direction should broaden away from adding local auxiliary heads to the full-scale skip ASPP/detail branch. Contract-compliant options include a different architecture that improves recall before full-resolution fusion, a calibrated loss/front-end choice that shifts default-threshold logits without sacrificing connectivity, or a broader preprocessing/inductive-bias scout that separates thin contrail evidence from cloud-edge clutter while leaving losses, targets, metrics, Artifact Filters, data loading, and thresholding provider-owned. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-158.

## Artifact references

- `run_20260901_105011_c26d0c/outputs/best_metrics.json`
- `run_20260901_105011_c26d0c/outputs/final_metrics.json`
- `run_20260901_105011_c26d0c/outputs/metrics.jsonl`
- `run_20260901_105011_c26d0c/outputs/resource_profile.json`
- `run_20260901_105011_c26d0c/outputs/model_summary.json`
- `run_20260901_105011_c26d0c/outputs/prediction_samples/samples.json`
- `run_20260901_105011_c26d0c/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_095946_b45eb3/outputs/best_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260901_081321_b38989/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
