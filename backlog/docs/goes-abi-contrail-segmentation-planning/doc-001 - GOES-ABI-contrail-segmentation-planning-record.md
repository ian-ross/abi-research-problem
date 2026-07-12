---
id: doc-001
title: GOES ABI contrail segmentation planning record
type: planning
created_date: '2026-07-12 12:11'
---

# GOES ABI contrail segmentation planning record

This document preserves planning context that should survive deletion of `planning-inputs/`. It complements `CONTEXT.md`, `docs/adr/`, and the backlog tasks `ABI-001` through `ABI-015`.

## Research target

The research problem is **GOES ABI Contrail Segmentation**: binary semantic segmentation of contrail pixels from GOES ABI imagery. The target is a **Contrail Mask**, not instance segmentation and not MCAST operational detection.

Labels in the training data are bit-packed instance/overlap layers. For this research problem, labels are collapsed to binary with:

```python
contrail_mask = labels != 0
```

Any nonzero bit means the pixel is positive for contrail.

## Sample unit

The first-class sample is an **ABI Patch**: a `256 x 256` spatial tile with channel-first tensor inputs and a `[1, 256, 256]` Contrail Mask target.

- Google data are already `256 x 256` patches.
- MIT data are full `2000 x 3000` scenes and must be indexed/windowed into `256 x 256` patches.
- Full-scene inference can be a later evaluation/deployment capability; it is not the v0 candidate training contract.

## Dataset sources and splits

The two Dataset Sources are MIT and Google. They address the same task but were collected with different methodologies and have observable differences. Training/evaluation should keep source provenance visible.

Required policies:

- `mit_only`
- `google_only`
- `combined_source_balanced`

Splits must be **Leakage-Safe**:

- Google: respect original `train-*` and `validation-*` scene-name provenance.
- MIT: split by whole scene, never by random patch.
- Combined training uses Google train + MIT train; validation reports aggregate, MIT-specific, and Google-specific metrics.

Combined training should use **Source-Balanced Sampling**, not raw concatenation. Positive-patch preference should be explicit, logged, and provider/harness-owned.

## Input modes

Candidate code must not own data slicing. The provider owns channel selection and exposes only declared input modes.

Initial input modes:

- `abi_16ch`: GOES ABI channels 1-16.
- `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input.
- `abi_thermal_10ch`: GOES ABI channels 7-16.

Longitude and latitude must never be exposed as candidate inputs. They encourage route-location priors and reduce transferability to other domains and sensors.

Channel terminology follows the data description:

- ABI channels 1-6 are reflectance factor channels.
- ABI channels 7-16 are brightness-temperature channels.
- Solar zenith angle is optional Solar Geometry Input, not an ABI channel.

## Learned channel mixers

The agent-facing brief should explicitly mention that physically meaningful contrail signal often appears in brightness-temperature differences (BTDs), especially combinations among thermal ABI channels. This guidance should remain lightweight so agents can explore rather than merely reproduce hand-engineered features.

The ABI provider package should include reusable model-support utilities:

- `Conv1x1ChannelMixer(in_channels, out_channels)`
- `RawPlusLearnedChannelMixer(raw_indices, learned_out_channels)`

These are candidate-usable architecture utilities, not trusted loss/evaluation components. Candidates may import them or implement architectural variants within normal candidate model constraints.

## Baseline segmenters

MCAST detection model versions 1.1 and 2.1 should be integrated as provider-owned **Baseline Segmenters** once baseline evaluation is validated.

Important baseline details to preserve:

- MCAST baselines are segmentation-style models with two output classes; class 1 is contrail.
- They use three derived inputs only: `C11`, `C14`, and `C13-C15`.
- For zarr training data, these correspond to zero-based ABI channel indices:
  - `C11`: index 10
  - `C14`: index 13
  - `C13-C15`: index 12 minus index 14
- MCAST 1.1 uses an SMP U-Net ResNet18 model and threshold `0.42`.
- MCAST 2.1 uses an SMP MAnet ResNet18 model and threshold from its model directory (`threshold.dat`, observed as `0.314` in planning inputs).
- The baseline adapter should return class-1 probabilities and thresholded masks before MCAST operational postprocessing.
- Do not call full MCAST `run_detection` for primary baseline evaluation unless deliberately evaluating the operational pipeline.
- Artifact Filters must be applied consistently to baseline and candidate predictions.

Baseline integration is staged:

1. First get the provider/training vertical slice working.
2. Then validate MCAST baseline loading/evaluation.
3. Then use the best validated Baseline Segmenter in acceptance-gate comparison.

## Artifact filters

Known false positives include static geographic features such as coastlines/rivers and scanline/instrument artifacts. Because these are known systematic failure modes, evaluation must include deterministic artifact filtering.

Decision recorded in ADR-0001:

- Artifact filters are owned by the ABI research problem package because they are domain-specific.
- The harness applies them during assessment so baselines and candidate models are treated consistently.
- Candidate code must not define or override filters.

Required filters:

- **Geographic Feature Filter** for static geographic structures such as coastlines and rivers.
- **Scanline Artifact Filter** for long, approximately constant ABI-y structures associated with instrument scan artifacts.

Evaluation should report both raw and filtered metrics, plus removed-pixel diagnostics: number/area of predicted-positive pixels removed by filters.

## Metrics and acceptance

v0 primary checkpoint metric: `val/filtered_dice` (ADR-0003).

Rationale:

- Dice is interpretable and directly measures mask overlap.
- Dice is less dominated by the large background class than raw accuracy or BCE.
- Focal/Focal-Tversky losses are useful training objectives but should not be used as checkpoint-selection metrics.
- Composite acceptance is valuable, but checkpoint selection should remain simple for v0.

Reported metrics should include:

- raw Dice/IoU/precision/recall
- filtered Dice/IoU/precision/recall
- Contrail Connectivity Metric such as clDice or centerline recall
- source-stratified versions of raw and filtered metrics
- Artifact Filter removed-pixel diagnostics

Acceptance gate shape:

A candidate is acceptable if, compared with the best validated Baseline Segmenter under the same protocol, it:

1. improves aggregate filtered Dice or filtered IoU;
2. does not reduce aggregate filtered recall beyond a configured tolerance;
3. improves or maintains the Contrail Connectivity Metric;
4. does not catastrophically fail either Dataset Source;
5. does not depend excessively on Artifact Filters.

Exact numeric tolerances should be set after baseline evaluation.

## Losses and auxiliary targets

Candidate-defined arbitrary losses are not allowed (ADR-0002). Candidates select losses from a trusted allowlist exposed by the research problem spec. New losses require a capability request, approval, implementation in trusted harness/problem-support code, and agent-control-boundary updates.

Initial trusted loss allowlist:

- `bce_dice`
- `focal_tversky`
- `bce_dice_cldice`

Trusted segmentation support currently includes `bce_dice_loss`, Dice/IoU/precision/recall metrics, line/boundary target helpers, and weighted BCE auxiliary loss. It does not yet include focal-Tversky, clDice, centerline metric/loss, or raw+filtered metric support.

Initial auxiliary targets:

- `line`
- `boundary`
- `centerline`

Centerline should be available both as part of clDice/connectivity loss/metrics and as an optional auxiliary output head such as `centerline_logits`.

## Infrastructure ownership

ABI research problem repo should own:

- zarr/parquet dataset adapters;
- MIT patch indexing/windowing;
- Google patch dataset handling;
- label bit-plane collapse to Contrail Mask;
- provider-owned input-mode channel selection;
- source-balanced/positive-biased sampling policy definitions;
- Artifact Filters;
- ABI diagnostic rendering;
- MCAST baseline adapter/evaluator;
- Learned Channel Mixer utilities;
- research brief and dataset profile.

`ml-autoresearch` should own or expose:

- trusted segmentation losses and metrics used across providers;
- clDice/centerline support when generic enough;
- hooks for provider-owned filtered assessment;
- raw + filtered evaluation reporting;
- source-stratified metric aggregation if this belongs in generic evaluation support;
- provider-owned sampling-policy hooks if the current generic policies are insufficient.

## Build sequence

The agreed build sequence is a vertical slice followed by capability deepening:

1. Scaffold ABI provider with minimal spec.
2. Implement minimal ABI Patch dataset loading and label collapse.
3. Add Leakage-Safe Split and patch indexing.
4. Wire minimal training smoke path with `abi_16ch`, `bce_dice`, and temporary `val/dice`.
5. Add input modes: `abi_16ch_plus_sza`, `abi_thermal_10ch`.
6. Add Learned Channel Mixer utilities and briefing guidance.
7. Add provider-owned Artifact Filters and harness-applied filtered assessment.
8. Promote `val/filtered_dice` to v0 primary metric.
9. Add focal-Tversky, clDice/connectivity support, and `bce_dice_cldice`.
10. Add line/boundary/centerline auxiliary targets.
11. Add Source-Balanced Sampling policies.
12. Add Dataset Source-stratified metrics.
13. Integrate MCAST Baseline Segmenters.
14. Create the full ABI research brief and dataset profile.
15. Implement acceptance-gate reporting.

These steps correspond to backlog tasks `ABI-001` through `ABI-015`.
