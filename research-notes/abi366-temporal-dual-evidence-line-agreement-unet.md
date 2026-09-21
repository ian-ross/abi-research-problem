# ABI-366 temporal dual-evidence line-agreement U-Net

research-figures: []

## Scope

This note records ABI-366, Candidate `abi366_temporal_dual_evidence_line_agreement_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260920_103228_7b2609`.

ABI-366 was an exploratory temporal family-development Candidate after ABI-350 and the recent ABI-356/359/360/361/365 temporal line-support sequence. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 2. The architectural question was whether separate center-detail and temporal-change encoders, merged through cross-scale agreement gates before line-aware decoder fusion, could preserve recall while avoiding broad clutter and improving connected-line continuity.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-366 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The exploratory/default budget was used; no late-improving budget was requested for this first dual-evidence agreement scout.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `exploratory`, 12 epochs, 3,600 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,884,045, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,061,557,760 / 4,397,727,744 bytes.
- Training wall time: 1,756.7 s; validation wall time: 1,085.2 s; total Run wall time: 2,843.9 s, within the exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 9.

## Temporal-eligible aggregate metrics

| Metric | ABI-366 dual-evidence agreement | ABI-350 line support late36 | ABI-349 exploratory parent | ABI-365 five-frame line support | ABI-361 shift alignment | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 9 | 33 | 12 | 31 | 27 | 36 |
| Filtered Dice | 0.385607 | 0.431103 | 0.389171 | 0.407516 | 0.414944 | 0.419776 |
| MIT filtered Dice | 0.369484 | 0.409536 | 0.369849 | 0.384403 | 0.388679 | 0.398498 |
| Google filtered Dice | 0.425659 | 0.490518 | 0.440561 | 0.465848 | 0.482763 | 0.476764 |
| Filtered precision | 0.386198 | 0.494306 | 0.478850 | 0.459703 | 0.456387 | 0.483764 |
| Filtered recall | 0.385017 | 0.382230 | 0.327784 | 0.365970 | 0.380401 | 0.370738 |
| Filtered connectivity | 0.290653 | 0.358283 | 0.337620 | 0.297708 | 0.298575 | 0.412427 |
| Filtered predicted-positive pixels | 545,140 | 422,831 | 374,305 | 435,318 | 455,771 | 419,056 |

ABI-366 is finite and non-collapsed, but it is negative evidence for this exact dual-encoder agreement mechanism. It does improve fixed-threshold recall relative to ABI-349 and narrowly exceeds ABI-350/365/361/223 recall at the selected checkpoint, but it does so with much lower precision and a substantially broader footprint. Relative to ABI-350, ABI-366 loses -0.0455 aggregate filtered Dice, -0.0401 MIT Dice, -0.0649 Google Dice, -0.1081 precision, and -0.0676 connectivity while predicting +122,309 more filtered-positive pixels. Relative to ABI-365, it loses -0.0219 aggregate Dice, -0.0149 MIT Dice, -0.0402 Google Dice, -0.0735 precision, and -0.0071 connectivity despite higher recall.

The result also falls just below ABI-349's exploratory parent score while producing a much larger predicted-positive footprint. That comparison is important because ABI-350 showed that ABI-349's pre-decoder line-support mechanism benefited from late training; ABI-366, in contrast, did not produce a stronger exploratory launch point than ABI-349. Its center/change agreement gates raised recall but did not sufficiently suppress clutter or stabilize connected-line evidence.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.400496 versus filtered Dice 0.385607, raw recall was 0.415812 versus filtered recall 0.385017, and raw predicted-positive pixels were 588,636 versus 545,140 filtered. Artifact Filters removed 43,496 predicted-positive pixels and lowered the score.

The retained fixed `first_n` prediction samples have nonzero per-sample Dice values (0.25 to 0.56), so they do not indicate an all-negative or all-positive qualitative collapse. They are only the first four validation samples and should not override the aggregate temporal-eligible metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.201122 | 0.202029 | 0.199279 | 0.215111 | 0.188842 | 0.149092 | 480,036 |
| 2 | 0.231888 | 0.237173 | 0.221537 | 0.208433 | 0.261291 | 0.124515 | 685,483 |
| 3 | 0.281461 | 0.266817 | 0.315102 | 0.344606 | 0.237873 | 0.198467 | 377,451 |
| 4 | 0.314607 | 0.298725 | 0.352252 | 0.395066 | 0.261375 | 0.245601 | 361,770 |
| 5 | 0.359537 | 0.343823 | 0.398421 | 0.438419 | 0.304712 | 0.297091 | 380,047 |
| 6 | 0.336962 | 0.339077 | 0.332393 | 0.282317 | 0.417838 | 0.206925 | 809,300 |
| 7 | 0.350589 | 0.331096 | 0.402568 | 0.532584 | 0.261298 | 0.425539 | 268,279 |
| 8 | 0.383556 | 0.368565 | 0.422700 | 0.480500 | 0.319163 | 0.358176 | 363,209 |
| 9 | 0.385607 | 0.369484 | 0.425659 | 0.386198 | 0.385017 | 0.290653 | 545,140 |
| 10 | 0.346774 | 0.328882 | 0.392612 | 0.468594 | 0.275224 | 0.276149 | 321,165 |
| 11 | 0.385038 | 0.361432 | 0.442644 | 0.430884 | 0.348010 | 0.294609 | 441,641 |
| 12 | 0.337392 | 0.310917 | 0.407627 | 0.527858 | 0.247932 | 0.401139 | 256,834 |

The trajectory explains the negative classification. ABI-366 repeatedly finds different useful operating points, but it does not combine them. Epoch 7 and epoch 12 have strong connectivity/precision states, but both are compact and recall-poor. Epoch 6 and epoch 9 raise recall, but they broaden predictions and connectivity drops. Epoch 11 nearly ties the selected aggregate score with better Google Dice and a smaller footprint than epoch 9, but still lacks connectivity. The final epoch is not collapsed, yet it regresses sharply from the selected score and settles into a high-precision, low-recall state.

Because the best checkpoint is not at the epoch-12 boundary and the late exploratory trajectory alternates among incompatible precision, recall, and connectivity states, this exact ABI-366 branch does not justify a late-improving continuation. More epochs might move the operating point, but the current evidence does not show that the agreement gates are converging toward a stable joint solution.

## Interpretation

Classify ABI-366 as a finite, resource-safe, negative temporal family-development result. The separate center-detail and temporal-change encoders are contract-safe and resource-feasible, but the capped evidence does not support the hypothesis that cross-scale agreement gates can preserve recall, suppress clutter, and improve continuity on this scaffold. The mechanism tends to separate into either broad recall with weak connectivity or compact high-connectivity/precision with insufficient recall.

Do not promote ABI-366 and do not spend a Run on an unchanged late36 continuation, minor gate-strength tuning, or another local head-weight shuffle of the same dual-evidence agreement scaffold. The recent ABI-350/356/359/360/361/365/366 sequence now has substantial bounded evidence that local temporal line-support and agreement variants oscillate among compact precision, broad recall, and transient connectivity without a stable joint improvement.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-366 is below the main temporal-eligible comparators on aggregate/source Dice, precision, and connectivity, and capped metrics are sufficient to classify the exact branch as non-frontier. If temporal work continues, it should broaden the mechanism rather than tune this branch locally: for example, a genuinely different temporal backbone, architecture-level evidence sharpening tied to ABI-223-style attention, explicit MIT-positive-tail support, or a single-frame C4/detail recall-support mechanism. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_103228_7b2609/candidate/PROPOSAL.md`
- `run_20260920_103228_7b2609/candidate/README.md`
- `run_20260920_103228_7b2609/candidate/manifest.yaml`
- `run_20260920_103228_7b2609/resolved_manifest.yaml`
- `run_20260920_103228_7b2609/execution.json`
- `run_20260920_103228_7b2609/run_metadata.json`
- `run_20260920_103228_7b2609/outputs/model_summary.json`
- `run_20260920_103228_7b2609/outputs/best_metrics.json`
- `run_20260920_103228_7b2609/outputs/final_metrics.json`
- `run_20260920_103228_7b2609/outputs/metrics.jsonl`
- `run_20260920_103228_7b2609/outputs/resource_profile.json`
- `run_20260920_103228_7b2609/outputs/validation_postprocessing/index.json`
- `run_20260920_103228_7b2609/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260919_004607_f785f8/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-349 exploratory-parent context
- `run_20260920_081530_7577c1/outputs/best_metrics.json` and `/history/research-notes/abi365-temporal-fiveframe-predecoder-line-support-center-detail-late36.md` for ABI-365 comparator context
- `run_20260919_233003_a91c98/outputs/best_metrics.json` and `/history/research-notes/abi361-temporal-shift-aligned-detail-consensus-line-support-late36.md` for ABI-361 comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 temporal-attention comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
