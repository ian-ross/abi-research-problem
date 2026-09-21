# ABI-368 temporal recurrent C4 connectivity decoder late36

research-figures: []

## Scope

This note records ABI-368, Candidate `abi368_temporal_recurrent_c4_connectivity_decoder_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_135212_ff1f2a`.

ABI-368 was a mechanism-changing temporal recurrent-family continuation of ABI-255. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 2. The architectural question was whether adding a final C4 orientation-shared connectivity decoder to the compact ConvGRU recurrent temporal U-Net could address ABI-255's thin-line continuity weakness without changing trusted data, losses, metrics, thresholds, postprocessing, Artifact Filters, sampling, temporal provisioning, or coordinates.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-368 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested late-improving budget was approved.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Budget parent: `run_20260911_210922_27f346` (ABI-255).
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,227,164, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,314,738,176 / 4,506,779,648 bytes.
- Training wall time: 3,602.3 s; validation wall time: 3,300.2 s; total Run wall time: 6,904.5 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Temporal-eligible aggregate metrics

| Metric | ABI-368 recurrent C4 decoder | ABI-255 recurrent parent | ABI-223 temporal attention | ABI-350 line support | ABI-359 early C4 alignment | ABI-367 detail tail | ABI-356 recall parent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 36 | 36 | 33 | 27 | 27 | 36 |
| Filtered Dice | 0.419767 | 0.417348 | 0.419776 | 0.431103 | 0.426759 | 0.420955 | 0.426056 |
| MIT filtered Dice | 0.402286 | 0.400833 | 0.398498 | 0.409536 | 0.406428 | 0.404132 | 0.411375 |
| Google filtered Dice | 0.464166 | 0.463143 | 0.476764 | 0.490518 | 0.481165 | 0.465751 | 0.465688 |
| Filtered precision | 0.421074 | 0.468293 | 0.483764 | 0.494306 | 0.474933 | 0.459504 | 0.421447 |
| Filtered recall | 0.418469 | 0.376400 | 0.370738 | 0.382230 | 0.387459 | 0.388373 | 0.430766 |
| Filtered connectivity | 0.240897 | 0.281116 | 0.412427 | 0.358283 | 0.376348 | 0.245025 | 0.282116 |
| Filtered predicted-positive pixels | 543,430 | 439,511 | 419,056 | 422,831 | 446,099 | 462,166 | 558,903 |

ABI-368 is finite and source-informative, but it is negative evidence for the stated C4 connectivity-decoder hypothesis. Relative to the recurrent parent ABI-255, it slightly improves aggregate filtered Dice (+0.0024), MIT Dice (+0.0015), Google Dice (+0.0010), and recall (+0.0421), but this comes with much lower precision (-0.0472), a much broader footprint (+103,919 filtered-positive pixels), and worse connectivity (-0.0402). The final C4 decoder did not solve ABI-255's thin-line continuity weakness.

The near tie with ABI-223 on aggregate filtered Dice is misleading for the intended mechanism. ABI-368 is lower than ABI-223 by only -0.000008 aggregate Dice and has higher MIT Dice and recall, but it loses substantial Google Dice (-0.0126), precision (-0.0627), and especially connectivity (-0.1715), while predicting +124,374 more filtered-positive pixels. Relative to ABI-350 and ABI-359, ABI-368 is clearly weaker on aggregate/source Dice, precision, and connected-line continuity. Relative to ABI-367, it trades a small amount of aggregate/source Dice and connectivity for higher recall and a much broader prediction footprint. Relative to ABI-356, ABI-368 is slightly more compact but does not exceed the recall parent on recall, Dice, source balance, or connectivity.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.436175 versus filtered Dice 0.419767, raw recall was 0.451848 versus filtered recall 0.418469, and raw predicted-positive pixels were 586,109 versus 543,430 filtered. Artifact Filters removed 42,679 predicted-positive pixels and lowered the score.

The retained fixed `first_n` prediction samples have nonzero per-sample Dice values of 0.4638, 0.2490, 0.4650, and 0.3502. They do not indicate all-negative or all-positive qualitative collapse, but they are only the first four validation samples and should not override the aggregate temporal-eligible metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.229929 | 0.223288 | 0.245257 | 0.303043 | 0.185237 | 0.204015 | 334,243 |
| 6 | 0.361600 | 0.351096 | 0.386963 | 0.342866 | 0.382501 | 0.254107 | 610,023 |
| 12 | 0.369948 | 0.347742 | 0.424979 | 0.438356 | 0.320009 | 0.216390 | 399,185 |
| 15 | 0.395562 | 0.373868 | 0.450580 | 0.462002 | 0.345828 | 0.308546 | 409,312 |
| 22 | 0.409889 | 0.392678 | 0.454353 | 0.424103 | 0.396597 | 0.241599 | 511,348 |
| 27 | 0.408460 | 0.384337 | 0.472382 | 0.495222 | 0.347567 | 0.340818 | 383,775 |
| 29 | 0.411252 | 0.387341 | 0.473757 | 0.512718 | 0.343312 | 0.340841 | 366,141 |
| 31 | 0.320242 | 0.292516 | 0.390537 | 0.487468 | 0.238444 | 0.221560 | 267,472 |
| 34 | 0.415963 | 0.395613 | 0.470667 | 0.491740 | 0.360422 | 0.324577 | 400,787 |
| 35 | 0.356991 | 0.329119 | 0.428843 | 0.510122 | 0.274570 | 0.249765 | 294,318 |
| 36 | 0.419767 | 0.402286 | 0.464166 | 0.421074 | 0.418469 | 0.240897 | 543,430 |

The late budget was useful as evidence because the selected checkpoint arrived at the final epoch and the branch materially changed after the exploratory epoch-12 boundary. The trajectory nevertheless shows the same recurrent/temporal-line pattern observed in prior notes: compact precision/connectivity states and broad recall states appear in different epochs rather than combining.

Epochs 27, 29, and 34 are more compact and have better precision/connectivity than the selected epoch, but they give up recall and do not beat the temporal-frontier aggregate metrics. Epoch 36 reaches the best aggregate score by broadening into a high-recall, low-connectivity state. The final C4 connectivity decoder can produce moderate orientation/continuity signal at some epochs, but the selected fixed-threshold Result does not preserve it.

## Interpretation

Classify ABI-368 as a finite, resource-safe, mixed-negative recurrent temporal family-development result. It mildly improves the ABI-255 recurrent branch on aggregate/source Dice and fixed-threshold recall, and the final-epoch selection confirms that the recurrent family can still be late-maturing. However, the specific hypothesis was to improve thin-line continuity through a final C4 orientation-shared connectivity decoder. That hypothesis is not supported: connectivity regresses versus ABI-255 and remains far below ABI-223/350/359.

Do not promote ABI-368. Do not spend another Run on an unchanged recurrent C4 decoder late36 continuation, gate-strength tweak, auxiliary-weight shuffle, or minor width variant. The exact attachment point appears to trade recurrent compactness and connectivity for recall breadth rather than resolving the recurrent family's thin-line weakness.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-368 is near ABI-223 on aggregate capped temporal-eligible Dice and modestly improves ABI-255 overlap/recall, but its intended connectivity signal is weak and prior temporal-eligible diagnostics already show the relevant failure mode: high aggregate scores can still hide MIT-positive-tail and connected-line deficits. If recurrent temporal work continues, it should be mechanism-changing rather than a local C4-decoder repeat, for example a line-aware recurrent state, an earlier temporal alignment/continuity path, or a source-agnostic dual-evidence head that raises true contrail logits at threshold 0.5 without broadening negative-patch clutter. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_135212_ff1f2a/candidate/PROPOSAL.md`
- `run_20260920_135212_ff1f2a/candidate/README.md`
- `run_20260920_135212_ff1f2a/candidate/manifest.yaml`
- `run_20260920_135212_ff1f2a/candidate/budget_request.yaml`
- `run_20260920_135212_ff1f2a/resolved_manifest.yaml`
- `run_20260920_135212_ff1f2a/execution.json`
- `run_20260920_135212_ff1f2a/run_metadata.json`
- `run_20260920_135212_ff1f2a/outputs/model_summary.json`
- `run_20260920_135212_ff1f2a/outputs/best_metrics.json`
- `run_20260920_135212_ff1f2a/outputs/final_metrics.json`
- `run_20260920_135212_ff1f2a/outputs/metrics.jsonl`
- `run_20260920_135212_ff1f2a/outputs/resource_profile.json`
- `run_20260920_135212_ff1f2a/outputs/validation_postprocessing/index.json`
- `run_20260920_135212_ff1f2a/outputs/prediction_samples/samples.json`
- `run_20260911_210922_27f346/outputs/best_metrics.json` and `/history/research-notes/abi255-temporal-recurrent-change-state-unet-late36.md` for ABI-255 recurrent-parent context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 temporal-attention comparator context
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 line-support comparator context
- `run_20260919_175950_ac7b89/outputs/best_metrics.json` and `/history/research-notes/abi359-temporal-alignment-c4-center-detail-bridge-late36.md` for ABI-359 early-C4 comparator context
- `run_20260920_112921_1ee9bd/outputs/best_metrics.json` and `/history/research-notes/abi367-temporal-center-detail-tail-support-late36.md` for ABI-367 local temporal-tail comparator context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 recall-parent context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
