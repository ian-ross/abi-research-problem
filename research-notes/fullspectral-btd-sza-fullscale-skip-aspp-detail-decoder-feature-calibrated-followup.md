# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder feature-calibrated BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-156 after Run `run_20260901_090713_9c7d32` completed.

Source Runs:

- ABI-156 feature-calibrated full-scale skip ASPP/detail decoder continuation: `run_20260901_090713_9c7d32`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity target and whole-validation-tested branch: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-155 failed final-head recall-calibration continuation: `run_20260901_081321_b38989`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice precision/connectivity comparator: `run_20260831_085615_d05ab3`

ABI-156 was a family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was moving calibration from ABI-155's final mask-head patch into a neutral-initialized, low-capacity SZA-conditioned feature-fusion calibrator before final feature projection.

## Contract and resource observation

ABI-156 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,754,970 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,601.8 seconds total wall time, 18.71 training samples per second, 8,720,158,720 bytes peak CUDA allocated, 10,238,296,064 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 9 rather than the final epoch.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_081321_b38989` | ABI-155 | final-head recall-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3834 | 0.3669 | 0.4252 | 0.4685 | 0.3244 | 0.3641 | 0.00251 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |

ABI-156 partially achieved the intended recall-calibration direction but did not preserve ABI-154's defining precision/connectivity profile. Relative to ABI-154, ABI-156 increased filtered recall from 0.3359 to 0.3487 (+0.0128) and Google filtered Dice from 0.4260 to 0.4353 (+0.0093). However, aggregate filtered Dice fell from 0.3944 to 0.3926 (-0.0018), MIT filtered Dice fell from 0.3824 to 0.3762 (-0.0062), filtered precision fell from 0.4777 to 0.4491 (-0.0286), filtered connectivity fell from 0.4374 to 0.3884 (-0.0490), and the filtered predicted-positive fraction rose from 0.00255 to 0.00281.

Relative to ABI-155, moving calibration earlier in feature fusion was clearly better: aggregate filtered Dice improved by 0.0091, MIT filtered Dice by 0.0093, Google filtered Dice by 0.0101, filtered recall by 0.0243, and filtered connectivity by 0.0243, while precision remained reasonably high. This suggests the feature-fusion placement was a better local calibration mechanism than final-head calibration. It is still not an aggregate improvement over ABI-154 or ABI-130.

Relative to ABI-130, ABI-156 remains slightly lower on aggregate filtered Dice (-0.0027), Google filtered Dice (-0.0051), and recall (-0.0091). It improves precision (+0.0076) and connectivity (+0.0033) but not by enough to match ABI-154's cleaner precision/connectivity branch. Relative to ABI-068, ABI-156 has lower aggregate Dice (-0.0038), MIT Dice (-0.0124), recall (-0.0449), and near-tie connectivity, while improving Google Dice and precision. Relative to ABI-126, ABI-156 improves aggregate Dice, MIT Dice, Google-to-MIT balance, and recall, but trails ABI-126's precision/connectivity operating point.

## ABI-156 trajectory

ABI-156 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1997, 0.2908, 0.3137, 0.3433, 0.3244, 0.3419, 0.3645, 0.3764, 0.3926, 0.3608, 0.3670, and 0.3688. The selected best checkpoint was epoch 9; epochs 10-12 did not recover to the epoch-9 aggregate result.

The trajectory shows an improving early-to-mid run followed by late instability rather than a clean terminal improvement. Epoch 9 combined raw Dice 0.4076, filtered Dice 0.3926, filtered precision 0.4491, filtered recall 0.3487, filtered connectivity 0.3884, and filtered predicted-positive fraction 0.00281. Source-stratified filtered Dice was 0.3762 for MIT and 0.4353 for Google. MIT had filtered precision 0.4480, recall 0.3242, connectivity 0.3904, and predicted-positive fraction 0.00391; Google had filtered precision 0.4515, recall 0.4201, connectivity 0.3865, and predicted-positive fraction 0.00172.

The final epoch had lower filtered Dice, 0.3688, with filtered precision 0.4449, recall 0.3149, connectivity 0.3337, MIT filtered Dice 0.3474, and Google filtered Dice 0.4197. Because the Harness selected epoch 9, the final-epoch regression is not a lifecycle problem, but it weakens the case for extending this exact branch without a clearer stability hypothesis.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.4076 versus filtered Dice 0.3926, and raw predicted-positive fraction was 0.00301 versus filtered 0.00281. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction artifacts have near-zero per-sample Dice under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-156 as a completed, finite, non-collapsed, scientifically mixed-to-negative result for the specific SZA-conditioned feature-fusion calibration variant. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result is scientifically informative because it separates calibration placement effects. ABI-156 improved materially over ABI-155's late final-head calibration and recovered some ABI-154-relative recall and Google Dice, so feature-level calibration is a better local mechanism than logit-only calibration. The cost was losing most of ABI-154's distinctive precision and connectivity advantage while still failing to match ABI-130 or ABI-068 on capped aggregate filtered Dice. The best checkpoint also occurred at epoch 9 with a late regression, so the branch does not present a strong stable improvement trajectory.

ABI-154 remains the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference. ABI-130 remains the SZA-aware ASPP/detail aggregate/reference branch. ABI-068 remains the local capped aggregate/source-balance reference. ABI-156 should be retained as evidence that feature-fusion calibration can improve over final-head calibration but does not by itself solve the default-threshold precision/recall/connectivity trade-off.

## Decision

Do not promote ABI-156, do not request whole-validation diagnostics for it, and do not repeat this exact feature-calibrated full-scale skip variant unchanged. The result does not exceed ABI-154's capped precision/connectivity branch, ABI-130's SZA-aware ASPP/detail aggregate branch, or ABI-068's aggregate/source-balance reference.

The next useful direction should broaden beyond local calibration patches on the full-scale skip ASPP/detail branch. Contract-compliant options include a controlled loss or sampling-policy continuation if tied to a specific source/recall hypothesis, an architecture that improves default-threshold recall earlier than the final fused features without candidate-owned thresholding, or a broader family scout aimed at negative-patch clutter and thin-line continuity from a different inductive bias. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-156.

## Artifact references

- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260901_090713_9c7d32/outputs/final_metrics.json`
- `run_20260901_090713_9c7d32/outputs/metrics.jsonl`
- `run_20260901_090713_9c7d32/outputs/resource_profile.json`
- `run_20260901_090713_9c7d32/outputs/model_summary.json`
- `run_20260901_090713_9c7d32/outputs/prediction_samples/samples.json`
- `run_20260901_090713_9c7d32/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_081321_b38989/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
