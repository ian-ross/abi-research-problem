# ABI-323 temporal-attention logit-consensus floor late36

research-figures: []

## Scope

This note records ABI-323, Candidate `abi323_temporal_attention_logit_consensus_floor_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260916_164624_1768fd`.

ABI-323 was a close continuation of the ABI-223 compact three-frame temporal-attention U-Net family. It kept the provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-1, 0, 1]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The intended mechanism change was a bounded architecture-internal logit-consensus floor: line, centerline, high-resolution detail, and decoder-context evidence could add a small non-negative residual to the mask logit, attenuated by a learned conflict gate.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable to the full-validation ABI-202/249 frontier.

## Execution result

ABI-323 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-223 (`run_20260908_154531_8c7e2b`) and ABI-321 (`run_20260915_183315_3f1d30`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,178,951, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 3,759,439,872 / 4,076,863,488 bytes.
- Training wall time: 3,270.3 s; validation wall time: 3,114.5 s; total Run wall time: 6,386.8 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 34.

## Best-validation metrics

| Metric | ABI-323 consensus floor | ABI-223 temporal attention | Delta vs ABI-223 | ABI-321 detail sharpening | Delta vs ABI-321 | ABI-311 five-frame C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | -2 | 8 | +26 | 27 |
| Filtered Dice | 0.410164 | 0.419776 | -0.009612 | 0.380685 | +0.029480 | 0.425000 |
| MIT filtered Dice | 0.393764 | 0.398498 | -0.004734 | 0.367130 | +0.026634 | 0.403831 |
| Google filtered Dice | 0.452657 | 0.476764 | -0.024107 | 0.416557 | +0.036100 | 0.482615 |
| Filtered precision | 0.453704 | 0.483764 | -0.030060 | 0.455716 | -0.002012 | 0.459703 |
| Filtered recall | 0.374249 | 0.370738 | +0.003511 | 0.326867 | +0.047382 | 0.395169 |
| Filtered connectivity | 0.259715 | 0.412427 | -0.152712 | 0.338630 | -0.078915 | 0.366735 |
| Filtered predicted-positive fraction | 0.004264 | 0.003962 | +0.000302 | 0.003708 | +0.000556 | 0.004444 |

ABI-323 partially achieved the threshold-recall intent relative to ABI-223, but only by a very small amount and with clear losses in aggregate filtered Dice, precision, Google performance, and especially connectivity. Relative to ABI-321, the longer-budget ABI-223-style consensus floor is much stronger on aggregate/source Dice and recall, but it still loses ABI-321's already-limited connectivity signal. Relative to ABI-311, ABI-323 is lower on aggregate/source Dice, precision, recall, and connectivity while retaining a slightly smaller footprint.

At the selected checkpoint, raw Dice was 0.428218 versus filtered Dice 0.410164, raw recall was 0.404770 versus filtered recall 0.374249, and raw predicted-positive fraction was 0.004603 versus filtered predicted-positive fraction 0.004264. Artifact Filters reduce the predicted footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.175806 | 0.167347 | 0.198780 | 0.451340 | 0.109164 | 0.384731 | 0.001250 |
| 6 | 0.333926 | 0.335966 | 0.329413 | 0.292741 | 0.388598 | 0.181034 | 0.006862 |
| 10 | 0.380960 | 0.365646 | 0.418201 | 0.423056 | 0.346483 | 0.279520 | 0.004234 |
| 14 | 0.235490 | 0.216593 | 0.288353 | 0.546469 | 0.150083 | 0.362576 | 0.001420 |
| 17 | 0.395175 | 0.373602 | 0.452267 | 0.443540 | 0.356320 | 0.270615 | 0.004153 |
| 20 | 0.403288 | 0.381237 | 0.461147 | 0.472667 | 0.351669 | 0.282290 | 0.003846 |
| 25 | 0.400319 | 0.378317 | 0.457658 | 0.478758 | 0.343965 | 0.259241 | 0.003714 |
| 29 | 0.401428 | 0.379635 | 0.457312 | 0.432349 | 0.374635 | 0.244588 | 0.004479 |
| 30 | 0.406637 | 0.383151 | 0.467050 | 0.486210 | 0.349447 | 0.290838 | 0.003715 |
| 33 | 0.397770 | 0.373587 | 0.461160 | 0.512242 | 0.325115 | 0.333416 | 0.003281 |
| 34 | 0.410164 | 0.393764 | 0.452657 | 0.453704 | 0.374249 | 0.259715 | 0.004264 |
| 35 | 0.359101 | 0.330256 | 0.434253 | 0.505540 | 0.278445 | 0.321190 | 0.002847 |
| 36 | 0.397587 | 0.377763 | 0.447820 | 0.445805 | 0.358781 | 0.235208 | 0.004160 |

The trajectory is finite and non-collapsed but unstable. ABI-323 climbs into the 0.40 filtered-Dice band late, selecting epoch 34, but several high-connectivity epochs do not coincide with the best Dice/source-balance point. The final epoch remains finite but falls below the selected checkpoint on filtered Dice, MIT/Google Dice, recall, and connectivity. This does not provide a clean late-improvement argument for another unchanged continuation.

The consensus floor behaved more like a mild recall/footprint lift than a robust line-continuity mechanism. It did not reproduce ABI-223's connectivity, and the best epoch's connectivity is also below recent temporal C4 comparators ABI-306/309/311.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4280, 0.1166, 0.3891, and 0.3608. This confirms finite non-collapsed predictions, with one weak retained sample, but does not provide qualitative support for promotion.

## Interpretation

Classify ABI-323 as a valid but not frontier-improving temporal-attention continuation. It improves strongly over ABI-321's shallow detail-sharpening scout and shows that the late36 temporal-attention branch can remain finite with a small architecture-head modification. However, it does not improve the ABI-223 comparator in the way required: the small recall gain is outweighed by lower filtered Dice, lower precision, weaker Google performance, and a large connectivity regression.

The main lesson is that architecture-internal consensus-floor calibration is not enough to recover connected thin-line continuity for the temporal-attention family. The branch is useful as negative evidence against further minor output-head variants that try to raise fixed-threshold logits without changing temporal alignment, continuity modeling, or cross-scale evidence construction.

Comparator roles after ABI-323:

- ABI-223 remains the temporal-attention diagnostic comparator.
- ABI-311 remains the balanced five-frame temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 comparator.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-321 is superseded as weak/early negative temporal-attention detail-head evidence.
- ABI-323 is negative evidence for a bounded logit-consensus floor as the next temporal-attention improvement mechanism.

## Decision

Do not promote ABI-323. Do not request temporal-eligible failure-bucket diagnostics for this capped Result: aggregate/source metrics and the connectivity regression already answer the stated hypothesis. Do not submit another unchanged ABI-223-style gated output-head/logit-floor continuation.

Future work should be mechanism-changing. Reasonable next directions are either a temporal architecture with explicit alignment/change evidence that preserves connectivity, or a return to single-frame ABI-249-style C4/orientation support paired with cross-scale/detail recall support. If temporal work continues, it should target connected-line continuity directly rather than only raising logits at the final head.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260916_164624_1768fd/candidate/PROPOSAL.md`
- `run_20260916_164624_1768fd/candidate/README.md`
- `run_20260916_164624_1768fd/candidate/manifest.yaml`
- `run_20260916_164624_1768fd/candidate/budget_request.yaml`
- `run_20260916_164624_1768fd/resolved_manifest.yaml`
- `run_20260916_164624_1768fd/execution.json`
- `run_20260916_164624_1768fd/outputs/model_summary.json`
- `run_20260916_164624_1768fd/outputs/best_metrics.json`
- `run_20260916_164624_1768fd/outputs/final_metrics.json`
- `run_20260916_164624_1768fd/outputs/metrics.jsonl`
- `run_20260916_164624_1768fd/outputs/resource_profile.json`
- `run_20260916_164624_1768fd/outputs/validation_postprocessing/index.json`
- `run_20260916_164624_1768fd/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260915_183315_3f1d30/outputs/best_metrics.json` and `/history/research-notes/abi321-temporal-attention-center-detail-evidence-sharpening-unet.md` for ABI-321 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
