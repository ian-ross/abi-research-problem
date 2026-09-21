# ABI-271 temporal-attention fusion focal-Tversky loss-policy continuation

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-271, Candidate `abi271_temporal_attention_fusion_focal_tversky_line_centerline_aux_v1`, Run `run_20260912_155232_ec268d`.

ABI-271 was a controlled family-development continuation of the ABI-223 temporal-attention fusion U-Net branch. It kept the provider-owned `abi_16ch_plus_sza_temporal` input path with offsets `[-1, 0, 1]`, trusted temporal-eligible center selection, source-balanced sampling, random mirroring, the compact temporal-attention architecture, and Line plus Centerline auxiliary outputs. The controlled change was selecting the trusted allowlisted `focal_tversky` primary loss instead of BCE-Dice to test whether recall-oriented optimization could lift under-confident true contrail evidence at the fixed Harness threshold.

The Candidate remained architecture/manifest-only: it did not own data loading, temporal lookup, frame repair, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Execution result

ABI-271 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Sample counts after capped temporal-eligible selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,095,836, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 2.76 / 3.02 GB.
- Training wall time: 902.2 s; validation wall time: 962.9 s; total Run wall time: 1,866.8 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-271 best epoch 12 | ABI-222 temporal-attention 12ep | ABI-223 temporal-attention late36 | ABI-255 recurrent temporal late36 | ABI-261 highres temporal recall | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.354546 | 0.374329 | 0.419776 | 0.417348 | 0.377171 | 0.427570 |
| Raw Dice | 0.367151 | — | — | — | — | 0.442746 |
| Filtered precision | 0.328770 | 0.466148 | 0.483764 | 0.468293 | 0.361650 | 0.439467 |
| Filtered recall | 0.384708 | 0.312729 | 0.370738 | 0.376400 | 0.394084 | 0.416301 |
| Filtered connectivity | 0.187194 | 0.281396 | 0.412427 | 0.281116 | 0.264338 | 0.457773 |
| MIT filtered Dice | 0.351877 | 0.357658 | 0.398498 | 0.400833 | 0.365117 | 0.411992 |
| Google filtered Dice | 0.360768 | 0.416510 | 0.476764 | 0.463143 | 0.406542 | 0.468151 |
| Filtered predicted-positive fraction | 0.006049 | 0.003468 | 0.003962 | 0.004155 | 0.005633 | 0.003433 |

ABI-271 did raise recall versus the 12-epoch ABI-222 parent by about +0.072, but this came with a large precision drop (-0.137), lower filtered Dice (-0.020), lower connectivity (-0.094), and weaker Google/source behavior (-0.056 Google filtered Dice). Relative to the late36 ABI-223 comparator, it has only a small recall gain (+0.014) while losing about -0.065 filtered Dice, -0.155 precision, -0.225 connectivity, -0.047 MIT filtered Dice, and -0.116 Google filtered Dice. Relative to the recent ABI-261 temporal recall attempt, ABI-271 is worse on Dice, precision, recall, connectivity, MIT, and Google metrics while predicting slightly more positive pixels.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.151798 | 0.171007 | 0.120109 | 0.095393 | 0.371404 | 0.095325 | 0.020127 |
| 2 | 0.223218 | 0.226371 | 0.216545 | 0.222900 | 0.223538 | 0.171396 | 0.005184 |
| 3 | 0.257219 | 0.272065 | 0.228109 | 0.219567 | 0.310458 | 0.164910 | 0.007310 |
| 4 | 0.194380 | 0.211306 | 0.166076 | 0.134134 | 0.352873 | 0.097772 | 0.013600 |
| 5 | 0.273204 | 0.278593 | 0.262088 | 0.233549 | 0.329080 | 0.139751 | 0.007284 |
| 6 | 0.284742 | 0.294250 | 0.264474 | 0.217818 | 0.411030 | 0.139776 | 0.009755 |
| 7 | 0.316697 | 0.302286 | 0.354715 | 0.446645 | 0.245322 | 0.348986 | 0.002839 |
| 8 | 0.334251 | 0.346367 | 0.306981 | 0.270560 | 0.437161 | 0.181915 | 0.008353 |
| 9 | 0.291358 | 0.300005 | 0.274152 | 0.219072 | 0.434840 | 0.148516 | 0.010261 |
| 10 | 0.349003 | 0.349916 | 0.346982 | 0.313727 | 0.393216 | 0.162486 | 0.006479 |
| 11 | 0.315345 | 0.324985 | 0.295172 | 0.242926 | 0.449281 | 0.181881 | 0.009561 |
| 12 | 0.354546 | 0.351877 | 0.360768 | 0.328770 | 0.384708 | 0.187194 | 0.006049 |

The selected checkpoint is at the final exploratory epoch, but the trajectory is volatile rather than cleanly late-improving. High-recall epochs repeatedly coincide with large predicted-positive fractions, low precision, and weak connectivity. Epoch 7 briefly has much better precision/connectivity, but it achieves only 0.3167 filtered Dice and low recall. The final epoch improves aggregate Dice and source balance versus epoch 11, yet connectivity remains far below temporal comparators.

## Interpretation

Classify ABI-271 as a finite negative/mixed loss-policy test. The focal-Tversky swap confirms that the temporal-attention branch can be pushed toward more positive predictions and higher recall at threshold 0.5, but the gain is not selective enough. The model broadens predicted positives, loses precision, and fragments connected thin-line behavior. This directly matches the proposal fallback condition for stopping this exact focal-Tversky temporal-attention branch.

The result is still useful campaign evidence. It suggests ABI-223's under-confident temporal evidence is not solved by a trusted loss swap alone. Architecture-level evidence sharpening remains more promising than repeating the same compact temporal-attention architecture with focal-Tversky, especially if it can preserve ABI-223/249-style precision and improve connected-line continuity.

## Decision

Do not promote ABI-271, do not request whole-validation diagnostics, and do not request a late-improving budget for this exact focal-Tversky temporal-attention branch. Although its best checkpoint is at epoch 12 and recall improved versus ABI-222/223, precision and connectivity regress too sharply, and ABI-271 is below ABI-223, ABI-255, ABI-261, and ABI-202 on selected filtered Dice.

Future temporal work should be mechanism-changing: examples include architecture-level evidence sharpening that raises true contrail logits without expanding clutter, temporal attention with explicit line-support decoding that preserves connectivity, or calibrated/dual-evidence heads that recover recall while keeping ABI-223-style precision. A plain focal-Tversky continuation of the same ABI-223 architecture should not be repeated unchanged.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_155232_ec268d/candidate/PROPOSAL.md`
- `run_20260912_155232_ec268d/candidate/README.md`
- `run_20260912_155232_ec268d/candidate/manifest.yaml`
- `run_20260912_155232_ec268d/resolved_manifest.yaml`
- `run_20260912_155232_ec268d/outputs/model_summary.json`
- `run_20260912_155232_ec268d/outputs/best_metrics.json`
- `run_20260912_155232_ec268d/outputs/final_metrics.json`
- `run_20260912_155232_ec268d/outputs/metrics.jsonl`
- `run_20260912_155232_ec268d/outputs/resource_profile.json`
- `run_20260912_155232_ec268d/outputs/validation_postprocessing/index.json`
- `run_20260912_155232_ec268d/outputs/prediction_samples/samples.json`
- `run_20260908_150315_9aea3f` for ABI-222 temporal-attention 12-epoch parent context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_210922_27f346` for ABI-255 recurrent temporal comparator context
- `run_20260912_031837_f40c59` for ABI-261 temporal high-resolution recall context
- `run_20260904_043143_ee0005` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
