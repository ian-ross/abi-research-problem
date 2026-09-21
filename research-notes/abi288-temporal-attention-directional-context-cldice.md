# ABI-288 temporal attention directional-context clDice scout

research-figures: []

## Scope

This note records ABI-288, Candidate `abi288_temporal_attention_directional_context_cldice_line_centerline_aux_v1`, Run `run_20260913_143121_ebfc60`.

ABI-288 is a trusted-loss mechanism scout in the temporal-attention family. It reused the resource-profiled ABI-238 temporal-attention directional-context U-Net architecture over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, but changed the trusted primary loss from `bce_dice` to provider-owned `bce_dice_cldice`. The hypothesis was that training-time clDice connectivity pressure might improve connected thin-line continuity without adding another unstable C4/continuity branch and without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, or sample selection into Candidate code.

The Candidate consumed only provider-owned temporal ABI/Solar Geometry Input tensors. It used trusted `temporal_eligible_center` selection, source-balanced sampling, trusted random mirroring, BCE-Dice-clDice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-288 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal` with 51 input channels.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,135,364, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.54 / 3.91 GiB.
- Training wall time: 1,250.9 s; validation wall time: 1,033.7 s; total Run wall time: 2,286.4 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-288 best epoch 11 | ABI-288 final epoch 12 | ABI-238 temporal directional-context late36 | ABI-223 temporal attention late36 | ABI-285 temporal C4 late36 | ABI-255 recurrent temporal late36 | ABI-286 continuity bridge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.376321 | 0.369041 | 0.420235 | 0.419776 | 0.422195 | 0.417348 | 0.393183 |
| Raw Dice | 0.390671 | 0.385450 | 0.438718 | 0.438487 | 0.439439 | 0.435656 | 0.409514 |
| Filtered precision | 0.381459 | 0.422760 | 0.488730 | 0.483764 | 0.448400 | 0.468293 | 0.419944 |
| Filtered recall | 0.371320 | 0.327434 | 0.368578 | 0.370738 | 0.398883 | 0.376400 | 0.369628 |
| Filtered connectivity | 0.237941 | 0.293510 | 0.352239 | 0.412427 | 0.243387 | 0.281116 | 0.280479 |
| MIT filtered Dice | 0.369607 | 0.352804 | 0.405383 | 0.398498 | 0.400831 | 0.400833 | 0.381112 |
| Google filtered Dice | 0.392678 | 0.409940 | 0.460838 | 0.476764 | 0.477410 | 0.463143 | 0.424115 |
| Filtered predicted-positive fraction | 0.005032 | 0.004004 | 0.003899 | 0.003962 | 0.004599 | 0.004155 | 0.004550 |
| Filtered predicted-positive pixels | 532,277 | 423,515 | 412,381 | 419,056 | 486,427 | 439,511 | 481,295 |

ABI-288 is a negative result for the intended loss-policy mechanism. Relative to the same-architecture ABI-238 comparator, the selected checkpoint is much lower on filtered Dice (-0.0439), MIT Dice (-0.0358), Google Dice (-0.0682), precision (-0.1073), and connectivity (-0.1143), while recall is essentially unchanged (+0.0027). Relative to ABI-223, the same pattern holds: nearly equal recall but much lower precision, aggregate Dice, source-stratified Dice, and connectivity. Thus the trusted clDice primary loss did not convert the temporal-attention directional-context architecture into better connected-line evidence at the fixed 0.5 threshold; it mostly broadened predictions and reduced precision.

The final epoch is more compact than the selected checkpoint and has better connectivity (0.2935 versus 0.2379), but it pays with lower recall and aggregate Dice. Even that final connectivity remains below ABI-238 and ABI-223, and aggregate/source Dice remains far below the temporal-eligible comparator band. The run is finite and source-informative, but it does not support an unchanged late36 continuation of the ABI-238-plus-clDice branch.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.187751 | 0.208721 | 0.152816 | 0.144836 | 0.266808 | 0.104308 | 0.009523 |
| 2 | 0.235742 | 0.224305 | 0.265532 | 0.389354 | 0.169047 | 0.340996 | 0.002244 |
| 3 | 0.293208 | 0.279227 | 0.327085 | 0.379802 | 0.238769 | 0.286218 | 0.003250 |
| 4 | 0.281310 | 0.259420 | 0.337453 | 0.443629 | 0.205954 | 0.340522 | 0.002400 |
| 5 | 0.315750 | 0.300414 | 0.353134 | 0.400463 | 0.260620 | 0.279741 | 0.003364 |
| 6 | 0.293671 | 0.280755 | 0.324347 | 0.367881 | 0.244375 | 0.284655 | 0.003434 |
| 7 | 0.320018 | 0.300901 | 0.369721 | 0.447536 | 0.249055 | 0.381058 | 0.002877 |
| 8 | 0.350472 | 0.347144 | 0.358154 | 0.332077 | 0.371023 | 0.230107 | 0.005776 |
| 9 | 0.352098 | 0.352723 | 0.350740 | 0.298622 | 0.428904 | 0.202810 | 0.007425 |
| 10 | 0.362834 | 0.345514 | 0.406758 | 0.442671 | 0.307394 | 0.335865 | 0.003590 |
| 11 | 0.376321 | 0.369607 | 0.392678 | 0.381459 | 0.371320 | 0.237941 | 0.005032 |
| 12 | 0.369041 | 0.352804 | 0.409940 | 0.422760 | 0.327434 | 0.293510 | 0.004004 |

The trajectory is finite, non-collapsed, and source-informative, but unstable. Epoch 9 reaches high recall (0.4289) only by expanding the predicted-positive fraction to 0.007425 and dropping precision to 0.2986. Epoch 11 is the filtered-Dice optimum, but its connectivity is low. Epoch 12 improves connectivity and precision while reducing recall and Dice. This oscillation suggests the clDice pressure did not align connectivity, recall, and source balance into one stable operating point.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3907 versus filtered Dice 0.3763, and raw predicted-positive pixels 572,975 versus filtered predicted-positive pixels 532,277. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3524, 0.4049, 0.4977, and 0.3971. They are consistent with finite non-collapsed predictions, but none provides evidence that the clDice loss-policy change improved aggregate temporal connectivity relative to ABI-238 or ABI-223.

## Interpretation

Classify ABI-288 as a finite, resource-safe, negative trusted-loss scout for the temporal-attention directional-context branch. The provider-owned BCE-Dice-clDice primary loss did not improve the same ABI-238 architecture's connected-line continuity at the selected fixed-threshold checkpoint and materially worsened precision and source-stratified Dice. It also did not match the ABI-285 temporal recall comparator or the ABI-223/238 temporal line-continuity comparators.

The result does not eliminate trusted clDice in all architectures, but it answers the narrow question tested here: switching ABI-238's primary loss to `bce_dice_cldice` is not enough to recover connected thin-line continuity and harms the precision/recall balance. Future temporal work should be mechanism-changing rather than an unchanged longer repeat of ABI-288, for example a temporal attention/change branch that keeps recall evidence and continuity evidence separated until late logits, a center-frame detail branch with cleaner precision support, or a different architecture that can use connectivity pressure without broadening negative-patch clutter. Any follow-up must continue to avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-288. Do not request temporal-eligible or whole-validation failure-bucket diagnostics for this capped temporal-eligible result. Do not request an unchanged late36 continuation of the ABI-288 loss-policy branch. Treat ABI-288 as a characterized negative mechanism test and broaden the next hypothesis away from loss-only clDice on ABI-238's temporal directional-context architecture.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_143121_ebfc60/candidate/PROPOSAL.md`
- `run_20260913_143121_ebfc60/candidate/README.md`
- `run_20260913_143121_ebfc60/candidate/manifest.yaml`
- `run_20260913_143121_ebfc60/resolved_manifest.yaml`
- `run_20260913_143121_ebfc60/execution.json`
- `run_20260913_143121_ebfc60/outputs/model_summary.json`
- `run_20260913_143121_ebfc60/outputs/best_metrics.json`
- `run_20260913_143121_ebfc60/outputs/final_metrics.json`
- `run_20260913_143121_ebfc60/outputs/metrics.jsonl`
- `run_20260913_143121_ebfc60/outputs/resource_profile.json`
- `run_20260913_143121_ebfc60/outputs/validation_postprocessing/index.json`
- `run_20260913_143121_ebfc60/outputs/prediction_samples/samples.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal comparison context
- `run_20260913_123056_4152f3/outputs/best_metrics.json` for ABI-286 continuity-bridge comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi287-temporal-c4-recall-protected-continuity-bridge-unet.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
