# Full-spectral BTD+SZA ASPP/detail decoder deterministic-shuffle BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-135 after Run `run_20260831_162753_adfc95` completed.

Source Runs:

- ABI-135 SZA-aware ASPP/detail decoder deterministic-shuffle BCE-Dice Centerline-auxiliary continuation: `run_20260831_162753_adfc95`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-131, ABI-132, and ABI-133 SZA-aware ASPP/detail head/auxiliary negative comparators: `run_20260831_130730_08040a`, `run_20260831_135752_1ac18c`, and `run_20260831_144720_475594`
- ABI-134 SZA-aware frequency-gated line U-Net BCE-Dice comparator: `run_20260831_153303_7701f1`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`

ABI-135 was a controlled data-policy continuation of ABI-130. It kept ABI-130's provider-approved `abi_16ch_plus_sza` input, deterministic raw ABI plus thermal BTD plus Solar Geometry front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest-only change was `data.sampling_policy: deterministic_shuffle` instead of ABI-130's `combined_source_balanced` traversal.

## Contract and resource observation

ABI-135 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, deterministic-shuffle implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,620,010 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,229.0 seconds total wall time, 992.2 seconds training wall time, 1,234.7 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, combined source-balanced | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_153303_7701f1` | ABI-134 | frequency-gated line U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3866 | 0.3714 | 0.4238 | 0.4033 | 0.3712 | 0.3279 | 0.00334 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_130730_08040a` | ABI-131 | ABI-130 plus continuity bridge | 12 | 0.3880 | 0.3720 | 0.4279 | 0.4235 | 0.3581 | 0.2703 | 0.00306 |
| `run_20260831_135752_1ac18c` | ABI-132 | ABI-130 plus region-line agreement head | 12 | 0.3853 | 0.3730 | 0.4163 | 0.4394 | 0.3431 | 0.2971 | 0.00283 |
| `run_20260831_144720_475594` | ABI-133 | ABI-130 plus Line+Centerline auxiliary targets | 12 | 0.3879 | 0.3727 | 0.4254 | 0.4269 | 0.3554 | 0.3390 | 0.00302 |
| `run_20260831_162753_adfc95` | ABI-135 | ABI-130 architecture with deterministic-shuffle traversal | 12 | 0.3758 | 0.3703 | 0.3880 | 0.3394 | 0.4209 | 0.2174 | 0.00449 |

ABI-135 did not meet the controlled deterministic-shuffle hypothesis relative to ABI-130. Aggregate filtered Dice fell from 0.3953 to 0.3758 (-0.0195), Google filtered Dice fell from 0.4404 to 0.3880 (-0.0524), filtered precision fell from 0.4415 to 0.3394 (-0.1020), and filtered connectivity fell from 0.3851 to 0.2174 (-0.1677). MIT filtered Dice was only slightly lower, 0.3703 versus 0.3779, and filtered recall increased from 0.3578 to 0.4209, but that recall gain came with a much higher filtered predicted-positive fraction, 0.00449 versus 0.00294.

The result is therefore not a useful ABI-130 extension. Deterministic shuffle pushed the branch toward a recall-heavy, low-precision operating point and especially damaged Google performance, the main strength of ABI-130. It also underperformed ABI-131/ABI-133 on aggregate filtered Dice, underperformed ABI-126/ABI-066 on precision and connectivity, and underperformed ABI-068 on aggregate Dice, MIT Dice, Google Dice, precision, connectivity, and positive-area discipline. ABI-135's only clear comparative strength is higher recall, but that was not the requested trade-off and was accompanied by excessive positive area and low connectivity.

## ABI-135 trajectory

ABI-135 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2007, 0.2272, 0.2791, 0.2912, 0.3349, 0.3581, 0.3206, 0.3709, 0.3468, 0.3249, 0.3560, and 0.3758. The selected checkpoint was the final epoch 12, so the Run did show late improvement rather than a strict plateau or divergence.

The trajectory was highly oscillatory across precision/recall regimes. Epoch 10 reached high filtered precision and connectivity (0.5603 precision, 0.4870 connectivity) but low recall (0.2288) and lower Dice (0.3249). Epoch 12 recovered recall strongly (0.4209) and selected Dice, but connectivity collapsed to 0.2174 and precision fell to 0.3394. Epoch 8 already had a similar recall-heavy point, with 0.3709 filtered Dice, 0.3354 precision, 0.4149 recall, and 0.2182 connectivity. This suggests deterministic shuffle changed or destabilized the branch's calibration cadence rather than simply improving source integration.

At the selected checkpoint, source-stratified filtered Dice was 0.3703 for MIT and 0.3880 for Google. MIT had filtered precision 0.3577, recall 0.3839, connectivity 0.2556, and predicted-positive fraction 0.00580. Google had filtered precision 0.3063, recall 0.5292, connectivity 0.1792, and predicted-positive fraction 0.00319. Both Dataset Sources remained finite and non-collapsed, but the Google precision/connectivity collapse is a strong negative signal for this data-policy branch.

Raw-to-filtered differences were modest: raw Dice was 0.3875 versus filtered Dice 0.3758, and raw predicted-positive fraction was 0.00479 versus filtered 0.00449. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples all had near-zero per-sample Dice, but the retention policy is `first_n`, so those bounded samples are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-135 as a completed, finite, non-collapsed, but negative data-policy result for this exact SZA-aware ASPP/detail deterministic-shuffle branch. It is not a candidate bug, contract violation, resource failure, or Harness failure. The controlled manifest-only traversal change answered the training-policy question: replacing combined source-balanced traversal with deterministic shuffle did not stabilize or improve ABI-130, and it converted the branch into a high-recall, low-precision, low-connectivity operating point with a large Google regression.

This strengthens the case that ABI-130's useful SZA-aware calibration depends on the combined source-balanced traversal under the current capped representative budget. It also supports the prior ABI-131/132/133 interpretation that simple head, auxiliary, or now traversal changes around ABI-130 are not currently recovering the desired precision/connectivity balance. ABI-130 remains the SZA-aware ASPP/detail reference with whole-validation diagnostic support. ABI-068 remains the local capped aggregate-Dice/source-balance reference, ABI-066 remains the high-connectivity reference, and ABI-126 remains the ASPP/detail high-precision/connectivity comparator.

## Decision

Do not promote ABI-135. Do not request whole-validation diagnostics for ABI-135 from this capped result, because it failed the controlled comparison against ABI-130 and did not establish a distinctive useful operating point beyond recall-heavy positive-area expansion. Do not repeat the exact deterministic-shuffle SZA-aware ASPP/detail BCE-Dice Centerline-auxiliary branch unchanged.

Retain `combined_source_balanced` as the stronger traversal for ABI-130-like SZA-aware ASPP/detail work under the current policy. A reasonable later Autonomy Step should broaden away from simple ASPP/detail SZA head/auxiliary/traversal tweaks, either toward a distinct compact architecture/preprocessing frontier or toward an in-contract calibration idea that directly targets false positives and connectivity without candidate-owned thresholding, postprocessing, Artifact Filters, or data handling.

No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260831_162753_adfc95/outputs/best_metrics.json`
- `run_20260831_162753_adfc95/outputs/final_metrics.json`
- `run_20260831_162753_adfc95/outputs/metrics.jsonl`
- `run_20260831_162753_adfc95/outputs/resource_profile.json`
- `run_20260831_162753_adfc95/outputs/model_summary.json`
- `run_20260831_162753_adfc95/outputs/prediction_samples/samples.json`
- `run_20260831_162753_adfc95/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_130730_08040a/outputs/best_metrics.json`
- `run_20260831_135752_1ac18c/outputs/best_metrics.json`
- `run_20260831_144720_475594/outputs/best_metrics.json`
- `run_20260831_153303_7701f1/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
