# ABI-316 temporal five-frame decoder line-continuity bridge late36

research-figures: []

## Scope

This note records the bounded late-improving temporal-eligible Result for ABI-316, Candidate `abi316_temporal_fiveframe_decoder_line_continuity_bridge_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260915_110252_3a6dca`.

ABI-316 was a mechanism-changing family-development continuation of ABI-311's five-frame temporal C4 persistence/contrast line-state branch. It kept the provider-owned five-frame `abi_16ch_plus_sza_temporal` input, centered temporal attention, early C4 orientation line state, compact U-Net encoder/decoder, and dual-evidence mask/Line/Centerline head. The changed mechanism was decoder-stage line-continuity bridges: the early temporal C4 line state was resized into decoder scales and added through gated orientation-aware refinements before logits, rather than through the late-logit calibration used by ABI-312/313.

The intended target was to preserve ABI-311's balanced footprint while improving MIT filtered Dice, fixed-threshold recall, or connected-line continuity. This is capped temporal-eligible feasibility evidence only, not whole-validation promotion evidence and not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-316 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from parent Runs `run_20260915_015552_1ac51f`, `run_20260915_043533_14234b`, and `run_20260915_072045_06149f`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,383,351, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 8.01 / 8.70 GB.
- Total Run wall time: 10,487.9 s, within the 10,800 s late-improving timeout but near the ceiling.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 34.

## Best-validation metrics

| Metric | ABI-316 decoder bridge | ABI-311 five-frame C4 | Delta vs ABI-311 | ABI-309 recall head | Delta vs ABI-309 | ABI-306 compact C4 | Delta vs ABI-306 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 34 | 27 | +7 | 29 | +5 | 36 | -2 |
| Filtered Dice | 0.416386 | 0.425000 | -0.008614 | 0.423544 | -0.007158 | 0.422548 | -0.006162 |
| MIT filtered Dice | 0.395914 | 0.403831 | -0.007917 | 0.402446 | -0.006532 | 0.402764 | -0.006850 |
| Google filtered Dice | 0.468367 | 0.482615 | -0.014248 | 0.478510 | -0.010143 | 0.476152 | -0.007785 |
| Filtered precision | 0.451488 | 0.459703 | -0.008215 | 0.401806 | +0.049682 | 0.493422 | -0.041933 |
| Filtered recall | 0.386349 | 0.395169 | -0.008820 | 0.447768 | -0.061420 | 0.369478 | +0.016871 |
| Filtered connectivity | 0.257752 | 0.366735 | -0.108982 | 0.316074 | -0.058322 | 0.299384 | -0.041632 |
| Filtered predicted-positive fraction | 0.004424 | 0.004444 | -0.000020 | 0.005761 | -0.001337 | 0.003871 | +0.000553 |
| Filtered predicted-positive pixels | 467,919 | 470,049 | -2,130 | 609,361 | -141,442 | 409,457 | +58,462 |

ABI-316 does not improve the main target trade-off. Against ABI-311 it keeps essentially the same compact prediction footprint, but is lower on aggregate filtered Dice, both Dataset Sources, precision, recall, and especially connected-line continuity. Against ABI-309 it avoids the broad recall-heavy footprint and has better precision, but loses substantial recall and connectivity. Against ABI-306 it buys modest recall at the cost of lower precision, worse aggregate/source Dice, weaker connectivity, and a larger footprint.

At the selected checkpoint, raw Dice was 0.433711 versus filtered Dice 0.416386, raw recall was 0.417041 versus filtered recall 0.386349, and raw predicted-positive pixels were 504,777 versus 467,919 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212887 | 0.202507 | 0.240009 | 0.402379 | 0.144730 | 0.354698 | 0.001859 |
| 2 | 0.255424 | 0.264089 | 0.239303 | 0.203225 | 0.343707 | 0.126240 | 0.008743 |
| 3 | 0.311359 | 0.292456 | 0.355635 | 0.379883 | 0.263778 | 0.249394 | 0.003590 |
| 4 | 0.308158 | 0.289729 | 0.348977 | 0.366620 | 0.265777 | 0.202048 | 0.003748 |
| 5 | 0.306413 | 0.280911 | 0.373513 | 0.568472 | 0.209730 | 0.462719 | 0.001907 |
| 6 | 0.314269 | 0.304131 | 0.335703 | 0.324621 | 0.304556 | 0.144720 | 0.004850 |
| 7 | 0.317893 | 0.287917 | 0.395154 | 0.518618 | 0.229188 | 0.346332 | 0.002285 |
| 8 | 0.371702 | 0.359352 | 0.399616 | 0.356066 | 0.388775 | 0.200610 | 0.005644 |
| 9 | 0.378696 | 0.364195 | 0.413898 | 0.383602 | 0.373915 | 0.219353 | 0.005039 |
| 10 | 0.347790 | 0.318970 | 0.420414 | 0.529265 | 0.258988 | 0.360449 | 0.002530 |
| 11 | 0.396402 | 0.375879 | 0.448103 | 0.451701 | 0.353165 | 0.283192 | 0.004042 |
| 12 | 0.379534 | 0.357801 | 0.434707 | 0.480074 | 0.313814 | 0.322030 | 0.003379 |
| 13 | 0.382303 | 0.363602 | 0.427481 | 0.399512 | 0.366515 | 0.216870 | 0.004743 |
| 14 | 0.322727 | 0.297973 | 0.384731 | 0.501378 | 0.237943 | 0.249868 | 0.002453 |
| 15 | 0.360059 | 0.338865 | 0.414176 | 0.502646 | 0.280491 | 0.327637 | 0.002885 |
| 16 | 0.384253 | 0.365245 | 0.429627 | 0.412963 | 0.359275 | 0.183830 | 0.004497 |
| 17 | 0.381615 | 0.356551 | 0.442214 | 0.431560 | 0.342032 | 0.264573 | 0.004097 |
| 18 | 0.375698 | 0.367125 | 0.395641 | 0.330035 | 0.436026 | 0.166619 | 0.006830 |
| 19 | 0.379310 | 0.353741 | 0.442679 | 0.470569 | 0.317698 | 0.262985 | 0.003490 |
| 20 | 0.384033 | 0.359433 | 0.447022 | 0.490942 | 0.315359 | 0.228819 | 0.003321 |
| 21 | 0.398662 | 0.379227 | 0.445755 | 0.438676 | 0.365338 | 0.231849 | 0.004305 |
| 22 | 0.411254 | 0.391180 | 0.464057 | 0.472307 | 0.364178 | 0.334471 | 0.003986 |
| 23 | 0.382149 | 0.363081 | 0.430259 | 0.475281 | 0.319536 | 0.239911 | 0.003476 |
| 24 | 0.393312 | 0.369515 | 0.453548 | 0.483677 | 0.331397 | 0.305638 | 0.003542 |
| 25 | 0.396387 | 0.372570 | 0.459930 | 0.546725 | 0.310897 | 0.431885 | 0.002940 |
| 26 | 0.384312 | 0.360549 | 0.446519 | 0.528889 | 0.301809 | 0.380210 | 0.002950 |
| 27 | 0.407354 | 0.382783 | 0.468845 | 0.447672 | 0.373699 | 0.295446 | 0.004315 |
| 28 | 0.363953 | 0.338726 | 0.429570 | 0.528819 | 0.277454 | 0.322818 | 0.002712 |
| 29 | 0.406793 | 0.389811 | 0.447459 | 0.415217 | 0.398704 | 0.296927 | 0.004964 |
| 30 | 0.379003 | 0.350652 | 0.449249 | 0.495232 | 0.306961 | 0.283260 | 0.003204 |
| 31 | 0.400187 | 0.373645 | 0.467327 | 0.469059 | 0.348950 | 0.222245 | 0.003846 |
| 32 | 0.398053 | 0.369435 | 0.471590 | 0.528843 | 0.319128 | 0.290199 | 0.003120 |
| 33 | 0.404194 | 0.380828 | 0.463294 | 0.458633 | 0.361307 | 0.200266 | 0.004073 |
| 34 | 0.416386 | 0.395914 | 0.468367 | 0.451488 | 0.386349 | 0.257752 | 0.004424 |
| 35 | 0.378376 | 0.352027 | 0.445116 | 0.501949 | 0.303627 | 0.291956 | 0.003127 |
| 36 | 0.390885 | 0.365775 | 0.454158 | 0.405260 | 0.377495 | 0.293081 | 0.004815 |

The trajectory is finite and source-informative, with several late recoveries after noisy regressions. However, it is not a stable late-improving frontier trajectory. The selected epoch 34 peak follows oscillations rather than a clean ascent, and the final two epochs fall back below the peak. Connectivity spikes appear at epochs 5, 25, and 26, but none coincide with the best Dice/recall/source balance and none are retained at the selected checkpoint. This is the same failure pattern seen in several temporal continuity variants: architecture-internal line support can briefly raise connectivity-like signal, but it does not convert into stable fixed-threshold connected Contrail Masks.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2842, 0.1897, 0.4693, and 0.2971. This confirms finite non-collapsed predictions but also shows mixed retained-sample quality with no obvious qualitative basis for promotion.

## Interpretation

Classify ABI-316 as a valid but negative temporal C4 decoder-continuity continuation. It demonstrates that multi-scale decoder injection of the early temporal C4 line state is executable within the active late-improving resource policy, but it does not repair ABI-311's core weakness. The bridge preserves a compact footprint, yet loses the very metrics it was meant to improve: MIT filtered Dice, fixed-threshold recall, and especially connected-line continuity.

The likely mechanism failure is that resizing and gating an early orientation line state into decoder features acts mostly as another noisy feature-conditioning path. It sometimes produces high precision or transient connectivity, but the selected checkpoint does not retain a connected-line advantage. The added decoder bridge also increases runtime and peak memory relative to simpler temporal C4 comparators while remaining below them scientifically.

Comparator roles after ABI-316:

- ABI-311 remains the balanced five-frame temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 comparator with known footprint cost.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-312 and ABI-313 remain negative/mixed late-logit calibration continuations.
- ABI-316 is a resource-feasible but non-frontier decoder-continuity-bridge continuation.

ABI-316 does not warrant an immediate temporal-eligible failure-bucket evaluation. The capped aggregate/source/connectivity metrics already show that it misses the specified target improvements, and its wall time is close enough to the late-improving timeout that unchanged continuations would be a poor use of budget.

## Decision

Do not promote ABI-316 and do not submit an unchanged continuation of the five-frame temporal C4 decoder-bridge branch. Treat it as evidence that simply injecting early temporal C4 line state into decoder scales does not stabilize connected thin-line predictions.

The next useful hypothesis should broaden away from this exact temporal C4 decoder/head-calibration neighborhood. Good next directions include a different temporal-attention evidence-sharpening mechanism that raises true contrail logits without expanding clutter, or a return to single-frame C4/orientation recall support where ABI-249's precision can be paired with center-frame detail or cross-scale evidence. Any next work must preserve provider-owned temporal input, trusted losses/metrics/Artifact Filters, coordinate exclusion, and Harness-owned resource policy.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_110252_3a6dca/candidate/PROPOSAL.md`
- `run_20260915_110252_3a6dca/candidate/README.md`
- `run_20260915_110252_3a6dca/candidate/manifest.yaml`
- `run_20260915_110252_3a6dca/candidate/budget_request.yaml`
- `run_20260915_110252_3a6dca/resolved_manifest.yaml`
- `run_20260915_110252_3a6dca/execution.json`
- `run_20260915_110252_3a6dca/outputs/model_summary.json`
- `run_20260915_110252_3a6dca/outputs/best_metrics.json`
- `run_20260915_110252_3a6dca/outputs/final_metrics.json`
- `run_20260915_110252_3a6dca/outputs/metrics.jsonl`
- `run_20260915_110252_3a6dca/outputs/resource_profile.json`
- `run_20260915_110252_3a6dca/outputs/validation_postprocessing/index.json`
- `run_20260915_110252_3a6dca/outputs/prediction_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260915_043533_14234b/outputs/best_metrics.json` and `/history/research-notes/abi312-temporal-fiveframe-selective-consensus-stabilized-late36.md` for ABI-312 comparison context
- `run_20260915_072045_06149f/outputs/best_metrics.json` and `/history/research-notes/abi313-temporal-fiveframe-continuity-protected-calibration-late36.md` for ABI-313 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
