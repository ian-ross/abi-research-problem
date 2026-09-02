# Full-spectral BTD+SZA UPerNet directional line-context follow-up

research-figures: []

## Scope

This note records ABI-180 after Run `run_20260902_063801_88ca01` completed.

Source Runs:

- ABI-180 full-spectral BTD+SZA UPerNet directional line-context BCE-Dice Line+Centerline auxiliary continuation: `run_20260902_063801_88ca01`
- ABI-179 UPerNet pyramid/detail parent scout: `run_20260902_054206_a6b406`
- ABI-173 signed-detail full-scale skip ASPP decoder SZA-aware aggregate reference: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 prior SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`

ABI-180 was a focused UPerNet-family continuation after ABI-179. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes, normalized/cosine Solar Geometry Input features, a learned 1x1 spectral projection, ABI-179's compact UPerNet-style pyramid/detail hierarchy, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, and disabled early stopping. The controlled changes were an additive directional line-context stage plus provider-derived Line Target auxiliary supervision at weight 0.01 alongside Centerline Target auxiliary supervision at weight 0.02.

## Contract and resource observation

ABI-180 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, channel set `goes_abi_channels_1_16_plus_solar_geometry_input`, approved GOES ABI channel numbers 1-16 plus Solar Geometry Input, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 7,603,107 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,987.1 seconds total wall time, 1,564.4 seconds training wall time, 1,420.7 seconds validation wall time, 15.71 training samples per second, 17.30 validation samples per second, 8,382,793,216 bytes peak CUDA allocated, and 10,326,376,448 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 12, matching the final epoch.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_054206_a6b406` | ABI-179 | UPerNet pyramid/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3939 | 0.3774 | 0.4354 | 0.4520 | 0.3490 | 0.2895 | 0.00280 |
| `run_20260902_063801_88ca01` | ABI-180 | UPerNet directional line-context, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3885 | 0.3738 | 0.4242 | 0.4304 | 0.3541 | 0.2943 | 0.00298 |

ABI-180 is finite, resource-safe, and non-degenerate, but it did not meet the main UPerNet-continuation goal. Relative to ABI-179, the directional line-context plus Line Target auxiliary change slightly improved filtered recall from 0.3490 to 0.3541 (+0.0051) and filtered connectivity from 0.2895 to 0.2943 (+0.0049). Those gains were too small to offset losses in aggregate filtered Dice from 0.3939 to 0.3885 (-0.0054), MIT filtered Dice from 0.3774 to 0.3738 (-0.0036), Google filtered Dice from 0.4354 to 0.4242 (-0.0113), precision from 0.4520 to 0.4304 (-0.0216), and positive-area discipline from 0.00280 to 0.00298.

Relative to ABI-173, ABI-180 reduced aggregate filtered Dice by 0.0077, MIT filtered Dice by 0.0100, Google filtered Dice by 0.0027, precision by 0.0066, recall by 0.0179, and connectivity by 0.0260. Relative to ABI-154, ABI-180 had higher recall (+0.0182) and Google filtered Dice was close (-0.0019), but it remained lower on aggregate Dice (-0.0059), MIT Dice (-0.0086), precision (-0.0473), connectivity (-0.1431), and positive-area discipline. Relative to ABI-130 and ABI-068, it was lower on aggregate/source Dice and connectivity and did not supply a compensating precision, recall, or source-transfer advantage.

## ABI-180 trajectory

Filtered Dice by epoch was 0.2231, 0.2604, 0.3055, 0.3189, 0.3575, 0.3495, 0.3729, 0.3856, 0.3653, 0.3756, 0.3384, and 0.3885. Training loss declined from 0.9778 at epoch 1 to 0.8460 at epoch 12; validation loss declined from 0.9498 to 0.8792. The selected epoch 12 checkpoint reached raw Dice 0.4035 and filtered Dice 0.3885, with raw recall 0.3785 versus filtered recall 0.3541 and raw predicted-positive fraction 0.00317 versus filtered predicted-positive fraction 0.00298. This raw-to-filtered gap is modest and does not indicate primary Artifact Filter dependence.

The trajectory was finite and recovered after an epoch-11 dip, but it did not show the clean late UPerNet improvement seen in ABI-179. ABI-180's best epoch remained the final epoch, yet it ended below ABI-179's epoch-12 aggregate/source operating point. The directional line-context mechanism may have nudged connectivity and recall upward, but the effect size was small and not enough to move the UPerNet branch toward ABI-068/130/154 connectivity behavior. MIT filtered Dice also remained weaker than the main capped references.

The fixed first-four retained prediction samples all had near-zero per-sample Dice under the `first_n` retention policy. These artifacts are useful traceability samples but should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-180 as a completed, finite, non-collapsed, scientifically mixed-to-negative UPerNet-family continuation. The intended direction of effect was barely visible in recall and connectivity, but the gains were too small to compensate for lower aggregate Dice, lower source-stratified Dice, lower precision, and continued connectivity weakness relative to the leading capped references.

This result argues against further local UPerNet/SZA-aware context-detail tweaks as the immediate next branch. ABI-179 already showed that the compact UPerNet hierarchy can reach the capped reference band with strong Google/precision behavior; ABI-180 shows that additive directional line context and extra low-weight Line Target supervision do not repair the branch's weak continuity/MIT signal. This is not a contract, resource, Harness, non-finite, or prediction-collapse failure, and it is not evidence that all context-pyramid ideas are exhausted. It is sufficient evidence to stop this exact UPerNet continuation line and broaden to a different in-contract architecture, data-policy, preprocessing, calibration, loss/auxiliary configuration, or evaluation frontier in a later Autonomy Step.

## Decision

Do not promote ABI-180, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-180 from this capped result alone. Retain ABI-068 as the current capped aggregate/source-balance comparator, ABI-173 as the strongest SZA-aware ASPP/detail aggregate branch with whole-validation diagnostics, ABI-154 as the SZA-aware precision/connectivity branch, ABI-130 as the prior SZA-aware aggregate reference, and ABI-179 as the efficient UPerNet scout reference.

A reasonable next hypothesis should broaden away from UPerNet/SZA-aware context-detail local patches toward a more distinct in-contract architecture, data policy, preprocessing/calibration mechanism, or targeted diagnostic request. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_063801_88ca01/outputs/best_metrics.json`
- `run_20260902_063801_88ca01/outputs/final_metrics.json`
- `run_20260902_063801_88ca01/outputs/metrics.jsonl`
- `run_20260902_063801_88ca01/outputs/resource_profile.json`
- `run_20260902_063801_88ca01/outputs/model_summary.json`
- `run_20260902_063801_88ca01/outputs/prediction_samples/samples.json`
- `run_20260902_063801_88ca01/outputs/validation_postprocessing/epoch_012.json`
- `run_20260902_063801_88ca01/resolved_manifest.yaml`
- `run_20260902_054206_a6b406/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
