# Full-spectral BTD frequency-gated line U-Net deterministic-shuffle follow-up

research-figures: []

## Scope

This note records ABI-096 after Run `run_20260830_021504_c112f8` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-085 frequency-gated line U-Net low-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-091 frequency-gated line U-Net low-learning-rate clDice reference: `run_20260829_231700_96b245`
- ABI-096 deterministic-shuffle data-policy continuation: `run_20260830_021504_c112f8`

ABI-096 preserved the ABI-068 full-spectral BTD frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal brightness-temperature-difference features, trusted `focal_tversky` primary loss, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change was manifest-selected trusted sampling policy: `deterministic_shuffle` instead of ABI-068's `combined_source_balanced` traversal. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped data-policy/family-development evidence rather than full-data promotion evidence.

## ABI-096 implementation and resource observation

ABI-096 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed provider-approved ABI channels 1-16 only, with forbidden longitude/latitude source channels excluded. The Run completed at batch size 4 on the A100 with 2,692.3 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior matched the recent ABI-068/085 frequency-gated envelope and remained within the current 3,600-second Docker training timeout.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, combined source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, combined source-balanced | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, lower learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_231700_96b245` | ABI-091 | ABI-066 loss branch, lower learning rate 0.0001 | 12 | 0.3679 | 0.3613 | 0.3835 | 0.3872 | 0.3505 | 0.3085 | 0.00328 |
| `run_20260830_021504_c112f8` | ABI-096 | ABI-068 branch, `deterministic_shuffle` sampling | 10 | 0.3628 | 0.3472 | 0.4024 | 0.4242 | 0.3169 | 0.4195 | 0.00271 |

ABI-096 produced the intended lower-positive-area, higher-precision shift relative to ABI-068, but the tradeoff was too expensive. Relative to ABI-068, filtered predicted-positive fraction fell from 0.00357 to 0.00271, filtered precision improved by about +0.0250, and filtered connectivity improved by about +0.0295. However, aggregate filtered Dice fell by about -0.0336, MIT filtered Dice by about -0.0414, Google filtered Dice by about -0.0137, and filtered recall by about -0.0767.

Relative to ABI-066, ABI-096 did not recover the precision/connectivity-forward reference. It was lower on aggregate filtered Dice (-0.0197), MIT filtered Dice (-0.0166), Google filtered Dice (-0.0268), precision (-0.0186), recall (-0.0198), and connectivity (-0.0536). Its filtered predicted-positive fraction was slightly lower than ABI-066, but that came with lower recall and no aggregate-Dice advantage. Relative to ABI-085, ABI-096 was a cleaner but substantially lower-recall operating point; relative to ABI-091, it was slightly lower in aggregate Dice but higher in Google Dice, precision, and connectivity.

## ABI-096 trajectory

ABI-096 trained finitely and avoided terminal all-negative/all-positive collapse, but its validation trajectory was oscillatory. Filtered Dice by epoch was 0.1798, 0.2928, 0.2933, 0.2873, 0.3089, 0.1383, 0.3620, 0.3457, 0.3541, 0.3628, 0.3146, and 0.3188. The selected checkpoint was epoch 10, not the final epoch.

The best checkpoint represented the intended conservative operating profile: filtered precision 0.4242, filtered recall 0.3169, filtered connectivity 0.4195, filtered predicted-positive fraction 0.00271, MIT filtered Dice 0.3472, and Google filtered Dice 0.4024. The final checkpoint shifted back toward a recall-heavy, positive-area-expanded profile: filtered precision 0.2332, recall 0.5038, connectivity 0.1640, filtered predicted-positive fraction 0.00783, MIT filtered Dice 0.3310, and Google filtered Dice 0.2948. That late degradation argues against treating deterministic shuffle as a stabilizing replacement for combined source-balanced traversal under the current 12-epoch constant-LR budget.

The retained fixed first-four prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-096 as finite, resource-feasible, non-collapsed, and diagnostically informative but negative capped family-development evidence for the exact deterministic-shuffle data-policy branch. It partially validated the mechanism that less aggressive source/positive balancing can reduce predicted-positive burden and raise precision/connectivity, but it failed the proposal's useful-continuation criteria because aggregate filtered Dice was not within 0.015 of ABI-068, it did not come within 0.01 of ABI-066 while improving recall, and MIT filtered Dice slipped just below the 0.35 source-balanced target.

The result suggests ABI-068's remaining clutter is not solved by simply switching traversal to `deterministic_shuffle`. The source-balanced policy appears important for preserving recall and MIT-source performance, while deterministic shuffle produces an unstable precision/recall tradeoff that peaks briefly and then deteriorates. This does not eliminate the frequency-gated line U-Net family; ABI-068 remains the strongest local whole-validation-tested aggregate-Dice reference, and ABI-066 remains the precision/connectivity-forward reference.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-096 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-096. Do not repeat the exact ABI-068 architecture plus `focal_tversky` plus centerline auxiliary branch with `deterministic_shuffle` unchanged. Retain `combined_source_balanced` as the preferred sampling traversal for the ABI-068 frequency-gated branch unless a materially different trusted data-policy hypothesis is introduced.

Do not request a whole-validation failure-bucket diagnostic for ABI-096 ahead of ABI-068/066. The run did show a lower-positive-area precision/connectivity shift, but the capped aggregate and source-stratified losses are too large to justify scarce diagnostic priority. A useful next hypothesis should broaden beyond another small sampling-policy tweak, for example by testing a materially different architecture family or a trusted policy axis that can target false-positive clutter without sacrificing the ABI-068 recall/source-balance profile. Candidate code should continue to leave thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

## Artifact references

- `run_20260830_021504_c112f8/outputs/best_metrics.json`
- `run_20260830_021504_c112f8/outputs/final_metrics.json`
- `run_20260830_021504_c112f8/outputs/metrics.jsonl`
- `run_20260830_021504_c112f8/outputs/resource_profile.json`
- `run_20260830_021504_c112f8/outputs/model_summary.json`
- `run_20260830_021504_c112f8/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_231700_96b245/outputs/best_metrics.json`
