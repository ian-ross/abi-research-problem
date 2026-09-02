# Thermal BTD signed-detail full-scale skip ASPP decoder follow-up

research-figures: []

## Scope

This note records ABI-178 after Run `run_20260902_044555_a3f915` completed.

Source Runs:

- ABI-178 thermal-only BTD signed-detail full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary continuation: `run_20260902_044555_a3f915`
- ABI-173 signed-detail full-scale skip ASPP decoder parent and whole-validation-tested SZA-aware ASPP/detail aggregate branch: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 prior SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`
- ABI-177 recurrent line-refinement ASPP decoder immediate predecessor: `run_20260902_035240_71e96b`

ABI-178 was a family-development continuation on the input/preprocessing frontier. It kept the signed-detail ASPP decoder pattern, compact residual encoder, full-scale skip aggregation, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled change was provider-approved `abi_thermal_10ch` input: only GOES ABI channels 7-16 were exposed, then normalized thermal channels, deterministic thermal BTD planes, learned thermal mixtures, and patch-local signed thermal anomaly features were used. Reflective channels, Solar Geometry Input, longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights were not candidate inputs.

## Contract and resource observation

ABI-178 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_thermal_10ch`, channel set `goes_abi_channels_7_16`, approved GOES ABI channel numbers 7-16 with source channel indices 6-15, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,865,338 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,804.7 seconds total wall time, 1,460.8 seconds training wall time, 1,341.9 seconds validation wall time, 16.82 training samples per second, 18.31 validation samples per second, 9,142,251,008 bytes peak CUDA allocated, and 10,659,823,616 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 11; final epoch 12 was slightly lower on the primary selection metric.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_044555_a3f915` | ABI-178 | thermal-only signed-detail full-scale skip ASPP decoder, BCE-Dice, thermal ABI+BTD | 11 | 0.3818 | 0.3713 | 0.4060 | 0.3906 | 0.3733 | 0.2851 | 0.00346 |
| `run_20260902_035240_71e96b` | ABI-177 | recurrent line-refinement ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 8 | 0.3739 | 0.3518 | 0.4302 | 0.4064 | 0.3463 | 0.3820 | 0.00309 |

ABI-178 is finite and non-degenerate, but scientifically negative for the thermal-only signed-detail hypothesis. Relative to ABI-173, it reduced aggregate filtered Dice from 0.3962 to 0.3818 (-0.0144), MIT filtered Dice from 0.3838 to 0.3713 (-0.0125), Google filtered Dice from 0.4269 to 0.4060 (-0.0209), precision from 0.4238 to 0.3906 (-0.0331), and connectivity from 0.3203 to 0.2851 (-0.0352). Recall was essentially unchanged at 0.3733 versus 0.3720, but this came with a higher filtered predicted-positive fraction than ABI-173 (0.00346 versus 0.00318), so the thermal-only change did not deliver the intended false-positive discipline.

Relative to ABI-154, ABI-178 had higher recall (0.3733 versus 0.3359), but lower aggregate filtered Dice (-0.0126), MIT filtered Dice (-0.0111), Google filtered Dice (-0.0200), precision (-0.0870), connectivity (-0.1524), and predicted-positive discipline. Relative to ABI-130 and ABI-068 it also remained below the aggregate/source-balance band and did not recover their connectivity. Compared with ABI-177, ABI-178 improved aggregate filtered Dice (+0.0079), MIT filtered Dice (+0.0195), and recall (+0.0271), but lost Google filtered Dice (-0.0242), precision (-0.0158), connectivity (-0.0969), and positive-area discipline. This makes ABI-178 a different but not better tradeoff.

## ABI-178 trajectory

ABI-178 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1949, 0.2774, 0.2895, 0.3299, 0.3484, 0.3610, 0.3552, 0.3622, 0.3774, 0.3626, 0.3818, and 0.3801. The best checkpoint occurred at epoch 11, with final epoch 12 only slightly lower on filtered Dice but substantially different in calibration.

Training loss declined from 0.9884 to 0.8530, and validation loss declined from 0.9536 to a low of 0.8821 at epoch 11 before a small rise at epoch 12. The epoch path shows optimization progress rather than execution failure, but it oscillated between recall-forward and precision/connectivity-forward regimes late in training. Epoch 11 selected a recall-forward balance: filtered Dice 0.3818, precision 0.3906, recall 0.3733, connectivity 0.2851, and filtered predicted-positive fraction 0.00346. Epoch 12 had higher precision 0.4537 and connectivity 0.3764 with lower positive fraction 0.00261, but recall fell to 0.3270 and filtered Dice fell to 0.3801. Neither operating point reaches the ABI-173 aggregate/source band or ABI-154 precision/connectivity band.

At the selected checkpoint, raw Dice was 0.3955 versus filtered Dice 0.3818, raw recall was 0.3992 versus filtered recall 0.3733, and raw predicted-positive fraction was 0.00369 versus filtered 0.00346. This raw-to-filtered gap is modest and does not indicate primary Artifact Filter dependence. Source behavior was source-informative but weaker than the references: Google filtered Dice was 0.4060 with recall 0.4715 and precision 0.3565, while MIT filtered Dice was 0.3713 with recall 0.3398 and precision 0.4092. The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-178 as a completed, finite, non-collapsed capped family-development result, but not a successful thermal-only input/preprocessing continuation. The removal of reflective channels and Solar Geometry Input did not improve the suspected negative-patch clutter/precision/connectivity weakness of ABI-173. Instead, the selected checkpoint preserved recall while losing precision, connectivity, and both source-stratified Dice values. The final checkpoint suggested thermal-only features can move toward cleaner positive-area and connectivity, but only by sacrificing recall and without reaching ABI-154's cleaner SZA-aware operating point.

The result suggests that reflective/SZA cues were not the main cause of ABI-173's false-positive and connectivity limitations, at least for this signed-detail ASPP decoder. Thermal-only BTD/anomaly evidence is sufficient for finite non-degenerate learning, but it appears weaker for the current aggregate/source tradeoff than the SZA-aware full-spectral branch. Because ABI-178 cleanly answered the proposal's input-frontier question and lost both ABI-173-like aggregate performance and ABI-154-like precision/connectivity, additional thermal-only signed-detail ASPP runs are a low-priority next use of the capped budget unless future diagnostics reveal a specific thermal-only failure mode to repair.

## Decision

Do not promote ABI-178, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-178 from this capped result alone. Stop this exact thermal-only signed-detail ASPP branch under the proposal's negative-outcome criterion: it completed finitely and non-degenerately, but it did not improve false-positive discipline, connectivity, MIT Dice, source balance, or aggregate filtered Dice relative to ABI-173/154 and did not produce a better tradeoff than ABI-068/130.

Retain ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware ASPP/detail precision/connectivity branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the broader aggregate/source-balance comparator. A reasonable next hypothesis should broaden away from thermal-only signed-detail ASPP toward a more distinct in-contract architecture, data-policy, calibration, preprocessing, or evaluation frontier rather than another local patch to this branch. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_044555_a3f915/outputs/best_metrics.json`
- `run_20260902_044555_a3f915/outputs/final_metrics.json`
- `run_20260902_044555_a3f915/outputs/metrics.jsonl`
- `run_20260902_044555_a3f915/outputs/resource_profile.json`
- `run_20260902_044555_a3f915/outputs/model_summary.json`
- `run_20260902_044555_a3f915/outputs/prediction_samples/samples.json`
- `run_20260902_044555_a3f915/outputs/validation_postprocessing/epoch_011.json`
- `run_20260902_044555_a3f915/resolved_manifest.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260902_035240_71e96b/outputs/best_metrics.json`
