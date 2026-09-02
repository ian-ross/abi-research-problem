# Full-spectral BTD wavelet-detail U-Net scout

research-figures: []

## Scope

This note records ABI-129 after Run `run_20260831_112408_9d8d5b` completed.

Source Runs:

- ABI-129 wavelet-detail U-Net scout: `run_20260831_112408_9d8d5b`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-121 ASPP/detail decoder focal-Tversky recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-126 ASPP/detail decoder BCE-Dice precision/connectivity and Google-Dice comparator: `run_20260831_085615_d05ab3`
- Earlier detail-heavy negative scouts discussed in history: ABI-079 nested-skip U-Net (`run_20260828_104353_1455f1`), ABI-084 multi-resolution line-HRNet (`run_20260829_171549_19184b`), and ABI-113 patch-anomaly line U-Net (`run_20260830_220436_b4eadb`).

ABI-129 was a family scout after the ABI-120 through ABI-128 ASPP/detail-decoder sequence. It used a compact wavelet-detail U-Net intended to preserve multiscale high-frequency thin-line evidence while using low-frequency context to gate decoder skips. It kept provider-approved `abi_16ch` input, deterministic raw-plus-thermal-BTD features derived only from GOES ABI channels 1-16, trusted `focal_tversky` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-129 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over approved ABI Channel Input and deterministic brightness-temperature-difference planes derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, Solar Geometry Input, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 15,319,436 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,236.2 seconds total wall time, 966.9 seconds training wall time, 1,267.0 seconds validation wall time, 6,855,228,416 bytes peak CUDA allocated, 8,155,824,128 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 8.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, centerline aux | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_112408_9d8d5b` | ABI-129 | wavelet-detail U-Net, focal-Tversky, centerline aux | 8 | 0.3676 | 0.3621 | 0.3804 | 0.3722 | 0.3631 | 0.3459 | 0.00353 |

ABI-129 completed finite and source-informative, but it did not meet the family-scout useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3676 (-0.0287), MIT filtered Dice from 0.3886 to 0.3621 (-0.0265), Google filtered Dice from 0.4161 to 0.3804 (-0.0357), filtered precision from 0.3992 to 0.3722 (-0.0269), filtered recall from 0.3936 to 0.3631 (-0.0305), and filtered connectivity from 0.3900 to 0.3459 (-0.0441). The filtered predicted-positive fraction, 0.00353, was close to ABI-068's 0.00357, so the branch did not fail by excessive positive area; it failed by losing both recall and precision enough to depress Dice.

Relative to ABI-066, ABI-129 had slightly lower MIT filtered Dice (-0.0017) but much lower Google filtered Dice (-0.0488), aggregate Dice (-0.0149), precision (-0.0705), and connectivity (-0.1272), with higher recall (+0.0264) and a larger positive fraction. It therefore did not recover ABI-066's precision/connectivity advantage. Relative to ABI-121, ABI-129 improved precision and connectivity and used a smaller positive fraction, but it lost aggregate Dice, both source Dice values, and recall. Relative to ABI-126, ABI-129 retained roughly the same MIT filtered Dice and higher recall, but was much lower on Google Dice, precision, and connectivity.

The scout is better calibrated than the worst detail-heavy alternatives ABI-079, ABI-084, and ABI-113. It avoided their very large positive fractions and very low connectivity, and it improved substantially on ABI-079/084 aggregate Dice. However, that secondary advantage is not enough to justify continuing this exact wavelet-detail branch, because it remains below the stronger frequency-gated and ASPP/detail references on the metrics that motivated the scout.

## ABI-129 trajectory

ABI-129 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1436, 0.2271, 0.2525, 0.3039, 0.3238, 0.2682, 0.3511, 0.3676, 0.2924, 0.3538, 0.3513, and 0.3648. The selected checkpoint was epoch 8. Epoch 9 regressed sharply, and epochs 10-12 recovered close to but below the epoch-8 best.

At the selected checkpoint, raw Dice was 0.3805 and filtered Dice was 0.3676. Filtered precision was 0.3722, filtered recall 0.3631, filtered connectivity 0.3459, and filtered predicted-positive fraction 0.00353. Source-stratified filtered Dice was 0.3621 for MIT and 0.3804 for Google. At final epoch 12, aggregate filtered Dice was 0.3648, filtered precision 0.3098, recall 0.4437, connectivity 0.1521, MIT filtered Dice 0.3719, and Google filtered Dice 0.3502. The late trajectory therefore drifted toward recall-heavy, low-connectivity behavior even though aggregate Dice nearly recovered.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3805 versus filtered Dice 0.3676, and raw predicted-positive fraction 0.00377 versus filtered 0.00353. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are available in `outputs/prediction_samples/samples.json`, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-129 as finite, resource-feasible, non-collapsed, and informative, but negative capped family-scout evidence for this exact wavelet-detail U-Net design. The wavelet-detail/context-gated skip idea avoided the extreme clutter profile of several previous detail-heavy scouts, but it did not produce the intended ABI-068-like MIT recall/source balance or a compensating precision/connectivity advantage. The best checkpoint was below ABI-068 by about 0.029 filtered Dice and below ABI-066/ABI-126 on the precision/connectivity metrics that remain important for thin contrail segmentation.

This result does not eliminate all wavelet, multiscale-detail, or high-frequency-preserving architectures. It does provide enough evidence to avoid repeating ABI-129 unchanged: the best checkpoint did not meet the approximate ABI-068 proximity target, and the final epochs showed degradation in precision/connectivity rather than a clean improving late trajectory. Canonical MCAST 2.1 remains full Working Validation Split promotion context. ABI-129 is capped representative evidence only and should not be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-129. Do not request whole-validation diagnostics for ABI-129 ahead of stronger capped references. Stop this exact compact wavelet-detail U-Net branch unless later implementation review identifies a narrow candidate bug that explains the epoch-9 regression and final precision/connectivity collapse.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance comparator, and ABI-126 as the ASPP/detail precision/connectivity and Google-Dice comparator. For the next in-contract step, prefer broadening rather than stacking another local detail-preservation variant: useful directions include a training/data-policy diagnostic around the stronger references, a different non-suppressive line-continuity architecture, or a calibration mechanism that improves MIT/source balance without inflating positive area or moving thresholding/postprocessing into Candidate code.

## Artifact references

- `run_20260831_112408_9d8d5b/outputs/best_metrics.json`
- `run_20260831_112408_9d8d5b/outputs/final_metrics.json`
- `run_20260831_112408_9d8d5b/outputs/metrics.jsonl`
- `run_20260831_112408_9d8d5b/outputs/resource_profile.json`
- `run_20260831_112408_9d8d5b/outputs/model_summary.json`
- `run_20260831_112408_9d8d5b/outputs/prediction_samples/samples.json`
- `run_20260831_112408_9d8d5b/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_104353_1455f1/outputs/best_metrics.json`
- `run_20260829_171549_19184b/outputs/best_metrics.json`
- `run_20260830_220436_b4eadb/outputs/best_metrics.json`
