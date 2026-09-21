# ABI-324 temporal five-frame detail-consensus stabilized line-state late36

research-figures: []

## Scope

This note records ABI-324, Candidate `abi324_temporal_fiveframe_detail_consensus_stabilized_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260916_184108_954ec7`.

ABI-324 was a close but mechanism-changing continuation of ABI-311's five-frame temporal C4 persistence/contrast line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, BCE-Dice loss, Line and Centerline auxiliaries, AdamW with constant LR, and batch size 2. The mechanism change was a `DetailConsensusStabilizedHead` that fuses decoder evidence, center-frame temporal-stem detail, and early C4 line-state support, then adds a bounded non-negative recall residual only where learned mask/Line/Centerline and temporal-detail agreement survive a learned conflict guard.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable to the full-validation ABI-202/249 frontier.

## Execution result

ABI-324 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-311 (`run_20260915_015552_1ac51f`), ABI-306 (`run_20260914_124245_de843c`), and ABI-309 (`run_20260914_205014_1794f8`) parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,254,908, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,557,149,696 / 6,920,601,600 bytes.
- Training wall time: 5,237.0 s; validation wall time: 3,435.6 s; total Run wall time: 8,674.7 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-324 detail-consensus stabilized | ABI-311 five-frame C4 | Delta vs ABI-311 | ABI-306 compact C4 | ABI-309 recall head | ABI-223 temporal-attention comparator |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 0 | 36 | 29 | 36 |
| Filtered Dice | 0.429430 | 0.425000 | +0.004430 | 0.422548 | 0.423544 | 0.419776 |
| MIT filtered Dice | 0.408188 | 0.403831 | +0.004357 | 0.402764 | 0.402446 | 0.398498 |
| Google filtered Dice | 0.487231 | 0.482615 | +0.004616 | 0.476152 | 0.478510 | 0.476764 |
| Filtered precision | 0.470412 | 0.459703 | +0.010709 | 0.493422 | 0.401806 | 0.483764 |
| Filtered recall | 0.395017 | 0.395169 | -0.000152 | 0.369478 | 0.447768 | 0.370738 |
| Filtered connectivity | 0.397925 | 0.366735 | +0.031190 | 0.299384 | 0.316074 | 0.412427 |
| Filtered predicted-positive fraction | 0.004341 | 0.004444 | -0.000103 | 0.003871 | 0.005761 | 0.003962 |
| Filtered predicted-positive pixels | 459,172 | 470,049 | -10,877 | 409,457 | 609,361 | 419,056 |

ABI-324 is a positive temporal C4 family-development Result. Relative to the direct ABI-311 comparator, it improves aggregate filtered Dice, both Dataset Sources, precision, and connectivity while keeping recall essentially tied and producing a slightly smaller filtered footprint. This is the first recent temporal C4 head/stem continuation to improve ABI-311's selected operating point rather than merely trading precision against recall.

Relative to ABI-306, ABI-324 sacrifices some compact high precision but gains aggregate/source Dice, recall, and a large connectivity improvement. Relative to ABI-309, ABI-324 avoids the recall-head clutter mode: it is lower recall, but much higher precision, much stronger connectivity, higher aggregate/source Dice, and about 150k filtered pixels more compact. Relative to ABI-223, ABI-324 now leads on aggregate/source Dice and recall, but still trails ABI-223's temporal-attention connectivity.

At the selected checkpoint, raw Dice was 0.447954 versus filtered Dice 0.429430, raw recall was 0.427299 versus filtered recall 0.395017, and raw predicted-positive pixels were 496,384 versus 459,172 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232301 | 0.235256 | 0.225986 | 0.224230 | 0.240975 | 0.146807 | 0.005556 |
| 6 | 0.337637 | 0.334931 | 0.343594 | 0.304441 | 0.378958 | 0.194008 | 0.006435 |
| 10 | 0.374564 | 0.354368 | 0.423895 | 0.451935 | 0.319812 | 0.322404 | 0.003658 |
| 14 | 0.360559 | 0.332157 | 0.432415 | 0.492011 | 0.284538 | 0.272974 | 0.002990 |
| 18 | 0.385797 | 0.362249 | 0.443774 | 0.435485 | 0.346287 | 0.299556 | 0.004111 |
| 22 | 0.406227 | 0.385755 | 0.460369 | 0.453598 | 0.367814 | 0.298626 | 0.004192 |
| 26 | 0.368846 | 0.347603 | 0.421049 | 0.451606 | 0.311721 | 0.235990 | 0.003568 |
| 27 | 0.429430 | 0.408188 | 0.487231 | 0.470412 | 0.395017 | 0.397925 | 0.004341 |
| 28 | 0.384742 | 0.358489 | 0.450035 | 0.481068 | 0.320556 | 0.288966 | 0.003445 |
| 30 | 0.395798 | 0.370820 | 0.462178 | 0.534559 | 0.314230 | 0.460806 | 0.003039 |
| 32 | 0.419505 | 0.398118 | 0.474980 | 0.449128 | 0.393548 | 0.295511 | 0.004530 |
| 34 | 0.410375 | 0.390519 | 0.463200 | 0.493594 | 0.351168 | 0.304204 | 0.003678 |
| 36 | 0.415652 | 0.395697 | 0.470140 | 0.516047 | 0.347959 | 0.355821 | 0.003486 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The selected epoch 27 is well beyond the exploratory ceiling and is a clean aggregate/source/precision/recall/connectivity improvement over ABI-311's selected epoch. The later trajectory remains oscillatory: epoch 30 reaches very high precision and connectivity, but at lower recall and Dice; epoch 36 is compact and precise but does not recover the selected epoch's recall, connectivity, or source Dice. This supports the mechanism as useful but not fully stable.

The main positive sign is that the detail-consensus residual did not merely broaden predictions. It improved ABI-311 while reducing the filtered predicted-positive footprint. The remaining limitation is that connectivity can still decouple from aggregate Dice, and ABI-223 retains the strongest temporal-attention connectivity reference.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4487, 0.3889, 0.5440, and 0.4274. This confirms finite non-collapsed predictions and stronger retained-sample behavior than several recent temporal variants, but it does not establish promotion evidence.

## Interpretation

Classify ABI-324 as positive capped temporal-family development evidence and the current local temporal-eligible capped aggregate filtered-Dice comparator among the recent temporal C4 branch. It validates the proposed head-level mechanism: fusing center-frame detail with temporal C4 line-state agreement can raise selected fixed-threshold evidence while preserving compactness better than ABI-309 and improving connected-line continuity over ABI-311/306.

Comparator roles after ABI-324:

- ABI-324 becomes the best capped temporal C4 balance so far and should replace ABI-311 as the local temporal C4 aggregate/connected-recall comparator.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy/broad-footprint temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.
- ABI-322 remains negative evidence for an unchanged ABI-311 architecture trained with `bce_dice_cldice`.
- ABI-323 remains negative evidence for a minor ABI-223-style output consensus-floor continuation.

ABI-324 is still capped temporal-eligible evidence. It should not be promoted against ABI-202/249 without trusted evaluation. The next scientific question is whether the epoch-27 improvement corresponds to fewer positive-patch fragmentation and MIT undercoverage failures without hidden negative-patch clutter.

## Decision

Do not promote ABI-324 directly from capped temporal-eligible evidence. Do treat it as a strong candidate for a future temporal-eligible failure-bucket Evaluation Request, compared against ABI-311, ABI-306, ABI-309, and ABI-223. That diagnostic should test whether its smaller footprint and higher connectivity relative to ABI-311 actually reduce positive-patch fragmentation and negative-patch clutter buckets.

Do not submit another unchanged ABI-311/324-style late36 head stabilization continuation before diagnostics. If future work proceeds without diagnostics, it should be mechanism-changing: e.g. stabilize the high-connectivity epoch-30 state while recovering recall, or combine ABI-324's detail-consensus C4 branch with a materially different temporal alignment/change mechanism.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260916_184108_954ec7/candidate/PROPOSAL.md`
- `run_20260916_184108_954ec7/candidate/README.md`
- `run_20260916_184108_954ec7/candidate/manifest.yaml`
- `run_20260916_184108_954ec7/candidate/budget_request.yaml`
- `run_20260916_184108_954ec7/resolved_manifest.yaml`
- `run_20260916_184108_954ec7/execution.json`
- `run_20260916_184108_954ec7/outputs/model_summary.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json`
- `run_20260916_184108_954ec7/outputs/final_metrics.json`
- `run_20260916_184108_954ec7/outputs/metrics.jsonl`
- `run_20260916_184108_954ec7/outputs/resource_profile.json`
- `run_20260916_184108_954ec7/outputs/validation_postprocessing/index.json`
- `run_20260916_184108_954ec7/outputs/prediction_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `run_20260915_191945_382cc4/outputs/best_metrics.json` and `/history/research-notes/abi322-temporal-fiveframe-c4-cldice-connectivity-line-state-late36.md` for ABI-322 trusted-loss comparison context
- `run_20260916_164624_1768fd/outputs/best_metrics.json` and `/history/research-notes/abi323-temporal-attention-logit-consensus-floor-late36.md` for ABI-323 temporal-attention head comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
