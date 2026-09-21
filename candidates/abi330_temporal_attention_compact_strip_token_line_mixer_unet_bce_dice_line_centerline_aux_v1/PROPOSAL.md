# ABI-330 temporal-attention compact strip-token line-mixer U-Net

## Hypothesis

ABI-329 showed that temporal-attention strip-token line mixing can produce finite, source-informative predictions, but the exact branch exceeded the exploratory 3,600-second wall-clock budget before completing 12 epochs. A narrower base-width-20 version with shorter strip kernels should preserve the differentiable line-token evidence path while fitting the trusted exploratory budget. This is a **family-development continuation** after a resource-failed scout, not a promotion claim and not a request for Candidate-owned scheduling.

## Comparison Target

Primary comparison target: ABI-329 partial Run `run_20260917_084054_9439c2`, which reached epoch 10 before Harness-recorded `resource_failure`. It had best observed epoch 10 filtered Dice 0.3699, MIT 0.3502, Google 0.4169, precision 0.4034, recall 0.3415, and connectivity 0.2251 on the capped temporal-eligible validation population. Broader temporal context remains ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention diagnostic comparator and ABI-324/325/328 as recent five-frame/C4 temporal-family evidence. This Candidate produces capped feasibility evidence only.

## Expected Effect

The compact model should complete the 12-epoch exploratory budget without changing the trusted data/loss/evaluation contract. If the strip-token mechanism is useful rather than merely slow, ABI-330 should retain non-collapsed fixed-threshold predictions and the ABI-329 source balance while recovering enough throughput to expose a valid terminal Result. It may trade some capacity for resource fit; that trade is acceptable if the Run completes and remains source-informative.

## Implementation Sketch

`model.py` is copied from ABI-329 with bounded resource changes only: base width is reduced from 24 to 20, and the horizontal/vertical strip-token mixer kernels are shortened at stem, encoder, ASPP, decoder, and refinement scales. The model still builds finite normalized ABI, thermal BTD, and Solar Geometry Input features per temporal frame, applies shared per-pixel temporal attention over previous/center/next frames, uses differentiable strip-token feature mixing inside the U-Net hierarchy, and emits `mask_logits`, `line_logits`, and `centerline_logits`.

There is no threshold selection, morphology, connected-component logic, postprocessing, Artifact Filtering, data loading, temporal lookup, coordinate input, custom loss, custom metric, or Candidate-owned resource scheduling.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate code owns only model architecture over provider-supplied tensors.

## Budget Requested

Exploratory default budget: 12 epochs, batch size 2. No `late_improving` budget is requested because the immediate question is resource fit and terminal evidence for the compact strip-token mechanism.

## Success Criteria

A useful continuation must finish within the Harness-owned exploratory budget, remain finite and non-collapsed, and be source-informative. Continue this family only if ABI-330 reaches at least one of: (1) filtered Dice within roughly 0.02 of ABI-329's epoch-10 partial score while completing terminal metrics, (2) filtered recall near or above 0.34 without MIT collapse, (3) connectivity materially above ABI-329's low 0.225 while preserving precision above roughly 0.38, or (4) a clearly improving terminal trajectory that supports a future close continuation under the approved late-improving criteria.

## Fallback/Next Decision

If ABI-330 still times out, treat the strip-token U-Net hierarchy as resource-infeasible under the current exploratory policy and pivot away from this exact branch rather than requesting Candidate-owned scheduling. If it completes but loses the ABI-329 source balance or collapses recall/connectivity, pivot to a different temporal attention/backbone or a trusted calibration/loss direction. If it completes with comparable metrics and better resource behavior, use the terminal evidence to decide whether a focused diagnostic Evaluation Request or close continuation is justified.
