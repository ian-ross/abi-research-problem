# ABI-322 temporal five-frame C4 clDice-connectivity line-state late36

research-figures: []

## Scope

This note records ABI-322, Candidate `abi322_temporal_fiveframe_c4_cldice_connectivity_line_state_late36_bce_dice_cldice_line_centerline_aux_v1`, Run `run_20260915_191945_382cc4`.

ABI-322 was a trusted-loss-policy continuation of ABI-311's five-frame temporal C4 persistence/contrast line-state U-Net. It kept the provider-owned five-frame `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` selection with offsets `[-2, -1, 0, 1, 2]`, combined source-balanced sampling, random mirroring, Line and Centerline auxiliaries, and the ABI-311 architecture. The intended mechanism change was only to replace the primary loss with the allowlisted `bce_dice_cldice`, testing whether topology-aware loss optimization would improve connected thin-line continuity or MIT/positive-patch undercoverage without Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, temporal lookup, sampling, coordinates, or resource control.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable to the full-validation ABI-202/249 frontier.

## Execution result

ABI-322 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from parent Runs `run_20260915_015552_1ac51f`, `run_20260915_110252_3a6dca`, and `run_20260915_072045_06149f`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,245,655, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 6,407,848,960 / 6,736,052,224 bytes.
- Training wall time: 5,619.9 s; validation wall time: 3,698.7 s; total Run wall time: 9,320.8 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-322 clDice loss | ABI-311 BCE-Dice C4 | Delta vs ABI-311 | ABI-309 recall head | ABI-306 compact C4 | ABI-223 temporal-attention comparator |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | 0 | 29 | 36 | 36 |
| Filtered Dice | 0.408833 | 0.425000 | -0.016167 | 0.423544 | 0.422548 | 0.419776 |
| MIT filtered Dice | 0.389965 | 0.403831 | -0.013866 | 0.402446 | 0.402764 | 0.398498 |
| Google filtered Dice | 0.454823 | 0.482615 | -0.027792 | 0.478510 | 0.476152 | 0.476764 |
| Filtered precision | 0.432738 | 0.459703 | -0.026965 | 0.401806 | 0.493422 | 0.483764 |
| Filtered recall | 0.387431 | 0.395169 | -0.007738 | 0.447768 | 0.369478 | 0.370738 |
| Filtered connectivity | 0.344667 | 0.366735 | -0.022068 | 0.316074 | 0.299384 | 0.412427 |
| Filtered predicted-positive fraction | 0.004628 | 0.004444 | +0.000184 | 0.005761 | 0.003871 | 0.003962 |

ABI-322 did not deliver the intended topology-aware gain. Relative to ABI-311, the same architecture trained with `bce_dice_cldice` is lower on aggregate filtered Dice, both Dataset Sources, precision, recall, and connectivity while producing a slightly larger filtered footprint. Relative to ABI-309, ABI-322 is more precise and more compact but loses substantial recall and aggregate/source Dice. Relative to ABI-306, ABI-322 buys modest recall and connectivity but loses aggregate/source Dice, precision, and compactness. Relative to ABI-223, ABI-322 has slightly higher recall but lower Dice, precision, Google performance, and much lower connectivity.

At the selected checkpoint, raw Dice was 0.425574 versus filtered Dice 0.408833, raw recall was 0.418418 versus filtered recall 0.387431, and raw predicted-positive fraction was 0.004996 versus filtered predicted-positive fraction 0.004628. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.212677 | 0.211711 | 0.214838 | 0.260766 | 0.179563 | 0.217169 | 0.003560 |
| 2 | 0.164242 | 0.174593 | 0.147365 | 0.115712 | 0.282885 | 0.101936 | 0.012638 |
| 3 | 0.284799 | 0.280684 | 0.294088 | 0.282975 | 0.286647 | 0.199557 | 0.005237 |
| 4 | 0.288791 | 0.277920 | 0.313051 | 0.279360 | 0.298882 | 0.152285 | 0.005531 |
| 5 | 0.317361 | 0.294197 | 0.374701 | 0.399469 | 0.263251 | 0.324452 | 0.003407 |
| 6 | 0.284678 | 0.289498 | 0.274833 | 0.215534 | 0.419139 | 0.181087 | 0.010053 |
| 7 | 0.352796 | 0.338539 | 0.387386 | 0.377161 | 0.331388 | 0.266079 | 0.004542 |
| 8 | 0.353065 | 0.337994 | 0.390745 | 0.408935 | 0.310626 | 0.337324 | 0.003927 |
| 9 | 0.354288 | 0.347388 | 0.369845 | 0.343155 | 0.366168 | 0.247986 | 0.005516 |
| 10 | 0.359901 | 0.342503 | 0.401002 | 0.386645 | 0.336617 | 0.320997 | 0.004501 |
| 11 | 0.361145 | 0.347866 | 0.392164 | 0.381275 | 0.343034 | 0.266371 | 0.004651 |
| 12 | 0.335007 | 0.322304 | 0.362852 | 0.337945 | 0.332120 | 0.214162 | 0.005080 |
| 13 | 0.339604 | 0.321868 | 0.382611 | 0.428312 | 0.281336 | 0.310413 | 0.003396 |
| 14 | 0.301844 | 0.278553 | 0.358099 | 0.360642 | 0.259532 | 0.257577 | 0.003720 |
| 15 | 0.376090 | 0.360583 | 0.416899 | 0.485748 | 0.306824 | 0.467109 | 0.003265 |
| 16 | 0.376947 | 0.367348 | 0.399722 | 0.354755 | 0.402102 | 0.243504 | 0.005860 |
| 17 | 0.357745 | 0.345609 | 0.385703 | 0.329814 | 0.390844 | 0.246017 | 0.006126 |
| 18 | 0.343181 | 0.328951 | 0.374146 | 0.328495 | 0.359242 | 0.231587 | 0.005653 |
| 19 | 0.363209 | 0.349542 | 0.396412 | 0.381716 | 0.346413 | 0.264058 | 0.004691 |
| 20 | 0.390353 | 0.372284 | 0.436898 | 0.480157 | 0.328848 | 0.400187 | 0.003541 |
| 21 | 0.375946 | 0.352860 | 0.433199 | 0.462223 | 0.316811 | 0.366548 | 0.003543 |
| 22 | 0.383912 | 0.369239 | 0.423006 | 0.495880 | 0.313194 | 0.486769 | 0.003265 |
| 23 | 0.389476 | 0.368701 | 0.443132 | 0.455098 | 0.340393 | 0.350571 | 0.003867 |
| 24 | 0.372625 | 0.346762 | 0.436289 | 0.447784 | 0.319069 | 0.358523 | 0.003684 |
| 25 | 0.364979 | 0.341409 | 0.426308 | 0.507123 | 0.285074 | 0.405810 | 0.002906 |
| 26 | 0.391507 | 0.378054 | 0.424294 | 0.406752 | 0.377364 | 0.295892 | 0.004796 |
| 27 | 0.408833 | 0.389965 | 0.454823 | 0.432738 | 0.387431 | 0.344667 | 0.004628 |
| 28 | 0.351870 | 0.331893 | 0.400083 | 0.447197 | 0.290043 | 0.276880 | 0.003353 |
| 29 | 0.380954 | 0.363661 | 0.422208 | 0.426912 | 0.343930 | 0.269740 | 0.004165 |
| 30 | 0.394069 | 0.372778 | 0.449247 | 0.479988 | 0.334239 | 0.420890 | 0.003600 |
| 31 | 0.369260 | 0.350285 | 0.416097 | 0.443581 | 0.316270 | 0.250271 | 0.003686 |
| 32 | 0.369074 | 0.346738 | 0.423995 | 0.423943 | 0.326780 | 0.268881 | 0.003985 |
| 33 | 0.400078 | 0.381597 | 0.445921 | 0.412801 | 0.388117 | 0.338150 | 0.004860 |
| 34 | 0.378203 | 0.366287 | 0.406525 | 0.374979 | 0.381484 | 0.353343 | 0.005259 |
| 35 | 0.350769 | 0.327121 | 0.409561 | 0.452051 | 0.286565 | 0.308443 | 0.003277 |
| 36 | 0.404330 | 0.389553 | 0.440571 | 0.406485 | 0.402199 | 0.296586 | 0.005115 |

The trajectory is finite and source-informative, but unstable. ABI-322 reaches transient high-connectivity checkpoints at epochs 15, 22, 25, and 30, yet none coincide with the selected best Dice/source-balance checkpoint. The selected epoch 27 improves aggregate/source Dice after a late recovery, but its connectivity remains below ABI-311 and ABI-223. The final epoch has higher recall than the selected checkpoint, but only with lower precision, lower Google Dice, and much weaker connectivity. This is not evidence that more epochs would cleanly solve the target trade-off.

The clDice loss appears to broaden or destabilize the prediction surface rather than preserve ABI-311's balanced compact operating point. It can briefly raise the topology metric, but those peaks do not translate into stable filtered Dice, source balance, or retained connected-line improvement at the fixed threshold.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4146, 0.1184, 0.4290, and 0.3886. This confirms finite non-collapsed predictions but includes one very weak retained sample and does not provide qualitative support for promotion.

## Interpretation

Classify ABI-322 as a valid but negative trusted-loss-policy continuation. It cleanly tested an allowlisted loss change under the Candidate boundary and within the approved late-improving budget, but `bce_dice_cldice` did not stabilize connected thin-line predictions for the ABI-311 temporal C4 line-state architecture.

The main lesson is that topology-aware loss alone is insufficient for this branch. ABI-322 loses the key ABI-311 balanced aggregate/source/precision/recall trade-off and does not retain a connectivity advantage. Its transient connectivity spikes resemble the broader pattern from ABI-316 and nearby temporal continuity variants: architecture/loss mechanisms can momentarily raise line-like metrics, but the selected fixed-threshold mask remains below the stronger temporal C4 and temporal-attention comparators.

Comparator roles after ABI-322:

- ABI-311 remains the balanced five-frame temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 comparator.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-316 remains negative evidence for decoder-stage line-continuity bridge injection.
- ABI-322 is negative evidence for an unchanged ABI-311 architecture trained with trusted `bce_dice_cldice`.

## Decision

Do not promote ABI-322. Do not request temporal-eligible failure-bucket diagnostics for this capped Result: aggregate/source metrics, fixed-threshold recall/precision behavior, and the connectivity trajectory already show that the target improvement was not achieved. Do not submit an unchanged clDice continuation of ABI-311; the branch used the late-improving budget and regressed against its direct parent.

Future temporal work should be mechanism-changing rather than another ABI-311 loss/calibration/head variant. Better next directions include a different temporal-attention evidence-sharpening path that raises true contrail logits without broadening clutter, or a return to single-frame ABI-249-style C4/orientation support paired with center-frame detail/cross-scale recall support.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_191945_382cc4/candidate/PROPOSAL.md`
- `run_20260915_191945_382cc4/candidate/README.md`
- `run_20260915_191945_382cc4/candidate/manifest.yaml`
- `run_20260915_191945_382cc4/candidate/budget_request.yaml`
- `run_20260915_191945_382cc4/resolved_manifest.yaml`
- `run_20260915_191945_382cc4/execution.json`
- `run_20260915_191945_382cc4/outputs/model_summary.json`
- `run_20260915_191945_382cc4/outputs/best_metrics.json`
- `run_20260915_191945_382cc4/outputs/final_metrics.json`
- `run_20260915_191945_382cc4/outputs/metrics.jsonl`
- `run_20260915_191945_382cc4/outputs/resource_profile.json`
- `run_20260915_191945_382cc4/outputs/validation_postprocessing/index.json`
- `run_20260915_191945_382cc4/outputs/prediction_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260915_110252_3a6dca/outputs/best_metrics.json` and `/history/research-notes/abi316-temporal-fiveframe-decoder-line-continuity-bridge-late36.md` for ABI-316 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
