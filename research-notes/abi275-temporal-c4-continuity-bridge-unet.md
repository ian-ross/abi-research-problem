# ABI-275 temporal C4 continuity-bridge U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-275, Candidate `abi275_temporal_c4_continuity_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_203536_240ad8`.

ABI-275 was a mechanism-changing continuation after ABI-274. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, batch size 2, and Line plus Centerline auxiliary targets. The architectural change was a full-resolution C4 continuity bridge before the heads: one shared rotated line-support filter was applied at four right-angle orientations, rotated responses were fused with the carried temporal line state, and a learned residual gate injected supported continuity evidence into the decoder features.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Execution result

ABI-275 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Sample counts after capped temporal-eligible selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,281,592, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.97 / 6.34 GB.
- Training wall time: 1,624.8 s; validation wall time: 1,133.3 s; total Run wall time: 2,759.9 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 8.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-275 best epoch 8 | ABI-274 temporal line-state late36 | ABI-273 line-state parent | ABI-223 temporal attention late36 | ABI-238 temporal directional late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.385365 | 0.419364 | 0.389683 | 0.419776 | 0.420235 | 0.427570 |
| Raw Dice | 0.401336 | 0.436760 | 0.406280 | 0.438487 | 0.438718 | 0.442746 |
| Filtered precision | 0.413604 | 0.454127 | 0.446534 | 0.483764 | 0.488730 | 0.439467 |
| Filtered recall | 0.360736 | 0.389545 | 0.345673 | 0.370738 | 0.368578 | 0.416301 |
| Filtered connectivity | 0.266368 | 0.282911 | 0.283368 | 0.412427 | 0.352239 | 0.457773 |
| MIT filtered Dice | 0.372421 | 0.399386 | 0.369240 | 0.398498 | 0.405383 | 0.411992 |
| Google filtered Dice | 0.417764 | 0.472606 | 0.441559 | 0.476764 | 0.460838 | 0.468151 |
| Filtered predicted-positive fraction | 0.004509 | 0.004434 | 0.004002 | 0.003962 | 0.003899 | 0.003433 |

ABI-275 does not meet its primary comparison target. Relative to ABI-274, the selected checkpoint is about -0.0340 filtered Dice, -0.0405 precision, -0.0288 recall, -0.0165 connectivity, -0.0270 MIT filtered Dice, and -0.0548 Google filtered Dice, while predicting a slightly larger filtered-positive fraction. Relative to the 12-epoch ABI-273 parent, ABI-275 is also slightly lower on aggregate filtered Dice, precision, connectivity, and Google filtered Dice, though it has higher recall and a small MIT Dice gain.

The result therefore argues that this full-resolution C4 bridge did not organize ABI-274's temporal line evidence. It weakened the high-performing late36 line-state behavior and did not recover ABI-223/238-style connected-line continuity.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.126988 | 0.118795 | 0.150551 | 0.569362 | 0.071463 | 0.427264 | 0.000649 |
| 2 | 0.252191 | 0.253783 | 0.249156 | 0.227638 | 0.282680 | 0.135650 | 0.006420 |
| 3 | 0.311129 | 0.298780 | 0.337649 | 0.329071 | 0.295043 | 0.197202 | 0.004635 |
| 4 | 0.292825 | 0.273899 | 0.338928 | 0.432262 | 0.221405 | 0.239021 | 0.002648 |
| 5 | 0.347775 | 0.343295 | 0.357983 | 0.362818 | 0.333930 | 0.162901 | 0.004758 |
| 6 | 0.376098 | 0.362455 | 0.412365 | 0.450125 | 0.322981 | 0.281002 | 0.003709 |
| 7 | 0.325921 | 0.310162 | 0.368436 | 0.557650 | 0.230244 | 0.368421 | 0.002134 |
| 8 | 0.385365 | 0.372421 | 0.417764 | 0.413604 | 0.360736 | 0.266368 | 0.004509 |
| 9 | 0.365789 | 0.357156 | 0.385577 | 0.319894 | 0.427059 | 0.188850 | 0.006901 |
| 10 | 0.357558 | 0.333847 | 0.415772 | 0.458412 | 0.293079 | 0.198290 | 0.003305 |
| 11 | 0.322662 | 0.308068 | 0.357934 | 0.426583 | 0.259455 | 0.175219 | 0.003144 |
| 12 | 0.349605 | 0.332609 | 0.390389 | 0.400958 | 0.309913 | 0.167794 | 0.003996 |

The trajectory is finite and non-collapsed, but it is not a late-improving case. The best aggregate checkpoint occurs at epoch 8; epochs 9 through 12 fail to recover that filtered Dice, and the final epoch is lower on Dice, recall, connectivity, MIT Dice, and Google Dice. The high-connectivity epochs are conservative operating points rather than useful continuity repair: epoch 1 reaches 0.427 connectivity only with 0.071 recall and almost no positive predictions, while epoch 7 reaches 0.368 connectivity with low recall and lower primary Dice.

## Interpretation

Classify ABI-275 as a finite negative mechanism test. The bridge is resource-safe and executable, but the central hypothesis is not supported: the shared C4 rotated support gate did not preserve ABI-274's recall/source lift and did not improve connected thin-line continuity at the selected checkpoint. Instead, it introduced a noisier tradeoff between conservative, higher-connectivity epochs and broader, lower-precision recall epochs.

This does not eliminate temporal modeling or C4/orientation priors as families, but it does narrow this exact integration point. Appending a full-resolution C4 continuity bridge after the temporal line-state decoder is not sufficient to repair the connected-line weakness found in ABI-274's failure-bucket evaluation. If C4/orientation support is revisited, it should be integrated earlier or more selectively, with explicit attention to preserving ABI-223/238-style precision and ABI-274-style source-balanced recall.

## Decision

Do not promote ABI-275, do not request temporal-eligible failure-bucket diagnostics, and do not request a late-improving budget for this exact C4 continuity-bridge branch. The selected checkpoint is below ABI-274, ABI-223, ABI-238, and ABI-202 on primary filtered Dice and below all of them on useful selected-checkpoint connectivity; the best epoch is mid-run rather than near the exploratory ceiling.

Do not repeat an unchanged ABI-275 bridge. Future work should be mechanism-changing: examples include a center-frame detail bridge over temporal attention, earlier orientation support inside the temporal stem or encoder injections, or a different recall-preserving calibration/dual-evidence architecture that raises true positives without broad negative-patch clutter. ABI-274 remains the recall/source-balance temporal comparator, while ABI-223 remains the cleaner temporal connectivity comparator.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_203536_240ad8/candidate/PROPOSAL.md`
- `run_20260912_203536_240ad8/candidate/README.md`
- `run_20260912_203536_240ad8/candidate/manifest.yaml`
- `run_20260912_203536_240ad8/resolved_manifest.yaml`
- `run_20260912_203536_240ad8/outputs/model_summary.json`
- `run_20260912_203536_240ad8/outputs/best_metrics.json`
- `run_20260912_203536_240ad8/outputs/final_metrics.json`
- `run_20260912_203536_240ad8/outputs/metrics.jsonl`
- `run_20260912_203536_240ad8/outputs/resource_profile.json`
- `run_20260912_203536_240ad8/outputs/validation_postprocessing/index.json`
- `run_20260912_203536_240ad8/outputs/prediction_samples/samples.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` for ABI-274 diagnostic comparison context
- `run_20260912_171825_ff0d00/outputs/best_metrics.json` for ABI-273 exploratory parent context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
