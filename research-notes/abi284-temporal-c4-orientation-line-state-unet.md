# ABI-284 temporal C4 orientation line-state U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-284, Candidate `abi284_temporal_c4_orientation_line_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_091156_167372`.

ABI-284 was a mechanism-changing temporal-family continuation after ABI-223, ABI-274, ABI-275, ABI-281, and ABI-282. ABI-274 established an early temporal line-state attention comparator with useful recall/source behavior but weak temporal-eligible connected-line continuity. ABI-275 and ABI-282 tested later C4/detail continuity bridges and tended to trade away recall or underpredict. ABI-284 moved the C4/orientation prior earlier by replacing the hand-built horizontal/vertical/diagonal temporal line-state extractor with a rotation-shared C4 orientation-consensus line-state module before the encoder pyramid.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Execution result

ABI-284 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,245,425, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.09 / 5.42 GiB.
- Training wall time: 1,500.3 s; validation wall time: 1,054.1 s; total Run wall time: 2,556.2 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-284 best epoch 12 | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 | ABI-275 temporal C4 bridge | ABI-281 center-detail agreement | ABI-282 C4 detail continuity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.390090 | 0.419364 | 0.419776 | 0.385365 | 0.375376 | 0.371561 |
| Raw Dice | 0.408012 | 0.436760 | 0.438487 | 0.401336 | 0.392039 | 0.387573 |
| Filtered precision | 0.475285 | 0.454127 | 0.483764 | 0.413604 | 0.418431 | 0.437707 |
| Filtered recall | 0.330796 | 0.389545 | 0.370738 | 0.360736 | 0.340355 | 0.322782 |
| Filtered connectivity | 0.254710 | 0.282911 | 0.412427 | 0.266368 | 0.251147 | 0.230765 |
| MIT filtered Dice | 0.371847 | 0.399386 | 0.398498 | 0.372421 | 0.365315 | 0.354712 |
| Google filtered Dice | 0.436956 | 0.472606 | 0.476764 | 0.417764 | 0.400773 | 0.412957 |
| Filtered predicted-positive fraction | 0.003598 | 0.004434 | 0.003962 | 0.004509 | 0.004205 | 0.003812 |
| Filtered predicted-positive pixels | 380,578 | 469,049 | 419,056 | 476,918 | 444,781 | 403,240 |

ABI-284 improves over the recent exploratory temporal C4/detail branches on aggregate filtered Dice. Relative to ABI-282, it gains +0.0185 filtered Dice, +0.0376 precision, +0.0080 recall, +0.0239 connectivity, +0.0171 MIT Dice, and +0.0240 Google Dice while predicting 22,662 fewer filtered-positive pixels. Relative to ABI-281, it gains +0.0147 filtered Dice, +0.0569 precision, +0.0036 connectivity, +0.0065 MIT Dice, and +0.0362 Google Dice, but recall is lower by -0.0096. Relative to ABI-275, it gains a small +0.0047 filtered Dice and much higher precision (+0.0617) with a much smaller footprint (-96,340 filtered-positive pixels), but recall drops by -0.0299 and connectivity by -0.0117.

Against the stronger late36 temporal comparators, ABI-284 remains below the target band. Relative to ABI-274 it is lower by about -0.0293 filtered Dice, -0.0587 recall, -0.0282 connectivity, -0.0275 MIT Dice, and -0.0356 Google Dice, although precision is higher by +0.0212 and the footprint is more compact. Relative to ABI-223 it is lower by about -0.0297 filtered Dice and -0.1577 connectivity; it nearly matches ABI-223 precision but is meaningfully lower recall and source Dice.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.162926 | 0.154759 | 0.185606 | 0.463510 | 0.098833 | 0.406056 | 0.001102 |
| 2 | 0.261499 | 0.242728 | 0.310721 | 0.447765 | 0.184676 | 0.325534 | 0.002132 |
| 3 | 0.343794 | 0.321192 | 0.399027 | 0.449010 | 0.278527 | 0.318281 | 0.003207 |
| 4 | 0.281362 | 0.261833 | 0.324874 | 0.338046 | 0.240959 | 0.211570 | 0.003685 |
| 5 | 0.345178 | 0.317719 | 0.414613 | 0.491555 | 0.265974 | 0.370499 | 0.002797 |
| 6 | 0.344525 | 0.322846 | 0.399083 | 0.453633 | 0.277726 | 0.340453 | 0.003165 |
| 7 | 0.317565 | 0.289946 | 0.390639 | 0.521418 | 0.228307 | 0.408451 | 0.002264 |
| 8 | 0.383347 | 0.360157 | 0.445300 | 0.541642 | 0.296650 | 0.458785 | 0.002831 |
| 9 | 0.388078 | 0.372341 | 0.427312 | 0.396482 | 0.380023 | 0.264615 | 0.004955 |
| 10 | 0.384394 | 0.362877 | 0.436803 | 0.429494 | 0.347865 | 0.286948 | 0.004187 |
| 11 | 0.360602 | 0.336728 | 0.423739 | 0.510021 | 0.278895 | 0.327532 | 0.002827 |
| 12 | 0.390090 | 0.371847 | 0.436956 | 0.475285 | 0.330796 | 0.254710 | 0.003598 |

The trajectory is finite, non-collapsed, source-informative, and still ambiguous at the exploratory ceiling. The selected checkpoint is the final epoch, and filtered Dice recovers to the Run maximum after an epoch-11 dip. The branch repeatedly alternates between compact high-precision/high-connectivity states and broader higher-recall states. Epoch 8 is the clearest example of the intended early orientation effect: precision reaches 0.5416 and connectivity 0.4588, above ABI-274 and ABI-275 connectivity, but recall remains only 0.2967. Epoch 9 then raises recall to 0.3800 and MIT Dice to 0.3723, but loses most of the connectivity advantage. Epoch 12 is the best filtered-Dice compromise, not the best line-continuity state.

This pattern suggests that early C4 orientation line state is not a dead branch, but its current integration has not stabilized the desired recall/connectivity combination by 12 epochs.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4335, 0.4521, 0.6063, and 0.3564. This is consistent with finite non-collapsed predictions and notable per-sample positive performance in the retained trace samples, but it does not establish aggregate promotion evidence.

At the selected checkpoint, raw Dice was 0.4080 versus filtered Dice 0.3901, with 410,254 raw predicted-positive pixels versus 380,578 filtered predicted-positive pixels. Artifact Filters therefore lower rather than create the selected Result.

## Interpretation

Classify ABI-284 as a finite, resource-safe, partially useful temporal C4 mechanism test. It is the best of the recent exploratory temporal C4/detail line-continuity variants on aggregate temporal-eligible filtered Dice and is substantially cleaner than ABI-275/281/282 in precision and prediction footprint. Moving orientation consensus earlier is therefore more promising than the late post-decoder C4/detail bridges tested in ABI-275 and ABI-282.

However, ABI-284 did not solve the temporal connected-line weakness. Its selected checkpoint remains below ABI-274 on filtered Dice, recall, connectivity, and both Dataset Sources, and far below ABI-223 on connectivity. The high-connectivity epochs demonstrate that the model can enter a useful orientation-consensus regime, but that regime is coupled to conservative underprediction. When recall improves, the connectivity advantage disappears. The mechanism currently improves compactness and precision more reliably than it preserves connected recall.

This result narrows but does not eliminate early temporal C4 orientation-line-state modeling. The exact exploratory branch is not a promotion candidate, but the final-epoch best checkpoint and oscillatory late trajectory are compatible with a bounded late-improving continuation question: whether longer training can stabilize a compromise that keeps ABI-284's compact/high-precision behavior while recovering more of ABI-274's recall and ABI-223's continuity.

## Decision

Do not promote ABI-284. Do not request temporal-eligible failure-bucket diagnostics from this exploratory checkpoint; it is still below ABI-223/274 late36 temporal comparators and its main lesson is trajectory/mechanism behavior rather than diagnostic promotion readiness.

A late-improving close continuation can be considered in a future Autonomy Step because the best checkpoint is at epoch 12, the Run is finite and non-collapsed, both Dataset Sources are informative, and the trajectory remains ambiguous rather than clearly plateaued. If pursued, it should be framed as an ABI-284 late36 family-development test, not as a promotion claim. If not pursued immediately, future temporal work should still use a mechanism-changing path that preserves early orientation evidence while adding recall support, without moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_091156_167372/candidate/PROPOSAL.md`
- `run_20260913_091156_167372/candidate/README.md`
- `run_20260913_091156_167372/candidate/manifest.yaml`
- `run_20260913_091156_167372/resolved_manifest.yaml`
- `run_20260913_091156_167372/outputs/model_summary.json`
- `run_20260913_091156_167372/outputs/best_metrics.json`
- `run_20260913_091156_167372/outputs/final_metrics.json`
- `run_20260913_091156_167372/outputs/metrics.jsonl`
- `run_20260913_091156_167372/outputs/resource_profile.json`
- `run_20260913_091156_167372/outputs/validation_postprocessing/index.json`
- `run_20260913_091156_167372/outputs/prediction_samples/samples.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `run_20260912_203536_240ad8/outputs/best_metrics.json` for ABI-275 temporal C4 bridge comparison context
- `run_20260913_050456_f4352b/outputs/best_metrics.json` for ABI-281 center-detail agreement comparison context
- `run_20260913_054610_22cd27/outputs/best_metrics.json` for ABI-282 C4 detail-continuity comparison context
- `/history/research-notes/abi274-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi275-temporal-c4-continuity-bridge-unet.md`
- `/history/research-notes/abi281-temporal-attention-center-detail-agreement-unet.md`
- `/history/research-notes/abi282-temporal-c4-detail-continuity-unet.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
