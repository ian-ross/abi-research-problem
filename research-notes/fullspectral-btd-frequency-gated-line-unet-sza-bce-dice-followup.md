# Full-spectral BTD+SZA frequency-gated line U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-134 after Run `run_20260831_153303_7701f1` completed.

Source Runs:

- ABI-134 SZA-aware frequency-gated line U-Net BCE-Dice Centerline-auxiliary continuation: `run_20260831_153303_7701f1`
- ABI-076 same SZA-aware frequency-gated architecture with trusted focal-Tversky: `run_20260828_080008_ce4819`
- ABI-078 non-SZA frequency-gated architecture with trusted BCE-Dice: `run_20260828_094949_ad2af0`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-130 ASPP/detail decoder BTD+SZA BCE-Dice whole-validation-tested calibration reference: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`

ABI-134 was a controlled family-development continuation of ABI-076 and ABI-078. It kept ABI-076's provider-approved `abi_16ch_plus_sza` input and frequency-gated full-spectral BTD line U-Net architecture, retained provider-derived Centerline Target auxiliary supervision at trusted `weighted_bce` weight 0.02, and changed the trusted primary loss to `bce_dice`. It used combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. This is capped family-development evidence rather than full-data promotion evidence.

## Contract and resource observation

ABI-134 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. The model used deterministic thermal brightness-temperature-difference planes derived from approved ABI channels and normalized SZA/`cos(SZA)` features. It did not receive longitude, latitude, reconstructed coordinates, Dataset Source identity, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem persistence, network access, pretrained weights, or lifecycle behavior.

`outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude/latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. It reported 12,087,841 parameters, below the 25,000,000-parameter smoke ceiling.

The Run completed on the A100 at batch size 4 with 2,705.2 seconds total wall time, 1,317.3 seconds training wall time, 1,385.7 seconds validation wall time, 8,146,627,072 bytes peak CUDA allocated, 9,556,721,664 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_080008_ce4819` | ABI-076 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD+SZA | 12 | 0.3790 | 0.3718 | 0.3962 | 0.3463 | 0.4184 | 0.3013 | 0.00438 |
| `run_20260828_094949_ad2af0` | ABI-078 | frequency-gated line U-Net, BCE-Dice, ABI-16+BTD | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260831_153303_7701f1` | ABI-134 | frequency-gated line U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3866 | 0.3714 | 0.4238 | 0.4033 | 0.3712 | 0.3279 | 0.00334 |

ABI-134 mostly met the controlled factorial hypothesis relative to ABI-076. Switching the SZA-aware frequency-gated branch from focal-Tversky to BCE-Dice improved aggregate filtered Dice by +0.0076, filtered precision by +0.0570, filtered connectivity by +0.0266, Google filtered Dice by +0.0276, and reduced filtered predicted-positive fraction by -0.00104. The expected cost also appeared: filtered recall fell by -0.0472 and MIT filtered Dice was effectively tied/slightly lower by -0.0004. This confirms that the cleaner BCE-Dice loss can temper the overly permissive SZA focal-Tversky operating point.

Relative to ABI-078, ABI-134 also provides useful but mixed evidence for Solar Geometry Input under BCE-Dice. Aggregate filtered Dice improved by +0.0050, filtered recall by +0.0122, filtered connectivity by +0.0218, and MIT filtered Dice by about +0.0010 versus ABI-078's selected best checkpoint. Precision was slightly lower (-0.0039), predicted-positive fraction was slightly higher (+0.00014), and Google filtered Dice was lower than ABI-078's final epoch but above ABI-078's selected epoch-11 Google Dice. Thus, SZA helped the BCE-Dice frequency-gated branch recover some recall and connectivity without reverting to ABI-076's excessive positive-area burden, but it did not produce an ABI-130-level clean SZA calibration result.

ABI-134 remains below the strongest current aggregate references. Compared with ABI-068, it is lower on aggregate filtered Dice (-0.0098), MIT filtered Dice (-0.0172), recall (-0.0224), connectivity (-0.0621), and Google Dice is slightly higher (+0.0077). Compared with ABI-130, it is lower on aggregate filtered Dice (-0.0087), precision (-0.0382), connectivity (-0.0572), and Google Dice (-0.0166), while improving recall (+0.0134) with a higher predicted-positive fraction (+0.00040). ABI-066 remains much stronger on connectivity and precision/positive-area discipline.

## ABI-134 trajectory

ABI-134 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2445, 0.2992, 0.3240, 0.3468, 0.3479, 0.3277, 0.3749, 0.3790, 0.3787, 0.3749, 0.3837, and 0.3866. The selected checkpoint was the final epoch 12, so the branch retained a late improvement signal rather than showing clear divergence or early collapse.

At the selected checkpoint, raw Dice was 0.4002 and filtered Dice was 0.3866. Filtered precision was 0.4033, filtered recall 0.3712, filtered connectivity 0.3279, and filtered predicted-positive fraction 0.00334. Source-stratified filtered Dice was 0.3714 for MIT and 0.4238 for Google. MIT had filtered precision 0.4095, recall 0.3398, connectivity 0.3424, and predicted-positive fraction 0.00448; Google had filtered precision 0.3907, recall 0.4630, connectivity 0.3134, and predicted-positive fraction 0.00219. Both Dataset Sources remained finite and non-collapsed, but the Google-recall/MIT-under-recall split persists.

The late trajectory improved steadily after the epoch-6 dip, but the final score did not catch ABI-068 or ABI-130. The operating point is intermediate: less recall-heavy and less positive than ABI-076, more recall-capable than ABI-078's selected checkpoint, but neither as aggregate-strong/source-balanced as ABI-068 nor as cleanly SZA-calibrated as ABI-130. Raw-to-filtered differences were modest: raw Dice 0.4002 versus filtered Dice 0.3866, and raw predicted-positive fraction 0.00356 versus filtered 0.00334. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-134 as a completed, finite, non-collapsed, contract-compliant, mixed-positive factorial result for the SZA plus BCE-Dice frequency-gated branch. It validates the narrow hypothesis that BCE-Dice tempers the permissive SZA focal-Tversky behavior seen in ABI-076, and it improves the non-SZA BCE-Dice branch ABI-078 on aggregate Dice, recall, and connectivity at the selected checkpoint. The result is not a candidate bug, contract violation, resource failure, or Harness failure.

The evidence is not strong enough to make ABI-134 an active best branch. The branch does not surpass ABI-068 on capped aggregate Dice, recall, MIT strength, or connectivity. It also does not match ABI-130's whole-validation-supported SZA-aware ASPP/detail balance of aggregate Dice, precision, Google performance, and moderate connectivity. ABI-134 should therefore be retained as controlled evidence about the SZA/loss interaction within the frequency-gated line U-Net family, not as a promotion candidate or as a reason to repeat this exact combination.

The most useful scientific lesson is that Solar Geometry Input and BCE-Dice interact differently by architecture family. In the frequency-gated line U-Net, SZA+BCE-Dice lands between ABI-076's recall-heavy profile and ABI-078's conservative profile. In the ASPP/detail decoder, ABI-130 showed stronger aggregate and whole-validation behavior with the same broad input/loss axis. This suggests that further progress should not simply stack more heads onto the frequency-gated SZA branch; it should either exploit the ASPP/detail SZA calibration path with a carefully controlled non-suppressive continuity/calibration idea or broaden to a distinct architecture/preprocessing/training-policy frontier.

## Decision

Do not promote ABI-134 and do not request whole-validation diagnostics for this Run from the current capped result. It is source-informative and non-degenerate, but it does not improve enough over ABI-068 or ABI-130 to justify a diagnostic slot, and the narrow ABI-076/ABI-078 factorial question is answered at the capped-evidence level.

Do not repeat the exact SZA-aware frequency-gated BCE-Dice Centerline-auxiliary combination unchanged. Retain ABI-134 as evidence that BCE-Dice can moderate SZA-induced positive-area expansion in the frequency-gated family, but prioritize ABI-130 as the stronger SZA-aware default-threshold calibration reference and ABI-068/ABI-066 as the aggregate and connectivity references. A reasonable next step is a new controlled Candidate in a later Autonomy Step that broadens away from simple SZA/loss combinations: for example, a conservative SZA-aware calibration/continuity variant rooted in the ASPP/detail branch, or a distinct compact architecture/preprocessing scout that targets negative-patch clutter and connectivity without candidate-owned thresholding or Artifact Filters.

No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260831_153303_7701f1/outputs/best_metrics.json`
- `run_20260831_153303_7701f1/outputs/final_metrics.json`
- `run_20260831_153303_7701f1/outputs/metrics.jsonl`
- `run_20260831_153303_7701f1/outputs/resource_profile.json`
- `run_20260831_153303_7701f1/outputs/model_summary.json`
- `run_20260831_153303_7701f1/outputs/prediction_samples/samples.json`
- `run_20260831_153303_7701f1/resolved_manifest.yaml`
- `run_20260828_080008_ce4819/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
