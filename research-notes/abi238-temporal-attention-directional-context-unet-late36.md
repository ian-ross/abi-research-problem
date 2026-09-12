# ABI-238 temporal-attention directional-context U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-238, Candidate `abi238_temporal_attention_directional_context_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260911_004137_f54c45`.

ABI-238 was a close family-development continuation of ABI-223. It kept ABI-223's provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. The only intended architecture change was a full-resolution directional-context bridge before the heads. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-238 completed the approved `late_improving` 36-epoch budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; effective maximum epochs 36.
- Parent Run cited by the budget request: `run_20260908_154531_8c7e2b` (ABI-223).
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,135,364, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.17 / 3.45 GiB.
- Training wall time: 3,070.6 s; validation wall time: 2,979.5 s; total Run wall time: 6,052.2 s.

This is successful finite/resource evidence for the temporal-attention directional-context branch. Resource use remained safely below the trusted ceiling, but the Run was somewhat slower and slightly larger than ABI-223.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 29. The final epoch 36 regressed on the primary metric, recall, MIT Dice, Google Dice, and especially connectivity, so checkpoint selection matters.

| Metric | ABI-238 best epoch 29 | ABI-238 final epoch 36 |
| --- | ---: | ---: |
| Filtered Dice | 0.420235 | 0.405065 |
| Raw Dice | 0.438718 | 0.423175 |
| Filtered IoU | 0.266011 | 0.253969 |
| Filtered precision | 0.488730 | 0.480460 |
| Filtered recall | 0.368578 | 0.350122 |
| Filtered contrail connectivity | 0.352239 | 0.259982 |
| Filtered predicted-positive fraction | 0.003899 | 0.003767 |
| Raw predicted-positive fraction | 0.004212 | 0.004058 |
| MIT filtered Dice | 0.405383 | 0.386235 |
| Google filtered Dice | 0.460838 | 0.454535 |
| MIT filtered recall | 0.347833 | 0.323083 |
| Google filtered recall | 0.430301 | 0.430570 |
| Train loss | 0.784345 | 0.776822 |
| Validation loss | 0.846113 | 0.841223 |

The best checkpoint is finite, noncollapsed, and source-informative. It has high precision and a compact predicted-positive fraction. The primary score is essentially tied with ABI-223, but the directional-context bridge did not improve the intended recall/connectivity balance.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.184974 | 0.190993 | 0.144472 | 0.257032 | 0.201409 | 0.156553 | 0.096046 | 0.009197 |
| 6 | 0.327211 | 0.339739 | 0.323272 | 0.331247 | 0.319460 | 0.344894 | 0.184504 | 0.005297 |
| 12 | 0.357511 | 0.375189 | 0.470941 | 0.288115 | 0.337837 | 0.407224 | 0.242423 | 0.003163 |
| 18 | 0.376792 | 0.391700 | 0.378699 | 0.374904 | 0.360540 | 0.416530 | 0.197104 | 0.005118 |
| 24 | 0.378069 | 0.396771 | 0.513180 | 0.299275 | 0.350504 | 0.451234 | 0.321269 | 0.003015 |
| 27 | 0.404623 | 0.424291 | 0.524703 | 0.329269 | 0.381054 | 0.468101 | 0.427675 | 0.003244 |
| 29 | 0.420235 | 0.438718 | 0.488730 | 0.368578 | 0.405383 | 0.460838 | 0.352239 | 0.003899 |
| 30 | 0.383439 | 0.402847 | 0.529881 | 0.300414 | 0.356807 | 0.454034 | 0.359247 | 0.002931 |
| 33 | 0.399207 | 0.417583 | 0.495274 | 0.334353 | 0.376029 | 0.461118 | 0.308048 | 0.003490 |
| 36 | 0.405065 | 0.423175 | 0.480460 | 0.350122 | 0.386235 | 0.454535 | 0.259982 | 0.003767 |

The trajectory shows several high-precision, compact-positive checkpoints and a late primary peak at epoch 29. Unlike ABI-223, the best checkpoint did not occur at the final epoch. The final seven epochs are mixed rather than clearly budget-truncated: training and validation losses continue to decline, but filtered Dice and connectivity do not.

## Comparison context

| Metric | ABI-202 single-frame frontier | ABI-223 temporal attention late36 | ABI-232 MoE late36 | ABI-235 Radon late36 | ABI-238 directional temporal late36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 32 | 36 | 29 |
| Filtered Dice | 0.427570 | 0.419776 | 0.400942 | 0.407900 | 0.420235 |
| Raw Dice | 0.442746 | 0.438487 | 0.414940 | 0.423244 | 0.438718 |
| Filtered precision | 0.439467 | 0.483764 | 0.405218 | 0.432065 | 0.488730 |
| Filtered recall | 0.416301 | 0.370738 | 0.396756 | 0.386295 | 0.368578 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.383636 | 0.343190 | 0.352239 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.386542 | 0.393464 | 0.405383 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.439983 | 0.443533 | 0.460838 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.003548 | 0.003240 | 0.003899 |

Relative to ABI-223, ABI-238 is nearly tied on capped filtered Dice (+0.000459) and raw Dice (+0.000230), with slightly higher precision (+0.004967) and MIT filtered Dice (+0.006885). It gives up recall (-0.002160), Google filtered Dice (-0.015926), and a substantial amount of connectivity (-0.060188). Relative to ABI-202, ABI-238 remains lower on filtered Dice (-0.007336), recall (-0.047723), connectivity (-0.105534), MIT filtered Dice (-0.006609), and Google filtered Dice (-0.007313), while higher on precision (+0.049263).

## Interpretation

Classify ABI-238 as a finite but mixed-to-negative continuation of the ABI-223 temporal-attention branch. The directional-context bridge did not cause collapse and it slightly improved ABI-223's MIT Dice and precision, but the intended benefit was recall and thin-line continuity. On those metrics it regressed, especially connectivity. The primary metric tie is not enough to justify another local directional-context continuation because the added bridge trades away the temporal family's strongest continuity signal from ABI-223.

The result is still useful scientifically. It supports the broader conclusion that provider-owned three-frame temporal attention is competitive and source-informative under the late-improving budget, but it suggests that naive full-resolution horizontal/vertical/diagonal context after the decoder is not the missing ingredient. ABI-238's best epoch at 29 also weakens the case for a further late-budget extension of this exact branch; the branch had room inside the approved budget and ended below its selected checkpoint.

## Decision

Do not promote ABI-238 and do not request whole-validation diagnostics from this capped Result. Stop this exact high-resolution directional-context bridge branch unless a future proposal changes the mechanism materially.

The next in-contract hypothesis should broaden rather than repeat this local context tweak. Good options are a different temporal mechanism that preserves ABI-223's high connectivity, a temporal/Radon hybrid that accumulates line evidence before rather than after temporal fusion, or a modern lightweight backbone scout. If revisiting ABI-238's signal, preserve the MIT/precision gain but explicitly protect recall/connectivity rather than adding more post-decoder directional filtering.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_004137_f54c45/candidate/PROPOSAL.md`
- `run_20260911_004137_f54c45/candidate/README.md`
- `run_20260911_004137_f54c45/candidate/budget_request.yaml`
- `run_20260911_004137_f54c45/candidate/manifest.yaml`
- `run_20260911_004137_f54c45/resolved_manifest.yaml`
- `run_20260911_004137_f54c45/outputs/model_summary.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `run_20260911_004137_f54c45/outputs/final_metrics.json`
- `run_20260911_004137_f54c45/outputs/metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/resource_profile.json`
- `run_20260911_004137_f54c45/outputs/validation_postprocessing/index.json`
- `run_20260911_004137_f54c45/outputs/prediction_samples/samples.json`
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention parent context
- `run_20260910_163616_4f7416` for ABI-232 spectral-regime MoE late36 context
- `run_20260910_195407_469d7c` for ABI-235 Radon late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
