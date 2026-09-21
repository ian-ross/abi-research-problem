# ABI-359 temporal alignment C4 center-detail bridge late36

research-figures: []

## Scope

This note records ABI-359, Candidate `abi359_temporal_alignment_c4_center_detail_bridge_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_175950_ac7b89`.

ABI-359 was a close, mechanism-changing continuation after ABI-356 and ABI-358 on the capped temporal-eligible GOES ABI Contrail Segmentation population. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural question was whether moving C4/orientation continuity earlier into the center-detail and temporal-change alignment path could improve connected-line evidence without using the C4 path as a late compacting veto.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-359 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,719,629, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated memory: 7,377,981,952 bytes.
- Training wall time: 6,130.0 s; validation wall time: 3,639.1 s; total Run wall time: 9,771.3 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Temporal-eligible aggregate metrics

| Metric | ABI-359 early C4 alignment | ABI-358 recall-preserving C4 sidecar | ABI-356 recall parent | ABI-350 line-support late36 | ABI-202 whole-val reference, capped view |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 30 | 36 | 33 | 34 |
| Filtered Dice | 0.426759 | 0.427570 | 0.426056 | 0.431103 | 0.427570 |
| MIT filtered Dice | 0.406428 | 0.405720 | 0.411375 | 0.409536 | 0.411992 |
| Google filtered Dice | 0.481165 | 0.484984 | 0.465688 | 0.490518 | 0.468151 |
| Filtered precision | 0.474933 | 0.485745 | 0.421447 | 0.494306 | 0.439467 |
| Filtered recall | 0.387459 | 0.381839 | 0.430766 | 0.382230 | 0.416301 |
| Filtered connectivity | 0.376348 | 0.290228 | 0.282116 | 0.358283 | 0.457773 |
| Filtered positive fraction | 0.004217 | 0.004064 | 0.005284 | 0.003997 | unknown here |

ABI-359 is a mixed-positive family-development result. It does not beat ABI-358 on aggregate filtered Dice (-0.0008), and it remains below ABI-350 (-0.0043). However, it clearly improves the intended connected-line metric over the immediate temporal parents: +0.0861 versus ABI-358 and +0.0942 versus ABI-356. It also raises recall over ABI-358 from 0.3818 to 0.3875 while remaining much more compact and precise than ABI-356.

The source-stratified result is finite and non-collapsed. MIT filtered Dice is essentially tied with ABI-358 (+0.0007) and below ABI-356/350; Google filtered Dice is below ABI-358/350 but above ABI-356. The price of early alignment is lower precision than the sidecar parent, but it recovers the continuity signal the sidecar lacked.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.257906 | 0.258042 | 0.257608 | 0.266223 | 0.250093 | 0.145604 | 0.004856 |
| 5 | 0.345084 | 0.328537 | 0.384224 | 0.399987 | 0.303433 | 0.259723 | 0.003922 |
| 10 | 0.361429 | 0.343329 | 0.406816 | 0.438153 | 0.307570 | 0.275359 | 0.003629 |
| 15 | 0.409959 | 0.395327 | 0.449435 | 0.475730 | 0.360166 | 0.372229 | 0.003914 |
| 20 | 0.363203 | 0.341728 | 0.421851 | 0.556063 | 0.269672 | 0.383739 | 0.002507 |
| 25 | 0.380345 | 0.358236 | 0.439812 | 0.534757 | 0.295127 | 0.321640 | 0.002853 |
| 27 | 0.426759 | 0.406428 | 0.481165 | 0.474933 | 0.387459 | 0.376348 | 0.004217 |
| 30 | 0.401313 | 0.381435 | 0.452366 | 0.468910 | 0.350749 | 0.323344 | 0.003867 |
| 31 | 0.399884 | 0.388527 | 0.429257 | 0.422089 | 0.379898 | 0.236665 | 0.004653 |
| 32 | 0.416698 | 0.398810 | 0.462238 | 0.451105 | 0.387168 | 0.300167 | 0.004437 |
| 33 | 0.403052 | 0.376812 | 0.474731 | 0.545054 | 0.319748 | 0.481231 | 0.003033 |
| 34 | 0.401835 | 0.382623 | 0.450600 | 0.444621 | 0.366561 | 0.294649 | 0.004262 |
| 35 | 0.370399 | 0.351832 | 0.416980 | 0.473847 | 0.304026 | 0.227786 | 0.003317 |
| 36 | 0.410558 | 0.397916 | 0.444156 | 0.398449 | 0.423425 | 0.269774 | 0.005494 |

The trajectory is finite, source-informative, and late-budget-dependent, but unstable. Epoch 27 is the best balanced checkpoint. Epoch 33 shows that the architecture can produce high connectivity (0.4812) only by becoming too compact and low-recall. The final epoch swings toward higher recall (0.4234) but loses precision, filtered Dice, and connectivity. This suggests the early C4 bridge exposes useful continuity evidence, but the current head/decoder does not stably combine continuity and recall.

## Interpretation

Classify ABI-359 as a finite, resource-safe, mechanism-positive but non-frontier temporal family-development result. The core hypothesis was partly supported: early C4 alignment recovered connected-line evidence that ABI-358's sidecar did not, and it did so without collapsing recall below ABI-358. The cost is a small aggregate Dice and precision regression relative to ABI-358, and it still does not displace ABI-350 or ABI-202-style references.

Do not promote ABI-359. Do not spend another Run on an unchanged early-C4 bridge late36 continuation or a simple gate-strength shuffle. If continuing this branch, the next mechanism should specifically stabilize the epoch-27/33 continuity signal while preventing the final-epoch broad low-precision footprint, for example through a calibration/dual-evidence head or a temporally aligned continuity auxiliary path that remains architecture-internal and does not alter thresholds, losses, metrics, Artifact Filters, data loading, temporal lookup, sampling, coordinates, or postprocessing.

Because ABI-359 is close to the capped temporal frontier and uniquely improves connectivity over ABI-358/356, a future temporal-eligible failure-bucket diagnostic would be reasonable before choosing a further mechanism-changing continuation. That diagnostic should compare whether the connectivity gain corresponds to genuinely continuous contrails or just a different false-positive/false-negative mix.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_175950_ac7b89/candidate/PROPOSAL.md`
- `run_20260919_175950_ac7b89/candidate/README.md`
- `run_20260919_175950_ac7b89/candidate/manifest.yaml`
- `run_20260919_175950_ac7b89/candidate/budget_request.yaml`
- `run_20260919_175950_ac7b89/resolved_manifest.yaml`
- `run_20260919_175950_ac7b89/execution.json`
- `run_20260919_175950_ac7b89/run_metadata.json`
- `run_20260919_175950_ac7b89/outputs/model_summary.json`
- `run_20260919_175950_ac7b89/outputs/best_metrics.json`
- `run_20260919_175950_ac7b89/outputs/final_metrics.json`
- `run_20260919_175950_ac7b89/outputs/metrics.jsonl`
- `run_20260919_175950_ac7b89/outputs/resource_profile.json`
- `run_20260919_175950_ac7b89/outputs/validation_postprocessing/index.json`
- `run_20260919_175950_ac7b89/outputs/prediction_samples/samples.json`
- `run_20260919_151507_2ec383/outputs/best_metrics.json` and `/history/research-notes/abi358-temporal-recall-preserving-c4-sidecar-late36.md` for ABI-358 parent context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 parent context
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-202 reference context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
