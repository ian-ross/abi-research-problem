# ABI-338 temporal soft-band continuity reinjector late36

research-figures: []

## Scope

This note records ABI-338, Candidate `abi338_temporal_softband_continuity_reinjector_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_230319_ed1362`.

ABI-338 was a mechanism-changing family-development continuation of the five-frame temporal C4/detail-consensus branch. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The intended change was a `SoftBandContinuityReinjectorHead`: a bounded positive residual path gated by soft base-mask uncertainty plus learned Line/Centerline/detail/temporal C4 agreement.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a promotion comparison against ABI-202 or ABI-249.

## Execution result

ABI-338 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-324, ABI-337, and ABI-328 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,255,174, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,598,057,472 / 6,968,836,096 bytes.
- Training wall time: 5,345.9 s; validation wall time: 3,475.1 s; total Run wall time: 8,823.4 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-338 soft-band reinjector | ABI-324 balanced parent | Delta vs ABI-324 | ABI-337 no mirroring | ABI-328 soft-shift align | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 27 | +9 | 27 | 36 | 36 |
| Filtered Dice | 0.414875 | 0.429430 | -0.014555 | 0.428894 | 0.423805 | 0.419776 |
| MIT filtered Dice | 0.393182 | 0.408188 | -0.015006 | 0.411838 | 0.403841 | 0.398498 |
| Google filtered Dice | 0.473735 | 0.487231 | -0.013497 | 0.476340 | 0.476913 | 0.476764 |
| Filtered precision | 0.477241 | 0.470412 | +0.006830 | 0.466489 | 0.444466 | 0.483764 |
| Filtered recall | 0.366925 | 0.395017 | -0.028092 | 0.396906 | 0.404980 | 0.370738 |
| Filtered connectivity | 0.352106 | 0.397925 | -0.045819 | 0.365326 | 0.322966 | 0.412427 |
| Filtered predicted-positive pixels | 420,414 | 459,172 | -38,758 | 465,248 | 498,234 | 419,056 |
| Filtered positive fraction | 0.003975 | 0.004341 | -0.000366 | 0.004398 | 0.004710 | 0.003962 |

ABI-338 did not meet its success criteria. The soft-band continuity reinjection path did not raise fixed-threshold recall, MIT balance, or connected-line continuity versus ABI-324. Instead, it selected a more compact/higher-precision operating point: precision rose by about 0.0068 and the filtered footprint shrank by 38,758 pixels, but recall fell by about 0.028 and connectivity fell by about 0.046. Aggregate filtered Dice dropped below ABI-324, ABI-337, ABI-328, and ABI-223 on the same temporal-eligible validation surface.

At the selected checkpoint, raw Dice was 0.432855 versus filtered Dice 0.414875, raw recall was 0.395999 versus filtered recall 0.366925, and raw predicted-positive pixels were 453,695 versus 420,414 filtered. Artifact Filters reduced footprint and score; they did not create the result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 0.394167 | 0.368344 | 0.462331 | 0.505853 | 0.322879 | 0.324879 | 0.003300 |
| 26 | 0.404642 | 0.383477 | 0.461309 | 0.441742 | 0.373291 | 0.310535 | 0.004369 |
| 27 | 0.406542 | 0.386637 | 0.461215 | 0.431196 | 0.384554 | 0.333394 | 0.004610 |
| 28 | 0.389721 | 0.364326 | 0.456509 | 0.517481 | 0.312555 | 0.331727 | 0.003122 |
| 29 | 0.403105 | 0.384282 | 0.450837 | 0.391287 | 0.415658 | 0.249754 | 0.005492 |
| 30 | 0.372822 | 0.346257 | 0.443159 | 0.526512 | 0.288584 | 0.329765 | 0.002833 |
| 31 | 0.396124 | 0.375412 | 0.448819 | 0.473696 | 0.340384 | 0.248190 | 0.003715 |
| 32 | 0.380392 | 0.353166 | 0.453676 | 0.543477 | 0.292592 | 0.351432 | 0.002783 |
| 33 | 0.406780 | 0.386322 | 0.462855 | 0.515207 | 0.336055 | 0.358121 | 0.003372 |
| 34 | 0.405194 | 0.388493 | 0.451412 | 0.463979 | 0.359630 | 0.239546 | 0.004007 |
| 35 | 0.369770 | 0.348650 | 0.426214 | 0.487724 | 0.297759 | 0.308664 | 0.003156 |
| 36 | 0.414875 | 0.393182 | 0.473735 | 0.477241 | 0.366925 | 0.352106 | 0.003975 |

The trajectory remained finite, source-informative, and non-collapsed, but it was oscillatory. The final epoch was the best aggregate checkpoint, so the late-improving budget was useful for observing the branch. However, even the best late checkpoint stayed below ABI-324 and did not recover the intended recall/connectivity trade-off. Several late epochs show the recurring temporal C4 failure mode: broader recall states have low connectivity, while compact states improve precision or connectivity without enough recall.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3994, 0.0390, 0.5651, and 0.3729. These confirm finite non-collapsed predictions, but the weak second retained example and the aggregate metrics do not support a hidden favorable outcome.

## Interpretation

Classify ABI-338 as negative capped temporal-family evidence for the soft-band continuity reinjection mechanism. The branch stayed resource-safe and numerically healthy, but the added uncertainty-band residual appears to make the operating point more compact rather than improving true-line recall or continuity. It does not improve the key ABI-324 weaknesses and does not displace ABI-324 as the balanced five-frame temporal C4/detail-consensus comparator.

Comparator roles after ABI-338:

- ABI-324 remains the strongest local balanced five-frame temporal C4/detail-consensus comparator.
- ABI-337 remains a useful no-mirroring diagnostic control, not a new comparator.
- ABI-328 remains a soft-shift alignment diagnostic with higher recall than ABI-338 but weaker connectivity.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-338 is negative evidence for this exact soft-band continuity reinjection head.

ABI-338 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-338 and do not submit another unchanged late36 continuation of the soft-band continuity reinjector branch. The success criteria were not met: aggregate Dice, MIT Dice, recall, and connectivity all worsened versus ABI-324. No Evaluation Request is needed from ABI-338 at this point because the observed failure is already visible in aggregate/source metrics and the retained samples do not suggest a hidden favorable failure bucket. If the temporal family is revisited, the next Run should be mechanism-changing and not another local residual-head variant; a broader temporal attention/evidence-sharpening or non-temporal C4/orientation-recall mechanism would be a better frontier move.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_230319_ed1362/candidate/PROPOSAL.md`
- `run_20260917_230319_ed1362/candidate/README.md`
- `run_20260917_230319_ed1362/candidate/manifest.yaml`
- `run_20260917_230319_ed1362/candidate/budget_request.yaml`
- `run_20260917_230319_ed1362/resolved_manifest.yaml`
- `run_20260917_230319_ed1362/execution.json`
- `run_20260917_230319_ed1362/outputs/model_summary.json`
- `run_20260917_230319_ed1362/outputs/best_metrics.json`
- `run_20260917_230319_ed1362/outputs/final_metrics.json`
- `run_20260917_230319_ed1362/outputs/metrics.jsonl`
- `run_20260917_230319_ed1362/outputs/resource_profile.json`
- `run_20260917_230319_ed1362/outputs/validation_postprocessing/index.json`
- `run_20260917_230319_ed1362/outputs/prediction_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260917_201833_57b081/outputs/best_metrics.json` and `/history/research-notes/abi337-temporal-fiveframe-detail-consensus-no-mirroring-late36.md` for ABI-337 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
