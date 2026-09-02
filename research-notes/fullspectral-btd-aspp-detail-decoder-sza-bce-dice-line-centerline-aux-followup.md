# Full-spectral BTD+SZA ASPP/detail decoder BCE-Dice Line+Centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-133 after Run `run_20260831_144720_475594` completed.

Source Runs:

- ABI-133 SZA-aware ASPP/detail decoder BCE-Dice Line+Centerline auxiliary continuation: `run_20260831_144720_475594`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-131 and ABI-132 SZA-aware ASPP/detail head-geometry negative comparators: `run_20260831_130730_08040a` and `run_20260831_135752_1ac18c`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-127 non-SZA ASPP/detail decoder Line+Centerline auxiliary comparator: `run_20260831_094013_5ba974`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`

ABI-133 was a family-development continuation of ABI-130. It kept the provider-approved `abi_16ch_plus_sza` input, normalized raw ABI plus deterministic thermal BTD plus Solar Geometry Input front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was adding provider-derived Line Target auxiliary supervision at trusted `weighted_bce` weight 0.02 beside the existing Centerline Target auxiliary head at weight 0.02.

## Contract and resource observation

ABI-133 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, forbidden longitude and latitude source channels excluded, primary `mask_logits`, and provider-derived auxiliary outputs `centerline_logits` and `line_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,620,051 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,264.5 seconds total wall time, 997.4 seconds training wall time, 1,265.2 seconds validation wall time, 5,915,935,744 bytes peak CUDA allocated, 6,471,811,072 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_130730_08040a` | ABI-131 | ABI-130 plus continuity bridge | 12 | 0.3880 | 0.3720 | 0.4279 | 0.4235 | 0.3581 | 0.2703 | 0.00306 |
| `run_20260831_144720_475594` | ABI-133 | ABI-130 plus Line+Centerline auxiliary targets | 12 | 0.3879 | 0.3727 | 0.4254 | 0.4269 | 0.3554 | 0.3390 | 0.00302 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_135752_1ac18c` | ABI-132 | ABI-130 plus region-line agreement head | 12 | 0.3853 | 0.3730 | 0.4163 | 0.4394 | 0.3431 | 0.2971 | 0.00283 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_094013_5ba974` | ABI-127 | ABI-126 plus Line+Centerline aux, non-SZA | 9 | 0.3797 | 0.3653 | 0.4150 | 0.4280 | 0.3412 | 0.3054 | 0.00289 |

ABI-133 did not meet the controlled auxiliary-target hypothesis relative to ABI-130. Aggregate filtered Dice fell from 0.3953 to 0.3879 (-0.0074), MIT filtered Dice from 0.3779 to 0.3727 (-0.0052), Google filtered Dice from 0.4404 to 0.4254 (-0.0150), filtered precision from 0.4415 to 0.4269 (-0.0146), filtered recall from 0.3578 to 0.3554 (-0.0025), and filtered connectivity from 0.3851 to 0.3390 (-0.0461). Filtered predicted-positive fraction increased slightly from 0.00294 to 0.00302. The added Line Target head therefore neither recovered connectivity nor improved negative-patch/positive-area discipline while preserving ABI-130-level overlap.

The result is not a pure collapse or implementation failure. ABI-133 remained above ABI-126 on aggregate filtered Dice (+0.0020), MIT filtered Dice (+0.0092), and recall (+0.0303), but it lost the precision/connectivity signature that made ABI-126 distinctive: precision fell by 0.0477 and connectivity by 0.1127. Relative to ABI-127, the same Line+Centerline auxiliary idea did better after adding SZA and the ABI-130 front end on aggregate Dice, MIT/Google Dice, recall, and connectivity, but precision was essentially tied/lower and still did not recover the ABI-130 or ABI-126 connectivity range. Relative to ABI-131 and ABI-132, ABI-133 is an intermediate SZA-aware negative: better than ABI-132 on aggregate Dice, Google Dice, recall, and connectivity, and better than ABI-131 on connectivity, but still below ABI-130 on the metrics the proposal targeted.

## ABI-133 trajectory

ABI-133 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2069, 0.2832, 0.3142, 0.3030, 0.3497, 0.3313, 0.3644, 0.3379, 0.3448, 0.3509, 0.3748, and 0.3879. The selected checkpoint was the final epoch 12, so the Run retained a late improvement signal rather than showing a clean early plateau.

The late improvement was not enough to justify extending this exact branch. Epoch 7 briefly reached higher filtered connectivity (0.3974) and precision (0.4388), but with lower recall (0.3116) and lower Dice (0.3644). Epoch 12 recovered Dice and recall, but connectivity settled at 0.3390, below ABI-130, ABI-126, ABI-066, and ABI-068. Source-stratified filtered Dice at epoch 12 was 0.3727 for MIT and 0.4254 for Google, confirming finite signal on both Dataset Sources but no ABI-130-relative source improvement.

Raw-to-filtered differences were modest: raw Dice was 0.4019 versus filtered Dice 0.3879, and raw predicted-positive fraction was 0.00322 versus filtered 0.00302. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-133 as a completed, finite, non-collapsed, but negative family-development result for this exact SZA-aware ASPP/detail Line+Centerline auxiliary variant. It is not a candidate bug, contract violation, resource failure, or Harness failure. The controlled added Line Target supervision preserved trainability and source-informative predictions, but failed the proposal's useful-result criterion because it reduced aggregate Dice, source Dice, precision, and connectivity relative to ABI-130 while slightly increasing predicted-positive area.

Together with ABI-131 and ABI-132, this argues against further simple SZA-aware ASPP/detail head or auxiliary tweaks whose only goal is to recover ABI-130's lost connectivity. ABI-130 remains the better SZA-aware ASPP/detail reference because it has stronger capped aggregate Dice and a completed whole-validation diagnostic confirming the capped SZA calibration pattern. ABI-126 remains the ASPP/detail high-precision/connectivity comparator, ABI-066 remains the high-connectivity line-family comparator, and ABI-068 remains the local capped aggregate-Dice reference.

This does not eliminate Solar Geometry Input, ASPP/detail architectures, or auxiliary targets broadly. It only stops the exact ABI-133 branch: low-weight Line Target supervision added to ABI-130's SZA-aware BCE-Dice Centerline-auxiliary branch did not improve the targeted diagnostics under the current capped budget.

## Decision

Do not promote ABI-133. Do not request whole-validation diagnostics for ABI-133 from this capped result, because it failed to improve ABI-130 on the intended capped metrics and did not establish a stronger precision/connectivity operating point. Do not repeat the exact ABI-133 auxiliary-target combination unchanged.

A reasonable next Autonomy Step is to broaden away from simple SZA-aware ASPP/detail head/auxiliary modifications. In-contract alternatives include returning to a stronger line-aware family with a calibration/data-policy hypothesis, testing a distinct preprocessing or deterministic-feature front end, or exploring a different compact architecture family that improves false-positive discipline without sacrificing ABI-068/ABI-130-level recall and source balance.

## Artifact references

- `run_20260831_144720_475594/outputs/best_metrics.json`
- `run_20260831_144720_475594/outputs/final_metrics.json`
- `run_20260831_144720_475594/outputs/metrics.jsonl`
- `run_20260831_144720_475594/outputs/resource_profile.json`
- `run_20260831_144720_475594/outputs/model_summary.json`
- `run_20260831_144720_475594/outputs/prediction_samples/samples.json`
- `run_20260831_144720_475594/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_130730_08040a/outputs/best_metrics.json`
- `run_20260831_135752_1ac18c/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_094013_5ba974/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
