# ABI-276 temporal line-state center-detail U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-276, Candidate `abi276_temporal_line_state_center_detail_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_212900_56562e`.

ABI-276 was a mechanism-changing family-development continuation after ABI-274 and ABI-275. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. The architectural change was to inject center-frame high-resolution detail together with the temporal line state at each encoder scale and again before the final heads, testing whether center-frame thin-structure evidence could organize ABI-274's weak connected-line continuity earlier than ABI-275's failed post-decoder C4 bridge.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Execution result

ABI-276 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,352,272, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.95 / 6.34 GB.
- Training wall time: 1,661.2 s; validation wall time: 1,117.1 s; total Run wall time: 2,780.2 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-276 best epoch 11 | ABI-274 temporal line-state late36 | ABI-275 C4 bridge scout | ABI-254 center-detail attention scout | ABI-223 temporal attention late36 | ABI-255 recurrent temporal late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.392168 | 0.419364 | 0.385365 | 0.393943 | 0.419776 | 0.417348 | 0.427570 |
| Raw Dice | 0.409195 | 0.436760 | 0.401336 | — | 0.438487 | 0.433815 | 0.442746 |
| Filtered precision | 0.445297 | 0.454127 | 0.413604 | 0.486613 | 0.483764 | 0.468293 | 0.439467 |
| Filtered recall | 0.350365 | 0.389545 | 0.360736 | 0.330922 | 0.370738 | 0.376400 | 0.416301 |
| Filtered connectivity | 0.278531 | 0.282911 | 0.266368 | 0.365528 | 0.412427 | 0.281116 | 0.457773 |
| MIT filtered Dice | 0.375358 | 0.399386 | 0.372421 | 0.377873 | 0.398498 | 0.400833 | 0.411992 |
| Google filtered Dice | 0.434143 | 0.472606 | 0.417764 | 0.436096 | 0.476764 | 0.463143 | 0.468151 |
| Filtered predicted-positive fraction | 0.004067 | 0.004434 | 0.004509 | 0.003516 | 0.003962 | 0.004155 | 0.003433 |

ABI-276 improves over the failed ABI-275 post-decoder C4 bridge on filtered Dice (+0.0068), precision (+0.0317), connectivity (+0.0122), MIT Dice (+0.0029), and Google Dice (+0.0164), but it does not meet the stronger ABI-274 comparison target. Relative to ABI-274, ABI-276 is lower by about -0.0272 filtered Dice, -0.0088 precision, -0.0392 recall, -0.0044 connectivity, -0.0240 MIT Dice, and -0.0385 Google Dice. Relative to ABI-254, the earlier center-detail temporal-attention scout, ABI-276 is similar on aggregate Dice but lower on precision and connectivity while higher on recall.

The result therefore does not support the central hypothesis that center-frame high-resolution detail injected with the temporal line state repairs the continuity weakness. It modestly recovers from ABI-275's late C4-bridge regression, but not enough to rejoin the ABI-223/238/274 temporal comparator band.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.259363 | 0.256661 | 0.265401 | 0.260878 | 0.257866 | 0.204596 | 0.005110 |
| 2 | 0.287299 | 0.281263 | 0.301685 | 0.350351 | 0.243480 | 0.252732 | 0.003593 |
| 3 | 0.323073 | 0.311571 | 0.348575 | 0.345755 | 0.303185 | 0.182144 | 0.004533 |
| 4 | 0.329225 | 0.311791 | 0.371259 | 0.391609 | 0.283986 | 0.252787 | 0.003749 |
| 5 | 0.307053 | 0.286023 | 0.360765 | 0.485632 | 0.224499 | 0.347539 | 0.002390 |
| 6 | 0.372516 | 0.352555 | 0.422921 | 0.401943 | 0.347103 | 0.302351 | 0.004464 |
| 7 | 0.342742 | 0.311450 | 0.426444 | 0.571696 | 0.244731 | 0.492898 | 0.002213 |
| 8 | 0.369181 | 0.345425 | 0.433445 | 0.526795 | 0.284162 | 0.406853 | 0.002789 |
| 9 | 0.382655 | 0.369100 | 0.414538 | 0.374379 | 0.391305 | 0.263825 | 0.005403 |
| 10 | 0.326320 | 0.315914 | 0.350600 | 0.344375 | 0.310063 | 0.157006 | 0.004654 |
| 11 | 0.392168 | 0.375358 | 0.434143 | 0.445297 | 0.350365 | 0.278531 | 0.004067 |
| 12 | 0.385548 | 0.367021 | 0.431502 | 0.405544 | 0.367432 | 0.249465 | 0.004684 |

The trajectory is finite, source-informative, and non-collapsed, but noisy. Best filtered Dice occurs near the exploratory ceiling at epoch 11, yet the final epoch drops in filtered Dice, precision, connectivity, MIT Dice, and Google Dice while only recall rises. High-connectivity epochs 7 and 8 are conservative operating points with much lower recall and lower aggregate Dice, similar to ABI-275's pattern. This is not a clean late-improving case for an unchanged late36 continuation.

## Prediction sample check

The retained first-four validation prediction samples are only fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4370, 0.1261, 0.3923, and 0.3826. This is consistent with a finite non-collapsed model and a substantial low-quality tail, but the note does not reproduce raw samples, images, coordinates, scene identifiers, or patch identities.

## Interpretation

Classify ABI-276 as a finite negative-to-ambiguous mechanism test. It is resource-safe and improves on ABI-275's failed late C4 bridge, but it does not recover ABI-274's recall/source lift and does not improve selected-checkpoint continuity. The center-frame detail injector appears to sharpen some epochs into compact high-precision/high-connectivity predictions, but those operating points under-cover contrails; when recall rises, connectivity and precision fall. The mechanism therefore behaves like another unstable precision/recall tradeoff rather than a robust continuity organizer.

This does not eliminate temporal modeling, center-frame detail, or orientation support as families. It narrows the exact ABI-276 integration point: injecting full-resolution center-detail state beside the temporal line state at all encoder scales is insufficient by itself to close the ABI-274 connectivity gap. ABI-274 remains the temporal recall/source-balance comparator, ABI-223 remains the cleaner temporal connectivity comparator, ABI-255 remains the compact recurrent temporal comparator, ABI-249 remains the high-precision C4 whole-validation comparator, and ABI-202 remains the aggregate whole-validation reference.

## Decision

Do not promote ABI-276, do not request temporal-eligible failure-bucket diagnostics, and do not request a late-improving budget for this exact center-detail injection branch. Although the best checkpoint is near the exploratory ceiling, the branch failed its success criteria: it did not improve connectivity over ABI-274, did not preserve ABI-274 recall/source balance, and did not beat ABI-254's center-detail temporal-attention scout on the continuity signal.

Do not repeat ABI-276 unchanged. Future work should be mechanism-changing and should either return to ABI-223/238-style temporal attention with architecture-level evidence sharpening, or broaden to a different recall-preserving calibration/dual-evidence or selective orientation-consensus mechanism that raises true contrail logits without widening negative-patch clutter or moving thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, coordinates, or resource scheduling into Candidate code.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_212900_56562e/candidate/PROPOSAL.md`
- `run_20260912_212900_56562e/candidate/README.md`
- `run_20260912_212900_56562e/candidate/manifest.yaml`
- `run_20260912_212900_56562e/resolved_manifest.yaml`
- `run_20260912_212900_56562e/outputs/model_summary.json`
- `run_20260912_212900_56562e/outputs/best_metrics.json`
- `run_20260912_212900_56562e/outputs/final_metrics.json`
- `run_20260912_212900_56562e/outputs/metrics.jsonl`
- `run_20260912_212900_56562e/outputs/resource_profile.json`
- `run_20260912_212900_56562e/outputs/validation_postprocessing/index.json`
- `run_20260912_212900_56562e/outputs/prediction_samples/samples.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` for ABI-274 diagnostic comparison context
- `run_20260912_203536_240ad8/outputs/best_metrics.json` for ABI-275 C4 bridge comparison context
- `run_20260911_202724_fee837/outputs/best_metrics.json` for ABI-254 center-detail temporal-attention comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_210922_27f346/outputs/best_metrics.json` for ABI-255 recurrent temporal comparator context
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
