# ABI-343 full-spectral BTD+SZA C4 precision-veto recall bridge late36

research-figures: []

## Scope

This note records ABI-343, Candidate `abi343_fullspectral_btd_sza_c4_precision_veto_recall_late36_bce_dice_line_centerline_aux_v1`, and Run `run_20260918_081800_9f0872`.

ABI-343 was a mechanism-changing continuation of the ABI-249/ABI-342 single-frame C4 orientation-prior branch. It kept provider-owned `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW, constant LR, batch size 4, and the approved late-improving budget. The architecture changed ABI-342's direct recall bridge into an anchor-uncertainty-band recall lift, gated by C4 line/detail agreement and paired with a small differentiable low-line-evidence clutter veto.

This is capped representative feasibility evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-343 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved from parent Runs `run_20260911_111909_dd7ef7` and `run_20260918_055403_f17232`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 9,004,415, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 9,199,796,224 / 10,508,828,672 bytes.
- Training wall time: 4,251.3 s; validation wall time: 4,244.5 s; total Run wall time: 8,498.3 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 32.

## Best-validation metrics

| Metric | ABI-343 C4 precision-veto recall bridge | ABI-342 C4 recall bridge | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: |
| Best epoch | 32 | 36 | 31 | 34 |
| Filtered Dice | 0.409827 | 0.415499 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.392320 | 0.398614 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.453242 | 0.460044 | 0.468855 | 0.468151 |
| Filtered precision | 0.417766 | 0.397609 | 0.480886 | 0.439467 |
| Filtered recall | 0.402184 | 0.435075 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.379763 | 0.405280 | 0.392524 | 0.457773 |
| Filtered predicted-positive fraction | 0.003489 | 0.003965 | 0.002767 | 0.003433 |
| Filtered predicted-positive pixels | 468,221 | 532,191 | 371,346 | 460,724 |

The precision-veto head partly achieved its intended trade-off relative to ABI-342: precision improved by +0.0202 and filtered predicted-positive pixels fell by about 64k. However, recall dropped by -0.0329, connectivity dropped by -0.0255, and aggregate filtered Dice fell by -0.0057. Relative to ABI-249, ABI-343 kept a recall gain (+0.0350), but it remained less precise (-0.0631), predicted about 97k more filtered-positive pixels, and lost filtered Dice (-0.0066) and connectivity (-0.0128). It therefore did not meet the preregistered compact-recall success target of matching ABI-249 within about 0.003 filtered Dice while improving recall/connectivity.

Source behavior was finite and source-informative, but neither source improved enough to alter comparator roles. ABI-343 underperformed ABI-249 on MIT filtered Dice by about -0.0041 and on Google by about -0.0156. It also underperformed ABI-342 on both sources.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected epoch, raw Dice was 0.423897 and filtered Dice was 0.409827; raw recall was 0.429476 and filtered recall was 0.402184; raw predicted-positive pixels were 499,166 and filtered predicted-positive pixels were 468,221.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.193774 | 0.205408 | 0.173700 | 0.154661 | 0.259364 | 0.103512 | 0.006077 |
| 5 | 0.352656 | 0.332018 | 0.403561 | 0.446326 | 0.291482 | 0.379501 | 0.002367 |
| 10 | 0.378710 | 0.358847 | 0.425176 | 0.426795 | 0.340364 | 0.368409 | 0.002890 |
| 15 | 0.402344 | 0.392581 | 0.427156 | 0.390536 | 0.414888 | 0.375037 | 0.003850 |
| 20 | 0.401286 | 0.385522 | 0.438951 | 0.444119 | 0.365989 | 0.373928 | 0.002986 |
| 25 | 0.405874 | 0.390135 | 0.442849 | 0.422715 | 0.390324 | 0.342893 | 0.003346 |
| 30 | 0.397094 | 0.371886 | 0.460384 | 0.490506 | 0.333568 | 0.428547 | 0.002464 |
| 32 | 0.409827 | 0.392320 | 0.453242 | 0.417766 | 0.402184 | 0.379763 | 0.003489 |
| 34 | 0.408570 | 0.385027 | 0.468844 | 0.472287 | 0.360001 | 0.459577 | 0.002762 |
| 36 | 0.384610 | 0.355720 | 0.457831 | 0.482826 | 0.319597 | 0.467529 | 0.002399 |

The trajectory was finite and non-collapsed, with alternating compact high-precision states and broader recall states. The best filtered-Dice checkpoint was epoch 32, while the final epoch moved toward a compact high-connectivity/high-precision but low-recall state. This suggests the precision-veto mechanism can steer the C4 branch toward compact predictions, but the current coupling is unstable across epochs and does not preserve ABI-342's useful recall lift at the best aggregate checkpoint.

## Prediction sample check

The retained first-four validation samples all report sample Dice and IoU of 1.0. These fixed first-n samples are traceability artifacts, not representative diagnostics, and likely reflect easy empty or near-empty samples. They should not override the aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-343 as finite but non-frontier C4-family development evidence. It answers the mechanism question by showing that an architecture-internal precision veto can reduce ABI-342's excessive footprint, but the reduction comes with too much loss in recall/connectivity and still does not recover ABI-249's high-precision compact operating point.

Comparator roles after ABI-343:

- ABI-202 remains the aggregate whole-validation filtered-Dice reference.
- ABI-249 remains the compact high-precision single-frame C4 comparator.
- ABI-342 remains the recall-biased C4 diagnostic.
- ABI-343 is a precision-veto diagnostic, not a promotion candidate or comparator replacement.

Do not submit an unchanged late36 continuation of this exact precision-veto recall head. If revisiting the C4/orientation branch, change the mechanism more substantially, for example by separating a stable compact anchor from a learned agreement sidecar, or by using temporal/center-frame evidence sharpening rather than a single signed residual/veto trade-off.

## Decision

Do not promote ABI-343. Do not request a whole-validation diagnostic in this Autonomy Step: the capped result is below ABI-249 and ABI-342 on filtered Dice, misses the stated compact-recall success criteria, and does not create an ambiguous near-frontier promotion case. The next useful handoff should broaden or materially change the mechanism rather than repeat this precision-veto head unchanged.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_081800_9f0872/candidate/PROPOSAL.md`
- `run_20260918_081800_9f0872/candidate/README.md`
- `run_20260918_081800_9f0872/candidate/manifest.yaml`
- `run_20260918_081800_9f0872/candidate/budget_request.yaml`
- `run_20260918_081800_9f0872/resolved_manifest.yaml`
- `run_20260918_081800_9f0872/execution.json`
- `run_20260918_081800_9f0872/run_metadata.json`
- `run_20260918_081800_9f0872/outputs/model_summary.json`
- `run_20260918_081800_9f0872/outputs/best_metrics.json`
- `run_20260918_081800_9f0872/outputs/final_metrics.json`
- `run_20260918_081800_9f0872/outputs/metrics.jsonl`
- `run_20260918_081800_9f0872/outputs/resource_profile.json`
- `run_20260918_081800_9f0872/outputs/validation_postprocessing/index.json`
- `run_20260918_081800_9f0872/outputs/prediction_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 comparison context
- `run_20260918_055403_f17232/outputs/best_metrics.json` for ABI-342 comparison context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
