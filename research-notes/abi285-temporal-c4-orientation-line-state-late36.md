# ABI-285 temporal C4 orientation line-state late36 U-Net

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-285, Candidate `abi285_temporal_c4_orientation_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260913_100333_a250df`.

ABI-285 is the approved 36-epoch close continuation of ABI-284. ABI-284 moved C4/orientation-consensus line state earlier in the temporal U-Net and selected its best checkpoint at exploratory epoch 12, but remained below ABI-274 and ABI-223 on temporal-eligible filtered Dice, recall, and connected-line continuity. ABI-285 keeps the architecture unchanged and tests whether the late-improving budget stabilizes a better recall/precision compromise.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-285 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Parent/close-continuation Run: ABI-284, `run_20260913_091156_167372`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,245,425, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.09 / 5.42 GiB.
- Training wall time: 4,488.3 s; validation wall time: 3,255.1 s; total Run wall time: 7,745.4 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 32.

## Best-validation metrics

| Metric | ABI-285 best epoch 32 | ABI-284 exploratory | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 | ABI-255 recurrent temporal late36 | ABI-238 temporal directional-context late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.422195 | 0.390090 | 0.419364 | 0.419776 | 0.417348 | 0.420235 |
| Raw Dice | 0.439439 | 0.408012 | 0.436760 | 0.438487 | 0.435656 | 0.438718 |
| Filtered precision | 0.448400 | 0.475285 | 0.454127 | 0.483764 | 0.468293 | 0.488730 |
| Filtered recall | 0.398883 | 0.330796 | 0.389545 | 0.370738 | 0.376400 | 0.368578 |
| Filtered connectivity | 0.243387 | 0.254710 | 0.282911 | 0.412427 | 0.281116 | 0.352239 |
| MIT filtered Dice | 0.400831 | 0.371847 | 0.399386 | 0.398498 | 0.400833 | 0.405383 |
| Google filtered Dice | 0.477410 | 0.436956 | 0.472606 | 0.476764 | 0.463143 | 0.460838 |
| Filtered predicted-positive fraction | 0.004599 | 0.003598 | 0.004434 | 0.003962 | 0.004155 | 0.003899 |
| Filtered predicted-positive pixels | 486,427 | 380,578 | 469,049 | 419,056 | 439,511 | 412,381 |

The late-improving continuation answers the immediate ABI-284 question positively for aggregate temporal-eligible filtered Dice and recall, but negatively for compact high-precision connected-line behavior.

Relative to ABI-284, ABI-285 gains +0.0321 filtered Dice, +0.0681 recall, +0.0290 MIT Dice, and +0.0405 Google Dice. The trade-off is lower precision (-0.0269), slightly lower connectivity (-0.0113), and a larger filtered footprint (+105,849 positive pixels). Longer training therefore recovers substantial threshold-0.5 evidence, but it does not preserve ABI-284's compact/high-precision regime.

Relative to ABI-274, ABI-285 is slightly higher on aggregate filtered Dice (+0.0028), MIT Dice (+0.0014), Google Dice (+0.0048), and recall (+0.0093), with slightly lower precision (-0.0057) and much lower connectivity (-0.0395). Relative to ABI-223, ABI-285 is slightly higher on filtered Dice (+0.0024) and recall (+0.0281) but much lower on precision (-0.0354) and especially connectivity (-0.1690). It also edges ABI-238 on aggregate filtered Dice while trailing ABI-238 on MIT Dice, precision, and connectivity.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.236423 | 0.234798 | 0.240237 | 0.297140 | 0.196309 | 0.229671 | 0.003415 |
| 3 | 0.342184 | 0.322506 | 0.388933 | 0.389955 | 0.304840 | 0.244392 | 0.004041 |
| 5 | 0.373519 | 0.359042 | 0.409044 | 0.409572 | 0.343299 | 0.286599 | 0.004333 |
| 8 | 0.379437 | 0.357660 | 0.435348 | 0.479557 | 0.313901 | 0.346158 | 0.003384 |
| 12 | 0.383497 | 0.362159 | 0.436625 | 0.464694 | 0.326454 | 0.270004 | 0.003632 |
| 15 | 0.406563 | 0.389173 | 0.450096 | 0.426423 | 0.388470 | 0.272507 | 0.004709 |
| 16 | 0.408453 | 0.386239 | 0.465379 | 0.466507 | 0.363249 | 0.282669 | 0.004025 |
| 22 | 0.409225 | 0.391883 | 0.454238 | 0.438698 | 0.383463 | 0.244263 | 0.004519 |
| 24 | 0.403762 | 0.378232 | 0.470100 | 0.487504 | 0.344572 | 0.290833 | 0.003654 |
| 27 | 0.408108 | 0.383977 | 0.473797 | 0.505128 | 0.342352 | 0.392529 | 0.003504 |
| 29 | 0.408335 | 0.386015 | 0.465829 | 0.471672 | 0.359994 | 0.302978 | 0.003946 |
| 32 | 0.422195 | 0.400831 | 0.477410 | 0.448400 | 0.398883 | 0.243387 | 0.004599 |
| 34 | 0.406633 | 0.384313 | 0.466698 | 0.505181 | 0.340258 | 0.292092 | 0.003482 |
| 36 | 0.371776 | 0.344513 | 0.442837 | 0.520462 | 0.289167 | 0.304920 | 0.002872 |

The trajectory is finite, source-informative, and non-collapsed, but still oscillatory. ABI-285 crosses the 0.40 filtered-Dice band at epoch 15 and repeatedly revisits it through epoch 34. The selected checkpoint at epoch 32 is a recall-heavy compromise: it has the highest aggregate filtered Dice, the highest recall among the listed temporal comparators, and strong Google Dice, but its connectivity is weaker than ABI-274/223/238/255.

The high-precision/high-connectivity behavior remains intermittent rather than stabilized. Epoch 27 reaches precision 0.5051 and connectivity 0.3925, close to ABI-223 connectivity, but recall is only 0.3424. Epoch 32 raises recall to 0.3989 and aggregate Dice to the Run maximum, but connectivity drops to 0.2434. Epoch 36 ends in an even more conservative state: precision 0.5205, recall 0.2892, filtered Dice 0.3718. This supports checkpoint-level utility but not a stable final-training regime.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2504, 0.4308, 0.6119, and 0.3639. This is consistent with finite non-collapsed predictions and some strong per-sample positive behavior, but it does not establish aggregate promotion evidence.

At the selected checkpoint, raw Dice was 0.4394 versus filtered Dice 0.4222, with 523,939 raw predicted-positive pixels versus 486,427 filtered predicted-positive pixels. Artifact Filters therefore lower rather than create the selected Result.

## Interpretation

Classify ABI-285 as a useful late-improving temporal-family development result. It becomes the strongest currently observed capped temporal-eligible filtered-Dice Result among the indexed temporal comparators, narrowly above ABI-238, ABI-223, and ABI-274. The late budget validated that ABI-284's final-epoch exploratory behavior was not exhausted: longer training recovered recall and source-balanced Dice beyond the earlier 12-epoch branch.

However, ABI-285 did not solve the connected-line continuity weakness. Its best checkpoint sacrifices the intended compact high-precision/high-connectivity C4 orientation regime for broader recall. It is a better threshold-0.5 aggregate segmentation candidate than ABI-284, but the mechanism did not combine ABI-223-like continuity with ABI-274-like recall. The final epoch also regresses sharply from the selected checkpoint, so the late run provides checkpoint evidence rather than stable end-of-training convergence.

This makes ABI-285 a diagnostic frontier candidate, not a promotion claim. The next useful handoff should be a bounded temporal-eligible failure-bucket Evaluation Request for ABI-285, comparing it against ABI-223, ABI-274, ABI-238, and ABI-255 on source balance, false-negative thin-line continuity, and negative-patch clutter. That evaluation should not be created in this Autonomy Step because this Research Note is the single primary handoff.

## Decision

Do not promote ABI-285 on this capped temporal-eligible evidence alone. Do not launch an unchanged ABI-285 continuation: the late36 budget already ran, selected epoch 32, and the final epochs regressed. Keep ABI-285 as the current capped temporal-eligible aggregate filtered-Dice comparator and request temporal-eligible failure-bucket diagnostics in a future Autonomy Step before making stronger comparative claims.

Future architecture work should focus on preserving the epoch-32 recall/source-balance gains while adding explicit connected-line support that does not move thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_100333_a250df/candidate/PROPOSAL.md`
- `run_20260913_100333_a250df/candidate/README.md`
- `run_20260913_100333_a250df/candidate/manifest.yaml`
- `run_20260913_100333_a250df/candidate/budget_request.yaml`
- `run_20260913_100333_a250df/resolved_manifest.yaml`
- `run_20260913_100333_a250df/execution.json`
- `run_20260913_100333_a250df/outputs/model_summary.json`
- `run_20260913_100333_a250df/outputs/best_metrics.json`
- `run_20260913_100333_a250df/outputs/final_metrics.json`
- `run_20260913_100333_a250df/outputs/metrics.jsonl`
- `run_20260913_100333_a250df/outputs/resource_profile.json`
- `run_20260913_100333_a250df/outputs/validation_postprocessing/index.json`
- `run_20260913_100333_a250df/outputs/prediction_samples/samples.json`
- `run_20260913_091156_167372/outputs/best_metrics.json` for ABI-284 exploratory parent comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal late36 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context late36 comparison context
- `/history/research-notes/abi284-temporal-c4-orientation-line-state-unet.md`
- `/history/research-notes/abi274-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
