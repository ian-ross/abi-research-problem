# Full-spectral BTD ASPP/detail decoder clDice centerline-auxiliary scout

research-figures: []

## Scope

This note records ABI-120 after Run `run_20260831_033037_bad0bb` completed.

Source Runs:

- ABI-120 ASPP/detail decoder clDice centerline-auxiliary scout: `run_20260831_033037_bad0bb`
- ABI-052 DeepLabV3+ BTD clDice centerline-auxiliary comparison target: `run_20260827_131644_b76d09`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-119 recent context-pyramid agreement negative scout context: `run_20260831_025229_09ef74`

ABI-120 was a family-scout Candidate for a compact torch-only ASPP/detail encoder-decoder using full-spectral normalized ABI channels, deterministic thermal BTD planes derived only from GOES ABI channels 1-16, a learned spectral projection, high-resolution detail/context fusion, an ASPP bottleneck, and a line-aware refinement block. It kept trusted `bce_dice_cldice` primary loss plus a provider-derived Centerline Target auxiliary head at `weighted_bce` weight 0.02. This is capped representative feasibility evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-120 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved `abi_16ch` ABI Channel Input and deterministic BTD combinations derived from approved ABI channels. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice_cldice`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,619,514 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,313.6 seconds total wall time, 1,103.4 seconds training wall time, 1,208.3 seconds validation wall time, 5,984,592,384 bytes peak CUDA allocated, 6,643,777,536 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 10.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260827_131644_b76d09` | ABI-052 | DeepLabV3+ BTD, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.2214 | 0.2083 | 0.2542 | 0.2619 | 0.1918 | 0.3391 | 0.00265 |
| `run_20260831_025229_09ef74` | ABI-119 | context-pyramid agreement calibrator | 12 | 0.2869 | 0.2932 | 0.2748 | 0.2319 | 0.3761 | 0.1287 | 0.00588 |
| `run_20260831_033037_bad0bb` | ABI-120 | compact ASPP/detail decoder with clDice + centerline aux | 10 | 0.3667 | 0.3485 | 0.4078 | 0.4366 | 0.3161 | 0.3681 | 0.00262 |

ABI-120 strongly met the preregistered comparison against ABI-052. Relative to ABI-052, aggregate filtered Dice increased from 0.2214 to 0.3667 (+0.1453), MIT filtered Dice from 0.2083 to 0.3485 (+0.1402), Google filtered Dice from 0.2542 to 0.4078 (+0.1536), filtered precision from 0.2619 to 0.4366 (+0.1747), filtered recall from 0.1918 to 0.3161 (+0.1243), and filtered connectivity from 0.3391 to 0.3681 (+0.0290). The filtered predicted-positive fraction stayed disciplined at 0.00262, essentially tied with ABI-052's 0.00265 despite much higher Dice and recall.

Relative to ABI-068, ABI-120 did not set a new aggregate-Dice reference: filtered Dice was lower by 0.0296, MIT filtered Dice lower by 0.0401, Google filtered Dice lower by 0.0083, filtered recall lower by 0.0775, and filtered connectivity lower by 0.0219. It did improve precision by 0.0374 and used a smaller filtered predicted-positive fraction. Relative to ABI-066, ABI-120 was close on precision and positive-area discipline, but lower on aggregate Dice (-0.0158), MIT (-0.0153), Google (-0.0213), recall (-0.0206), and especially connectivity (-0.1050), so ABI-066 remains the stronger precision/connectivity reference.

Relative to ABI-119's context-pyramid branch, ABI-120 improved aggregate filtered Dice by 0.0798, MIT by 0.0553, Google by 0.1330, precision by 0.2047, connectivity by 0.2394, and positive-area discipline while losing recall by 0.0600. This suggests that ASPP/detail context is a much cleaner source-balanced architecture-scout axis than the context-pyramid agreement calibrator under the current capped policy.

## ABI-120 trajectory

ABI-120 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1763, 0.2875, 0.2440, 0.3269, 0.3194, 0.2860, 0.3523, 0.3256, 0.3645, 0.3667, 0.3490, and 0.3626. The selected checkpoint was epoch 10; the final epoch partially recovered after the epoch-11 dip but did not surpass the selected checkpoint.

At the selected checkpoint, raw Dice was 0.3810 and filtered Dice was 0.3667. Filtered precision was 0.4366, filtered recall 0.3161, filtered connectivity 0.3681, and filtered predicted-positive fraction 0.00262. Source-stratified filtered Dice was 0.3485 MIT and 0.4078 Google. Both Dataset Sources were finite and non-collapsed. The source profile was Google-strong and precision-forward: Google filtered recall reached 0.4242 at precision 0.3927, while MIT was more conservative at recall 0.2792 and precision 0.4635.

Raw-to-filtered differences were modest: raw Dice 0.3810 versus filtered Dice 0.3667, and raw predicted-positive fraction 0.00278 versus filtered 0.00262. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-120 as finite, resource-feasible, non-collapsed, and positive capped family-scout evidence for a compact ASPP/detail decoder compared with the DeepLabV3+ BTD clDice centerline-auxiliary target. It validates the hypothesis that architecture geometry, not merely auxiliary-head tuning, can recover a large fraction of the DeepLabV3+ BTD clDice family's source and recall weakness while preserving precision and positive-area discipline.

The result is still mixed against the mature frequency-gated line U-Net references. ABI-120 did not challenge ABI-068 on aggregate/source Dice or recall, and it did not challenge ABI-066 on connectivity. Its useful niche is a precision-forward, source-balanced clDice branch that is much stronger than ABI-052 and materially cleaner than ABI-119. The lower MIT recall and lower connectivity versus ABI-068/066 argue against promotion or immediate whole-validation diagnostics ahead of the stronger references.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-120 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-120 and do not request whole-validation diagnostics for ABI-120 ahead of ABI-068 or ABI-066. Retain ABI-068 as the local aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-120 as the strongest positive scout for a custom ASPP/detail decoder geometry under trusted `bce_dice_cldice` plus centerline-auxiliary supervision.

Continue the ASPP/detail family only through a controlled follow-up that targets the observed recall/connectivity gap without sacrificing its precision and positive-area discipline, for example a later focal-Tversky version of the same ASPP/detail decoder or a minimal ASPP/detail line-continuity refinement that leaves data loading, split logic, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, postprocessing, resource placement, and lifecycle under provider/Harness ownership. Do not repeat the exact ABI-120 configuration unchanged.

## Artifact references

- `run_20260831_033037_bad0bb/outputs/best_metrics.json`
- `run_20260831_033037_bad0bb/outputs/final_metrics.json`
- `run_20260831_033037_bad0bb/outputs/metrics.jsonl`
- `run_20260831_033037_bad0bb/outputs/resource_profile.json`
- `run_20260831_033037_bad0bb/outputs/model_summary.json`
- `run_20260831_033037_bad0bb/outputs/prediction_samples/samples.json`
- `run_20260831_033037_bad0bb/resolved_manifest.yaml`
- `run_20260827_131644_b76d09/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_025229_09ef74/outputs/best_metrics.json`
