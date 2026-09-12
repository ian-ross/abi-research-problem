# ABI-259 temporal-attention line-support decoder U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-259, Candidate `abi259_temporal_attention_line_support_decoder_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_012708_f5897e`.

ABI-259 was a temporal-attention family-development Candidate after ABI-223, ABI-255, and ABI-258. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 2, constant learning rate, and trusted Line/Centerline auxiliary outputs. The intended mechanism change was to keep ABI-223-style temporal-attention fusion while adding learned center-frame detail support and oriented line-support blocks inside the decoder, so connected contrail logits could be preserved before the final mask head rather than adjusted only by a final calibration head.

Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-259 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,709,876, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.66 / 5.17 GB.
- Training wall time: 1,376.4 s; validation wall time: 1,013.4 s; total Run wall time: 2,391.6 s.

This is valid finite/resource evidence for the temporal-attention line-support decoder on the capped temporal-eligible validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8.

| Metric | ABI-259 best epoch 8 | ABI-259 final epoch 12 | ABI-258 dual-evidence calibration | ABI-255 recurrent late36 | ABI-223 temporal-attn late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.381540 | 0.376367 | 0.388192 | 0.417348 | 0.419776 | 0.427570 |
| Raw Dice | 0.398247 | 0.392272 | 0.404756 | 0.435656 | 0.438487 | 0.442746 |
| Filtered precision | 0.438659 | 0.434484 | 0.422628 | 0.468293 | 0.483764 | 0.439467 |
| Filtered recall | 0.337582 | 0.331964 | 0.358944 | 0.376400 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.331613 | 0.287818 | 0.260347 | 0.281116 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.368471 | 0.355402 | 0.372045 | 0.400833 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.415787 | 0.429661 | 0.429000 | 0.463143 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.003978 | 0.003950 | 0.004391 | 0.004155 | 0.003962 | 0.003433 |

Relative to ABI-258, ABI-259 improved selected-checkpoint precision by about +0.0160 and connectivity by about +0.0713 while slightly reducing predicted-positive fraction, but it regressed filtered Dice by about -0.0067, recall by about -0.0214, MIT Dice by about -0.0036, and Google Dice by about -0.0132. Relative to ABI-223, ABI-259 remained lower by about -0.0382 filtered Dice, -0.0451 precision, -0.0332 recall, -0.0808 connectivity, -0.0300 MIT Dice, and -0.0610 Google Dice. Relative to ABI-255, it also lagged the primary overlap/source metrics, although its selected connectivity was higher than ABI-255's selected 0.2811.

The line-support decoder therefore met only a secondary part of its success criterion: it recovered some continuity compared with ABI-258 and ABI-255, but not enough to close the ABI-223 gap, and the improvement came with weaker recall and source Dice.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.225429 | 0.231801 | 0.212103 | 0.227058 | 0.223823 | 0.153765 | 0.005096 |
| 2 | 0.256328 | 0.245541 | 0.283164 | 0.342545 | 0.204785 | 0.254173 | 0.003091 |
| 3 | 0.276925 | 0.259902 | 0.317820 | 0.386473 | 0.215765 | 0.200720 | 0.002886 |
| 4 | 0.320877 | 0.301887 | 0.366836 | 0.381281 | 0.276995 | 0.190948 | 0.003756 |
| 5 | 0.325228 | 0.305288 | 0.374876 | 0.436651 | 0.259109 | 0.245917 | 0.003068 |
| 6 | 0.354720 | 0.336353 | 0.401039 | 0.433075 | 0.300374 | 0.277251 | 0.003586 |
| 7 | 0.302386 | 0.277486 | 0.370190 | 0.575992 | 0.205005 | 0.461708 | 0.001840 |
| 8 | 0.381540 | 0.368471 | 0.415787 | 0.438659 | 0.337582 | 0.331613 | 0.003978 |
| 9 | 0.364753 | 0.353721 | 0.391113 | 0.349622 | 0.381254 | 0.221714 | 0.005637 |
| 10 | 0.328330 | 0.318793 | 0.349908 | 0.296974 | 0.367090 | 0.164348 | 0.006390 |
| 11 | 0.375697 | 0.357396 | 0.422476 | 0.436387 | 0.329826 | 0.297353 | 0.003907 |
| 12 | 0.376367 | 0.355402 | 0.429661 | 0.434484 | 0.331964 | 0.287818 | 0.003950 |

The trajectory is finite and non-collapsed, but not cleanly late-improving for the primary metric. Filtered Dice peaks at epoch 8, falls sharply at epochs 9-10, and partially recovers by epochs 11-12 without exceeding the epoch-8 checkpoint. The highest connectivity checkpoint is epoch 7 at 0.461708, but that state is too conservative: precision rises to 0.575992 while recall drops to 0.205005 and predicted-positive fraction shrinks to 0.001840. The highest recall checkpoint is epoch 9 at 0.381254, but it loses precision and connectivity. The selected epoch is the best balance, not a sign that the exploratory epoch ceiling truncated a rising primary trajectory.

## Interpretation

Classify ABI-259 as a negative/mixed family-development Result for this exact temporal-attention line-support decoder. The Run confirms the mechanism is resource-safe, finite, source-informative, and capable of producing high-connectivity internal states. However, those high-connectivity states are too conservative at the trusted threshold, while the recall-recovering states lose continuity and precision. The best balanced checkpoint improves connectivity over ABI-258 but remains behind ABI-223 and ABI-255 on primary Dice and source-stratified overlap.

This does not eliminate temporal modeling or temporal-attention designs. ABI-223 remains the stronger temporal-attention comparator, ABI-255 remains the compact recurrent temporal comparator with stronger Dice, and ABI-253 remains the whole-validation-tested U-NetFormer/line-memory comparator. ABI-259 only argues against this exact decoder-side line-support repair as the next temporal-attention continuation.

## Decision

Do not promote ABI-259. Do not submit an unchanged late36 continuation of this exact line-support decoder: the best checkpoint was epoch 8, final epoch 12 only partially recovered, and the strongest connectivity signal occurred at an overly low-recall operating point rather than as a balanced late-improving trajectory.

If the campaign continues from this evidence, prefer a broader mechanism rather than another local decoder support block: for example, a differentiable line-accumulation design with explicit recall preservation, a compact motion/change stream that targets MIT under-coverage, or a non-temporal rotation-aware/line-network scout. Any follow-up must continue to avoid Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_012708_f5897e/candidate/PROPOSAL.md`
- `run_20260912_012708_f5897e/candidate/README.md`
- `run_20260912_012708_f5897e/candidate/manifest.yaml`
- `run_20260912_012708_f5897e/resolved_manifest.yaml`
- `run_20260912_012708_f5897e/outputs/model_summary.json`
- `run_20260912_012708_f5897e/outputs/best_metrics.json`
- `run_20260912_012708_f5897e/outputs/final_metrics.json`
- `run_20260912_012708_f5897e/outputs/metrics.jsonl`
- `run_20260912_012708_f5897e/outputs/resource_profile.json`
- `run_20260912_012708_f5897e/outputs/validation_postprocessing/index.json`
- `run_20260912_012708_f5897e/outputs/prediction_samples/samples.json`
- `run_20260912_004429_1eee45` for ABI-258 dual-evidence calibration context
- `run_20260911_210922_27f346` for ABI-255 recurrent late36 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
