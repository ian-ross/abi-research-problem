# ABI-349 temporal-attention pre-decoder line-support U-Net

research-figures: []

## Scope

This note records ABI-349, Candidate `abi349_temporal_attention_predecoder_line_support_unet_bce_dice_line_centerline_aux_v1`, and Run `run_20260919_004607_f785f8`.

ABI-349 was an exploratory, mechanism-changing temporal-attention family-development Candidate. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architecture moved orientation-aware line support into encoder skip features before decoder fusion, rather than adding another final-logit recall residual.

This is capped temporal-eligible exploratory evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-349 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,132,228, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,244,163,584 / 4,766,826,496 bytes.
- Training wall time: 1,337.6 s; validation wall time: 1,032.9 s; total Run wall time: 2,372.3 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-349 pre-decoder line support | ABI-223 temporal attention late36 | ABI-238 directional temporal attention late36 | ABI-345 center-detail sharpening late36 | ABI-348 compact five-frame C4 late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 36 | 29 | 29 | 36 |
| Filtered Dice | 0.389171 | 0.419776 | 0.420235 | 0.411455 | 0.427829 |
| MIT filtered Dice | 0.369849 | 0.398498 | 0.405383 | 0.391239 | 0.410244 |
| Google filtered Dice | 0.440561 | 0.476764 | 0.460838 | 0.464271 | 0.478363 |
| Filtered precision | 0.478850 | 0.483764 | 0.488730 | 0.425462 | 0.477546 |
| Filtered recall | 0.327784 | 0.370738 | 0.368578 | 0.398342 | 0.387488 |
| Filtered connectivity | 0.337620 | 0.412427 | 0.352239 | 0.286565 | 0.300904 |
| Filtered predicted-positive fraction | 0.003539 | 0.003962 | 0.003899 | 0.004840 | 0.004195 |

ABI-349 is below mature late-budget temporal comparators on aggregate/source Dice and recall. It is not a new comparator and should not be promoted. The useful signal is that the first exploratory pre-decoder line-support scout remained compact and precise: precision is essentially ABI-223/238-like, filtered predicted-positive footprint is smaller than ABI-223/238/345/348, and connectivity is already above ABI-345 and ABI-348 despite only 12 epochs.

The main negative is under-recall. Relative to ABI-223, ABI-349 loses -0.0306 filtered Dice, -0.0286 MIT Dice, -0.0362 Google Dice, -0.0430 recall, and -0.0748 connectivity. Relative to ABI-238, it loses -0.0311 filtered Dice and -0.0408 recall, though the connectivity gap is much smaller (-0.0146). Relative to ABI-345, ABI-349 avoids the broad-footprint/weak-connectivity failure mode, but gives back -0.0706 recall and -0.0223 filtered Dice.

At the selected checkpoint, raw Dice was 0.407479 versus filtered Dice 0.389171, raw recall was 0.354045 versus filtered recall 0.327784, and raw predicted-positive pixels were 403,401 versus 374,305 filtered. Artifact Filters removed 29,096 predicted-positive pixels and lowered the score; they did not create the Result.

## Same-budget trajectory context

Because ABI-349 was exploratory and selected epoch 12, the fair trajectory comparison is favorable relative to prior temporal-attention branches at their epoch-12 checkpoints:

| Epoch-12 metric | ABI-349 | ABI-223 at epoch 12 | ABI-238 at epoch 12 | ABI-345 at epoch 12 |
| --- | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.389171 | 0.359161 | 0.357511 | 0.349272 |
| MIT filtered Dice | 0.369849 | 0.341557 | 0.337837 | 0.325453 |
| Google filtered Dice | 0.440561 | 0.404893 | 0.407224 | 0.409567 |
| Filtered precision | 0.478850 | 0.465419 | 0.470941 | 0.469607 |
| Filtered recall | 0.327784 | 0.292404 | 0.288115 | 0.278028 |
| Filtered connectivity | 0.337620 | 0.275357 | 0.242423 | 0.234459 |
| Filtered positive fraction | 0.003539 | 0.003248 | 0.003163 | 0.003061 |

This is the strongest evidence for ABI-349: at the same epoch ceiling, it is better than ABI-223/238/345 on filtered Dice, both Dataset Sources, precision, recall, and connectivity. The line-support gates did not merely add broad area; they produced a compact, source-informative, non-collapsed checkpoint that is substantially ahead of the historical temporal-attention trajectory at the same budget.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.203872 | 0.203994 | 0.203604 | 0.225416 | 0.186086 | 0.169246 | 0.004268 |
| 2 | 0.251086 | 0.247287 | 0.259302 | 0.250493 | 0.251681 | 0.148810 | 0.005194 |
| 3 | 0.317366 | 0.306454 | 0.342221 | 0.345474 | 0.293488 | 0.230958 | 0.004392 |
| 4 | 0.321451 | 0.300473 | 0.373028 | 0.413913 | 0.262756 | 0.264366 | 0.003282 |
| 5 | 0.339395 | 0.314080 | 0.402970 | 0.440038 | 0.276219 | 0.285813 | 0.003245 |
| 6 | 0.324723 | 0.302965 | 0.379106 | 0.416321 | 0.266163 | 0.289000 | 0.003305 |
| 7 | 0.324195 | 0.295741 | 0.398892 | 0.524006 | 0.234700 | 0.407944 | 0.002315 |
| 8 | 0.378957 | 0.358788 | 0.432057 | 0.420422 | 0.344938 | 0.298873 | 0.004241 |
| 9 | 0.362866 | 0.350301 | 0.392102 | 0.331744 | 0.400432 | 0.195089 | 0.006240 |
| 10 | 0.338813 | 0.316334 | 0.394088 | 0.445136 | 0.273489 | 0.245637 | 0.003176 |
| 11 | 0.336720 | 0.314163 | 0.394653 | 0.464708 | 0.264008 | 0.260769 | 0.002937 |
| 12 | 0.389171 | 0.369849 | 0.440561 | 0.478850 | 0.327784 | 0.337620 | 0.003539 |

The trajectory is finite, non-collapsed, source-informative, and best at the final exploratory epoch. It is noisy: epoch 7 had the highest connectivity but low recall, and epoch 9 had the highest recall but poor precision/connectivity. Epoch 12 is the best aggregate balance and is still improving at the budget boundary. This meets the policy pattern for a possible late-improving continuation: the best checkpoint is at the final exploratory epoch, predictions are finite/non-degenerate, both Dataset Sources are viable, and the trajectory is improving or ambiguous rather than plateaued.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4195, 0.1176, 0.5135, and 0.3633. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-349 as mixed-positive exploratory evidence for pre-decoder line support in the temporal-attention family.

The branch did not yet match the late-budget temporal frontier, so it should not be promoted or treated as a comparator. However, unlike ABI-345, it did not buy recall by broadening the footprint and collapsing continuity. It produced a compact, high-precision, better-than-same-budget temporal-attention trajectory with final-epoch best selection. This supports the core mechanism: adding differentiable orientation-aware line support before decoder fusion is more promising than adding final-head recall residuals after the compact anchor has already been formed.

ABI-349 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-349 and do not request whole-validation evaluation from this exploratory capped Run. The appropriate next action is a close late-improving continuation of the same candidate family, preserving the pre-decoder line-support mechanism and trusted contract settings, because the exploratory result is finite, source-informative, non-collapsed, and best at epoch 12.

If a late continuation is submitted, success should require closing the recall and connectivity gaps to ABI-223/238 without losing ABI-349's compact footprint and source balance. If a 36-epoch continuation plateaus below ABI-223/238 or repeats the epoch-9 broad-recall/low-connectivity state, do not continue simple gate-strength changes; broaden to a different temporal alignment or line-continuity mechanism.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_004607_f785f8/candidate/PROPOSAL.md`
- `run_20260919_004607_f785f8/candidate/README.md`
- `run_20260919_004607_f785f8/candidate/manifest.yaml`
- `run_20260919_004607_f785f8/resolved_manifest.yaml`
- `run_20260919_004607_f785f8/execution.json`
- `run_20260919_004607_f785f8/run_metadata.json`
- `run_20260919_004607_f785f8/outputs/model_summary.json`
- `run_20260919_004607_f785f8/outputs/best_metrics.json`
- `run_20260919_004607_f785f8/outputs/final_metrics.json`
- `run_20260919_004607_f785f8/outputs/metrics.jsonl`
- `run_20260919_004607_f785f8/outputs/resource_profile.json`
- `run_20260919_004607_f785f8/outputs/validation_postprocessing/index.json`
- `run_20260919_004607_f785f8/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 comparison context
- `run_20260918_133432_9e7947/outputs/best_metrics.json` and `/history/research-notes/abi345-temporal-attention-center-detail-evidence-sharpening-late36.md` for ABI-345 comparison context
- `run_20260918_215534_a35ab9/outputs/best_metrics.json` and `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md` for ABI-348 comparison context
- `/history/research-notes/temporal-c4-frontier-reset-after-abi348.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
