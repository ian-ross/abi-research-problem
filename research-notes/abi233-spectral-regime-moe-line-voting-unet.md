# ABI-233 spectral-regime MoE line-voting U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-233, Candidate `abi233_fullspectral_btd_sza_moe_line_voting_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260910_181015_afea31`.

ABI-233 was a family-development continuation of the ABI-231/ABI-232 single-frame spectral/Solar Geometry Input mixture-of-experts branch. It kept the provider-owned `abi_16ch_plus_sza` input, approved-channel BTD features, trusted `bce_dice` primary loss, trusted Line and Centerline auxiliary targets, trusted source-balanced sampling, and trusted random mirroring. The only intended architectural change was a differentiable multi-orientation line-voting support module before the prediction heads.

Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, temporal cache access, or resource scheduling.

## Execution result

ABI-233 completed the full 12-epoch exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from Run artifacts:

- Status: completed.
- Budget: exploratory; 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 2,384,241, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 8.36 / 9.28 GiB.
- Training wall time: 924.5 s; validation wall time: 1,213.0 s; total Run wall time: 2,139.2 s.

This is successful finite/resource evidence for the MoE plus line-voting implementation, but the scientific signal is mixed and does not establish a new frontier.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 9. The final epoch 12 regressed on filtered Dice and recall while improving precision and connectivity, so checkpoint selection matters.

| Metric | ABI-233 best epoch 9 | ABI-233 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.379025 | 0.364089 |
| Raw Dice | 0.392046 | 0.379403 |
| Filtered IoU | 0.233825 | 0.222561 |
| Filtered precision | 0.364180 | 0.449157 |
| Filtered recall | 0.395132 | 0.306114 |
| Filtered contrail connectivity | 0.291487 | 0.345270 |
| Filtered predicted-positive fraction | 0.003932 | 0.002470 |
| MIT filtered Dice | 0.373808 | 0.349603 |
| Google filtered Dice | 0.391121 | 0.399540 |
| MIT filtered recall | 0.365371 | 0.280010 |
| Google filtered recall | 0.482171 | 0.382457 |
| Train loss | 0.854628 | 0.853706 |
| Validation loss | 0.885667 | 0.884535 |

The selected checkpoint is finite, noncollapsed, and source-informative. It reaches ABI-232-like recall at 12 epochs but does not preserve the high-connectivity signature that motivated the line-voting change.

## Learning trajectory

| Epoch | Filtered Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.221897 | 0.181874 | 0.284504 | 0.239113 | 0.189403 | 0.132977 | 0.005668 |
| 2 | 0.265451 | 0.277466 | 0.254434 | 0.264585 | 0.267322 | 0.183922 | 0.003323 |
| 3 | 0.294893 | 0.266148 | 0.330597 | 0.302800 | 0.278228 | 0.200427 | 0.004501 |
| 4 | 0.311713 | 0.302831 | 0.321133 | 0.312298 | 0.310500 | 0.194939 | 0.003843 |
| 5 | 0.318767 | 0.275359 | 0.378424 | 0.321688 | 0.312990 | 0.202266 | 0.004980 |
| 6 | 0.368309 | 0.440437 | 0.316480 | 0.355046 | 0.402088 | 0.396133 | 0.002604 |
| 7 | 0.355332 | 0.366043 | 0.345231 | 0.348351 | 0.370447 | 0.274776 | 0.003418 |
| 8 | 0.368379 | 0.381419 | 0.356202 | 0.356072 | 0.397167 | 0.305854 | 0.003384 |
| 9 | 0.379025 | 0.364180 | 0.395132 | 0.373808 | 0.391121 | 0.291487 | 0.003932 |
| 10 | 0.364412 | 0.378722 | 0.351144 | 0.351157 | 0.393238 | 0.295647 | 0.003360 |
| 11 | 0.375033 | 0.402056 | 0.351413 | 0.365793 | 0.397577 | 0.294807 | 0.003167 |
| 12 | 0.364089 | 0.449157 | 0.306114 | 0.349603 | 0.399540 | 0.345270 | 0.002470 |

The trajectory improves through epoch 9, then oscillates. Epoch 6 briefly shows high connectivity (0.396133) with strong precision and compact predicted-positive fraction, but the selected best-Dice checkpoint shifts toward recall and gives up that connected-line behavior. The final checkpoint recovers some connectivity and precision but loses too much recall and MIT overlap.

## Comparison context

| Metric | ABI-202 frontier | ABI-223 temporal late36 | ABI-231 MoE 12ep | ABI-232 MoE late36 | ABI-233 MoE line-voting 12ep |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 36 | 12 | 32 | 9 |
| Filtered Dice | 0.427570 | 0.419776 | 0.371985 | 0.400942 | 0.379025 |
| Raw Dice | 0.442746 | 0.438487 | 0.386649 | 0.414940 | 0.392046 |
| Filtered precision | 0.439467 | 0.483764 | 0.432192 | 0.405218 | 0.364180 |
| Filtered recall | 0.416301 | 0.370738 | 0.326502 | 0.396756 | 0.395132 |
| Filtered connectivity | 0.457773 | 0.412427 | 0.398515 | 0.383636 | 0.291487 |
| MIT filtered Dice | 0.411992 | 0.398498 | 0.355799 | 0.386542 | 0.373808 |
| Google filtered Dice | 0.468151 | 0.476764 | 0.413787 | 0.439983 | 0.391121 |
| Filtered predicted-positive fraction | 0.003433 | 0.003962 | 0.002738 | 0.003548 | 0.003932 |

Relative to ABI-231, ABI-233 improves aggregate filtered Dice by +0.007040, recall by +0.068630, and MIT Dice by +0.018009, but loses precision (-0.068012), connectivity (-0.107028), and Google Dice (-0.022666). Relative to ABI-232's late36 selected checkpoint, ABI-233 is lower on filtered Dice (-0.021917), precision (-0.041038), connectivity (-0.092149), MIT Dice (-0.012734), and Google Dice (-0.048862), with recall nearly tied (-0.001624).

Relative to the broader frontier, ABI-233 remains well below ABI-202 and ABI-223 on aggregate filtered Dice, connectivity, and source-stratified Dice. It is not a promotion candidate and does not warrant whole-validation diagnostics from this capped Result.

## Interpretation

Classify ABI-233 as a completed, finite, resource-safe but negative-to-mixed family-development Result for the exact MoE line-voting continuation. The architectural change did not satisfy its primary rationale: selected-checkpoint connectivity is substantially below both ABI-231 and ABI-232, even though the Run remained noncollapsed and achieved useful recall. The high-connectivity epoch 6 and final precision/connectivity recovery suggest the module can sometimes bias predictions toward compact connected structures, but it does not align those structures with the best filtered-Dice checkpoint.

This does not eliminate spectral/SZA-regime MoE in general, because ABI-232 remains a positive late-budget MoE Result. It does weaken the hypothesis that adding this simple strip/diagonal line-voting support is the right way to recover MoE connectivity. The branch looks more like a precision/recall oscillator than a late-improving continuation candidate.

## Decision

Do not promote ABI-233, do not request whole-validation diagnostics, and do not request a `late_improving` continuation of this exact MoE line-voting architecture. No repair Candidate is indicated because the Run completed successfully and the weakness is scientific rather than a contract or implementation failure.

For the next research step, prefer broadening rather than another small MoE head tweak. Reasonable directions are a materially different differentiable Hough/Radon-style line-accumulation scout, or a return to the stronger ABI-223 temporal-attention frontier with a controlled architecture change. If the campaign continues MoE later, it should target a different mechanism for preserving ABI-232 recall while stabilizing the high-connectivity epochs, not simply extend ABI-233 unchanged.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260910_181015_afea31/candidate/PROPOSAL.md`
- `run_20260910_181015_afea31/candidate/README.md`
- `run_20260910_181015_afea31/candidate/manifest.yaml`
- `run_20260910_181015_afea31/resolved_manifest.yaml`
- `run_20260910_181015_afea31/outputs/model_summary.json`
- `run_20260910_181015_afea31/outputs/best_metrics.json`
- `run_20260910_181015_afea31/outputs/final_metrics.json`
- `run_20260910_181015_afea31/outputs/metrics.jsonl`
- `run_20260910_181015_afea31/outputs/resource_profile.json`
- `run_20260910_181015_afea31/outputs/validation_postprocessing/index.json`
- `run_20260910_181015_afea31/outputs/prediction_samples/samples.json`
- `run_20260910_155936_362435` for ABI-231 MoE parent context
- `run_20260910_163616_4f7416` for ABI-232 late36 MoE context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-family frontier context
- `run_20260904_043143_ee0005` for ABI-202 current whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
