# ABI-241 temporal high-resolution change-skip U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-241, Candidate `abi241_temporal_highres_change_skip_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_050449_17cdcb`.

ABI-241 tested whether keeping temporal-difference evidence at full 256x256 resolution and injecting it through encoder/decoder skip features could improve the recall/connectivity balance after ABI-239/240 showed that low-resolution temporal line accumulation was overlap-useful but connectivity-weak. The Candidate consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-241 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,797,860, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.27 / 4.54 GiB.
- Training wall time: 1,292.8 s; validation wall time: 1,014.3 s; total Run wall time: 2,308.8 s.

This is successful finite/resource evidence for the high-resolution temporal change-skip formulation. Resource use stayed well inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 11. Final epoch 12 was worse on overlap/recall but slightly better on filtered connectivity.

| Metric | ABI-241 best epoch 11 | ABI-241 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.384180 | 0.328559 |
| Raw Dice | 0.399916 | 0.343846 |
| Filtered IoU | 0.237761 | 0.196573 |
| Filtered precision | 0.400177 | 0.407310 |
| Filtered recall | 0.369412 | 0.275327 |
| Filtered contrail connectivity | 0.238980 | 0.281625 |
| Filtered predicted-positive fraction | 0.004772 | 0.003494 |
| Raw predicted-positive fraction | 0.005145 | 0.003764 |
| MIT filtered Dice | 0.377453 | 0.311836 |
| Google filtered Dice | 0.401490 | 0.370234 |
| MIT filtered recall | 0.349223 | 0.249156 |
| Google filtered recall | 0.429479 | 0.353190 |
| Train loss | 0.823816 | 0.820385 |
| Validation loss | 0.863563 | 0.885787 |

The selected checkpoint is finite, noncollapsed, and source-informative. Both MIT and Google retain nontrivial filtered Dice and recall. However, the intended high-resolution change bridge did not recover the connectivity deficit: best-checkpoint connectivity is below ABI-240's 0.264863, ABI-238's 0.352239, ABI-223's 0.412427, and ABI-202's 0.457773.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.227817 | 0.239224 | 0.340249 | 0.171234 | 0.220014 | 0.247615 | 0.233738 | 0.002602 |
| 2 | 0.227360 | 0.239801 | 0.418677 | 0.156052 | 0.210337 | 0.270454 | 0.311105 | 0.001927 |
| 3 | 0.254595 | 0.267632 | 0.373174 | 0.193204 | 0.236417 | 0.296894 | 0.254710 | 0.002676 |
| 4 | 0.278792 | 0.289846 | 0.285710 | 0.272201 | 0.275072 | 0.286544 | 0.142955 | 0.004925 |
| 5 | 0.277017 | 0.291912 | 0.479703 | 0.194736 | 0.257363 | 0.327339 | 0.302094 | 0.002099 |
| 6 | 0.312544 | 0.328217 | 0.409804 | 0.252595 | 0.303958 | 0.333443 | 0.244410 | 0.003186 |
| 7 | 0.291180 | 0.306977 | 0.478288 | 0.209300 | 0.274024 | 0.335989 | 0.301183 | 0.002262 |
| 8 | 0.357827 | 0.373794 | 0.402217 | 0.322261 | 0.351665 | 0.372515 | 0.252551 | 0.004142 |
| 9 | 0.349095 | 0.362848 | 0.340292 | 0.358364 | 0.343540 | 0.362483 | 0.197514 | 0.005444 |
| 10 | 0.292137 | 0.305748 | 0.354881 | 0.248246 | 0.271645 | 0.341214 | 0.204092 | 0.003616 |
| 11 | 0.384180 | 0.399916 | 0.400177 | 0.369412 | 0.377453 | 0.401490 | 0.238980 | 0.004772 |
| 12 | 0.328559 | 0.343846 | 0.407310 | 0.275327 | 0.311836 | 0.370234 | 0.281625 | 0.003494 |

The trajectory is noisy rather than cleanly late-improving. Epoch 11 is near the exploratory ceiling, but the final epoch drops by -0.055620 filtered Dice and -0.094085 filtered recall while train loss continues to improve. Connectivity fluctuates independently of overlap: epochs 2, 5, 7, and 12 have higher connectivity than the selected epoch, but their Dice/recall tradeoffs are worse. This does not satisfy the proposed success criterion of improving the ABI-240 connectivity/recall balance.

## Comparison context

| Metric | ABI-241 high-res change skip | ABI-240 line-accum late36 | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_050449_17cdcb` | `run_20260911_031326_43ed12` | `run_20260911_004137_f54c45` | `run_20260908_154531_8c7e2b` | `run_20260904_043143_ee0005` |
| Best epoch | 11 | 29 | 29 | 36 | 34 |
| Filtered Dice | 0.384180 | 0.414892 | 0.420235 | 0.419776 | 0.427570 |
| Raw Dice | 0.399916 | 0.431959 | 0.438718 | 0.438487 | 0.442746 |
| Filtered precision | 0.400177 | 0.436241 | 0.488730 | 0.483764 | 0.439467 |
| Filtered recall | 0.369412 | 0.395534 | 0.368578 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.238980 | 0.264863 | 0.352239 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.377453 | 0.397067 | 0.405383 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.401490 | 0.460659 | 0.460838 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004772 | 0.004687 | 0.003899 | 0.003962 | 0.003433 |

ABI-241 trails ABI-240 by -0.030712 filtered Dice and -0.025882 filtered recall despite a similar predicted-positive fraction, and it trails by -0.025882 connectivity at the selected checkpoint. It roughly matches ABI-238/223 recall, but only with lower precision and much weaker connectivity. The largest source-specific gap is Google filtered Dice: ABI-241 reaches 0.401490 versus ABI-240/238/223 at roughly 0.461/0.461/0.477. MIT is less weak but still below the temporal frontier.

Against the single-frame ABI-202 frontier, ABI-241 is not competitive on capped overlap (-0.043391 filtered Dice), recall (-0.046889), or connectivity (-0.218793). This comparison does not eliminate temporal modeling as a family, but it is strong evidence against this exact high-resolution change-skip mechanism as currently configured.

## Interpretation

Classify ABI-241 as a useful finite scout that failed its intended scientific criterion. The full-resolution temporal-difference skip path is resource-safe and nondegenerate, but it did not preserve the ABI-240 recall gain or recover line continuity. Its selected checkpoint appears to require a larger predicted-positive fraction than ABI-238/223 for similar recall while losing precision and connectedness, suggesting that the skip bridge adds fragmented change evidence rather than coherent contrail support.

The result also weakens the case for an immediate late36 continuation. Although the best epoch is near the exploratory ceiling, the final epoch regresses sharply and the trajectory oscillates rather than showing a monotonic or ambiguous late-improving pattern. A late budget may still be appropriate for a redesigned temporal branch, but ABI-241 itself does not meet the approved longer-budget evidence standard.

## Decision

Do not promote ABI-241, do not request whole-validation diagnostics from this Result alone, and do not request a late36 continuation of the exact ABI-241 formulation. Treat the high-resolution change-skip idea as explored enough to avoid an unchanged budget extension.

Temporal modeling remains a viable underexplored frontier because ABI-223/238/240 remain near the single-frame frontier under capped evidence. A reasonable next in-contract hypothesis is to broaden toward a compact recurrent change block or modern temporal backbone that explicitly couples temporal state with continuity-preserving decoder features, rather than adding more independent high-resolution change skips or repeating low-resolution line accumulation.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_050449_17cdcb/candidate/PROPOSAL.md`
- `run_20260911_050449_17cdcb/candidate/README.md`
- `run_20260911_050449_17cdcb/candidate/manifest.yaml`
- `run_20260911_050449_17cdcb/resolved_manifest.yaml`
- `run_20260911_050449_17cdcb/outputs/model_summary.json`
- `run_20260911_050449_17cdcb/outputs/best_metrics.json`
- `run_20260911_050449_17cdcb/outputs/final_metrics.json`
- `run_20260911_050449_17cdcb/outputs/metrics.jsonl`
- `run_20260911_050449_17cdcb/outputs/resource_profile.json`
- `run_20260911_050449_17cdcb/outputs/validation_postprocessing/index.json`
- `run_20260911_050449_17cdcb/outputs/prediction_samples/samples.json`
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
