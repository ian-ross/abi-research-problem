# Full-spectral BTD frequency-gated line U-Net SZA follow-up

research-figures: []

## Scope

This note records ABI-076 after Run `run_20260828_080008_ce4819` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-070 centerline-guided residual-head comparison: `run_20260828_031118_326c4a`
- ABI-073 boundary-auxiliary comparison: `run_20260828_055812_4ba74e`
- ABI-076 frequency-gated line U-Net plus Solar Geometry Input: `run_20260828_080008_ce4819`

ABI-076 used provider-approved `abi_16ch_plus_sza` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted focal-Tversky primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-076 implementation and resource observation

ABI-076 started from ABI-068's frequency-gated line U-Net backbone and changed the input-policy axis from `abi_16ch` to `abi_16ch_plus_sza`. The model normalized the first 16 ABI channels, derived the same thermal BTD planes from approved ABI channels only, added normalized Solar Geometry Input features, and retained the high/low spatial-frequency stem, gated skip fusion, dilated bottleneck context, frequency-pyramid fusion, oriented high-frequency line refiner, primary `mask_logits` head, and `centerline_logits` auxiliary head.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights. The trusted model summary recorded `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18, while forbidden longitude/latitude source channel indices 16 and 17 remained excluded.

Model summary reported 12,087,841 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,708.8 seconds wall time, 9,556,721,664 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_031118_326c4a` | ABI-070 | ABI-068 plus centerline-guided residual head | 12 | 0.3807 | 0.3644 | 0.4210 | 0.4158 | 0.3512 | 0.4064 | 0.00306 |
| `run_20260828_055812_4ba74e` | ABI-073 | ABI-068 plus boundary aux weight 0.01 | 10 | 0.3778 | 0.3631 | 0.4131 | 0.3983 | 0.3594 | 0.3620 | 0.00327 |
| `run_20260828_080008_ce4819` | ABI-076 | ABI-068 plus provider-approved SZA input | 12 | 0.3790 | 0.3718 | 0.3962 | 0.3463 | 0.4184 | 0.3013 | 0.00438 |

ABI-076 did not match ABI-068's aggregate capped best-validation score. Relative to ABI-068, aggregate filtered Dice fell by about -0.0174, MIT filtered Dice by about -0.0168, Google filtered Dice by about -0.0199, filtered precision by about -0.0529, and filtered connectivity by about -0.0887. Filtered recall improved by about +0.0248 and the filtered predicted-positive fraction rose from 0.00357 to 0.00438, indicating a recall-forward, more positive operating point rather than the hoped-for precision or clutter-control gain from Solar Geometry Input.

Relative to ABI-066, ABI-076 essentially tied aggregate filtered Dice within -0.0036 and improved filtered recall by about +0.0817, but it lost materially on filtered precision (-0.0964), filtered connectivity (-0.1718), and Google filtered Dice (-0.0330). Relative to ABI-070 and ABI-073, ABI-076 is near-tied on aggregate filtered Dice while being the strongest recall point and the weakest precision/connectivity point among these local focal-Tversky frequency-gated variants.

## ABI-076 trajectory

ABI-076 trained finitely and avoided all-negative/all-positive prediction collapse. Filtered Dice by epoch was 0.1791, 0.2366, 0.2957, 0.2874, 0.3330, 0.2757, 0.3419, 0.3200, 0.3523, 0.3685, 0.3198, and 0.3790 at epoch 12. The best checkpoint was the final epoch, so the branch was still learning under the capped 12-epoch budget, but the middle trajectory was noisy and did not overcome the ABI-068 reference.

At the best checkpoint, both Dataset Sources remained non-catastrophic: MIT filtered Dice was 0.3718 and Google filtered Dice was 0.3962. The source balance was acceptable, but the Google score was lower than ABI-068, ABI-066, ABI-070, and ABI-073. The operating profile was clearly recall-forward: filtered recall reached 0.4184 while filtered precision fell to 0.3463 and connectivity to 0.3013. The four fixed retained prediction artifacts had near-zero sample Dice and are not representative qualitative evidence; aggregate/source-stratified validation metrics and trajectory are the useful evidence for this note.

## Interpretation

ABI-076 is finite, contract-compliant, and resource-safe, but it is neutral-to-negative evidence for the simple Solar Geometry Input continuation of ABI-068. The allowed SZA channel did move the model toward higher recall, but it did not recover false-positive control, precision, source stability, or connectivity. This does not eliminate Solar Geometry Input as a general feature, but it argues against repeating this exact SZA-only change on the same frequency-gated focal-Tversky backbone under the current capped policy.

ABI-068 remains the strongest local frequency-gated reference by capped aggregate filtered Dice and has whole-validation diagnostics showing filtered Dice 0.3951 on the canonical 3,088-sample Working Validation Split. ABI-066 remains the precision/connectivity-forward reference. Canonical MCAST 2.1 remains promotion context; none of these capped local results should be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-076 and do not request whole-validation diagnostics for this exact Run unless a later question specifically targets SZA-conditioned failure modes. Retain the result as evidence that adding provider-approved Solar Geometry Input to ABI-068 mainly increases recall and predicted-positive area while reducing precision/connectivity and Google-source strength.

The next useful research step should broaden away from simple SZA-only input expansion and from additional suppressive head stacking on ABI-068. In-contract alternatives include a different low-cost thin-line context module, a non-suppressive multi-orientation feature extractor that avoids the ABI-072 clutter profile, or a training-policy/loss/input combination that deliberately targets ABI-068's precision/connectivity loss while preserving its recall and source balance. Any such next step should continue to preserve provider/Harness ownership of data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle.

## Artifact references

- `run_20260828_080008_ce4819/outputs/best_metrics.json`
- `run_20260828_080008_ce4819/outputs/final_metrics.json`
- `run_20260828_080008_ce4819/outputs/metrics.jsonl`
- `run_20260828_080008_ce4819/outputs/resource_profile.json`
- `run_20260828_080008_ce4819/outputs/model_summary.json`
- `run_20260828_080008_ce4819/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_031118_326c4a/outputs/best_metrics.json`
- `run_20260828_055812_4ba74e/outputs/best_metrics.json`
