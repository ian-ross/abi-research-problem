# Full-spectral BTD+SZA recurrent line-refinement ASPP decoder follow-up

research-figures: []

## Scope

This note records ABI-177 after Run `run_20260902_035240_71e96b` completed.

Source Runs:

- ABI-177 recurrent line-refinement ASPP decoder BCE-Dice Centerline-auxiliary continuation: `run_20260902_035240_71e96b`
- ABI-173 signed-detail full-scale skip ASPP decoder parent and whole-validation-tested SZA-aware ASPP/detail aggregate branch: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-176 signed context-fusion ASPP decoder immediate negative predecessor: `run_20260902_025056_9e87d5`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-174 signed-detail line-consensus follow-up: `run_20260902_005632_5651ef`
- ABI-175 anti-aliased full-scale skip follow-up: `run_20260902_015941_3ebc45`
- ABI-130 prior SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`

ABI-177 was a family-development continuation intended to broaden beyond local signed-detail/full-scale fusion patches. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, compact residual encoder, ASPP context, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architecture change was a thermal-anchor support branch plus `RecurrentLineRefinement`, using three shared additive horizontal, vertical, diagonal/local, broad-context, and thermal-anchor feature updates before the mask and centerline heads.

## Contract and resource observation

ABI-177 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,434,466 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,647.9 seconds total wall time, 1,297.7 seconds training wall time, 1,348.1 seconds validation wall time, 18.94 training samples per second, 18.23 validation samples per second, 9,029,874,176 bytes peak CUDA allocated, and 10,869,538,816 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 8; final epoch 12 was lower on the primary selection metric.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_005632_5651ef` | ABI-174 | signed-detail line-consensus full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3929 | 0.3833 | 0.4178 | 0.4158 | 0.3724 | 0.3460 | 0.00325 |
| `run_20260902_025056_9e87d5` | ABI-176 | signed context-fusion ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3902 | 0.3739 | 0.4300 | 0.4377 | 0.3519 | 0.2866 | 0.00291 |
| `run_20260902_015941_3ebc45` | ABI-175 | anti-aliased full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3817 | 0.3687 | 0.4175 | 0.5035 | 0.3073 | 0.4929 | 0.00221 |
| `run_20260902_035240_71e96b` | ABI-177 | recurrent line-refinement ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 8 | 0.3739 | 0.3518 | 0.4302 | 0.4064 | 0.3463 | 0.3820 | 0.00309 |

ABI-177 is finite and non-degenerate, but scientifically negative for its stated recurrent refinement hypothesis. Relative to ABI-176, it improved selected-checkpoint connectivity from 0.2866 to 0.3820 (+0.0954) and very slightly improved Google filtered Dice from 0.4300 to 0.4302. However, it reduced aggregate filtered Dice from 0.3902 to 0.3739 (-0.0162), MIT filtered Dice from 0.3739 to 0.3518 (-0.0221), precision from 0.4377 to 0.4064 (-0.0313), and recall from 0.3519 to 0.3463 (-0.0057). The intended connectivity recovery came with a large aggregate/source-balance cost rather than a useful tradeoff.

Relative to ABI-173, ABI-177 reduced aggregate filtered Dice by 0.0223, MIT filtered Dice by 0.0320, precision by 0.0174, and recall by 0.0257, while improving connectivity by 0.0617 and Google Dice by 0.0033. It therefore did not approach the ABI-173 aggregate/source-balance operating point. Relative to ABI-154, ABI-177 had slightly higher recall (+0.0104) and Google Dice (+0.0042), but much lower precision (-0.0713), MIT Dice (-0.0306), aggregate Dice (-0.0205), and connectivity (-0.0555). Relative to ABI-068 and ABI-130 it remained clearly below on aggregate and MIT Dice, with only Google Dice competitive.

## ABI-177 trajectory

ABI-177 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.0679, 0.2217, 0.2441, 0.3008, 0.3239, 0.3040, 0.3309, 0.3739, 0.3270, 0.3592, 0.3686, and 0.3559. The best checkpoint occurred at epoch 8, after which the trajectory oscillated and did not recover the primary selection metric.

The epoch path shows optimization progress rather than execution failure: training loss declined from 1.0656 to 0.8618, and validation loss was lowest at epoch 11 before rising slightly at epoch 12. The recurrent branch shifted between recall-forward and conservative high-precision regimes late in training. Epoch 8 was the best overlap tradeoff with filtered Dice 0.3739, precision 0.4064, recall 0.3463, connectivity 0.3820, and filtered predicted-positive fraction 0.00309. Epoch 12 had higher precision 0.4785 and higher connectivity 0.3972, but recall fell to 0.2833 and filtered Dice fell to 0.3559.

At the selected checkpoint, raw Dice was 0.3861 versus filtered Dice 0.3739, raw recall was 0.3685 versus filtered recall 0.3463, and raw predicted-positive fraction was 0.00329 versus filtered 0.00309. This raw-to-filtered gap is modest and does not indicate primary Artifact Filter dependence. Source behavior was unbalanced: Google filtered Dice reached 0.4302 with recall 0.4421, while MIT filtered Dice was only 0.3518 with recall 0.3135. The fixed first-four retained prediction samples all had near-zero per-sample Dice under the `first_n` retention policy; these are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-177 as a completed, finite, non-collapsed capped family-development result, but not a successful recurrent line-refinement continuation. The recurrent additive updates achieved one intended effect: connectivity recovered relative to ABI-173/174/176 and approached ABI-068/130 levels at the selected checkpoint. The recovery was not enough to offset weaker MIT performance, lower precision than the cleaner SZA-aware branches, and lower recall than ABI-173/174.

This suggests that recurrent line propagation can encourage connected structures, but in this implementation it does not reliably align those structures with labeled Contrail Mask pixels across both Dataset Sources. The late-epoch movement toward high precision and low recall also resembles a calibration/area-selection instability rather than a clear path to aggregate improvement. Because ABI-177 broadened away from signed-detail fusion yet landed below the main capped reference band, additional local recurrent refinements are a lower-priority next use of the capped budget unless future whole-validation diagnostics on a stronger run identify a specific fixable connectivity failure that this mechanism addresses.

## Decision

Do not promote ABI-177, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-177 from this capped result alone. Stop this exact recurrent line-refinement branch under the proposal's negative-outcome criterion: it completed finitely and improved connectivity versus ABI-176, but it did not preserve aggregate Dice, MIT Dice, recall, or a useful precision/recall/connectivity balance relative to ABI-173 or the broader ABI-068/130/154 references.

Retain ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware ASPP/detail precision/connectivity branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the broader aggregate/source-balance comparator. A reasonable next hypothesis should broaden beyond signed-detail/full-scale and recurrent-line ASPP patches toward a more distinct in-contract architecture, data-policy, preprocessing, calibration, or evaluation frontier. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_035240_71e96b/outputs/best_metrics.json`
- `run_20260902_035240_71e96b/outputs/final_metrics.json`
- `run_20260902_035240_71e96b/outputs/metrics.jsonl`
- `run_20260902_035240_71e96b/outputs/resource_profile.json`
- `run_20260902_035240_71e96b/outputs/model_summary.json`
- `run_20260902_035240_71e96b/outputs/prediction_samples/samples.json`
- `run_20260902_035240_71e96b/outputs/validation_postprocessing/epoch_008.json`
- `run_20260902_035240_71e96b/resolved_manifest.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_025056_9e87d5/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260902_005632_5651ef/outputs/best_metrics.json`
- `run_20260902_015941_3ebc45/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
