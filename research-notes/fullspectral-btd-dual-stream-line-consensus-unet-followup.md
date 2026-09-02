# Full-spectral BTD dual-stream line-consensus U-Net follow-up

research-figures: []

## Scope

This note records ABI-104 after Run `run_20260830_083020_16590b` completed.

Source Runs:

- ABI-104 dual-stream line-consensus U-Net continuation: `run_20260830_083020_16590b`
- ABI-103 dual-stream spectral-gate line U-Net scout: `run_20260830_074456_5e0e5c`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-097 negative-bias frequency-gated focal-Tversky reference: `run_20260830_030927_4f7d3d`
- ABI-100 deterministic-shuffle clDice reference: `run_20260830_055047_fb5c2f`
- ABI-102 ultra-stable ConvNeXt U-Net repair reference: `run_20260830_070308_aeffc6`

ABI-104 was a family-development continuation of ABI-103. It kept ABI-103's in-contract spectral specialization over provider-approved reflective ABI channels, thermal ABI channels, and ABI-channel-derived thermal BTD planes, but strengthened the final full-resolution decoder with consensus-gated high-resolution detail, smoothed context, horizontal/vertical line branches, and a broad dilated branch. The intended repair was to retain ABI-103's recall while improving precision and Contrail Connectivity Metric without moving thresholding, postprocessing, Artifact Filters, losses, metrics, target derivation, sampling, augmentation, data loading, resource placement, or lifecycle logic into candidate code.

The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, provider-approved `abi_16ch` input, trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant LR, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. This is capped family-development evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-104 stayed inside the Candidate Experiment Contract. Candidate code owned only architecture over provider-approved ABI tensors plus deterministic BTD features derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`outputs/model_summary.json` reported 10,829,276 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,521.2 seconds total wall time, 1,194.1 seconds training wall time, 1,325.0 seconds validation wall time, 10,429,136,896 bytes peak CUDA reserved, and no terminal execution failure. ABI-104 was therefore resource-feasible under the current capped sequential policy.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_030927_4f7d3d` | ABI-097 | ABI-068 branch, negative logit bias | 12 | 0.3737 | 0.3737 | 0.3737 | 0.3231 | 0.4431 | 0.2614 | 0.00497 |
| `run_20260830_055047_fb5c2f` | ABI-100 | deterministic-shuffle clDice follow-up | 10 | 0.3674 | 0.3508 | 0.4089 | 0.4321 | 0.3195 | 0.4411 | 0.00268 |
| `run_20260830_074456_5e0e5c` | ABI-103 | dual-stream spectral-gate line U-Net scout | 12 | 0.3305 | 0.3248 | 0.3427 | 0.2715 | 0.4225 | 0.1742 | 0.00564 |
| `run_20260830_083020_16590b` | ABI-104 | ABI-103 branch, consensus-gated line decoder | 9 | 0.3220 | 0.3140 | 0.3389 | 0.2739 | 0.3904 | 0.1733 | 0.00516 |
| `run_20260830_070308_aeffc6` | ABI-102 | ultra-stable ConvNeXt U-Net repair | 10 | 0.1952 | 0.2033 | 0.1796 | 0.1482 | 0.2860 | 0.0976 | 0.00699 |

ABI-104 did not repair ABI-103's failure mode. Relative to ABI-103, aggregate filtered Dice decreased by about 0.0086, MIT filtered Dice decreased by about 0.0108, Google filtered Dice decreased by about 0.0038, recall decreased by about 0.0320, and connectivity was essentially unchanged. Filtered precision improved only trivially, from 0.2715 to 0.2739, while filtered predicted-positive fraction decreased from 0.00564 to 0.00516. The lower positive area therefore appears to be mostly a recall tradeoff rather than useful clutter suppression.

Relative to ABI-068, ABI-104 remained lower by about 0.0744 aggregate filtered Dice, 0.0746 MIT filtered Dice, 0.0772 Google filtered Dice, 0.1252 precision, and 0.2167 connectivity. Its recall was roughly matched to ABI-068, but without ABI-068's precision/connectivity. Relative to ABI-066, ABI-104 was lower by about 0.0606 aggregate filtered Dice, 0.1688 precision, and 0.2998 connectivity, while recall was higher by about 0.0537. This keeps ABI-104 in a recall-preserving but low-connectivity regime rather than producing a distinctive precision or line-continuity advantage.

## ABI-104 trajectory

ABI-104 trained finitely and avoided all-negative/all-positive aggregate collapse. Filtered Dice by epoch was 0.1038, 0.1491, 0.1671, 0.1887, 0.2517, 0.2532, 0.2469, 0.2999, 0.3220, 0.2866, 0.2358, and 0.3143. The selected checkpoint was epoch 9, not the final epoch; after a mid-run peak the model regressed at epochs 10-11 and only partially recovered at epoch 12. Training loss declined from 0.9566 at epoch 1 to 0.8655 at epoch 12, but the validation trajectory does not show ABI-103's final-epoch-best late-improvement pattern.

At the selected checkpoint, filtered Dice was 0.3220, filtered precision 0.2739, filtered recall 0.3904, filtered connectivity 0.1733, and filtered predicted-positive fraction 0.00516. Source-stratified metrics were MIT filtered Dice 0.3140 and Google filtered Dice 0.3389. Both sources stayed above the exact branch's hard-stop floor, but neither improved over ABI-103 or approached the stronger frequency-gated references.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3301 versus filtered Dice 0.3220, and raw predicted-positive fraction 0.00551 versus filtered 0.00516. The result is not primarily a provider-owned Artifact Filter dependence problem. The fixed first-four retained prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-104 as finite, resource-feasible, non-collapsed, but negative capped family-development evidence for the exact dual-stream line-consensus decoder continuation. It missed the proposal's useful-continuation criteria: it did not improve ABI-103 aggregate filtered Dice by 0.025, did not improve precision by 0.04 or connectivity by 0.08, did not reach within 0.03 filtered Dice of ABI-068, and did not show a late-improving trajectory with a meaningful metric gain. The only intended-direction movement was lower predicted-positive fraction, but it came with reduced recall and no useful Dice/connectivity gain.

The outcome suggests that adding a stronger full-resolution consensus gate to the current dual-stream spectral-specialization design is insufficient to solve the branch's low-precision, low-connectivity operating point. The spectral separation idea remains finite and above catastrophic floors, so one run does not invalidate all future spectral specialization. However, ABI-103 plus ABI-104 now provide two bounded observations that this dual-stream decoder lineage is not competitive with the frequency-gated line U-Net references under the current trusted focal-Tversky, centerline auxiliary, random-mirroring, combined source-balanced, constant-LR budget.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-104 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-104. Do not request whole-validation diagnostics for this exact checkpoint ahead of ABI-068/066-style references. Do not continue the ABI-103/104 dual-stream spectral-specialization branch with another small decoder-gate tweak unless the next hypothesis is materially different and specifically addresses the persistent low-connectivity and low-precision failure mode.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. A future useful hypothesis should broaden the frontier beyond this exact dual-stream consensus decoder, while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_083020_16590b/outputs/best_metrics.json`
- `run_20260830_083020_16590b/outputs/final_metrics.json`
- `run_20260830_083020_16590b/outputs/metrics.jsonl`
- `run_20260830_083020_16590b/outputs/resource_profile.json`
- `run_20260830_083020_16590b/outputs/model_summary.json`
- `run_20260830_083020_16590b/outputs/prediction_samples/samples.json`
- `run_20260830_074456_5e0e5c/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/best_metrics.json`
- `run_20260830_055047_fb5c2f/outputs/best_metrics.json`
- `run_20260830_070308_aeffc6/outputs/best_metrics.json`
