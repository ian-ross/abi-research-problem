# ABI-256 temporal recurrent centerline-decoder U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-256, Candidate `abi256_temporal_recurrent_centerline_decoder_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_230821_08caf0`.

ABI-256 was a mechanism-changing temporal recurrent family-development Candidate after ABI-255. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 2, constant learning rate, and trusted Line/Centerline auxiliary outputs. The intended change was a high-resolution centerline-preserving decoder bridge that fused decoder features, full-resolution skip evidence, temporal-stem evidence, and directional context before the mask and auxiliary heads.

Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-256 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,210,267, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.15 / 4.36 GB.
- Training wall time: 1,185.1 s; validation wall time: 1,070.6 s; total Run wall time: 2,257.4 s.

This is valid finite/resource evidence for the centerline-decoder bridge, but only capped temporal-eligible feasibility evidence, not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 11.

| Metric | ABI-256 best epoch 11 | ABI-256 final epoch 12 | ABI-255 recurrent late36 | ABI-254 center-detail exploratory | ABI-240 line-accum late36 | ABI-223 temporal-attn late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.388988 | 0.380444 | 0.417348 | 0.393943 | 0.414892 | 0.419776 | 0.427570 |
| Raw Dice | 0.404980 | 0.397525 | 0.435656 | 0.412509 | 0.431959 | 0.438487 | 0.442746 |
| Filtered precision | 0.415080 | 0.446448 | 0.468293 | 0.486613 | 0.436241 | 0.483764 | 0.439467 |
| Filtered recall | 0.365981 | 0.331443 | 0.376400 | 0.330922 | 0.395534 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.246300 | 0.267794 | 0.281116 | 0.365528 | 0.264863 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.367406 | 0.363754 | 0.400833 | 0.377873 | 0.397067 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.443100 | 0.422518 | 0.463143 | 0.436096 | 0.460659 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004558 | 0.003838 | 0.004155 | 0.003516 | 0.004687 | 0.003962 | 0.003433 |

Relative to ABI-255, ABI-256 regressed filtered Dice by about -0.0284, raw Dice by -0.0307, precision by -0.0532, recall by -0.0104, connectivity by -0.0348, MIT Dice by -0.0334, and Google Dice by -0.0200 at the selected checkpoint. The bridge therefore did not improve the recurrent branch's primary weakness. It raised the predicted-positive fraction relative to ABI-255 but did not convert that additional area into better precision, overlap, or continuity.

Relative to ABI-254, ABI-256 improved recall slightly but trailed on filtered Dice, precision, and especially connectivity. Relative to ABI-240, ABI-223, and ABI-202, ABI-256 remains materially behind the best temporal line/attention comparators and the single-frame whole-validation frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.225182 | 0.225470 | 0.224557 | 0.242348 | 0.210286 | 0.179459 | 0.004486 |
| 2 | 0.282695 | 0.281880 | 0.284452 | 0.281004 | 0.284407 | 0.167168 | 0.005232 |
| 3 | 0.299924 | 0.289740 | 0.322160 | 0.309140 | 0.291241 | 0.170397 | 0.004870 |
| 4 | 0.297649 | 0.275982 | 0.352446 | 0.462448 | 0.219447 | 0.313053 | 0.002453 |
| 5 | 0.338918 | 0.313722 | 0.403984 | 0.511128 | 0.253506 | 0.371507 | 0.002564 |
| 6 | 0.347559 | 0.348335 | 0.345787 | 0.285121 | 0.445010 | 0.189998 | 0.008069 |
| 7 | 0.259512 | 0.235241 | 0.322387 | 0.479083 | 0.177953 | 0.302277 | 0.001920 |
| 8 | 0.376732 | 0.361019 | 0.416105 | 0.423691 | 0.339144 | 0.260005 | 0.004138 |
| 9 | 0.366535 | 0.351668 | 0.402453 | 0.367096 | 0.365976 | 0.214549 | 0.005154 |
| 10 | 0.344476 | 0.318525 | 0.415137 | 0.582268 | 0.244589 | 0.452747 | 0.002172 |
| 11 | 0.388988 | 0.367406 | 0.443100 | 0.415080 | 0.365981 | 0.246300 | 0.004558 |
| 12 | 0.380444 | 0.363754 | 0.422518 | 0.446448 | 0.331443 | 0.267794 | 0.003838 |

The trajectory is finite and non-collapsed but noisy. The highest connectivity checkpoint, epoch 10, reached 0.452747 connectivity by shrinking the predicted-positive fraction to 0.002172 and sacrificing recall and aggregate Dice. The selected epoch 11 recovered recall and source-balanced overlap but lost most of that connectivity. This looks like an unstable precision/connectivity versus recall tradeoff, not a clean late-improving trajectory.

## Interpretation

Classify ABI-256 as a negative/mixed family-development Result for this exact centerline-decoder bridge. It confirms that the implementation is resource-safe and source-informative, but the bridge did not solve the ABI-255 diagnostic finding that recurrent temporal evidence is under-connected and somewhat diffuse. Instead, ABI-256 traded between compact high-connectivity low-recall states and broader lower-connectivity states, with the best filtered-Dice checkpoint below ABI-255 and below the strongest temporal attention/line comparators.

Low score alone does not eliminate temporal recurrent modeling. However, this exact decoder-bridge mechanism failed its proposal success criteria: it neither improved connectivity over ABI-255 at a useful overlap point nor improved filtered Dice over the recurrent late36 family. The result also does not justify a late-improving budget request, because the selected checkpoint is epoch 11 and final epoch 12 regressed.

## Decision

Do not promote ABI-256. Do not submit an unchanged late36 continuation of this centerline-decoder bridge. Stop this exact bridge unless future diagnostics reveal a specific repairable implementation issue.

If the campaign continues with temporal modeling, prefer a different mechanism: e.g. a line-aware recurrent state that carries orientation evidence through time, a temporal attention/change architecture that preserves ABI-223/238 connectivity, or a recall-preserving evidence head that raises true temporal contrail logits without Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling. If broadening away from temporal modeling, keep ABI-255 as the compact recurrent comparator and ABI-223/238 as the temporal attention/connectivity comparators.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_230821_08caf0/candidate/PROPOSAL.md`
- `run_20260911_230821_08caf0/candidate/README.md`
- `run_20260911_230821_08caf0/candidate/manifest.yaml`
- `run_20260911_230821_08caf0/resolved_manifest.yaml`
- `run_20260911_230821_08caf0/outputs/model_summary.json`
- `run_20260911_230821_08caf0/outputs/best_metrics.json`
- `run_20260911_230821_08caf0/outputs/final_metrics.json`
- `run_20260911_230821_08caf0/outputs/metrics.jsonl`
- `run_20260911_230821_08caf0/outputs/resource_profile.json`
- `run_20260911_230821_08caf0/outputs/validation_postprocessing/index.json`
- `run_20260911_230821_08caf0/outputs/prediction_samples/samples.json`
- `run_20260911_210922_27f346` for ABI-255 recurrent late36 comparator context
- `run_20260911_202724_fee837` for ABI-254 temporal center-detail exploratory context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-attention late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
