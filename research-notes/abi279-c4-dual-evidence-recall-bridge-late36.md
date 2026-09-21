# ABI-279 C4 dual-evidence recall bridge late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-279, Candidate `abi279_fullspectral_btd_sza_c4_dual_evidence_recall_bridge_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260913_000141_3344db`.

ABI-279 was a close, mechanism-changing continuation of ABI-249. It kept the full-spectral BTD+SZA front end, signed-detail U-Net body, ASPP context, C4 steerable line context, source-balanced training policy, BCE-Dice primary loss, and trusted Line/Centerline auxiliary heads, but replaced the final mask head with a bounded dual-evidence recall bridge:

`mask_logits = region_logits + 0.20*tanh(line_logits) + 0.15*gate*tanh(detail_logits)`

The hypothesis was that ABI-249's high-precision orientation prior could recover fixed-threshold recall and connected thin-line support without candidate-owned thresholding, morphology, postprocessing, or Artifact Filtering.

## Execution result

ABI-279 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs.
- Parent budget evidence: ABI-249, Run `run_20260911_111909_dd7ef7`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,880,854, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 8.55 / 9.96 GB.
- Training wall time: 4,018.6 s; validation wall time: 3,976.6 s; total Run wall time: 7,997.3 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 22.

This is valid finite capped validation evidence. It is not full-data promotion evidence.

## Best-validation metrics

| Metric | ABI-279 best epoch 22 | ABI-249 C4 best epoch 31 | ABI-202 aggregate reference best epoch 34 |
| --- | ---: | ---: | ---: |
| Filtered Dice | 0.414518 | 0.416400 | 0.427570 |
| Raw Dice | 0.429448 | 0.432320 | 0.442746 |
| Filtered precision | 0.442551 | 0.480886 | 0.439467 |
| Filtered recall | 0.389825 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.439185 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.398381 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.457385 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003192 | 0.002767 | 0.003433 |

Relative to ABI-249's selected checkpoint, ABI-279 traded precision for recall/connectivity: filtered Dice was slightly lower by about -0.0019, precision was lower by about -0.0383, recall was higher by about +0.0227, connectivity was higher by about +0.0467, MIT filtered Dice was slightly higher by about +0.0019, and Google filtered Dice was lower by about -0.0115. Predicted-positive fraction increased modestly from 0.00277 to 0.00319.

Relative to ABI-202, ABI-279 remained below the aggregate reference by about -0.0131 filtered Dice and -0.0265 recall, with similar precision and somewhat lower connectivity. It is therefore not a replacement for ABI-202 on capped evidence.

## Learning trajectory

Selected epoch 22 was a real mid-run peak rather than final-epoch selection. The late trajectory remained finite but oscillatory:

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.191849 | 0.211180 | 0.160467 | 0.140828 | 0.300842 | 0.118403 | 0.007741 |
| 6 | 0.372171 | 0.362023 | 0.397251 | 0.412011 | 0.339356 | 0.315299 | 0.002985 |
| 12 | 0.364987 | 0.347711 | 0.408454 | 0.461197 | 0.301989 | 0.348989 | 0.002373 |
| 18 | 0.365553 | 0.349477 | 0.404466 | 0.454639 | 0.305659 | 0.387666 | 0.002436 |
| 21 | 0.404326 | 0.393250 | 0.435096 | 0.403821 | 0.404832 | 0.424841 | 0.003633 |
| 22 | 0.414518 | 0.398381 | 0.457385 | 0.442551 | 0.389825 | 0.439185 | 0.003192 |
| 29 | 0.397309 | 0.383927 | 0.429624 | 0.398925 | 0.395705 | 0.334247 | 0.003594 |
| 31 | 0.397236 | 0.376746 | 0.451236 | 0.490620 | 0.333716 | 0.483878 | 0.002465 |
| 36 | 0.413490 | 0.397566 | 0.454414 | 0.442199 | 0.388281 | 0.429966 | 0.003182 |

The bridge remained non-collapsed and recovered much of the selected-epoch behavior by epoch 36, but it did not show a clean late upward trajectory after epoch 22. Some later checkpoints had very high connectivity with lower recall or lower Dice, suggesting an unstable precision/recall/connectivity balance rather than a clearly superior head.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 1.0, 1.0, approximately 0.0, and 1.0. This only confirms finite non-collapsed retained examples; it does not justify qualitative claims about the full validation population. This note does not reproduce raw samples, images, coordinates, scene identifiers, or patch identities.

At the selected checkpoint, raw Dice was 0.429448 and filtered Dice was 0.414518. Raw predicted-positive fraction was 0.003413 versus filtered predicted-positive fraction 0.003192, so Artifact Filters reduced the score and did not create the Result.

## Interpretation

Classify ABI-279 as a finite, partially positive C4-family continuation. The bounded dual-evidence bridge accomplished the intended recall/connectivity movement relative to ABI-249's compact high-precision selected checkpoint, and it slightly improved MIT capped filtered Dice, but the gain came with a meaningful precision drop and lower Google Dice. It remains behind ABI-202 in aggregate filtered Dice and recall.

This is enough evidence to justify trusted whole-validation failure-bucket diagnostics before spending another Run in this exact C4 recall-bridge branch. It is not enough to promote ABI-279, and it does not justify an unchanged late36 continuation because this Run already used the approved late-improving budget.

The useful mechanism signal is that C4 orientation context plus bounded line/detail residual support can raise fixed-threshold recall and connectivity without a large predicted-positive explosion. The unresolved weakness is calibration/source balance: the bridge reduces ABI-249's precision advantage and still does not recover ABI-202-level recall.

## Decision

Do not promote ABI-279 on capped evidence. Do not repeat ABI-279 unchanged. The next appropriate primary handoff is a bounded Evaluation Request for whole-validation failure-bucket diagnostics of Run `run_20260913_000141_3344db`, comparing against ABI-249 and ABI-202, if the campaign continues this branch.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_000141_3344db/candidate/PROPOSAL.md`
- `run_20260913_000141_3344db/candidate/README.md`
- `run_20260913_000141_3344db/candidate/manifest.yaml`
- `run_20260913_000141_3344db/candidate/budget_request.yaml`
- `run_20260913_000141_3344db/resolved_manifest.yaml`
- `run_20260913_000141_3344db/outputs/model_summary.json`
- `run_20260913_000141_3344db/outputs/best_metrics.json`
- `run_20260913_000141_3344db/outputs/final_metrics.json`
- `run_20260913_000141_3344db/outputs/metrics.jsonl`
- `run_20260913_000141_3344db/outputs/resource_profile.json`
- `run_20260913_000141_3344db/outputs/validation_postprocessing/index.json`
- `run_20260913_000141_3344db/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 C4 comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
