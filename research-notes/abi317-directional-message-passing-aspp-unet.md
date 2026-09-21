# ABI-317 directional message-passing ASPP U-Net

research-figures: []

## Scope

This note records ABI-317, Candidate `abi317_fullspectral_btd_sza_directional_message_passing_aspp_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260915_140910_e2f4a6`.

ABI-317 was a bounded exploratory single-frame continuation after the recent C4/orientation-prior and temporal continuity branches. It kept the provider-approved `abi_16ch_plus_sza` input and an ABI-202-style full-spectral BTD+Solar Geometry Input signed-detail ASPP U-Net, but replaced the final consensus bridge with an architecture-internal directional message-passing continuity bridge. The bridge propagated decoder/detail evidence along horizontal, vertical, and diagonal directions over no-wrap shift distances, then gated those messages with cross-scale and detail agreement before bounded residual refinement.

The intended mechanism was to improve connected thin-line support without Candidate-owned thresholds, morphology, postprocessing, Artifact Filters, custom losses, metrics, data loading, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-317 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude remained forbidden.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 8,148,096, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 11,362,946,560 / 12,956,205,056 bytes.
- Training wall time: 2,043.5 s; validation wall time: 1,537.8 s; total Run wall time: 3,583.2 s, within but very close to the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-317 message passing | ABI-202 aggregate reference | ABI-249 compact C4 | ABI-279 C4 recall bridge | ABI-280 selective C4 | ABI-302 clDice ABI-202 | ABI-303 protected C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 34 | 31 | 22 | 22 | 32 | 9 |
| Filtered Dice | 0.378578 | 0.427570 | 0.416400 | 0.414518 | 0.415244 | 0.407105 | 0.377921 |
| MIT filtered Dice | 0.358874 | 0.411992 | 0.396436 | 0.398381 | 0.405113 | 0.398270 | 0.361436 |
| Google filtered Dice | 0.429382 | 0.468151 | 0.468855 | 0.457385 | 0.442121 | 0.428892 | 0.419321 |
| Filtered precision | 0.430076 | 0.439467 | 0.480886 | 0.442551 | 0.425162 | 0.377587 | 0.446396 |
| Filtered recall | 0.338094 | 0.416301 | 0.367165 | 0.389825 | 0.405778 | 0.441628 | 0.327659 |
| Filtered connectivity | 0.384513 | 0.457773 | 0.392524 | 0.439185 | 0.316291 | 0.398449 | 0.322926 |
| Filtered predicted-positive fraction | 0.002849 | 0.003433 | 0.002767 | 0.003192 | 0.003458 | 0.004238 | 0.002660 |
| Filtered predicted-positive pixels | 382,342 | 460,724 | 371,346 | 428,416 | 464,188 | not recorded here | 356,995 |

ABI-317 is finite and source-informative, but not a frontier result. It lands near ABI-303 in aggregate filtered Dice while using a slightly broader footprint and achieving better recall/connectivity than ABI-303. That comparison shows that non-C4 directional message passing can create a more connected selected checkpoint than the protected C4 recall head.

However, relative to the real comparators, ABI-317 remains clearly weak. Against ABI-202 it is lower by about -0.0490 filtered Dice, -0.0531 MIT filtered Dice, -0.0388 Google filtered Dice, -0.0094 precision, -0.0782 recall, and -0.0733 connectivity. Against ABI-249 it is lower by about -0.0378 filtered Dice, -0.0376 MIT Dice, -0.0395 Google Dice, -0.0508 precision, -0.0291 recall, and -0.0080 connectivity, with a slightly broader footprint. Against ABI-279/280, ABI-317 does not recover the desired fixed-threshold recall or source balance.

At the selected checkpoint, raw Dice was 0.393402 versus filtered Dice 0.378578, raw recall was 0.361983 versus filtered recall 0.338094, and raw predicted-positive fraction was 0.003045 versus filtered predicted-positive fraction 0.002849. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.172970 | 0.202682 | 0.131010 | 0.117804 | 0.325313 | 0.087612 | 0.010007 |
| 2 | 0.274354 | 0.284754 | 0.254271 | 0.250276 | 0.303558 | 0.171795 | 0.004395 |
| 3 | 0.322391 | 0.331708 | 0.302471 | 0.292055 | 0.359759 | 0.215281 | 0.004464 |
| 4 | 0.287401 | 0.305868 | 0.254366 | 0.230709 | 0.381033 | 0.133092 | 0.005985 |
| 5 | 0.343906 | 0.341297 | 0.349656 | 0.364206 | 0.325749 | 0.230500 | 0.003241 |
| 6 | 0.359299 | 0.358552 | 0.360925 | 0.337160 | 0.384549 | 0.234093 | 0.004133 |
| 7 | 0.301398 | 0.287338 | 0.336927 | 0.497831 | 0.216121 | 0.400172 | 0.001573 |
| 8 | 0.358261 | 0.354341 | 0.366679 | 0.385543 | 0.334584 | 0.243150 | 0.003145 |
| 9 | 0.341196 | 0.324212 | 0.382205 | 0.420917 | 0.286865 | 0.272026 | 0.002470 |
| 10 | 0.351906 | 0.342306 | 0.372396 | 0.368804 | 0.336488 | 0.194295 | 0.003306 |
| 11 | 0.371052 | 0.367619 | 0.379091 | 0.357408 | 0.385781 | 0.223920 | 0.003911 |
| 12 | 0.378578 | 0.358874 | 0.429382 | 0.430076 | 0.338094 | 0.384513 | 0.002849 |

The trajectory is finite and not collapsed. The best checkpoint occurs at the final exploratory epoch, and filtered Dice improves from epochs 10 through 12. That late peak means the mechanism is not proven fully exhausted by this 12-epoch scout.

The detailed trajectory also shows the main failure mode. Directional message passing can create compact/high-connectivity states: epoch 7 reached 0.4978 precision and 0.4002 connectivity, and epoch 12 retained 0.3845 connectivity. But those states under-recall true contrails. The more recall-heavy checkpoints at epochs 4, 6, and 11 do not preserve the connected-line signal or aggregate/source Dice. The bridge therefore exposes the familiar precision/recall/connectivity trade-off rather than resolving it.

The source split is also not favorable. The selected checkpoint has Google filtered Dice 0.4294 but MIT filtered Dice only 0.3589, a gap of about 0.0705. A mechanism meant to support thin-line continuity should not worsen MIT/source balance this strongly relative to ABI-202/249/279/280.

## Prediction sample check

The retained fixed first-four validation prediction samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were near zero, near zero, near zero, and 1.0. This confirms finite non-collapsed retained outputs but does not provide qualitative evidence for promotion or elimination.

## Interpretation

Classify ABI-317 as a valid, resource-feasible, scientifically useful but negative directional-message-passing scout. It demonstrates that no-wrap shift-based line propagation can be executed within the Candidate contract and can produce compact connected-line evidence. It does not yet translate that evidence into the target fixed-threshold trade-off: filtered Dice, recall, and MIT/source balance remain well below the current single-frame comparators.

This should not be read as a hard stop for all non-C4 line-continuity mechanisms. The final-epoch best checkpoint and finite trajectory leave room for a mechanism-changing or resource-slimmed development step. But an unchanged late36 continuation is risky: ABI-317 nearly consumed the 3,600 s exploratory timeout, a linear 36-epoch run would be close to the 10,800 s late-improving timeout, and the selected metrics are too far below ABI-202/249/279/280 to justify spending the longer budget unchanged.

The most useful lesson is architectural: propagation by itself is not enough. Future line-continuity work should couple propagated line support to evidence that raises true contrail logits at threshold 0.5 without broad clutter, and should explicitly protect MIT/source balance. That could mean a narrower directional bridge with stronger cross-scale evidence gating, a temporal-attention evidence-sharpening variant, or a different line-continuity family that avoids another late residual head over compact predictions.

## Decision

Do not promote ABI-317. Do not request whole-validation diagnostics for this capped Result. Do not submit an unchanged late-improving continuation of ABI-317: the final-epoch peak is interesting but the branch is far below the current frontier and has very little wall-clock margin.

Record ABI-317 as bounded negative evidence for the exact directional message-passing ASPP bridge and as partial feasibility evidence for non-C4 line-propagation mechanisms. A future proposal should materially change the mechanism or reduce resource cost before using more budget.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_140910_e2f4a6/candidate/PROPOSAL.md`
- `run_20260915_140910_e2f4a6/candidate/README.md`
- `run_20260915_140910_e2f4a6/candidate/manifest.yaml`
- `run_20260915_140910_e2f4a6/resolved_manifest.yaml`
- `run_20260915_140910_e2f4a6/execution.json`
- `run_20260915_140910_e2f4a6/outputs/model_summary.json`
- `run_20260915_140910_e2f4a6/outputs/best_metrics.json`
- `run_20260915_140910_e2f4a6/outputs/final_metrics.json`
- `run_20260915_140910_e2f4a6/outputs/metrics.jsonl`
- `run_20260915_140910_e2f4a6/outputs/resource_profile.json`
- `run_20260915_140910_e2f4a6/outputs/validation_postprocessing/index.json`
- `run_20260915_140910_e2f4a6/outputs/prediction_samples/samples.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 aggregate-reference context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 compact C4 context
- `run_20260913_000141_3344db/outputs/best_metrics.json` and `/history/research-notes/abi279-c4-dual-evidence-recall-bridge-late36.md` for ABI-279 recall-bridge context
- `run_20260913_023629_7902f3/outputs/best_metrics.json` and `/history/research-notes/abi280-c4-selective-consensus-recall-bridge-late36.md` for ABI-280 selective-consensus context
- `run_20260914_065219_50e898/outputs/best_metrics.json` and `/history/research-notes/abi302-crossscale-directional-consensus-aspp-cldice-late36.md` for ABI-302 clDice context
- `run_20260914_095802_a2f059/outputs/best_metrics.json` and `/history/research-notes/abi303-c4-centerline-protected-recall-bridge-unet.md` for ABI-303 protected-C4 context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
