# Full-spectral BTD+SZA ASPP/detail decoder MIT-only BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-140 after Run `run_20260831_201630_7359a3` completed.

Source Runs:

- ABI-140 ASPP/detail decoder BTD+SZA MIT-only BCE-Dice centerline-auxiliary data-policy continuation: `run_20260831_201630_7359a3`
- ABI-130 ASPP/detail decoder BTD+SZA BCE-Dice centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice centerline-auxiliary high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-115 frequency-gated line U-Net MIT-only data-policy reference: `run_20260830_235533_487b1c`

ABI-140 was a controlled data-policy continuation of ABI-130. It kept the same compact full-spectral BTD+SZA ASPP/detail architecture, provider-approved `abi_16ch_plus_sza` input, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended controlled change was only `data.sampling_policy: mit_only` instead of ABI-130's `combined_source_balanced` traversal.

## Contract and resource observation

ABI-140 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, Solar Geometry Input source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,620,010 parameters, below the 25,000,000-parameter smoke ceiling and matching ABI-130's model scale. The Run completed on the A100 at batch size 4 with 2,214.6 seconds total wall time, 991.4 seconds training wall time, 1,221.3 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 11; final epoch 12 had lower filtered Dice.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input/data policy | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD, source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, source-balanced | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD, source-balanced | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260830_235533_487b1c` | ABI-115 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD, MIT-only | 9 | 0.3515 | 0.3588 | 0.3345 | 0.3085 | 0.4084 | 0.2795 | 0.00480 |
| `run_20260831_201630_7359a3` | ABI-140 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, MIT-only | 11 | 0.3752 | 0.3728 | 0.3811 | 0.3821 | 0.3685 | 0.4049 | 0.00349 |

ABI-140 did not meet the preregistered useful-evidence criteria. Relative to ABI-130, aggregate filtered Dice decreased from 0.3953 to 0.3752 (-0.0201), just outside the planned within-0.02 tolerance. MIT filtered Dice also decreased from 0.3779 to 0.3728 (-0.0051). MIT filtered recall improved from 0.3313 to 0.3493 (+0.0180), but that gain was well below the requested about +0.04 MIT-recall improvement and did not convert into better MIT Dice. Google filtered Dice decreased materially from 0.4404 to 0.3811 (-0.0592), below the preregistered 0.40 transfer floor. Aggregate precision decreased from 0.4415 to 0.3821 (-0.0593), while aggregate recall increased modestly from 0.3578 to 0.3685 (+0.0107).

There were two partial positives. ABI-140 kept filtered predicted-positive fraction controlled at 0.00349, below the preregistered 0.0045 ceiling and still below the recall-heavy MIT-only frequency-gated ABI-115 value of 0.00480. It also reached filtered connectivity 0.4049, slightly above ABI-130's 0.3851 and ABI-068's 0.3900, though still below ABI-126's high-connectivity 0.4517. These partial positives were not enough to offset the aggregate-Dice, precision, and Google-transfer losses.

## ABI-140 trajectory

ABI-140 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2093, 0.2417, 0.2425, 0.3157, 0.3163, 0.3510, 0.3389, 0.3471, 0.3631, 0.3548, 0.3752, and 0.3539. The selected best checkpoint was epoch 11, not the final epoch.

At the selected checkpoint, raw Dice was 0.3886 and filtered Dice was 0.3752. Filtered precision was 0.3821, filtered recall 0.3685, filtered connectivity 0.4049, and filtered predicted-positive fraction 0.00349. Source-stratified filtered Dice was 0.3728 for MIT and 0.3811 for Google. MIT had filtered precision 0.3997, recall 0.3493, connectivity 0.4342, and predicted-positive fraction 0.00472. Google had filtered precision 0.3457, recall 0.4247, connectivity 0.3756, and predicted-positive fraction 0.00227. Both Dataset Sources were finite and non-collapsed, but the Google precision/Dice loss is the clearest transfer cost.

The final epoch shifted toward a larger positive-area, lower-precision operating point: filtered Dice dropped to 0.3539, precision to 0.3104, and connectivity to 0.2081, while recall increased to 0.4116 and filtered predicted-positive fraction rose to 0.00480. This mirrors the broader risk seen in ABI-115: MIT-only traversal can encourage recall expansion that does not improve the main Dice/source-transfer objective under the current capped 12-epoch constant-LR budget.

Raw-to-filtered differences at the best checkpoint were modest: raw Dice 0.3886 versus filtered Dice 0.3752, and raw predicted-positive fraction 0.00373 versus filtered 0.00349. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are all near-zero-Dice `first_n` traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-140 as a completed, finite, resource-feasible, non-collapsed, but negative capped data-policy result for the exact ABI-130 plus `mit_only` branch. The run answers the intended question: simple MIT-only traversal did not recover ABI-130's MIT operating point enough to justify the Google transfer and precision cost. It slightly increased MIT recall and connectivity, but did not improve MIT Dice, aggregate Dice, or source robustness.

Together with ABI-115, this makes simple MIT-only traversal lower priority for both the frequency-gated focal-Tversky branch and the ASPP/detail SZA+BCE branch. `combined_source_balanced` remains the better default for promotion-oriented capped experiments because it preserved stronger aggregate Dice, Google transfer, and precision while remaining finite and source-balanced.

This is capped representative evidence only, not full-data promotion evidence. Canonical MCAST 2.1 and the full 3,088-sample Working Validation Split remain the promotion context.

## Decision

Do not promote ABI-140. Do not repeat the exact ABI-130 architecture/loss/input with `mit_only` sampling unchanged. Do not request whole-validation diagnostics for ABI-140 ahead of ABI-130, ABI-126, ABI-068, or ABI-066 because ABI-140 did not become locally competitive and mainly confirms the source-transfer risk of the simple MIT-only traversal.

Retain ABI-068 as the capped aggregate-Dice reference, ABI-130 as the strongest SZA-aware ASPP/detail capped branch, ABI-126 as the ASPP/detail high-precision/connectivity comparator, and ABI-066 as the high-connectivity reference. A later Autonomy Step should broaden away from simple source-traversal swaps toward a different in-contract mechanism for source-robust calibration or thin-line continuity, while leaving thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

No new Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_201630_7359a3/outputs/best_metrics.json`
- `run_20260831_201630_7359a3/outputs/final_metrics.json`
- `run_20260831_201630_7359a3/outputs/metrics.jsonl`
- `run_20260831_201630_7359a3/outputs/resource_profile.json`
- `run_20260831_201630_7359a3/outputs/model_summary.json`
- `run_20260831_201630_7359a3/outputs/prediction_samples/samples.json`
- `run_20260831_201630_7359a3/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260830_235533_487b1c/outputs/best_metrics.json`
