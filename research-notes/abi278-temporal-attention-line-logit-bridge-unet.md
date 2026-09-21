# ABI-278 temporal-attention line-logit bridge U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-278, Candidate `abi278_temporal_attention_line_logit_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_232028_0c31f7`.

ABI-278 was a mechanism-changing temporal-family continuation after ABI-274 through ABI-277. It returned to the cleaner ABI-223-style temporal-attention U-Net family and added a learned oriented line-evidence bridge immediately before the mask logits. The bridge applied one shared horizontal line-support filter under four right-angle rotations, fused the rotated support responses with high-resolution decoder features, and added a bounded gated residual to `mask_logits`. Line and Centerline auxiliary heads read the same bridge features.

The Candidate used provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` frame selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. It remained architecture/manifest-only and did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Execution result

ABI-278 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,125,070, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.59 / 3.85 GB.
- Training wall time: 1,037.0 s; validation wall time: 972.8 s; total Run wall time: 2,011.6 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-278 best epoch 12 | ABI-277 bidirectional scout | ABI-274 temporal line-state late36 | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-255 recurrent temporal late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.353766 | 0.384239 | 0.419364 | 0.420235 | 0.419776 | 0.417348 | 0.427570 |
| Raw Dice | 0.370630 | 0.401624 | 0.436760 | 0.437776 | 0.438487 | 0.433815 | 0.442746 |
| Filtered precision | 0.433119 | 0.457624 | 0.454127 | 0.488730 | 0.483764 | 0.468293 | 0.439467 |
| Filtered recall | 0.298988 | 0.331138 | 0.389545 | 0.368578 | 0.370738 | 0.376400 | 0.416301 |
| Filtered connectivity | 0.199816 | 0.263442 | 0.282911 | 0.352239 | 0.412427 | 0.281116 | 0.457773 |
| MIT filtered Dice | 0.334650 | 0.364664 | 0.399386 | 0.405383 | 0.398498 | 0.400833 | 0.411992 |
| Google filtered Dice | 0.401941 | 0.436066 | 0.472606 | 0.460838 | 0.476764 | 0.463143 | 0.468151 |
| Filtered predicted-positive fraction | 0.003569 | 0.003741 | 0.004434 | 0.003899 | 0.003962 | 0.004155 | 0.003433 |

ABI-278 did not meet its primary comparison targets. Relative to ABI-223, it is lower by about -0.0660 filtered Dice, -0.0499 precision, -0.0718 recall, -0.2126 connectivity, -0.0638 MIT Dice, and -0.0748 Google Dice. Relative to ABI-274, it is lower by about -0.0656 filtered Dice, -0.0210 precision, -0.0906 recall, -0.0831 connectivity, -0.0647 MIT Dice, and -0.0707 Google Dice. Relative to ABI-277, it is lower by about -0.0305 filtered Dice, -0.0245 precision, -0.0322 recall, -0.0636 connectivity, -0.0300 MIT Dice, and -0.0341 Google Dice.

The oriented line-logit bridge therefore did not sharpen temporal-attention evidence at threshold 0.5. It produced a finite, non-collapsed model, but the selected checkpoint under-covers both sources and especially fails the connected-thin-line continuity objective.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212944 | 0.215826 | 0.206575 | 0.219462 | 0.206802 | 0.165516 | 0.004871 |
| 2 | 0.246092 | 0.234906 | 0.271930 | 0.325568 | 0.197805 | 0.229963 | 0.003141 |
| 3 | 0.291546 | 0.279481 | 0.319820 | 0.356675 | 0.246529 | 0.251131 | 0.003573 |
| 4 | 0.292546 | 0.274851 | 0.334043 | 0.383872 | 0.236323 | 0.221553 | 0.003183 |
| 5 | 0.265311 | 0.260952 | 0.274617 | 0.264656 | 0.265969 | 0.140760 | 0.005195 |
| 6 | 0.329417 | 0.320294 | 0.349620 | 0.319264 | 0.340236 | 0.186961 | 0.005509 |
| 7 | 0.290587 | 0.269127 | 0.345287 | 0.468293 | 0.210650 | 0.260316 | 0.002325 |
| 8 | 0.340448 | 0.338108 | 0.346128 | 0.319298 | 0.364599 | 0.173713 | 0.005903 |
| 9 | 0.350095 | 0.343431 | 0.364976 | 0.307776 | 0.405907 | 0.174228 | 0.006818 |
| 10 | 0.346523 | 0.323514 | 0.401339 | 0.414258 | 0.297826 | 0.205637 | 0.003717 |
| 11 | 0.349429 | 0.335165 | 0.385415 | 0.434961 | 0.292007 | 0.220969 | 0.003471 |
| 12 | 0.353766 | 0.334650 | 0.401941 | 0.433119 | 0.298988 | 0.199816 | 0.003569 |

The trajectory is finite and non-collapsed, and the best checkpoint occurs at the final exploratory epoch. However, the late gain is small and remains far below the relevant temporal comparators. The model oscillates between high-recall/low-precision broad predictions at epochs 8-9 and compact high-precision/low-recall predictions at epochs 10-12. Connectivity never exceeds 0.2603 and ends at 0.1998, so the proposed oriented line-logit residual does not act as a robust continuity organizer. The final-epoch best alone is not enough to justify an unchanged late36 continuation because the branch is already substantially behind ABI-223, ABI-274, and ABI-277 on the intended recall/connectivity axes.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2502, 0.4192, 0.5053, and 0.4000. This is consistent with finite non-collapsed predictions and substantial per-sample variability. This note does not reproduce raw samples, images, coordinates, scene identifiers, or patch identities.

At the selected checkpoint, Artifact Filters removed about 29,105 predicted-positive pixels (`406,576` raw predicted-positive pixels versus `377,471` filtered). Raw Dice was 0.3706 versus filtered Dice 0.3538, so filtering lowers rather than creates the Result.

## Interpretation

Classify ABI-278 as a finite negative mechanism test. The narrow line-logit bridge is resource-safe and does not collapse, but it regresses versus both the cleaner ABI-223 temporal-attention comparator and the recent ABI-274/277 line-state branches. It did not recover ABI-223-style connectivity and did not preserve ABI-274-style recall/source balance. The bridge appears to perturb logits without organizing longer connected structures; when the model broadens, precision and connectivity are weak, and when it becomes compact, recall stays too low.

This does not eliminate temporal attention or orientation-aware evidence mechanisms as families. It narrows the exact integration point: adding a bounded oriented support residual only at the final mask-logit stage is insufficient. Future temporal work should avoid repeating ABI-278 unchanged and should use a mechanism-changing design, such as earlier cross-scale orientation consensus, a dual-evidence/calibration head that preserves recall without suppressing continuity, or a return to ABI-223/238-style temporal attention with explicit center-frame detail preservation. ABI-223 remains the temporal connectivity comparator, ABI-274 remains the temporal recall/source-balance comparator, ABI-255 remains the compact recurrent temporal comparator, ABI-249 remains the high-precision C4 whole-validation comparator, and ABI-202 remains the aggregate whole-validation reference.

## Decision

Do not promote ABI-278, do not request temporal-eligible failure-bucket diagnostics, and do not request a late-improving budget for this exact line-logit bridge branch. The branch failed its stated success criteria: it did not approach the ABI-223/238 temporal Dice band, did not improve ABI-223 recall, did not repair ABI-274/277 connectivity, and did not improve MIT/source balance.

Do not repeat ABI-278 unchanged. A future Run should be mechanism-changing and should target recall-preserving connectivity or calibration with stronger cross-scale support, without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_232028_0c31f7/candidate/PROPOSAL.md`
- `run_20260912_232028_0c31f7/candidate/README.md`
- `run_20260912_232028_0c31f7/candidate/manifest.yaml`
- `run_20260912_232028_0c31f7/resolved_manifest.yaml`
- `run_20260912_232028_0c31f7/outputs/model_summary.json`
- `run_20260912_232028_0c31f7/outputs/best_metrics.json`
- `run_20260912_232028_0c31f7/outputs/final_metrics.json`
- `run_20260912_232028_0c31f7/outputs/metrics.jsonl`
- `run_20260912_232028_0c31f7/outputs/resource_profile.json`
- `run_20260912_232028_0c31f7/outputs/validation_postprocessing/index.json`
- `run_20260912_232028_0c31f7/outputs/prediction_samples/samples.json`
- `run_20260912_222529_d1a74a/outputs/best_metrics.json` for ABI-277 bidirectional-consistency comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal comparator context
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
