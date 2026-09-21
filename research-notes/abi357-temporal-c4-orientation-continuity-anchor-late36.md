# ABI-357 temporal C4 orientation-continuity anchor late36

research-figures: []

## Scope

This note records ABI-357, Candidate `abi357_temporal_c4_orientation_continuity_anchor_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_123025_7cd861`.

ABI-357 was a close, mechanism-changing late-improving continuation after ABI-356 and ABI-350. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural question was whether ABI-356's recall-positive multi-scale temporal change/detail fusion could be constrained by a compact C4 rotation-shared orientation-continuity anchor, preserving true-positive recovery while reducing broad positive footprint and raising connected thin-line continuity.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-357 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Budget request parents: `run_20260919_095725_843317` (ABI-356) and `run_20260919_013306_9ca44e` (ABI-350).
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,674,581, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,728,054,784 / 7,233,077,248 bytes.
- Training wall time: 5,677.4 s; validation wall time: 3,551.6 s; total Run wall time: 9,231.3 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at the final epoch 36.

## Temporal-eligible aggregate metrics

| Metric | ABI-357 C4 continuity anchor | ABI-356 recall parent | ABI-350 line-support late36 | ABI-348 compact five-frame C4 | ABI-324 balanced five-frame C4 | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 36 | 33 | 36 | 27 | 36 |
| Filtered Dice | 0.418378 | 0.426056 | 0.431103 | 0.427829 | 0.429430 | 0.419776 |
| MIT filtered Dice | 0.401020 | 0.411375 | 0.409536 | 0.410244 | 0.408188 | 0.398498 |
| Google filtered Dice | 0.465032 | 0.465688 | 0.490518 | 0.478363 | 0.487231 | 0.476764 |
| Filtered precision | 0.481194 | 0.421447 | 0.494306 | 0.477546 | 0.470412 | 0.483764 |
| Filtered recall | 0.370069 | 0.430766 | 0.382230 | 0.387488 | 0.395017 | 0.370738 |
| Filtered connectivity | 0.350215 | 0.282116 | 0.358283 | 0.300904 | 0.397925 | 0.412427 |
| Filtered predicted-positive pixels | 420,533 | 558,903 | 422,831 | 443,691 | 459,172 | 419,056 |

ABI-357 partially answered the mechanism question, but not in a frontier-positive way. Relative to ABI-356, the C4 continuity anchor sharply constrained the broad recall footprint: filtered predicted-positive pixels fell by 138,370, precision improved by +0.0597, and connectivity improved by +0.0681. That is the intended direction for compactness and connected-line support. The cost was too high: recall fell by -0.0607, MIT filtered Dice by -0.0104, and aggregate filtered Dice by -0.0077. The anchor converted ABI-356's recall-biased state into a compact state rather than preserving recall and adding continuity.

Relative to ABI-350, ABI-357 is almost the same size of prediction footprint but worse on every main aggregate quality dimension: -0.0127 filtered Dice, -0.0085 MIT Dice, -0.0255 Google Dice, -0.0131 precision, -0.0122 recall, and -0.0081 connectivity. ABI-350 remains the stronger compact temporal line-support comparator.

Relative to ABI-348, ABI-357 improves compactness and connectivity (+0.0493 connectivity and 23,158 fewer filtered-positive pixels) with nearly equal precision, but it gives back -0.0174 recall and -0.0095 aggregate filtered Dice. This is useful evidence that the C4 orientation-continuity anchor can raise the connectivity component of compact temporal-C4-like states, but it does not recover enough true positive area to replace ABI-348 or ABI-324.

At the selected checkpoint, raw Dice was 0.436985 versus filtered Dice 0.418378, raw recall was 0.399909 versus filtered recall 0.370069, and raw predicted-positive pixels were 454,023 versus 420,533 filtered. Artifact Filters removed 33,490 predicted-positive pixels and lowered the primary score, so the Result is not being created by postprocessing.

The retained fixed first-four validation samples had raw sample Dice values 0.2866, 0.6481, 0.6099, and 0.4937. These are traceability artifacts only and do not override aggregate validation metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218162 | 0.219168 | 0.216008 | 0.229908 | 0.207558 | 0.161471 | 0.004667 |
| 5 | 0.345780 | 0.324419 | 0.398397 | 0.440335 | 0.284655 | 0.282378 | 0.003342 |
| 10 | 0.379867 | 0.356478 | 0.438685 | 0.429255 | 0.340671 | 0.279884 | 0.004103 |
| 15 | 0.395523 | 0.371917 | 0.456442 | 0.470849 | 0.340975 | 0.369814 | 0.003744 |
| 20 | 0.382080 | 0.357937 | 0.446456 | 0.518267 | 0.302572 | 0.281635 | 0.003018 |
| 25 | 0.387224 | 0.362867 | 0.452533 | 0.531897 | 0.304423 | 0.354240 | 0.002959 |
| 30 | 0.380214 | 0.357312 | 0.437936 | 0.481295 | 0.314221 | 0.290580 | 0.003375 |
| 31 | 0.390829 | 0.365026 | 0.458574 | 0.500540 | 0.320565 | 0.310971 | 0.003311 |
| 32 | 0.360051 | 0.335054 | 0.421988 | 0.468818 | 0.292249 | 0.266931 | 0.003223 |
| 33 | 0.409168 | 0.383567 | 0.477172 | 0.519996 | 0.337282 | 0.369591 | 0.003353 |
| 34 | 0.396935 | 0.373932 | 0.457294 | 0.459923 | 0.349122 | 0.309175 | 0.003924 |
| 35 | 0.391707 | 0.367458 | 0.456296 | 0.539178 | 0.307581 | 0.362000 | 0.002949 |
| 36 | 0.418378 | 0.401020 | 0.465032 | 0.481194 | 0.370069 | 0.350215 | 0.003976 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The final epoch is the selected checkpoint and the only checkpoint that combines aggregate filtered Dice above 0.418 with MIT Dice above 0.40. The late trajectory is nevertheless oscillatory. Epochs 20, 25, 33, and 35 find compact high-precision states with weak recall; epoch 33 reaches the strongest connectivity but still only 0.337 recall. The final epoch recovers some recall while retaining a compact footprint, but it does not reach ABI-350/324 aggregate quality or ABI-223/324 connectivity.

This pattern supports a precise failure classification: the C4 orientation-continuity anchor is not an implementation or resource failure, and it is not a prediction collapse. It is mixed-negative scientific evidence for this exact branch. The anchor constrains broad recall evidence and improves connectivity versus ABI-356, but it over-constrains positive-tail coverage and does not produce the intended recall-preserving continuity gain.

## Interpretation

Classify ABI-357 as a finite, resource-safe, mixed-negative late-budget continuation. The result is useful because it isolates a real trade-off in the current temporal branch: compact C4/orientation continuity support can raise precision and connectivity relative to broad temporal-attention recall, but the current implementation suppresses too much recall to improve capped temporal-eligible filtered Dice.

Do not promote ABI-357. It is below ABI-350, ABI-348, ABI-324, ABI-356, and ABI-223 on aggregate temporal-eligible filtered Dice, and it does not become a new comparator on connectivity. ABI-350 remains the compact line-support temporal comparator in this local line of work; ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator; ABI-223 remains the temporal-attention connectivity comparator; ABI-356 remains recall-biased diagnostic evidence rather than a comparator.

Do not run another unchanged late36 continuation of ABI-357, and do not spend a Run on a simple anchor-strength, gate-threshold, or final-head shuffle. If this branch continues, it should be mechanism-changing: decouple the compact C4 continuity anchor from recall evidence so the anchor protects line continuity without vetoing true positives, or move continuity support into an earlier center-detail/temporal-alignment path rather than using it as a late constraining path. Another reasonable broadening direction is a different temporal alignment or lightweight backbone mechanism that raises threshold-0.5 true-positive evidence while preserving compact negative-patch behavior.

ABI-357 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-357 and do not request a Post-Run Evaluation for this Run in this Autonomy Step. The capped aggregate result is sufficient to reject the exact recall-preserving continuity-anchor hypothesis as non-frontier: it improves compactness/connectivity versus ABI-356 but loses too much recall and does not beat the stronger temporal comparators. A future operator or Autonomy Step may request failure-bucket diagnostics only if the campaign specifically needs negative-patch or source-tail evidence for this exact anchor, but no such diagnostic is needed to choose the next research direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_123025_7cd861/candidate/PROPOSAL.md`
- `run_20260919_123025_7cd861/candidate/README.md`
- `run_20260919_123025_7cd861/candidate/manifest.yaml`
- `run_20260919_123025_7cd861/candidate/budget_request.yaml`
- `run_20260919_123025_7cd861/resolved_manifest.yaml`
- `run_20260919_123025_7cd861/execution.json`
- `run_20260919_123025_7cd861/run_metadata.json`
- `run_20260919_123025_7cd861/outputs/model_summary.json`
- `run_20260919_123025_7cd861/outputs/best_metrics.json`
- `run_20260919_123025_7cd861/outputs/final_metrics.json`
- `run_20260919_123025_7cd861/outputs/metrics.jsonl`
- `run_20260919_123025_7cd861/outputs/resource_profile.json`
- `run_20260919_123025_7cd861/outputs/validation_postprocessing/index.json`
- `run_20260919_123025_7cd861/outputs/prediction_samples/samples.json`
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 parent context
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260918_215534_a35ab9/outputs/best_metrics.json` and `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md` for ABI-348 comparator context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
