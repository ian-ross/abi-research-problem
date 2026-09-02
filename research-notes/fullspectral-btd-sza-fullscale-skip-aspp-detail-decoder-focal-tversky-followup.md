# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-172 after Run `run_20260901_225502_53acd2` completed.

Source Runs:

- ABI-172 full-scale skip ASPP/detail decoder, focal-Tversky Centerline-auxiliary continuation: `run_20260901_225502_53acd2`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice parent: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-169 full-scale skip ASPP/detail decoder BCE-Dice-clDice loss-swap comparison: `run_20260901_202820_08734b`
- ABI-171 full-scale skip ASPP/detail decoder Centerline Target auxiliary weight 0.01 comparison: `run_20260901_220525_8c0116`

ABI-172 was a controlled family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, compact residual encoder, ASPP bottleneck, full-scale skip fusion, high-resolution detail path, line-aware final refinement, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, the trusted 1,024-record-per-Dataset-Source/split representative cap, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled manifest change was switching the trusted primary loss from `bce_dice` to `focal_tversky`.

## Contract and resource observation

ABI-172 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, primary or auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling and matching the ABI-154/169/171 full-scale skip architecture size. The Run completed on the A100 at batch size 4 with 2,582.1 seconds total wall time, 1,265.4 seconds training wall time, 1,314.7 seconds validation wall time, 19.42 training samples per second, 18.69 validation samples per second, 8,020,934,144 bytes peak CUDA allocated, and 9,439,281,152 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 10 rather than the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_220525_8c0116` | ABI-171 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, centerline w0.01 | 8 | 0.3816 | 0.3703 | 0.4086 | 0.4101 | 0.3569 | 0.3473 | 0.00315 |
| `run_20260901_202820_08734b` | ABI-169 | full-scale skip ASPP/detail decoder, BCE-Dice-clDice, ABI-16+BTD+SZA | 12 | 0.3688 | 0.3645 | 0.3785 | 0.3878 | 0.3515 | 0.2813 | 0.00328 |
| `run_20260901_225502_53acd2` | ABI-172 | full-scale skip ASPP/detail decoder, focal-Tversky, ABI-16+BTD+SZA | 10 | 0.3578 | 0.3552 | 0.3631 | 0.3185 | 0.4081 | 0.2312 | 0.00464 |

ABI-172 answered the controlled focal-Tversky loss-swap hypothesis negatively. Relative to ABI-154, focal-Tversky did produce the intended recall-oriented shift: filtered recall rose from 0.3359 to 0.4081 (+0.0723) and filtered predicted-positive fraction rose from 0.00255 to 0.00464. However, the shift over-expanded predictions and degraded the branch's main strengths. Aggregate filtered Dice fell from 0.3944 to 0.3578 (-0.0366), MIT filtered Dice fell from 0.3824 to 0.3552 (-0.0272), Google filtered Dice fell from 0.4260 to 0.3631 (-0.0629), filtered precision fell from 0.4777 to 0.3185 (-0.1592), and filtered connectivity fell from 0.4374 to 0.2312 (-0.2062).

Relative to ABI-130 and ABI-068, ABI-172 remained well below the stronger capped references on aggregate/source Dice, precision, and connectivity. Its recall exceeded ABI-130 and ABI-068, but the gain did not translate into better overlap. Relative to ABI-171, ABI-172 recovered more recall but was lower on aggregate/source Dice, precision, and connectivity. Relative to ABI-169, ABI-172 recovered more recall but further weakened precision, connectivity, and aggregate/source Dice. This is consistent with the earlier ABI-145 SZA-aware ASPP/detail focal-Tversky result: focal-Tversky tends to expand positive area in this SZA-aware ASPP/detail lineage, but the extra positives are not sufficiently precise or connected at the active threshold.

## ABI-172 trajectory

ABI-172 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1520, 0.2008, 0.2559, 0.2275, 0.3029, 0.2746, 0.2761, 0.3437, 0.3384, 0.3578, 0.3173, and 0.3496. The selected checkpoint was epoch 10. The trajectory showed useful learning and a late partial recovery, but it was noisy and did not approach the parent or reference aggregate-Dice band.

At the best epoch, raw Dice was 0.3688, filtered Dice was 0.3578, filtered precision was 0.3185, filtered recall was 0.4081, filtered connectivity was 0.2312, and filtered predicted-positive fraction was 0.00464. Source-stratified filtered Dice was 0.3552 for MIT and 0.3631 for Google. MIT had filtered precision 0.3456, recall 0.3652, connectivity 0.2553, and Google had filtered precision 0.2752, recall 0.5337, connectivity 0.2071. The Google recall was high but paired with especially low precision, explaining much of the Google Dice loss versus ABI-154 and ABI-130.

The final epoch moved to a slightly more conservative but less connected operating point: final filtered Dice was 0.3496, MIT/Google filtered Dice was 0.3510/0.3468, filtered precision was 0.3464, filtered recall was 0.3528, filtered connectivity was 0.1447, and filtered predicted-positive fraction was 0.00369. This late drop in connectivity and source balance reinforces that the focal-Tversky branch did not find a stable, connected recall recovery.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3688 versus filtered Dice 0.3578, raw recall was 0.4359 versus filtered recall 0.4081, and raw predicted-positive fraction was 0.00494 versus filtered 0.00464. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples all have near-zero per-sample Dice under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-172 as a completed, finite, non-collapsed, scientifically negative controlled loss-swap result for the full-scale skip ASPP/detail decoder branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result shows that trusted focal-Tversky loss can recover default-threshold recall for ABI-154, but only by sacrificing too much precision and line connectivity. The full-scale skip architecture's BCE-Dice calibration appears to be responsible for its strong precision/connectivity profile; replacing the primary loss with focal-Tversky breaks that balance more severely than lowering the Centerline Target auxiliary weight or switching to clDice. Together, ABI-169, ABI-171, and ABI-172 narrow the local ABI-154 branch: simple loss-only or centerline-weight-only swaps do not improve the full-scale skip ASPP/detail trade-off.

This result does not eliminate focal-Tversky globally. ABI-068 remains the stronger focal-Tversky reference in a different architecture family, and focal-Tversky may still be useful when paired with architectures that constrain false positives and maintain connected line structure. It does argue against further unchanged focal-Tversky retuning on the SZA-aware full-scale skip ASPP/detail branch at learning rate 0.0003 and Centerline Target weight 0.02.

## Decision

Do not promote ABI-172 and do not request whole-validation diagnostics for it. Stop the exact full-scale skip ASPP/detail focal-Tversky loss-swap branch. No Capability Request or Campaign Report is required from this result.

For a later Autonomy Step, broaden away from simple ABI-154 local manifest-only tuning. Reasonable next frontiers include a distinct calibration mechanism that preserves ABI-154-like precision/connectivity while recovering recall, a data-policy or threshold-diagnostic-driven Evaluation Request for an already strong run, or a new architecture family with explicit high-resolution thin-line representation and false-positive control rather than another local loss swap.

## Artifact references

- `run_20260901_225502_53acd2/outputs/best_metrics.json`
- `run_20260901_225502_53acd2/outputs/final_metrics.json`
- `run_20260901_225502_53acd2/outputs/metrics.jsonl`
- `run_20260901_225502_53acd2/outputs/resource_profile.json`
- `run_20260901_225502_53acd2/outputs/model_summary.json`
- `run_20260901_225502_53acd2/outputs/prediction_samples/samples.json`
- `run_20260901_225502_53acd2/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260901_202820_08734b/outputs/best_metrics.json`
- `run_20260901_220525_8c0116/outputs/best_metrics.json`
