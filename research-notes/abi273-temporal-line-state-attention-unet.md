# ABI-273 temporal line-state attention U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-273, Candidate `abi273_temporal_line_state_attention_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_171825_ff0d00`.

ABI-273 was a mechanism-changing family-development continuation within the ABI-223/238 temporal-attention branch. It kept the provider-owned `abi_16ch_plus_sza_temporal` input path with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice, and Line plus Centerline auxiliary targets. The architectural change was to move orientation-aware line support upstream: a temporal-attention/change stem forms a bounded full-resolution line state, and lightweight gates inject that state into encoder scales before the ASPP decoder and simple mask/auxiliary heads.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Execution result

ABI-273 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Sample counts after capped temporal-eligible selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,243,288, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.02 / 5.36 GB.
- Training wall time: 1,432.7 s; validation wall time: 1,076.5 s; total Run wall time: 2,511.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-273 best epoch 12 | ABI-272 final-head dual evidence | ABI-259 line-support decoder | ABI-261 highres line recall | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.389683 | 0.384001 | 0.381540 | 0.377171 | 0.420235 | 0.419776 | 0.427570 |
| Raw Dice | 0.406280 | 0.399725 | 0.398247 | 0.390749 | 0.438718 | 0.438487 | 0.442746 |
| Filtered precision | 0.446534 | 0.420825 | 0.438659 | 0.361650 | 0.488730 | 0.483764 | 0.439467 |
| Filtered recall | 0.345673 | 0.353103 | 0.337582 | 0.394084 | 0.368578 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.283368 | 0.274499 | 0.331613 | 0.264338 | 0.352239 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.369240 | 0.363279 | 0.368471 | 0.365117 | 0.405383 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.441559 | 0.436032 | 0.415787 | 0.406542 | 0.460838 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004002 | 0.004338 | 0.003978 | 0.005633 | 0.003899 | 0.003962 | 0.003433 |

ABI-273 is an improvement over the immediately preceding ABI-272 final-head dual-evidence test: about +0.0057 filtered Dice, +0.0257 precision, +0.0089 connectivity, +0.0060 MIT Dice, and +0.0055 Google Dice, while reducing filtered predicted-positive fraction from 0.00434 to 0.00400. This supports the proposal's premise that moving line evidence earlier is more useful than adding line/centerline residuals only at the final head.

Against the other recent temporal line-support tests, ABI-273 is mixed. It improves primary filtered Dice over ABI-259 and ABI-261 and avoids ABI-261's broad positive expansion, but it does not recover ABI-259's best selected connectivity and remains lower-recall than ABI-261. Against the mature temporal comparators, ABI-273 is still clearly behind: relative to ABI-223 it is about -0.0301 filtered Dice, -0.0372 precision, -0.0251 recall, -0.1291 connectivity, -0.0293 MIT Dice, and -0.0352 Google Dice. Relative to ABI-238 it is also weaker on primary Dice, precision, recall, connectivity, and MIT Dice.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.222071 | 0.226439 | 0.212584 | 0.233232 | 0.211928 | 0.172739 | 0.004697 |
| 2 | 0.192805 | 0.170500 | 0.251744 | 0.467038 | 0.121477 | 0.360662 | 0.001345 |
| 3 | 0.301611 | 0.280219 | 0.352860 | 0.409957 | 0.238563 | 0.256095 | 0.003008 |
| 4 | 0.309102 | 0.292225 | 0.348485 | 0.354647 | 0.273924 | 0.198740 | 0.003993 |
| 5 | 0.346024 | 0.319443 | 0.411178 | 0.440653 | 0.284853 | 0.314633 | 0.003342 |
| 6 | 0.355573 | 0.345189 | 0.380310 | 0.320579 | 0.399143 | 0.252642 | 0.006436 |
| 7 | 0.336992 | 0.311045 | 0.403717 | 0.469477 | 0.262823 | 0.255422 | 0.002894 |
| 8 | 0.368105 | 0.352290 | 0.407658 | 0.359707 | 0.376905 | 0.214093 | 0.005417 |
| 9 | 0.360720 | 0.340919 | 0.408478 | 0.367916 | 0.353800 | 0.196167 | 0.004971 |
| 10 | 0.353732 | 0.328518 | 0.417283 | 0.444809 | 0.293613 | 0.249915 | 0.003412 |
| 11 | 0.369271 | 0.348151 | 0.422963 | 0.463209 | 0.307010 | 0.223982 | 0.003426 |
| 12 | 0.389683 | 0.369240 | 0.441559 | 0.446534 | 0.345673 | 0.283368 | 0.004002 |

The trajectory is finite, source-informative, and non-collapsed. Unlike ABI-259/261/272, the selected checkpoint is the final exploratory epoch and it improves aggregate Dice, MIT Dice, Google Dice, recall, and connectivity over epochs 10 and 11 while keeping a compact predicted-positive fraction. The trajectory is still noisy: epoch 2 had high connectivity only by becoming extremely conservative, and epoch 6/8 had higher recall but lower precision or connectivity. However, the final epoch is the best balanced checkpoint in this exploratory run.

## Interpretation

Classify ABI-273 as a finite positive/mixed temporal-family development result. The early line-state injector is not a promotion candidate and does not close the gap to ABI-223/238 or ABI-202. Its connectivity remains too low for a branch whose explicit goal was connected thin-line support, and its selected recall is below the stronger temporal comparators.

The useful evidence is that early line-state injection improves over the recent final-head dual-evidence branch and outperforms recent decoder/recall-head temporal line-support variants on capped filtered Dice without expanding positive predictions. The best-at-final trajectory also differs from ABI-259/261/272, whose exploratory primary metrics peaked earlier or were volatile after the selected checkpoint.

## Decision

Do not promote ABI-273 and do not request whole-validation diagnostics from this capped temporal-eligible Result. The score remains below the temporal-family late36 comparators and the current aggregate reference.

A single late-improving close continuation is justified for this exact early-line-state mechanism under the approved budget-request path: ABI-273 is finite, resource-safe, source-informative, non-collapsed, selected at epoch 12, and improving at the epoch ceiling with bounded positive fraction. The continuation should keep the mechanism close rather than adding another final-head residual or loss swap. Its goal should be to test whether the late trajectory can approach ABI-223/238 while recovering connectivity; if late36 does not substantially improve recall/connectivity, stop this early-line-state injector and broaden away from temporal line-state variants.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_171825_ff0d00/candidate/PROPOSAL.md`
- `run_20260912_171825_ff0d00/candidate/README.md`
- `run_20260912_171825_ff0d00/candidate/manifest.yaml`
- `run_20260912_171825_ff0d00/resolved_manifest.yaml`
- `run_20260912_171825_ff0d00/outputs/model_summary.json`
- `run_20260912_171825_ff0d00/outputs/best_metrics.json`
- `run_20260912_171825_ff0d00/outputs/final_metrics.json`
- `run_20260912_171825_ff0d00/outputs/metrics.jsonl`
- `run_20260912_171825_ff0d00/outputs/resource_profile.json`
- `run_20260912_171825_ff0d00/outputs/validation_postprocessing/index.json`
- `run_20260912_171825_ff0d00/outputs/prediction_samples/samples.json`
- `run_20260912_163151_b5c94d` for ABI-272 final-head dual-evidence comparison context
- `run_20260912_012708_f5897e` for ABI-259 temporal line-support decoder comparison context
- `run_20260912_031837_f40c59` for ABI-261 temporal high-resolution line-accumulation recall comparison context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
