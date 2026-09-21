# ABI-363 full-spectral BTD+SZA source-robust detail-support late36

research-figures: []

## Scope

This note records ABI-363, Candidate `abi363_fullspectral_btd_sza_source_robust_detail_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_044100_71b924`.

ABI-363 was a mechanism-changing single-frame family-development continuation after ABI-362. It kept provider-owned `abi_16ch_plus_sza` inputs, trusted source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 4. The architectural question was whether a source-agnostic multi-scale signed-detail tail-support path plus a bounded architecture-internal dual-evidence calibration head could improve MIT/source-balanced fixed-threshold recall and connected thin-line continuity without widening negative-patch clutter.

This is capped representative feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-363 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested `late_improving` budget was approved from late-selecting single-frame parent Runs.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Trusted augmentation policy: `random_mirroring`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,194,054, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 9,329,240,064 / 10,647,240,704 bytes.
- Training wall time: 4,756.3 s; validation wall time: 4,220.7 s; total Run wall time: 8,979.3 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 22.

## Capped best-validation metrics

| Metric | ABI-363 source-robust detail support | ABI-362 decoupled anchor/sidecar | ABI-353 C4 detail agreement | ABI-342 recall bridge | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 22 | 34 | 34 | 36 | 31 | 34 |
| Filtered Dice | 0.406556 | 0.407108 | 0.417439 | 0.415499 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.386570 | 0.390686 | 0.401665 | 0.398614 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.458372 | 0.446130 | 0.456492 | 0.460044 | 0.468855 | 0.468151 |
| Filtered precision | 0.425509 | 0.417976 | 0.442512 | 0.397609 | 0.480886 | 0.439467 |
| Filtered recall | 0.389220 | 0.396791 | 0.395056 | 0.435075 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.363194 | 0.359966 | 0.348271 | 0.405280 | 0.392524 | 0.457773 |
| Filtered predicted-positive pixels | 444,884 | 461,711 | 434,203 | 532,191 | 371,346 | 460,724 |

ABI-363 is finite and source-informative, but it is a negative result for the source-robust detail-tail support hypothesis. Relative to ABI-362 it is effectively tied on aggregate filtered Dice (-0.0006), with better Google Dice (+0.0122), precision (+0.0075), connectivity (+0.0032), and a smaller footprint (-16,827 filtered-positive pixels), but it loses MIT Dice (-0.0041) and recall (-0.0076). That is not the intended MIT/source-balance improvement.

Relative to ABI-353, ABI-363 loses aggregate filtered Dice (-0.0109), MIT Dice (-0.0151), precision (-0.0170), and recall (-0.0058), while only slightly improving Google Dice (+0.0019) and connectivity (+0.0149). Relative to ABI-249, ABI-363 recovers recall (+0.0221), but at large costs in precision (-0.0554), MIT Dice (-0.0099), Google Dice (-0.0105), connectivity (-0.0293), and footprint (+73,538 filtered-positive pixels). Relative to ABI-342, it is more compact and precise but loses too much recall and connectivity to serve as a recall-bridge replacement.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected capped checkpoint, raw Dice was 0.421284 versus filtered Dice 0.406556; raw recall was 0.416369 versus filtered recall 0.389220; raw predicted-positive pixels were 475,014 versus 444,884 filtered. Artifact Filters removed 30,130 predicted-positive pixels and lowered the score.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.205738 | 0.233855 | 0.163371 | 0.150507 | 0.325005 | 0.103511 | 0.007825 |
| 5 | 0.334194 | 0.336553 | 0.329051 | 0.294300 | 0.386599 | 0.228624 | 0.004760 |
| 10 | 0.364308 | 0.348931 | 0.398662 | 0.393226 | 0.339352 | 0.323190 | 0.003127 |
| 12 | 0.386005 | 0.367513 | 0.431593 | 0.421620 | 0.355939 | 0.362782 | 0.003059 |
| 15 | 0.406016 | 0.393599 | 0.438265 | 0.402585 | 0.409506 | 0.403163 | 0.003686 |
| 18 | 0.343952 | 0.318191 | 0.405904 | 0.463257 | 0.273512 | 0.317092 | 0.002139 |
| 21 | 0.395841 | 0.390985 | 0.407453 | 0.368180 | 0.427996 | 0.250531 | 0.004212 |
| 22 | 0.406556 | 0.386570 | 0.458372 | 0.425509 | 0.389220 | 0.363194 | 0.003315 |
| 25 | 0.402697 | 0.392780 | 0.426324 | 0.375857 | 0.433665 | 0.310672 | 0.004181 |
| 28 | 0.398067 | 0.382264 | 0.435971 | 0.418362 | 0.379649 | 0.335780 | 0.003288 |
| 32 | 0.398635 | 0.381035 | 0.439445 | 0.397875 | 0.399398 | 0.324948 | 0.003638 |
| 36 | 0.385120 | 0.364584 | 0.435646 | 0.467381 | 0.327482 | 0.384409 | 0.002539 |

The trajectory is finite but unstable. The late budget was useful in the limited sense that the best checkpoint arrives after the exploratory epoch-12 boundary, and several epochs after 12 remain competitive. However, the intended support mechanisms do not converge toward a stable better operating point. Epoch 15 has the strongest local aggregate/source/connectivity mix, epoch 21/25 has broader recall but lower precision or Google Dice, epoch 22 is the selected Google-supported checkpoint, and epoch 36 becomes compact/high-precision but recall-poor. The branch repeats the familiar single-frame pattern: recall, compactness, and connectivity appear at different epochs rather than combining in one selected state.

## Interpretation

Classify ABI-363 as a finite, resource-safe, negative single-frame family-development result. The source-agnostic multi-scale signed-detail support path is contract-safe and computationally feasible, but the capped evidence does not support the hypothesis that it improves MIT/source-balanced recall or connected-line continuity while controlling clutter.

The best signal is modest: ABI-363 improves Google Dice and slightly improves precision/connectivity versus ABI-362 while using a smaller footprint. But the proposal's target was MIT/source balance and useful positive-tail recall. On those criteria it regresses versus ABI-362/353/342 and remains below ABI-202/249 comparators. It also does not justify a whole-validation diagnostic: capped aggregate Dice is below ABI-353, ABI-342, ABI-249, and ABI-202, and the source/recall/connectivity trade-off is not compelling enough to spend an evaluation request.

Do not promote ABI-363. Do not run an unchanged late36 continuation, gate-strength tweak, or local head-weight shuffle of this detail-tail support design. Future work should broaden away from this exact source-agnostic detail-tail mechanism. Plausible in-contract directions remain a mechanism-changing temporal-attention/center-detail design that raises true contrail evidence before final logits, a genuinely different lightweight backbone with an explicit line-continuity decoder, or a trusted policy/loss variation only if tied to a specific source-balance or connectivity failure mode. Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of bounds.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_044100_71b924/candidate/PROPOSAL.md`
- `run_20260920_044100_71b924/candidate/README.md`
- `run_20260920_044100_71b924/candidate/manifest.yaml`
- `run_20260920_044100_71b924/candidate/budget_request.yaml`
- `run_20260920_044100_71b924/resolved_manifest.yaml`
- `run_20260920_044100_71b924/execution.json`
- `run_20260920_044100_71b924/run_metadata.json`
- `run_20260920_044100_71b924/outputs/model_summary.json`
- `run_20260920_044100_71b924/outputs/best_metrics.json`
- `run_20260920_044100_71b924/outputs/final_metrics.json`
- `run_20260920_044100_71b924/outputs/metrics.jsonl`
- `run_20260920_044100_71b924/outputs/resource_profile.json`
- `run_20260920_044100_71b924/outputs/validation_postprocessing/index.json`
- `run_20260920_044100_71b924/outputs/prediction_samples/samples.json`
- `run_20260920_020446_9c2fa1/outputs/best_metrics.json` and `/history/research-notes/abi362-fullspectral-btd-sza-c4-decoupled-anchor-recall-sidecar-late36.md` for ABI-362 comparator context
- `run_20260919_053527_64085b/outputs/best_metrics.json` and `/history/research-notes/abi353-fullspectral-btd-sza-c4-crossscale-detail-agreement-late36.md` for ABI-353 comparator context
- `run_20260918_055403_f17232/outputs/best_metrics.json` and `/history/research-notes/abi342-fullspectral-btd-sza-c4-recall-bridge-late36.md` for ABI-342 comparator context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-249 comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-202 reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
