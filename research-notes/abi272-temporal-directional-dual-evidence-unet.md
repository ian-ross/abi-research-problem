# ABI-272 temporal directional dual-evidence U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-272, Candidate `abi272_temporal_directional_dual_evidence_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_163151_b5c94d`.

ABI-272 was a mechanism-changing family-development continuation within the ABI-223/238 temporal-attention branch. It kept the provider-owned `abi_16ch_plus_sza_temporal` input path with offsets `[-1, 0, 1]`, trusted temporal-eligible center selection, source-balanced sampling, random mirroring, BCE-Dice, and Line plus Centerline auxiliary targets. The controlled architectural change was a dual-evidence segmentation head: region, line, and centerline branches share a refinement trunk, and a learned bounded agreement gate adds line/centerline residual evidence to the region logit.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Execution result

ABI-272 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Sample counts after capped temporal-eligible selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,183,175, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.92 / 4.18 GB.
- Training wall time: 1,147.2 s; validation wall time: 1,059.2 s; total Run wall time: 2,208.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 10.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-272 best epoch 10 | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-271 focal-Tversky temporal | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.384001 | 0.420235 | 0.419776 | 0.354546 | 0.427570 |
| Raw Dice | 0.399725 | 0.438718 | 0.438487 | 0.367151 | 0.442746 |
| Filtered precision | 0.420825 | 0.488730 | 0.483764 | 0.328770 | 0.439467 |
| Filtered recall | 0.353103 | 0.368578 | 0.370738 | 0.384708 | 0.416301 |
| Filtered connectivity | 0.274499 | 0.352239 | 0.412427 | 0.187194 | 0.457773 |
| MIT filtered Dice | 0.363279 | 0.405383 | 0.398498 | 0.351877 | 0.411992 |
| Google filtered Dice | 0.436032 | 0.460838 | 0.476764 | 0.360768 | 0.468151 |
| Filtered predicted-positive fraction | 0.004338 | 0.003899 | 0.003962 | 0.006049 | 0.003433 |

ABI-272 improves over the negative ABI-271 focal-Tversky recall test by about +0.0295 filtered Dice, +0.0921 precision, +0.0873 connectivity, +0.0114 MIT filtered Dice, and +0.0753 Google filtered Dice, while reducing the filtered predicted-positive fraction from 0.00605 to 0.00434. However, it does not meet its main comparison target. Relative to ABI-238 it is about -0.0362 filtered Dice, -0.0679 precision, -0.0155 recall, -0.0777 connectivity, -0.0421 MIT filtered Dice, and -0.0248 Google filtered Dice. Relative to ABI-223 it is similarly weaker on Dice, recall, precision, connectivity, and source metrics.

The dual-evidence head therefore avoids the worst clutter expansion of ABI-271, but it does not selectively lift true contrail logits enough to improve recall or connected-line continuity over the stronger temporal comparators.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.199966 | 0.210318 | 0.180916 | 0.178035 | 0.228058 | 0.134091 | 0.006622 |
| 2 | 0.227477 | 0.213229 | 0.263507 | 0.391118 | 0.160377 | 0.279434 | 0.002120 |
| 3 | 0.308146 | 0.299805 | 0.327303 | 0.331037 | 0.288216 | 0.218211 | 0.004501 |
| 4 | 0.301721 | 0.283608 | 0.347334 | 0.392140 | 0.245187 | 0.239482 | 0.003232 |
| 5 | 0.344009 | 0.332332 | 0.370168 | 0.337926 | 0.350314 | 0.198406 | 0.005359 |
| 6 | 0.316174 | 0.313257 | 0.322834 | 0.269079 | 0.383251 | 0.140706 | 0.007363 |
| 7 | 0.332643 | 0.308675 | 0.396844 | 0.518225 | 0.244931 | 0.382122 | 0.002443 |
| 8 | 0.338176 | 0.314996 | 0.400191 | 0.535323 | 0.247154 | 0.401737 | 0.002387 |
| 9 | 0.365455 | 0.351996 | 0.397160 | 0.362010 | 0.368966 | 0.195933 | 0.005269 |
| 10 | 0.384001 | 0.363279 | 0.436032 | 0.420825 | 0.353103 | 0.274499 | 0.004338 |
| 11 | 0.325441 | 0.302303 | 0.380972 | 0.384286 | 0.282225 | 0.180848 | 0.003797 |
| 12 | 0.378374 | 0.363320 | 0.415890 | 0.399808 | 0.359122 | 0.243335 | 0.004643 |

The trajectory is finite and non-collapsed, but not a clean late-improving case. Aggregate Dice rises to epoch 10, drops sharply at epoch 11, then nearly recovers at epoch 12. The final checkpoint has slightly higher recall than the selected checkpoint, but lower filtered Dice, lower precision, lower connectivity, and lower Google filtered Dice. Epochs 7 and 8 show the best connectivity and precision, but only by becoming too conservative: recall falls below 0.25 and filtered Dice stays near 0.33. The selected checkpoint is a compromise rather than evidence that longer training is likely to solve the intended recall/connectivity gap.

## Interpretation

Classify ABI-272 as a finite mixed/negative temporal-head mechanism test. The architecture is resource-safe and source-informative, and it partially repairs ABI-271's broad-positive precision failure. But the central hypothesis was not confirmed: final-head dual evidence does not improve recall or connectivity versus ABI-238/223, and the selected checkpoint remains well below the temporal-family frontier and ABI-202 aggregate reference.

The failure mode appears architectural rather than contractual or resource-related. Agreement-gated line/centerline residuals at the final head can calibrate predictions away from ABI-271-like over-expansion, but the connected-line evidence is still too weak or too late in the network to preserve thin contrail continuity while raising true positives at threshold 0.5.

## Decision

Do not promote ABI-272, do not request whole-validation diagnostics, and do not request a late-improving budget for this exact final-head dual-evidence branch. Although the best checkpoint is near the exploratory epoch ceiling and the final epoch remains close, the run does not improve the target recall/connectivity metrics over ABI-238 or ABI-223 and is volatile after its best epoch.

Future temporal work should be mechanism-changing rather than another final-head-only variant. Higher-value continuations would move line support earlier into the decoder or temporal stem, combine temporal attention with stronger center-frame detail evidence, or use C4/orientation priors plus recall/connectivity support while preserving ABI-238/249-style precision. Repeating focal-Tversky loss swaps or final dual-evidence heads without deeper line-support integration is not justified by this result.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_163151_b5c94d/candidate/PROPOSAL.md`
- `run_20260912_163151_b5c94d/candidate/README.md`
- `run_20260912_163151_b5c94d/candidate/manifest.yaml`
- `run_20260912_163151_b5c94d/resolved_manifest.yaml`
- `run_20260912_163151_b5c94d/outputs/model_summary.json`
- `run_20260912_163151_b5c94d/outputs/best_metrics.json`
- `run_20260912_163151_b5c94d/outputs/final_metrics.json`
- `run_20260912_163151_b5c94d/outputs/metrics.jsonl`
- `run_20260912_163151_b5c94d/outputs/resource_profile.json`
- `run_20260912_163151_b5c94d/outputs/validation_postprocessing/index.json`
- `run_20260912_163151_b5c94d/outputs/prediction_samples/samples.json`
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260912_155232_ec268d` for ABI-271 focal-Tversky temporal comparison context
- `run_20260904_043143_ee0005` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
