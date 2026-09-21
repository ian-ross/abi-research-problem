# ABI-358 temporal recall-preserving C4 sidecar late36

research-figures: []

## Scope

This note records ABI-358, Candidate `abi358_temporal_recall_preserving_c4_sidecar_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_151507_2ec383`.

ABI-358 was a close, mechanism-changing continuation after ABI-356 and ABI-357 on the capped temporal-eligible GOES ABI Contrail Segmentation population. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural question was whether moving the C4 orientation-continuity module into a recall-preserving sidecar, rather than a late compacting anchor, could keep more of ABI-356's fixed-threshold recall while retaining some ABI-357 precision/connectivity benefit.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-358 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,684,445, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated memory: 6,866,591,744 bytes.
- Training wall time: 5,743.7 s; validation wall time: 3,588.0 s; total Run wall time: 9,334.2 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 30.

## Temporal-eligible aggregate metrics

| Metric | ABI-358 recall-preserving C4 sidecar | ABI-356 recall parent | ABI-357 C4 anchor | ABI-350 line-support late36 | ABI-353 single-frame C4/detail late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 30 | 36 | 36 | 33 | 34 |
| Filtered Dice | 0.427570 | 0.426056 | 0.418378 | 0.431103 | 0.417439 |
| MIT filtered Dice | 0.405720 | 0.411375 | 0.401020 | 0.409536 | 0.401665 |
| Google filtered Dice | 0.484984 | 0.465688 | 0.465032 | 0.490518 | 0.456492 |
| Filtered precision | 0.485745 | 0.421447 | 0.481194 | 0.494306 | 0.442512 |
| Filtered recall | 0.381839 | 0.430766 | 0.370069 | 0.382230 | 0.395056 |
| Filtered connectivity | 0.290228 | 0.282116 | 0.350215 | 0.358283 | 0.348271 |
| Filtered positive fraction | 0.004064 | 0.005284 | 0.003976 | 0.003997 | 0.003235 |

ABI-358 improves aggregate capped temporal-eligible filtered Dice over both immediate parents: +0.0015 versus ABI-356 and +0.0092 versus ABI-357. The sidecar does recover part of the intended trade-off. Relative to ABI-356, it is much more compact and precise: filtered positive fraction falls from 0.005284 to 0.004064 and precision rises from 0.4214 to 0.4857. Relative to ABI-357, it keeps a similar compact footprint while improving recall from 0.3701 to 0.3818 and aggregate filtered Dice from 0.4184 to 0.4276.

The improvement is still not a new temporal frontier. ABI-358 remains slightly below ABI-350 on aggregate filtered Dice (-0.0035), Google filtered Dice (-0.0055), precision (-0.0086), recall (-0.0004), and connectivity (-0.0681). It also does not match ABI-357/350's connectivity. The C4 sidecar solved much of ABI-357's excessive recall suppression, but it did not convert the C4 continuity path into connected-line advantage.

At the final epoch, ABI-358 was nearly tied with the selected checkpoint on filtered Dice (0.427146) and had higher recall (0.390065) and connectivity (0.326577), but lower precision (0.472018). This late behavior suggests the branch is finite and still trading precision, recall, and connectivity across late epochs rather than collapsing.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.229515 | 0.220955 | 0.251409 | 0.346056 | 0.171693 | 0.250037 | 0.002565 |
| 5 | 0.295530 | 0.268689 | 0.366009 | 0.531714 | 0.204633 | 0.386147 | 0.001990 |
| 10 | 0.379042 | 0.356187 | 0.436496 | 0.480745 | 0.312857 | 0.309012 | 0.003364 |
| 15 | 0.380039 | 0.349965 | 0.457445 | 0.517773 | 0.300185 | 0.403856 | 0.002997 |
| 20 | 0.412212 | 0.390945 | 0.468578 | 0.487429 | 0.357106 | 0.402995 | 0.003787 |
| 25 | 0.414609 | 0.394329 | 0.466920 | 0.485896 | 0.361563 | 0.302146 | 0.003847 |
| 30 | 0.427570 | 0.405720 | 0.484984 | 0.485745 | 0.381839 | 0.290228 | 0.004064 |
| 31 | 0.407716 | 0.384495 | 0.467132 | 0.475116 | 0.357062 | 0.220814 | 0.003885 |
| 32 | 0.407696 | 0.384026 | 0.469815 | 0.496465 | 0.345856 | 0.272329 | 0.003601 |
| 33 | 0.381126 | 0.355660 | 0.449510 | 0.551700 | 0.291118 | 0.354561 | 0.002728 |
| 34 | 0.420216 | 0.399978 | 0.472349 | 0.466179 | 0.382503 | 0.268673 | 0.004242 |
| 35 | 0.398402 | 0.378712 | 0.451120 | 0.538733 | 0.316070 | 0.285028 | 0.003033 |
| 36 | 0.427146 | 0.405770 | 0.483538 | 0.472018 | 0.390065 | 0.326577 | 0.004272 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The early high-connectivity epochs have weak recall; epochs 30 and 36 are the most useful checkpoints because they combine source-balanced Dice above 0.405 MIT / 0.483 Google with non-collapsed precision and recall. The epoch-30 selected checkpoint is the strongest primary score; the final checkpoint may be scientifically interesting because it moves toward recall/connectivity without much filtered-Dice loss.

## Interpretation

Classify ABI-358 as a finite, resource-safe, mixed-positive but non-frontier family-development result. The recall-preserving C4 sidecar is better than the ABI-357 compact anchor and slightly better than ABI-356 on aggregate filtered Dice. It demonstrates that decoupling C4 continuity from a late recall veto was the right direction for fixed-threshold detection quality.

Do not promote ABI-358. It does not beat ABI-350, ABI-348/324-style temporal C4 comparators, or ABI-202/249 whole-validation references, and its selected checkpoint does not improve connected-line continuity. Do not spend another Run on an unchanged C4-sidecar late36 continuation or a simple final-head/gate-strength shuffle.

The useful next frontier is mechanism-changing: move continuity evidence earlier into temporal alignment or center-detail evidence before the decoder commits to compact states, or broaden to a different lightweight temporal alignment/backbone or calibration-style architecture that can preserve epoch-36 recall/connectivity without relying on Candidate-owned thresholds, postprocessing, losses, metrics, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not request a Post-Run Evaluation for ABI-358 in this Autonomy Step. The capped temporal-eligible metrics are sufficient to classify the exact sidecar branch as improved over its immediate parents but not strong enough to require failure-bucket diagnostics before choosing the next research direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_151507_2ec383/candidate/PROPOSAL.md`
- `run_20260919_151507_2ec383/candidate/README.md`
- `run_20260919_151507_2ec383/candidate/manifest.yaml`
- `run_20260919_151507_2ec383/candidate/budget_request.yaml`
- `run_20260919_151507_2ec383/resolved_manifest.yaml`
- `run_20260919_151507_2ec383/execution.json`
- `run_20260919_151507_2ec383/run_metadata.json`
- `run_20260919_151507_2ec383/outputs/model_summary.json`
- `run_20260919_151507_2ec383/outputs/best_metrics.json`
- `run_20260919_151507_2ec383/outputs/final_metrics.json`
- `run_20260919_151507_2ec383/outputs/metrics.jsonl`
- `run_20260919_151507_2ec383/outputs/resource_profile.json`
- `run_20260919_151507_2ec383/outputs/validation_postprocessing/index.json`
- `run_20260919_151507_2ec383/outputs/prediction_samples/samples.json`
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 parent context
- `run_20260919_123025_7cd861/outputs/best_metrics.json` and `/history/research-notes/abi357-temporal-c4-orientation-continuity-anchor-late36.md` for ABI-357 parent context
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260919_053527_64085b/outputs/best_metrics.json` and `/history/research-notes/abi353-fullspectral-btd-sza-c4-crossscale-detail-agreement-late36.md` for contemporaneous single-frame C4/detail context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
